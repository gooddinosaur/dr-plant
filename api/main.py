from fastapi import FastAPI
from pydantic import BaseModel
from utils.predictor import predict_health

app = FastAPI(title="Dr.Plant API",
              description="API for predicting plant health")


class SensorData(BaseModel):
    moisture: float
    light: float
    temperature: float
    humidity: float


@app.get("/")
def root():
    return {"message": "Welcome to Dr.Plant API"}


@app.post("/predict")
def predict(data: SensorData):
    result = predict_health(
        data.moisture, data.light, data.temperature, data.humidity
    )
    return {"prediction": result}
