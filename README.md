# CAS141---HIT137---Assignment-3
CDU - HIT 137 - Assignment 3. Semester2, 2024.

# Weather Forecast Application

This is a simple weather forecast application built using Python's `tkinter` library. The app allows users to select an Australian state capital city, input a specific date, and retrieve the weather forecast for that city on the selected date.

## Features

- Users can select from eight Australian state capital cities using a dropdown menu.
- Users can input a date in the `DDMMYYYY` format (e.g., 17102024 for October 17, 2024).
- The app fetches the weather forecast from the OpenWeatherMap API.
- The weather information, including temperature and general conditions, is displayed for the selected city and date.

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.x installed on your machine.
- The `requests` library installed. If you don’t have it, you can install it by running:

    ```bash
    pip install requests
    ```

## API Key

This application uses the OpenWeatherMap API. You must have a valid API key to use the application. If you don’t have one, you can register for free on [OpenWeatherMap](https://openweathermap.org/api) and generate your API key.

Once you have the API key, replace the placeholder in the script with your actual key:

```python
api_key = "YOUR_API_KEY"
