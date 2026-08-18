import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="UW Percussion Practice Rooms",
    page_icon="🥁",
)


st.title("🥁 UW Percussion Practice Rooms")

st.write("Practice room dashboard")

rooms = ["Studio", "1401", "1407", "1409", "1413", "1414", "1416", "1417", "1418"]

# live_schedule = st.Page("pages/1_live-schedule.py")
# occupancy_predictions = st.Page("pages/2_occupancy-predictions.py")


# pg = st.navigation([live_schedule, occupancy_predictions])
# pg.run()






