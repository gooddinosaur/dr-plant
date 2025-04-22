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
## Project Documents
All project documents are in the [Project Wiki](../../wiki/Home).
