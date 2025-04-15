import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="📊 Data Visualization", layout="wide")

st.sidebar.title("📅 Filter Options")

# ดึงข้อมูลจาก API
@st.cache_data
def fetch_data():
    response = requests.get("http://localhost:8000/data")
    response.raise_for_status()
    return pd.DataFrame(response.json())

try:
    df = fetch_data()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ----- Sidebar Filters -----
    min_date, max_date = df["timestamp"].min(), df["timestamp"].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    attribute = st.sidebar.selectbox(
        "Select Attribute",
        options=[col.capitalize() for col in df.columns if col not in ["id", "timestamp"]],
        index=0
    )
    attribute = attribute.lower()
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Line", "Bar"])

    # ----- Filtered Data -----
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]
    else:
        filtered_df = df

    st.title("📊 Plant Sensor Data Visualization")

    if filtered_df.empty:
        st.warning("No data available for the selected date range.")
    else:
        attribute_name = attribute.replace('_', ' ').capitalize()
        st.subheader(f"{attribute_name} Over Time")
        fig = None
        if chart_type == "Line":
            fig = px.line(filtered_df, x="timestamp", y=attribute, title=f"{attribute_name} Over Time")
        elif chart_type == "Bar":
            fig = px.bar(filtered_df, x="timestamp", y=attribute, title=f"{attribute_name} Over Time")
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 View Raw Data"):
            st.dataframe(filtered_df[["timestamp", attribute]])

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
