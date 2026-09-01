import streamlit as st
import pandas as pd
import datetime
from dateutil import parser
import gspread
from zoneinfo import ZoneInfo
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="Live Schedule",
    page_icon="📅",
)

st.title("📅 Live Schedule")

options = ["Today", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

default_index = options.index("Today")

day_option = st.selectbox(
    "Select Day of the Week",
    options,
    index=default_index
)

if day_option == "Today":
    date_time = datetime.datetime.now(ZoneInfo("America/Chicago"))
    date = date_time.date()
    day = date.strftime('%A')
else:
    day = day_option
    date = datetime.date.today()

# @st.cache_data
def get_data():
    creds_dict = st.secrets["gcp_service_account"]
    
    gc = gspread.service_account_from_dict(creds_dict)

    spreadsheet_key = '13CdEbddbIDDHdCVU9IvpHQzSB4lJroJ36Riufl5uvTk' # This is the real sheet
    book = gc.open_by_key(spreadsheet_key)

    # date_time = datetime.datetime.now(ZoneInfo("America/Chicago"))
    # date = date_time.date()
    # day = date.strftime('%A')

    # find week_num by comparing the dates in the spreadsheet to today's date
    week_num = None
    for i in range(1,3):
        week_num = i
        week = book.worksheet(f"Studio ({i})").acell('B2').value
        date_found = False
        for j in range(0,7):
            date_parsed = parser.parse(week[9:]).date() + datetime.timedelta(days=j)
            # st.write(f"Dates {i}: {date_parsed}")
            if date_parsed == date:
                # st.write(f"Found date {i}: {date_parsed}")
                date_found = True
                break
        if date_found:
            break

    all_sheets = book.worksheets()[:-1]
    wk_sheets = [sheet for sheet in all_sheets if f"({week_num})" in sheet.title] # filter for sheets with the current week number

    # convert current time to 15 minute increments

    if day_option == "Today":
        curr_time = date_time.time()

        def get_timeframe(curr_time):
            total_minutes = curr_time.hour * 60 + curr_time.minute
            rounded_minutes = (total_minutes // 15) * 15
            new_hour = rounded_minutes // 60
            new_minute = rounded_minutes % 60
            timeframe = datetime.time(hour=new_hour, minute=new_minute, second=0, microsecond=0)
            if (timeframe < datetime.time(hour=7, minute=0)) or (timeframe > datetime.time(hour=22, minute=45)):
                return None
            else:
                return timeframe
        
        timeframe = get_timeframe(curr_time)
        timeframe_formatted = timeframe.strftime("%I:%M %p").lstrip("0") if timeframe else None

        room_schedule_today = pd.DataFrame()
        rooms_occupied_now = []
        for room in wk_sheets:
            table = room.get_all_values()
            df = pd.DataFrame(table[3:67])
            df.columns = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df = df.set_index('Time').rename_axis('Time')
            if timeframe_formatted and timeframe_formatted in df.index:
                entry = df[day].loc[timeframe_formatted]
                if entry != '':
                    rooms_occupied_now.append(room.title[:-3])

            room_schedule_today[room.title[:-3]] = df[day]

        st.write(f"Current Schedule for {day} {date}:")
        st.dataframe(room_schedule_today)

        if rooms_occupied_now:
            st.write(f"Rooms currently occupied: {', '.join(rooms_occupied_now)}")
        else:
            st.write("No rooms are currently occupied.")
            if not timeframe_formatted:
                st.write("The practice rooms aren't open rn btw, I see you tryna be sneaky😏")

    else:
        room_schedule_today = pd.DataFrame()
        rooms_occupied_now = []
        for room in wk_sheets:
            table = room.get_all_values()
            df = pd.DataFrame(table[3:67])
            df.columns = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df = df.set_index('Time').rename_axis('Time')

            room_schedule_today[room.title[:-3]] = df[day]

        st.write(f"Current Schedule for {day} {date}:")
        st.dataframe(room_schedule_today)



    

data = get_data()