from fastapi import APIRouter
from pydantic import BaseModel
from utils.predictor import predict_health, generate_recommendations

router = APIRouter()


class HealthRequest(BaseModel):
    soil_moisture: float
    temperature: float
    humidity: float
    light: float


class HealthResponse(BaseModel):
    plant_health: str
    recommendation: list


@router.post("/predict-health", response_model=HealthResponse)
def predict_plant_health(data: HealthRequest):
    predicted = predict_health(
        data.soil_moisture,
        data.light,
        data.temperature,
        data.humidity,
    )
    recommendation = generate_recommendations(
        data.soil_moisture,
        data.humidity,
        data.light,
        data.temperature
    )
    return {"plant_health": predicted, "recommendation": recommendation}


