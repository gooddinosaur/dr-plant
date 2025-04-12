from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random
import requests
from fastapi import Query, HTTPException

API_KEY = "f453040f74cc60b5166a170317ef1d36"
app = FastAPI(title="Dr.Plant API",
              description="APIs for monitoring and predicting plant health",
              version="1.0")


# ==== Sample Models ====

class SensorData(BaseModel):
    soil_moisture: int
    temperature: float
    humidity: float
    light: int
    timestamp: datetime


class HealthRequest(BaseModel):
    soil_moisture: int
    temperature: float
    humidity: float
    light: int


class HealthResponse(BaseModel):
    plant_health: str
    recommendation: str


class StatValue(BaseModel):
    avg: float
    min: float
    max: float


class SensorStatistics(BaseModel):
    soil_moisture: StatValue
    temperature: StatValue
    humidity: StatValue
    light: StatValue


class WeatherResponse(BaseModel):
    city: str
    temp: float
    humidity: int


# ==== Sample Simulated Data ====

def simulate_sensor_data(n=50):
    now = datetime.now()
    return [
        {
            "timestamp": now - timedelta(minutes=i * 10),
            "soil_moisture": random.randint(300, 800),
            "temperature": round(random.uniform(24, 34), 2),
            "humidity": round(random.uniform(40, 90), 2),
            "light": random.randint(200, 1000)
        }
        for i in range(n)
    ]


sensor_history = simulate_sensor_data()


# ==== API Routes ====

@app.get("/sensor-data", response_model=SensorData)
def get_latest_sensor_data():
    return sensor_history[-1]


@app.post("/predict-health", response_model=HealthResponse)
def predict_plant_health(data: HealthRequest):
    if data.soil_moisture > 600 and data.humidity > 60:
        return {"plant_health": "Healthy",
                "recommendation": "Everything looks great!"}
    elif 400 < data.soil_moisture <= 600:
        return {"plant_health": "Moderate Stress",
                "recommendation": "Consider watering soon."}
    else:
        return {"plant_health": "High Stress",
                "recommendation": "Urgently water the plant and check lighting."}


@app.get("/statistics", response_model=SensorStatistics)
def get_statistics(
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    filtered = sensor_history
    if start_time and end_time:
        filtered = [x for x in sensor_history if
                    start_time <= x["timestamp"] <= end_time]

    def compute_stats(key):
        values = [x[key] for x in filtered]
        return {"avg": sum(values) / len(values), "min": min(values),
                "max": max(values)}

    return {
        "soil_moisture": compute_stats("soil_moisture"),
        "temperature": compute_stats("temperature"),
        "humidity": compute_stats("humidity"),
        "light": compute_stats("light")
    }


@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(..., description="City name to get weather")):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )
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


@app.get("/sensor-history", response_model=List[SensorData])
def get_sensor_history(
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = 20
):
    data = sensor_history
    if start_time and end_time:
        data = [x for x in data if start_time <= x["timestamp"] <= end_time]
    return data[-limit:]


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}
