from fastapi import APIRouter, HTTPException
import pandas as pd
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
import pymysql
from dbutils.pooled_db import PooledDB

router = APIRouter()

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=10,
    blocking=True
)


@router.get("/descriptive-stats")
def get_descriptive_statistics():
    try:
        conn = pool.connection()
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM drplant")
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

    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    desc_stats = numeric_df.describe().T.round(2).to_dict()

    return desc_stats
