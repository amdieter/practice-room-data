from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Statistics",
    page_icon="📊",
)

st.title("📊 Statistics")

@st.cache_data
def load_entries():
    return pd.read_csv(
        "entries.csv",
        parse_dates=["datetime"]
    )


entries = load_entries()

# entries by person by day plot
person = title = st.text_input("Entry name", "Aaron Dieter") # input for person name
fig, ax = plt.subplots()

if person not in entries["person"].unique():
    st.write(f"{person} not found in entries")
else:
    ax.plot(entries.groupby(["person","day"]).size()[person].index, entries.groupby(["person","day"]).size()[person])
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of Entries")
    ax.set_title(person + " vs. Number of Entries")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
