# 🌿 Dr.Plant

**Dr.Plant** is a smart plant care web application built with **Streamlit** and **FastAPI**.  
It leverages data from **KidBright sensors**, **OpenWeather API**, and a **Kaggle dataset** to monitor plant health and provide actionable care recommendations.

A machine learning model analyzes:
- 🌱 Soil Moisture  
- 💧 Humidity  
- 🔆 Light Intensity  
- 🌡️ Ambient Temperature  

Based on this analysis, the system suggests ways to improve growing conditions.  
Users can also explore interactive charts and historical data to better understand their plant's needs.

---

## ✅ Features

- 📊 **Home Page**: Display the latest data collected from sensors.
- 🧮 **Descriptive Statistics**: Show basic statistics like mean, min, and max of each feature.
- 📈 **Data Over Time**: Visualize trends using line charts filtered by date and sensor type.
- 🤖 **Predict Health**: Enter custom sensor values to predict plant health using a trained model.
- 🌱 **Care Recommendations**: Get personalized suggestions based on the predicted health and clustering results.
- 📷 **Data Visualization**: Create charts (histogram, scatter plot) to explore the data.

---
## 👥 Team Members
- 6610545341 Pannatat Nakornpuckdee (Software and Knowledge Engineering)
- 6610545464 Peerapat Seenoi (Software and Knowledge Engineering)
---


## 🛠️ Required Libraries and Tools

| Tool / Library       | Version     | Purpose                                |
|----------------------|-------------|----------------------------------------|
| Python               | 3.11+       | Core language                          |
| Streamlit            | 1.30.0      | Web UI framework                       |
| FastAPI              | 0.110.0     | API backend                            |
| scikit-learn         | 1.3.2       | Machine learning model                 |
| pandas               | 2.2.1       | Data processing and analysis           |
| matplotlib           | 3.8.3       | Data visualization                     |
| joblib               | 1.3.2       | Load/save ML model and scaler          |
| SQLAlchemy           | 2.0.27      | Database ORM                           |
| mysql-connector-python | 8.3.0     | MySQL connection                       |
| uvicorn              | 0.29.0      | ASGI server for FastAPI                |

---
## ⚙️ Installation

📄 Follow the step-by-step instructions [here](./Installation.md).

---

## 🚀 Running the Application

- Start the Streamlit Server
```
python -m streamlit run 0_Home.py
 ```

- Start the FastAPI server
```
python -m uvicorn api.main:app --reload --port 8000
 ```

---
## 📃 Project Documents
All project documents are in the [Project Wiki](../../wiki/Home) (Diagrams, Presentation Slide).
