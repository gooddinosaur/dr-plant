import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="🔍 Attribute Relationship", layout="wide")

st.sidebar.title("⚙️ Scatter Plot Options")


@st.cache_data
def fetch_data():
    response = requests.get("http://localhost:8000/data")
    response.raise_for_status()
    return pd.DataFrame(response.json())


try:
    df = fetch_data()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    attribute_options = [col.capitalize() for col in df.columns if
                         col not in ["id", "timestamp"]]

    x_attr = st.sidebar.selectbox("Select X-axis Attribute",
                                  options=attribute_options, index=0)
    y_attr = st.sidebar.selectbox("Select Y-axis Attribute",
                                  options=attribute_options, index=1)

    x_attr = x_attr.lower()
    y_attr = y_attr.lower()
    st.title("🔍 Scatter Plot : Attribute Relationship")
    st.markdown(f"""
        This scatter plot shows the relationship between **{x_attr.capitalize()}** and **{y_attr.capitalize()}**.
    """)

    if x_attr == y_attr:
        st.warning("Please select two different attributes.")
    else:
        fig = px.scatter(
            df, x=x_attr, y=y_attr,
            title=f"{y_attr.capitalize()} vs {x_attr.capitalize()}",
            labels={x_attr: x_attr.replace("_", " ").title(),
                    y_attr: y_attr.replace("_", " ").title()},
            trendline="ols"
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 View Raw Data"):
            st.dataframe(df[[x_attr, y_attr]])

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
