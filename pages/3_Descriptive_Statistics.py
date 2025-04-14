import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Descriptive Statistics",
    page_icon="📶",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center;'>📶 Descriptive Statistics</h1>
""", unsafe_allow_html=True)

st.markdown("---")

API_URL = "http://localhost:8000/descriptive-stats"

try:
    with st.spinner("Fetching data..."):
        response = requests.get(API_URL)
        response.raise_for_status()
        result = response.json()
        stats = pd.DataFrame(result).T

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Summary Statistics")
        metrics = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
        for metric in metrics:
            if metric in stats.index:
                with st.expander(f"{metric.capitalize()}"):
                    metric_values = stats.loc[metric]
                    for column in stats.columns:
                        st.metric(
                            label=column.replace("_", " ").title(),
                            value=f"{metric_values[column]:.2f}" if isinstance(
                                metric_values[column], float) else
                            metric_values[column]
                        )

    with col2:
        st.subheader("📈 Statistic Visualization")

        selected_metric = st.selectbox(
            "📌 Select a metric to visualize",
            options=[m for m in metrics if m in stats.index]
        )

        if selected_metric:
            chart_data = pd.DataFrame({
                'Sensor': stats.columns,
                'Value': stats.loc[selected_metric].values
            })

            fig = px.bar(
                chart_data,
                x='Sensor',
                y='Value',
                title=f"{selected_metric.capitalize()} Values Across Sensors",
                color='Sensor',
                labels={'Value': selected_metric.capitalize()}
            )
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 View Full Data Table"):
        st.dataframe(stats, use_container_width=True)
        csv = stats.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"plant_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

except requests.exceptions.RequestException as e:
    st.error(f"❌ Failed to fetch data: {e}")
    st.info("ℹ️ Please check if the API server is running at the specified URL.")
except KeyError as ke:
    st.error(f"❌ Unexpected response format from API: {ke}")
except Exception as ex:
    st.error(f"❌ An error occurred: {ex}")
