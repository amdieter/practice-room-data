import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="UW Percussion Practice Rooms",
    page_icon="🥁",
)


st.title("🥁 UW Percussion Practice Rooms")

st.write("Select a page from the navigation bar or below to view the live schedule, occupancy predictions, or statistics.")

# rooms = ["Studio", "1401", "1407", "1409", "1413", "1414", "1416", "1417", "1418"]

live_schedule_page = st.Page("pages/1_Live_Schedule.py")
occupancy_predictions_page = st.Page("pages/2_Occupancy_Predictions.py")
statistics_page = st.Page("pages/3_Statistics.py")

pg = st.navigation([live_schedule_page, occupancy_predictions_page, statistics_page], position="hidden")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link(live_schedule_page) # , label="Home", icon="📅"
with col2:
    st.page_link(occupancy_predictions_page) # , label="Dashboard", icon="🎯"
with col3:
    st.page_link(statistics_page) # , label="Statistics", icon="📊"

st.divider()

pg.run()






