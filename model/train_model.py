import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# โหลดข้อมูล
data = pd.read_csv("plant_health_data.csv")

# เลือกเฉพาะคอลัมน์ที่ต้องการ
X = data[["Soil_Moisture", "Humidity", "Light_Intensity", "Ambient_Temperature"]]
y = data["Plant_Health_Status"]

# แปลง label เป็นตัวเลข
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# แบ่งข้อมูล
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# เทรน KNN
knn_model = KNeighborsClassifier(n_neighbors=3)  # สามารถลองเปลี่ยนค่า k ได้เช่น 3, 7, 9
knn_model.fit(X_train, y_train)

# ประเมินผล
y_pred = knn_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=le.classes_))

# บันทึกโมเดล
joblib.dump(knn_model, "plant_health_model.pkl")
joblib.dump(le, "label_encoder.pkl")
