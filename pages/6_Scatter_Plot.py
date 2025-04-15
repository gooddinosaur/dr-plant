import streamlit as st
import pandas as pd
import requests

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

    attribute_options = [col.capitalize() for col in df.columns if col not in ["id", "timestamp"]]

    x_attr = st.sidebar.selectbox("Select X-axis Attribute", options=attribute_options, index=0)
    y_attr = st.sidebar.selectbox("Select Y-axis Attribute", options=attribute_options, index=1)

    x_attr = x_attr.lower()
    y_attr = y_attr.lower()
    st.title("🔍 Scatter Plot : Attribute Relationship")
    st.markdown(f"""
        This scatter plot shows the relationship between **{x_attr.capitalize()}** and **{y_attr.capitalize()}**.
    """)

    if x_attr == y_attr:
        st.warning("Please select two different attributes.")
    else:
        with st.spinner("Generating scatter plot..."):
            image_url = f"http://localhost:8000/scatter-plot?x_attr={x_attr}&y_attr={y_attr}"
            response = requests.get(image_url)

        if response.status_code == 200:
            st.image(response.content, caption=f"{y_attr.capitalize()} vs {x_attr.capitalize()}",
                     width=1000)
            with st.expander("📄 View Raw Data"):
                st.dataframe(df[[x_attr, y_attr]])
        else:
            st.error(f"Failed to load scatter plot: {response.status_code} - {response.text}")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
