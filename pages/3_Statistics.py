import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
import re
from datetime import datetime
from datetime import timedelta

st.set_page_config(
    page_title="Statistics",
    page_icon="📊",
)

st.title("📊 Statistics")

@st.cache_data
def load_entries():
    return pd.read_csv(
        "entries/entries-8_22_26.csv",
        parse_dates=["datetime"]
    )

@st.cache_data
def load_perc_stats():
    return pd.read_csv(
        "perc_stats/perc_stats-8_22_26.csv",
    )

perc_stats = load_perc_stats()

entries = load_entries()

# entries by person by day plot
person = title = st.text_input("Entry name", "Aaron Dieter") # input for person name
fig, ax = plt.subplots()

if person not in entries["person"].unique():
    st.write(f"{person} not found in entries")
else:
    # personal stats
    st.dataframe(perc_stats[perc_stats["Name"] == person])

    # plot person by day

    # Get this person's entries per day
    daily_entries = (
        entries[entries["person"] == person]
        .groupby("day")
        .size()
        .sort_index()
    )

    # Make sure day is datetime
    daily_entries.index = pd.to_datetime(daily_entries.index)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        daily_entries.index,
        daily_entries.values,
        marker="*",
        linewidth=2,
        color="green",
        markersize=5
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Entries")
    ax.set_title(f"{person}: Entries per Day", fontsize=14, fontweight="bold")

    # Format dates nicely
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    st.pyplot(fig)
