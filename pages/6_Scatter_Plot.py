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

    attribute_options = [col.capitalize() for col in df.columns if
                         col not in ["id", "timestamp"]]

    x_attr = st.sidebar.selectbox("Select X-axis Attribute",
                                  options=attribute_options, index=0)
    y_attr = st.sidebar.selectbox("Select Y-axis Attribute",
                                  options=attribute_options, index=1)

    st.sidebar.markdown("""
        <style>
        div.stButton > button {
            background-color: #2196F3;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0b7dda;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }
        div.stButton > button:active {
            transform: translateY(0px);
        }
        </style>
    """, unsafe_allow_html=True)

    generate_button = st.sidebar.button("🔄 Generate Scatter Plot",
                                        use_container_width=True)

    x_attr = x_attr.lower()
    y_attr = y_attr.lower()
    st.title("🔍 Scatter Plot : Attribute Relationship")
    st.markdown(f"""
        This scatter plot shows the relationship between **{x_attr.capitalize()}** and **{y_attr.capitalize()}**.
    """)

    if x_attr == y_attr:
        st.warning("Please select two different attributes.")
    elif generate_button:
        with st.spinner("Generating scatter plot..."):
            image_url = f"http://localhost:8000/scatter-plot?x_attr={x_attr}&y_attr={y_attr}"
            response = requests.get(image_url)

        if response.status_code == 200:
            st.image(response.content,
                     caption=f"{y_attr.capitalize()} vs {x_attr.capitalize()}",
                     width=1000)
            with st.expander("📄 View Raw Data"):
                st.dataframe(df[[x_attr, y_attr]])
        else:
            st.error(
                f"Failed to load scatter plot: {response.status_code} - {response.text}")
    else:
        st.info(
            "👈 Select your attributes and click 'Generate Scatter Plot' in the sidebar to create the visualization.")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")