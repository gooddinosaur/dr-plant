import pandas as pd
import joblib

def get_thresholds():
    df = pd.read_csv("plant_health_data.csv")  # เปลี่ยน path ให้ตรง

    # กรองเฉพาะพืชที่สุขภาพดี
    healthy_df = df[df['Plant_Health_Status'] == 'Healthy']

    # ใช้เฉพาะ features ที่เกี่ยวข้อง
    selected_features = ['Soil_Moisture', 'Humidity', 'Light_Intensity', 'Ambient_Temperature']
    stats = {}

    for col in selected_features:
        stats[col] = {
            'mean': healthy_df[col].mean(),
            'std': healthy_df[col].std(),
            'min': healthy_df[col].min(),
            'max': healthy_df[col].max(),
        }

    joblib.dump(stats, "feature_thresholds.pkl")

if __name__ == "__main__":
    get_thresholds()
