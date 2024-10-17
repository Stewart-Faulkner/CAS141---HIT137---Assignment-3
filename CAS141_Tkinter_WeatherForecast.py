import tkinter as tk
import requests
from tkinter import ttk
import datetime

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Forecast")
        self.geometry("600x400")
        
        # Create a dropdown (Combobox) for selecting the city
        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(self, textvariable=self.city_var)
        self.city_combobox['values'] = ("Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart", "Darwin", "Canberra")
        self.city_combobox.set("Select City")  # Set default value
        self.city_combobox.pack(padx=20, pady=10)
        
        # Create an input field for date (format: DDMMYYYY)
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.entry_var)
        entry.pack(padx=20, pady=20)
        
        # Create a button to request weather forecast
        button = ttk.Button(self, text="Get Weather", command=self.get_weather)
        button.pack(padx=20, pady=20)
        
        # The label to display the weather information
        self.weather_label = tk.Label(self, text="Weather information will appear here", font=("Helvetica", 12))
        self.weather_label.pack(padx=20, pady=20)

    def get_weather(self):
        # Get the input date in DDMMYYYY format
        date_str = self.entry_var.get()
        
        # Get the selected city
        city = self.city_var.get()
        if city == "Select City":
            self.weather_label.config(text="Please select a city.")
            return
        
        try:
            # Convert the input string to a valid date format (YYYY-MM-DD)
            date = datetime.datetime.strptime(date_str, "%d%m%Y")
            formatted_date = date.strftime("%Y-%m-%d")  # Convert to 'YYYY-MM-DD'
        except ValueError:
            self.weather_label.config(text="Invalid date format! Use DDMMYYYY.")
            return
        
        # Call the weather API
        api_key = "fb2182439edf3afe276a77473d3c9bc6"
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            forecast = self.find_forecast_for_date(weather_data, formatted_date)
            if forecast:
                # Display the weather forecast for the given date
                weather_info = f"Weather on {date_str} in {city}:\nTemperature: {forecast['main']['temp']}°C\n" \
                               f"Weather: {forecast['weather'][0]['description']}"
                self.weather_label.config(text=weather_info)
            else:
                self.weather_label.config(text="No weather data available for that date.")
        else:
            self.weather_label.config(text="Failed to retrieve weather data.")

    def find_forecast_for_date(self, weather_data, formatted_date):
        # OpenWeatherMap forecast data is for every 3 hours, so we need to match the date
        for forecast in weather_data['list']:
            forecast_time = forecast['dt_txt']
            if formatted_date in forecast_time:
                return forecast
        return None

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
