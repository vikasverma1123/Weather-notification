import tkinter as tk
from tkinter import messagebox
import requests
from plyer import notification
import time
import threading

def get_weather():
    city = city_entry.get()
    if city:
        try:
            api_key = "eba07ff9d3d82ad7b25fc5fdd5e0ef56"
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(base_url)
            data = response.json()

            if data["cod"] != "404":
                main = data["main"]
                wind = data["wind"]
                weather_desc = data["weather"][0]["description"]

                temperature = main["temp"]
                pressure = main["pressure"]
                humidity = main["humidity"]
                wind_speed = wind["speed"]

                weather_info = (f"Temperature: {temperature}°C\n"
                                f"Pressure: {pressure} hPa\n"
                                f"Humidity: {humidity}%\n"
                                f"Wind Speed: {wind_speed} m/s\n"
                                f"Description: {weather_desc}")
                
                notification.notify(
                    title=f"Weather in {city}",
                    message=weather_info,
                    timeout=10
                )
            else:
                messagebox.showerror("Error", "City Not Found!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter a city name!")

def schedule_weather_updates():
    while True:
        get_weather()
        time.sleep(10)  # Wait for 1 hour before the next update

def start_weather_updates():
    update_thread = threading.Thread(target=schedule_weather_updates)
    update_thread.daemon = True  # This allows the thread to exit when the main program exits
    update_thread.start()

# Create the main application window
app = tk.Tk()
app.title("Weather Notification App")
app.geometry("400x200")
app.resizable(False, False)

# Add a label and entry to take city input
tk.Label(app, text="Enter City Name:", font=("Helvetica", 14)).pack(pady=10)
city_entry = tk.Entry(app, font=("Helvetica", 14), width=30)
city_entry.pack(pady=5)

# Add a button to start weather updates
get_weather_button = tk.Button(app, text="Get Weather", command=start_weather_updates, font=("Helvetica", 14), bg="blue", fg="white")
get_weather_button.pack(pady=20)

# Add a status label to show if updates are running
status_label = tk.Label(app, text="", font=("Helvetica", 12))
status_label.pack(pady=5)

# Function to update the status label
def update_status():
    while True:
        status_label.config(text="Weather updates are running...")
        time.sleep(2)

# Start a thread to update the status label
status_thread = threading.Thread(target=update_status)
status_thread.daemon = True
status_thread.start()

# Start the main loop of the application
app.mainloop()