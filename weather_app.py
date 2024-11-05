import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to fetch weather data from OpenWeatherMap API
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = "your_openweathermap_api_key"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # For temperature in Celsius
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Extract weather details
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']

        # Update GUI with weather information
        weather_info.config(text=f"Temperature: {temp}°C\nHumidity: {humidity}%\nDescription: {description.capitalize()}\nWind Speed: {wind_speed} m/s")

        # Load and display the weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        icon_label.config(image=icon_image)
        icon_label.image = icon_image  # Store reference to avoid garbage collection
    else:
        messagebox.showerror("Error", "Could not retrieve data for the specified location.")

# Function to clear previous data
def clear_data():
    city_entry.delete(0, tk.END)
    weather_info.config(text="")
    icon_label.config(image='')

# Set up the GUI window
root = tk.Tk()
root.title("Weather App")

# City entry label and input box
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=10)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

# Button to fetch weather
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=10)

# Button to clear data
clear_button = tk.Button(root, text="Clear", command=clear_data)
clear_button.pack(pady=5)

# Label to display weather information
weather_info = tk.Label(root, text="", font=("Arial", 12))
weather_info.pack(pady=10)

# Label to display weather icon
icon_label = tk.Label(root)
icon_label.pack(pady=10)

# Run the GUI loop
root.mainloop()
