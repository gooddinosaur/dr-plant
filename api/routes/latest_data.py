from fastapi import APIRouter, HTTPException
from api.database import pool

router = APIRouter()


@router.get("/latest-data")
def get_latest_data():
    try:
        conn = pool.connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM drplant ORDER BY timestamp DESC LIMIT 1")
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            else:
                raise HTTPException(status_code=404, detail="No data found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    finally:
        conn.close()
