import os
import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timezone
import json
import uvicorn
from dotenv import load_dotenv
import traceback
import logging
import redis
from ratelimit import limits, sleep_and_retry

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path='/app/.env')

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES_FILE = "cities.json"
RATE_LIMIT = 60  # requests per minute
TIME_PERIOD = 60  # seconds
BATCH_SIZE = 60  # number of cities to process in each batch

print(f"API Key: {API_KEY}")
if API_KEY is None:
    raise ValueError("API_KEY is not set. Please check your .env file.")

# Redis client setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Load cities
with open(CITIES_FILE, "r") as f:
    CITIES = json.load(f)

class WeatherRequest(BaseModel):
    user_id: str

class WeatherData(BaseModel):
    user_id: str
    datetime: str
    city_id: int
    temperature: float
    humidity: int

@sleep_and_retry
@limits(calls=RATE_LIMIT, period=TIME_PERIOD)
async def fetch_weather_data(session, city_id, user_id):
    params = {
        "id": city_id,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                weather_data = WeatherData(
                    user_id=user_id,
                    datetime=datetime.now(timezone.utc).isoformat(),
                    city_id=city_id,
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"]
                )
                logging.info(f"Successfully fetched data for city ID {city_id}: {data['name']}, Temp: {data['main']['temp']}°C, Humidity: {data['main']['humidity']}%")
                return weather_data
            else:
                logging.error(f"Failed to fetch data for city ID {city_id}. Status: {response.status}, Message: {data.get('message', 'Unknown error')}")
                return None
    except aiohttp.ClientError as e:
        logging.error(f"Network error for city ID {city_id}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for city ID {city_id}: {str(e)}")
        return None

async def process_batch(session, batch, user_id):
    tasks = [fetch_weather_data(session, city_id, user_id) for city_id in batch]
    results = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]

def store_weather_data(user_id: str, data: list):
    redis_key = f"weather:{user_id}"
    serialized_data = json.dumps([d.dict() for d in data])
    redis_client.set(redis_key, serialized_data)

def get_weather_data(user_id: str) -> list:
    redis_key = f"weather:{user_id}"
    data = redis_client.get(redis_key)
    if data:
        return [WeatherData(**d) for d in json.loads(data)]
    return []

async def collect_weather_data(user_id):
    logging.info(f"Starting data collection for user {user_id}")
    try:
        async with aiohttp.ClientSession() as session:
            results = []
            total_cities = len(CITIES)
            
            # Load existing data if any
            results = get_weather_data(user_id)
            if results:
                logging.info(f"Resuming from {len(results)} previously collected cities.")
            
            # Determine which cities still need to be processed
            processed_city_ids = set(result.city_id for result in results)
            cities_to_process = [city for city in CITIES if city not in processed_city_ids]
            
            for i in range(0, len(cities_to_process), BATCH_SIZE):
                batch = cities_to_process[i:i+BATCH_SIZE]
                logging.info(f"Processing batch {i//BATCH_SIZE + 1} of {(len(cities_to_process)-1)//BATCH_SIZE + 1}")
                batch_results = await process_batch(session, batch, user_id)
                results.extend(batch_results)
                
                # Store intermediate results
                store_weather_data(user_id, results)
                
                # Log progress
                progress = len(results)
                logging.info(f"Progress: {progress}/{total_cities} cities processed ({progress/total_cities*100:.2f}%)")
                
                if i + BATCH_SIZE < len(cities_to_process):
                    logging.info("Waiting for 1 minute before next batch...")
                    await asyncio.sleep(60)  # Wait for 1 minute before the next batch
            
            logging.info(f"Data collection completed for user {user_id}")
            return len(results)
    except Exception as e:
        logging.error(f"An error occurred in collect_weather_data: {str(e)}")
        logging.error(traceback.format_exc())
        raise

@app.post("/weather")
async def post_weather_data(request: WeatherRequest):
    # Check if user_id already exists and if data collection is complete
    existing_data = get_weather_data(request.user_id)
    if existing_data:
        if len(existing_data) == len(CITIES):
            return {"message": "Data collection already completed for this user_id", "user_id": request.user_id}
        else:
            return {"message": "Resuming data collection", "user_id": request.user_id}
    
    # Start or resume data collection in the background
    asyncio.create_task(collect_weather_data(request.user_id))
    
    return {"message": "Data collection started", "user_id": request.user_id}

@app.get("/weather/{user_id}")
async def get_weather_progress(user_id: str):
    data = get_weather_data(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="User ID not found")
    progress = (len(data) / len(CITIES)) * 100
    return {"user_id": user_id, "progress": progress}

@app.middleware("http")
async def error_handling_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Unhandled error: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred"})

@app.on_event("startup")
async def startup_event():
    logging.info(f"Script execution started at {datetime.now().isoformat()}")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info(f"Script execution completed at {datetime.now().isoformat()}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)