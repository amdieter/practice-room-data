import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Occupancy Predictions",
    page_icon="🎯",
)

st.title("🎯 Occupancy Predictions")

st.write("ML model predictions for practice room occupancy")

@st.cache_data
def load_dataset():
    return pd.read_csv(
        "dataset.csv",
        parse_dates=["datetime"]
    )

dataset = load_dataset()

st.dataframe(dataset)