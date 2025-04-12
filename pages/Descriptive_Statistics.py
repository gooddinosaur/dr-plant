import streamlit as st
import pandas as pd
from utils.statistics import get_statistics

st.header("📊 Descriptive Statistics")

data = get_statistics()

if data.empty:
    st.warning("No data available for statistics.")
else:
    st.write("Here are your plant’s sensor stats:")
    st.dataframe(data.describe())
