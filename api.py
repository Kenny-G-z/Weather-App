import requests
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

def get_weather(city):
    forecast_url = (f"https://api.openweathermap.org/data/2.5/forecast"f"?q={city}&appid={api_key}&units=imperial")
    weather_url = (f"https://api.openweathermap.org/data/2.5/weather"f"?q={city}&appid={api_key}&units=imperial")

    forecast_response = requests.get(forecast_url)
    weather_response = requests.get(weather_url)

    if forecast_response.status_code != 200 or weather_response.status_code != 200:
        return None

    forecast_data = forecast_response.json()
    weather_data = weather_response.json()

    timezone_offset = weather_data["timezone"]
    city_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))
    current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(city_timezone)
    sunrise = datetime.datetime.fromtimestamp(weather_data["sys"]["sunrise"],city_timezone)
    sunset = datetime.datetime.fromtimestamp(weather_data["sys"]["sunset"],city_timezone)

    theme = "day"
    if current_time < sunrise or current_time >= sunset:
        theme = "night"

    current = {
        "time": current_time.strftime("%I:%M %p"),
        "weather": weather_data["weather"][0]["description"].title(),
        "temperature": f'{weather_data["main"]["temp"]:.1f}°F',
        "high": f'{weather_data["main"]["temp_max"]:.1f}°F',
        "low": f'{weather_data["main"]["temp_min"]:.1f}°F',
        "humidity": f'{weather_data["main"]["humidity"]}%',
        "feels like": f'{weather_data["main"]["feels_like"]:.1f}°F',
        "temp_diff":weather_data["main"]["temp"] >= weather_data["main"]["feels_like"]
    }

    today = current_time.date()
    tomorrow = today + datetime.timedelta(days=1)
    late_night = current_time.hour >= 21

    forecasts = []

    for forecast in forecast_data["list"]:
        forecast_time = datetime.datetime.strptime(forecast["dt_txt"],"%Y-%m-%d %H:%M:%S").replace(tzinfo=city_timezone)

        if forecast_time <= current_time:
            continue
        
        if late_night:
            if forecast_time.date() == today:
                pass
            elif forecast_time.date() == tomorrow:
                if forecast_time.hour > 6:
                    break
            else:
                break
        else:
            if forecast_time.date() != today:
                if forecast_time.hour != 0:
                    break

        forecasts.append({
            "time": forecast_time.strftime("%I:%M %p"),
            "weather":forecast["weather"][0]["description"].title(),
            "temperature":f'{forecast["main"]["temp"]:.1f}°F',
            "humidity":f'{forecast["main"]["humidity"]}%',
            "feels like":f'{forecast["main"]["feels_like"]:.1f}°F',
            "precipitation":f'{round(forecast["pop"] * 100)}%',
            "temp_diff":forecast["main"]["temp"] >= forecast["main"]["feels_like"]
        })

    return {
        "current": current,
        "sunrise": sunrise.strftime("%I:%M %p"),
        "sunset": sunset.strftime("%I:%M %p"),
        "theme": theme,
        "forecasts": forecasts
    }