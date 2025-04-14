import streamlit as st
import pandas as pd
import requests

st.header("📊 Descriptive Statistics")

# URL ของ API (เปลี่ยนตามที่อยู่จริงถ้าไม่ได้รันในเครื่องเดียวกัน)
API_URL = "http://localhost:8000/descriptive-stats"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    result = response.json()
    stats = pd.DataFrame(result).T

    st.write("Here are your plant’s sensor stats:")
    st.dataframe(stats)

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data: {e}")
except KeyError:
    st.error("Unexpected response format from API.")
