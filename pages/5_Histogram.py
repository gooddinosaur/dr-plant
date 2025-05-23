import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="📊 Histogram Generator", layout="wide")
st.sidebar.title("⚙️ Histogram Options")


@st.cache_data
def fetch_data():
    response = requests.get("http://localhost:8000/data")
    response.raise_for_status()
    return pd.DataFrame(response.json())


try:
    df = fetch_data()
    numeric_columns = [col.capitalize() for col in df.columns if
                       pd.api.types.is_numeric_dtype(df[col]) and col != "id"]

    selected_feature = st.sidebar.selectbox("Select Feature",
                                            options=numeric_columns, index=0)
    bin_value = st.sidebar.slider("Number of Bins", min_value=5, max_value=50,
                                  value=20, step=1)

    # Create a styled button in the sidebar
    st.sidebar.markdown("""
        <style>
        div.stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #3e8e41;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }
        div.stButton > button:active {
            transform: translateY(0px);
        }
        </style>
    """, unsafe_allow_html=True)

    generate_button = st.sidebar.button("🔄 Generate Histogram",
                                        use_container_width=True)

    selected_feature = selected_feature.lower()
    st.title("📊 Histogram Visualization")
    st.markdown(f"""
        This histogram shows the distribution of **{selected_feature.capitalize()}** using **{bin_value} bins**.
    """)

    if generate_button:
        with st.spinner("Generating histogram..."):
            img_url = f"http://localhost:8000/histogram?feature={selected_feature}&bin_value={bin_value}"
            response = requests.get(img_url)

        if response.status_code == 200:
            st.image(response.content,
                     caption=f"Histogram of {selected_feature.capitalize()}",
                     width=1000)
            with st.expander("📄 View Raw Data"):
                st.dataframe(df[[selected_feature]])
        else:
            st.error(
                f"Failed to generate histogram: {response.status_code} - {response.text}")
    else:
        st.info(
            "👈 Select your options and click 'Generate Histogram' in the sidebar to create the visualization.")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")