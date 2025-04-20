from fastapi import APIRouter, Query, HTTPException
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi.responses import StreamingResponse
import io

router = APIRouter()


def generate_histogram(df: pd.DataFrame, feature: str, bin_value: int = None):
    if feature not in df.columns:
        raise ValueError(f"Feature '{feature}' not found in the DataFrame.")

    if bin_value is None:
        bin_value = 10 if feature == "soil_moisture" else 30

    plt.figure(figsize=(10, 6))
    sns.histplot(df[feature], kde=True, bins=bin_value)
    plt.title(f'Histogram of {feature.capitalize()}')
    plt.xlabel(feature.capitalize())
    plt.ylabel('Frequency')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.get("/histogram", response_class=StreamingResponse)
def get_histogram(feature: str = Query(...), bin_value: int = Query(None)):
    try:
        response = requests.get("http://localhost:8000/data")
        response.raise_for_status()
        df = pd.DataFrame(response.json())

        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")

        return generate_histogram(df, feature, bin_value)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to generate histogram: {e}")
