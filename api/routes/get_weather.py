from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import requests

router = APIRouter()

API_KEY = "f453040f74cc60b5166a170317ef1d36"


class WeatherResponse(BaseModel):
    city: str
    temp: float
    humidity: int


@router.get("/weather", response_model=WeatherResponse)
def get_weather(
        city: str = Query(..., description="City name to get weather")):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            raise HTTPException(status_code=404, detail="City not found")

        return {
            "city": res["name"],
            "temp": res["main"]["temp"],
            "humidity": res["main"]["humidity"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
