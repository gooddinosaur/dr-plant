from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

router = APIRouter()

@router.get("/scatter-plot", response_class=StreamingResponse)
def get_scatter_plot(x_attr: str, y_attr: str):
    try:
        # ดึงข้อมูล
        response = requests.get("http://localhost:8000/data")
        response.raise_for_status()
        df = pd.DataFrame(response.json())

        # ตรวจสอบข้อมูล
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        if x_attr not in df.columns or y_attr not in df.columns:
            raise HTTPException(status_code=400, detail="Invalid attribute name")

        plt.figure(figsize=(10, 6))
        sns.regplot(data=df, x=x_attr, y=y_attr, scatter_kws={"s": 40}, line_kws={"color": "red"})
        plt.title(f"{y_attr.capitalize()} vs {x_attr.capitalize()}")
        plt.xlabel(x_attr.replace("_", " ").title())
        plt.ylabel(y_attr.replace("_", " ").title())

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plot: {e}")
