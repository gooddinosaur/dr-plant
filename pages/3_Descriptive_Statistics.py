import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Plant Monitoring Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Header with styling
st.markdown("""
    <h1 style='text-align: center; color: #2E7D32;'>🌱 Descriptive Statistics</h1>
""", unsafe_allow_html=True)

st.markdown("---")

API_URL = "http://localhost:8000/descriptive-stats"

try:
    # Display a spinner while loading data
    with st.spinner("Fetching data..."):
        response = requests.get(API_URL)
        response.raise_for_status()
        result = response.json()
        stats = pd.DataFrame(result).T

    # Create columns for stat metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Summary Statistics")

        # Display each metric in its own expandable section
        metrics = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]

        for metric in metrics:
            if metric in stats.index:
                with st.expander(f"{metric.capitalize()} Values"):
                    metric_values = stats.loc[metric]

                    # Create a clean horizontal display for each sensor type
                    for column in stats.columns:
                        st.metric(
                            label=column.replace("_", " ").title(),
                            value=f"{metric_values[column]:.2f}" if isinstance(
                                metric_values[column], float) else
                            metric_values[column]
                        )

    with col2:
        st.subheader("📈 Visualization")

        # Create dropdown to select which metric to visualize
        selected_metric = st.selectbox(
            "Select statistic to visualize:",
            options=[m for m in metrics if m in stats.index]
        )

        if selected_metric:
            # Prepare data for chart
            chart_data = pd.DataFrame({
                'Sensor': stats.columns,
                'Value': stats.loc[selected_metric].values
            })

            # Create bar chart
            fig = px.bar(
                chart_data,
                x='Sensor',
                y='Value',
                title=f"{selected_metric.capitalize()} Values Across Sensors",
                color='Sensor',
                labels={'Value': selected_metric.capitalize()}
            )
            st.plotly_chart(fig, use_container_width=True)

    # Show full data table in expandable section
    with st.expander("View Full Data Table"):
        st.dataframe(stats, use_container_width=True)

        # Add download button for CSV
        csv = stats.to_csv().encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"plant_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data: {e}")
    st.info("Please check if the API server is running at the specified URL.")
except KeyError as ke:
    st.error(f"Unexpected response format from API: {ke}")
except Exception as ex:
    st.error(f"An error occurred: {ex}")
