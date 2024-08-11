# Weather Service API (DevGrid)

This project is a FastAPI-based weather service that collects and provides weather data for multiple cities using the OpenWeatherMap API. It features asynchronous data collection, rate limiting, and Redis-based data storage for efficient operation.
It was made as Tech Test challenge for the DevGrid company.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [How to Get Your OpenWeatherMap API Key](#how-to-get-your-openweathermap-api-key)
3. [Project Structure](#project-structure)
4. [Docker Installation](#docker-installation)
5. [How to Run](#how-to-run)
6. [How to Test](#how-to-test)
7. [API Endpoints](#api-endpoints)
8. [Cities Data](#cities-data)
9. [Data Storage and Format](#data-storage-and-format)
10. [Environment Variables and Configuration](#environment-variables-and-configuration)
11. [How It Works](#how-it-works)
12. [Features](#features)
13. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker (optional, but recommended)
- Python 3.10+
- OpenWeatherMap API key

## How to Get Your OpenWeatherMap API Key

To use this Weather Service API, you'll need an API key from OpenWeatherMap. Follow these steps to obtain your key:

1. **Create an Account**: 
   - Go to the [OpenWeatherMap website](https://openweathermap.org/).
   - Click on the "Sign In" button in the top right corner.
   - If you don't have an account, click on "Create an Account" and follow the registration process.

2. **Log In**:
   - Once your account is created, log in to the OpenWeatherMap website.

3. **Navigate to API Keys**:
   - After logging in, click on your username in the top right corner.
   - From the dropdown menu, select "My API Keys".
   - Alternatively, you can directly visit the [API keys page](https://home.openweathermap.org/api_keys) after logging in.

4. **Generate a Key**:
   - On the API Keys page, you'll see a section called "Create Key".
   - Enter a name for your key (e.g., "Weather Service API") in the input field.
   - Click on the "Generate" button.

5. **Copy Your API Key**:
   - Your new API key will appear in the list of API keys.
   - Copy this key; you'll need to add it to your `.env` file as described in the "Environment Variables and Configuration" section.

6. **API Key Activation**:
   - Note that it may take a few hours for your API key to become fully activated.
   - If you encounter any "unauthorized" errors when first using your key, please wait a bit and try again.

7. **Free vs Paid Plans**:
   - OpenWeatherMap offers both free and paid plans. The free plan should be sufficient for testing and small-scale use of this Weather Service API.
   - Be aware of the rate limits and restrictions on the free plan, which are subject to change. Check the [OpenWeatherMap pricing page](https://openweathermap.org/price) for the most up-to-date information.

Remember to keep your API key secure and never share it publicly or commit it to version control systems.

## Project Structure

### Dockerfile

The project includes a Dockerfile for containerizing the application. Here's an explanation of the Dockerfile:

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Uses Python 3.10 as the base image
- Sets the working directory to `/app`
- Copies and installs the requirements
- Copies the application files and the `.env` file into the container
- Runs the application using Uvicorn

### Requirements

The `requirements.txt` file lists all the Python dependencies for the project. Here are the main dependencies and their purposes:

```
fastapi==0.68.0
uvicorn==0.15.0
aiohttp==3.8.1
pydantic==1.8.2
python-dotenv==0.19.0
redis==4.2.2
ratelimit==2.2.1
```

- **FastAPI**: The web framework used for building the API
- **Uvicorn**: ASGI server for running the FastAPI application
- **aiohttp**: Asynchronous HTTP client for making API requests
- **Pydantic**: Data validation and settings management using Python type annotations
- **python-dotenv**: Loads environment variables from a .env file
- **redis**: Redis database interface
- **ratelimit**: Provides rate limiting functionality

To install these requirements:

1. Ensure you have Python 3.10 or later installed.
2. Run the following command:

   ```
   pip install -r requirements.txt
   ```

Note: If you're using Docker, the requirements will be automatically installed in the container, so you don't need to install them separately.

## Docker Installation

1. Install Docker on your system:
   - For Ubuntu: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
   - For macOS: [Install Docker Desktop on Mac](https://docs.docker.com/desktop/install/mac-install/)
   - For Windows: [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)

2. Verify the installation:
   ```
   docker --version
   ```

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/lucasvhol/Weather-Service-API-DevGrid.git
   cd weather-service
   ```

2. Create a `.env` file in the project root and add your OpenWeatherMap API key:
   ```
   OPEN_WEATHER_API_KEY=your_api_key_here
   ```

3. Choose a method to run the application:

### Using Docker

#### Windows (Command Prompt)
```
docker build -t weather-service .
docker run -d -p 8000:8000 --env-file .env weather-service
```

#### Windows (PowerShell)
```powershell
docker build -t weather-service .
docker run -d -p 8000:8000 --env-file ${PWD}\.env weather-service
```

#### macOS/Linux (Bash/Zsh)
```bash
docker build -t weather-service .
docker run -d -p 8000:8000 --env-file ./.env weather-service
```

### Using Docker Compose

#### Windows/macOS/Linux
```
docker-compose up -d
```

### Running Without Docker

1. Ensure you have Python 3.10+ installed.

2. Install the required dependencies:

   #### Windows (Command Prompt/PowerShell)
   ```
   pip install -r requirements.txt
   ```

   #### macOS/Linux
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the application:

   #### Windows (Command Prompt/PowerShell)
   ```
   python main.py
   ```

   #### macOS/Linux
   ```bash
   python3 main.py
   ```

   Note: Replace `main.py` with the actual name of your main Python file if it's different.

4. The API should now be running and accessible at `http://localhost:8000`.

## How to Test

1. Ensure the application is running (either in Docker or natively).

2. Run the tests using pytest:

   ### Using Docker Compose
   ```
   docker-compose exec app pytest tests/
   ```

   ### Without Docker

   #### Windows (Command Prompt/PowerShell)
   ```
   pytest tests/
   ```

   #### macOS/Linux
   ```bash
   python3 -m pytest tests/
   ```

3. For manual testing, you can use tools like cURL or Postman to interact with the API endpoints.

   ### Example using cURL

   #### Start weather data collection (POST request)
   ```bash
   curl -X POST http://localhost:8000/weather -H "Content-Type: application/json" -d '{"user_id": "test_user"}'
   ```

   #### Check collection progress (GET request)
   ```bash
   curl http://localhost:8000/weather/test_user
   ```

## API Endpoints

- `POST /weather`
  - Starts weather data collection for a given user ID.
  - Request body: `{"user_id": "your_custom_identifier"}`

- `GET /weather/{user_id}`
  - Retrieves the progress of weather data collection for a specific user ID.

## Cities Data

The Weather Service API uses a predefined list of cities for which it collects weather data. This list is stored in a `cities.json` file in the project root directory.

### cities.json File

The `cities.json` file contains an array of city objects, each with the following structure:

```json
{
  "id": 3439525,
  "name": "São Paulo",
  "state": "",
  "country": "BR",
  "coord": {
    "lon": -46.636108,
    "lat": -23.547501
  }
}
```

- `id`: OpenWeatherMap city ID
- `name`: City name
- `state`: State code (if applicable)
- `country`: Country code
- `coord`: Coordinates (longitude and latitude)

This file is based on the Appendix A from the Tech Case and includes a curated list of cities for which the weather data will be collected.

### Modifying the Cities List

If you need to modify the list of cities:

1. Open the `cities.json` file in a text editor.
2. Add, remove, or modify city entries as needed.
3. Ensure the JSON structure remains valid.
4. Save the file and restart the application for changes to take effect.

Note: Adding a large number of cities may impact performance and API usage limits.

## Data Storage and Format

The Weather Service API collects and stores weather data for each city in a structured JSON format.

### Data Storage

- The collected weather data is stored in Redis, an in-memory data structure store.
- Each user's data is stored under a unique key based on their user ID.

### Weather Data Format

The weather data for each city is stored in the following JSON format:

```json
{
  "city_id": 3439525,
  "city_name": "São Paulo",
  "temperature": 22.5,
  "humidity": 70,
  "pressure": 1012,
  "weather_description": "Partly cloudy",
  "wind_speed": 3.5,
  "wind_direction": 180,
  "timestamp": "2024-08-11T14:30:00Z"
}
```

- `city_id`: OpenWeatherMap city ID
- `city_name`: Name of the city
- `temperature`: Temperature in Celsius
- `humidity`: Humidity percentage
- `pressure`: Atmospheric pressure in hPa
- `weather_description`: Brief description of the weather conditions
- `wind_speed`: Wind speed in meters per second
- `wind_direction`: Wind direction in degrees
- `timestamp`: UTC timestamp of when the data was collected

### Accessing Stored Data

To access the stored weather data:

1. Use the GET endpoint: `/weather/{user_id}`
2. The response will include the progress of data collection and the collected data for each city.

Example response:

```json
{
  "status": "in_progress",
  "data": [
    {
      "city_id": 3439525,
      "city_name": "São Paulo",
      "temperature": 22.5,
      "humidity": 70,
      "pressure": 1012,
      "weather_description": "Partly cloudy",
      "wind_speed": 3.5,
      "wind_direction": 180,
      "timestamp": "2024-08-11T14:30:00Z"
    },
    // ... data for other cities ...
  ]
}
```

The `status` field indicates whether the data collection is complete or still in progress.

## Environment Variables and Configuration

This service uses environment variables for configuration, including sensitive information like API keys. 

### Setting up the .env file

1. **Create the .env file**:
   - In the root directory of the project, create a new file named exactly `.env` (including the dot at the beginning).
   - On Windows, you might need to name it `.env.` (with a dot at the end) in File Explorer, which will automatically remove the trailing dot.

2. **Add configuration to the .env file**:
   - Open the `.env` file with a text editor.
   - Add the following lines, replacing `your_api_key_here` with your actual OpenWeatherMap API key:

     ```
     OPEN_WEATHER_API_KEY=your_api_key_here
     REDIS_HOST=localhost
     REDIS_PORT=6379
     REDIS_DB=0
     ```

3. **Save the file**:
   - Make sure to save the `.env` file after adding your configuration.

4. **Protect your .env file**:
   - **IMPORTANT:** Never commit the `.env` file to version control. Add it to your `.gitignore`:
     ```
     echo ".env" >> .gitignore
     ```
   - If you're using a different version control system, ensure you exclude the `.env` file from being tracked.

### Using the .env file

- When running the application locally, it will automatically read the environment variables from the `.env` file.
- For Docker deployments, you'll pass the `.env` file to Docker as described in the "How to Run" section.

### Troubleshooting .env issues

- Ensure the file is named exactly `.env` with no additional extensions.
- Check that the file is in the root directory of the project.
- Verify that there are no spaces around the `=` sign in each line of the `.env` file.
- If using Windows, make sure your text editor didn't save the file with a hidden extension (e.g., `.env.txt`).

Remember, the `.env` file contains sensitive information. Keep it secure and never share its contents publicly.

### Handling the OpenWeatherMap API Key

The OpenWeatherMap API key is sensitive information and should be handled securely:

- For local development, use the `.env` file as described above.
- For production deployments, consider using Docker Secrets or your cloud provider's secret management service.
- Never hard-code the API key in your application code or commit it to version control.

### Docker and Environment Variables

When running the application with Docker, pass the environment variables using the `--env-file` option:

```
docker run -d -p 8000:8000 --env-file .env weather-service
```

For Docker Compose, you can specify the env_file in your `docker-compose.yml`:

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
```

### Production Considerations

For production deployments, consider:

- Using Docker Secrets for sensitive information.
- Implementing a secrets management system appropriate for your infrastructure (e.g., AWS Secrets Manager, HashiCorp Vault).
- Rotating secrets regularly and having a process for secret revocation.

## How It Works

The Weather Service API is built using FastAPI and leverages asynchronous programming for efficient data collection. Here's an overview of how the code works:

1. **Initialization**: The application loads environment variables, sets up logging, and initializes the FastAPI app and Redis client.

2. **Data Collection**:
   - The `collect_weather_data` function is the core of the data collection process.
   - It uses `aiohttp` to make asynchronous HTTP requests to the OpenWeatherMap API.
   - Data is collected in batches to manage API rate limits and system resources.

3. **Rate Limiting**:
   - The `ratelimit` decorator is used to ensure the application doesn't exceed OpenWeatherMap's API rate limits.

4. **Data Storage**:
   - Collected weather data is stored in Redis, keyed by user ID.
   - Redis allows for fast data retrieval and supports concurrent access.
   - 
5. **API Endpoints**:
   - The POST endpoint initiates data collection for a given user ID.
   - The GET endpoint retrieves the progress of data collection for a specific user ID.

6. **Error Handling**:
   - A middleware catches and logs unhandled exceptions, returning appropriate error responses.

## Features

- **Asynchronous Data Collection**: Utilizes `aiohttp` for non-blocking API requests, allowing for efficient collection of data from multiple cities.
- **Rate Limiting**: Implements rate limiting to comply with OpenWeatherMap API usage policies and prevent request failures.
- **Redis-based Storage**: Uses Redis for fast, in-memory data storage and retrieval, supporting concurrent access and reducing database load.
- **Progress Tracking**: Allows users to check the progress of data collection in real-time.
- **Docker Support**: Easily deployable using Docker, ensuring consistency across different environments.
- **Environment-based Configuration**: Uses environment variables for configuration, allowing for easy adjustment of settings without code changes.
- **Error Handling and Logging**: Comprehensive error handling and logging for easier debugging and monitoring.

## Troubleshooting

If you encounter any issues:

1. Ensure Docker is running correctly on your system (if using Docker).
2. Check that the `.env` file contains the correct API key.
3. Verify that the required ports (8000 for the API, 6379 for Redis) are not in use by other applications.
4. Review the application logs for any error messages:
   - If using Docker: `docker logs weather-service`
   - If running natively: Check the console output or log files

5. Ensure all dependencies are correctly installed (if running without Docker).
6. Verify that Redis is running and accessible (if running without Docker).

For further assistance, please open an issue on the project's GitHub repository.
