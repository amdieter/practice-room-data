import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
import re
from datetime import date, datetime
from datetime import time
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


entries = load_entries()

min_date = pd.to_datetime(entries["datetime"]).min().date()
max_date = pd.to_datetime(entries["datetime"]).max().date()

# select timeframe
timeframe = st.slider(
    "Select timeframe", value=(min_date, max_date), format="MM/DD/YYYY", 
    min_value=min_date, max_value=max_date, step=timedelta(days=1)
)

st.write("Timeframe selected:", timeframe[0], "to", timeframe[1])

entries = entries[(entries["datetime"].dt.date >= timeframe[0]) & (entries["datetime"].dt.date <= timeframe[1])]

# Functions to summarize stats
# entries to time conversion function
def entries_to_time(row):
    hours = row['Entries']*15/60
    hours_mins = str(hours).split('.')
    if int(hours_mins[0]) == 0:
        return str(int(float('.'+hours_mins[1])*60)) + 'mins'
    else: 
        return str(hours_mins[0]) + 'hrs ' + str(int(float('.'+hours_mins[1])*60)) + 'mins'

def entries_to_time_reg(entries):
    hours = entries*15/60
    hours_mins = str(hours).split('.')
    if int(hours_mins[0]) == 0:
        return str(int(float('.'+hours_mins[1])*60)) + 'mins'
    else: 
        return str(hours_mins[0]) + 'hrs ' + str(int(float('.'+hours_mins[1])*60)) + 'mins'

# entries to time per day (assume 7 days a week)
def entries_to_time_p_day(row):
    hours = row['Entries']*15/60/(len(entries.groupby(['person',"day"]).size()[row['Name']]))  # divide by the 7 days in the week
    hours_mins = str(hours).split('.')
    if int(hours_mins[0]) == 0:
        return str(int(float('.'+hours_mins[1])*60)) + 'mins'
    else: 
        return str(hours_mins[0]) + 'hrs ' + str(int(float('.'+hours_mins[1])*60)) + 'mins'

def entries_to_entries_p_day(row):
    entries_per_day = row['Entries']/(len(entries.groupby(['person',"day"]).size()[row['Name']]))  # divide by the 7 days in the week
    return round(entries_per_day, 2)

def fav(row, series):
    try:
        person_series = series.loc[row["Name"]]
    except KeyError:
        return []

    max_val = person_series.max()
    favorites = person_series[person_series == max_val]

    return [
        (idx, entries_to_time_reg(max_val))
        for idx in favorites.index
    ]


def get_summarized_stats(entries):
    perc_stats = entries.groupby(["person","grade"]).size().reset_index()
    perc_stats.columns = ['Name',"Grade",'Entries']

    # Time Practiced
    perc_stats['Time Practiced'] = perc_stats.apply(entries_to_time, axis=1)

    # Entries/Day
    perc_stats['AVG Entries per Day'] = perc_stats.apply(entries_to_entries_p_day, axis=1)

    # Time/Day
    perc_stats['AVG Time per Day'] = perc_stats.apply(entries_to_time_p_day, axis=1)

    # Favorite Practice Timeframe
    perc_stats['Favorite Practice Timeframe'] = perc_stats.apply(fav, args = (entries.groupby(["person",'time']).size(),), axis=1)

    # Favorite Practice Room
    perc_stats['Favorite Practice Room'] = perc_stats.apply(fav, args = (entries.groupby(['person','room']).size(),), axis=1)

    # Most Practicing in a Day
    perc_stats['Most Practicing in a Day'] = perc_stats.apply(fav, args = (entries.groupby(['person',"day"]).size(),), axis=1)

    return perc_stats

perc_stats = get_summarized_stats(entries)



# select individual person or overall stats
option = st.selectbox(
    "Whose stats do you want to see?",
    ("Overall", "Individual")
)

if option == "Overall":
    st.write("Overall stats for all entries in the selected timeframe")

    sort_option = st.selectbox(
        "Sort by:",
        ("Name", "Grade", "Entries/Time Practiced", "AVG Entries/Time per Day")
    )
    if sort_option == "Name":
        perc_stats = perc_stats.sort_values(by=["Name"])
    elif sort_option == "Grade":
        perc_stats = perc_stats.sort_values(by=["Grade"])
    elif sort_option == "Entries/Time Practiced":
        perc_stats = perc_stats.sort_values(by=["Entries"], ascending=False)
    elif sort_option == "AVG Entries/Time per Day":
        perc_stats = perc_stats.sort_values(by=["AVG Entries per Day"], ascending=False)

    filter_options = st.multiselect(
        "Filters:",
        ["Studio Members", "Unknown Entries", "Freshman", "Sophomore", "Junior", "Senior", 
         "Graduate", "Super-Senior", "Masters", "DMA"],
        default=["Studio Members"],
    )
    if not filter_options:
        pass
    else:
        perc_stats = perc_stats[perc_stats["Grade"].isin(filter_options)]
    

    st.dataframe(perc_stats)

if option == "Individual":
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
        plt.ylim(0)
        plt.xlim(timeframe[0], timeframe[1])


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
