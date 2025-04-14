import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Dr.Plant",
    page_icon="🌿",
    layout="wide"
)


st.title("🌿 Dr.Plant: Plant Health Predictor")

st.markdown(
    """
Welcome to **Dr.Plant**!  
A smart assistant that helps you take care of your plant using sensor data and weather info.  
Navigate through the pages using the sidebar.
"""
)

st.markdown("---")


st.subheader("🌱 Latest Sensor Data")
with st.spinner("Fetching latest data..."):
    try:
        response = requests.get("http://localhost:8000/latest-data")
        if response.status_code == 200:
            data = response.json()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌡 Temperature (°C)", f"{data['temperature']}")
            col2.metric("💧 Humidity (%)", f"{data['humidity']}")
            col3.metric("🌞 Light Intensity (lux)", f"{data['light']}")
            col4.metric("🌱 Soil Moisture (%)", f"{data['soil']}")
            timestamp = datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            st.markdown(f"<h5 style='margin-top:30px;'>🕒 Time: {timestamp}</h5>", unsafe_allow_html=True)

        else:
            st.error("❌ Could not fetch data from API.")
    except Exception as e:
        st.error(f"❌ Error connecting to API: {e}")
