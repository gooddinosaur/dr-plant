from fastapi import APIRouter, HTTPException
import pandas as pd
from api.database import pool

router = APIRouter()


@router.get("/data")
def fetch_data():
    try:
        conn = pool.connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM drplantdata")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to fetch data: {e}")
    finally:
        conn.close()

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found.")

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime(
        "%Y-%m-%d %H:%M:%S")
    return df.to_dict(orient="records")
