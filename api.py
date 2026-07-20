import requests
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()

    options = {"weather": data["weather"][0]["description"].title(),
        "temperature": f'{data["main"]["temp"]}°F',
        "humidity": f'{data["main"]["humidity"]}%',
        "feels like": f'{data["main"]["feels_like"]}°F',
        "sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
        "sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")}
    
    return options