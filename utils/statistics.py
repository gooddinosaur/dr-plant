import pandas as pd
import os

def get_statistics():
    # Simulate sensor data
    # In real app, load from database or file
    if os.path.exists("sensor_data.csv"):
        df = pd.read_csv("sensor_data.csv")
        return df
    else:
        return pd.DataFrame()
