from fastapi import FastAPI
from api.routes import predict_health, get_weather, descriptive_statistics

API_KEY = "f453040f74cc60b5166a170317ef1d36"
app = FastAPI(title="Dr.Plant API",
              description="APIs for monitoring and predicting plant health",
              version="1.0")


app.include_router(predict_health.router)
app.include_router(get_weather.router)
app.include_router(descriptive_statistics.router)