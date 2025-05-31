from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Replace with your OpenWeatherMap API key
API_KEY = "4988dec189d63fb1fcca182bb4c849e1"
BASE_URL = "http://api.openweathermap.org/data/2.5"

@app.get("/current-weather")
def get_current_weather(city: str, units: str = "metric"):
    """Fetch current weather for a given city."""
    url = f"{BASE_URL}/weather"
    params = {"q": city, "units": units, "appid": API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
        }
    else:
        raise HTTPException(status_code=404, detail="City not found")

@app.get("/forecast")
def get_forecast(city: str, days: int = 3, units: str = "metric"):
    """Fetch weather forecast for a given city."""
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "units": units, "appid": API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data["list"][:days * 8]:  # 8 data points per day
            forecast.append({
                "date": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"],
            })
        return {"city": city, "forecast": forecast}
    else:
        raise HTTPException(status_code=404, detail="City not found")
