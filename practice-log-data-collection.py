import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import tkinter as tk

def get_data(week_num):
    # glibber glabber that I copied and pasted
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Documents/Python Scripts/Practice Log/practice-log-444917-d375b6889398.json', scope)
    gc = gspread.authorize(credentials)

    # spreadsheet_key = '1AgQWFFgXEYRAtokWU8NNDdGKy5R7DYBoPMFukrRtMiA' # This is the test sheet
    spreadsheet_key = '13CdEbddbIDDHdCVU9IvpHQzSB4lJroJ36Riufl5uvTk' # This is the real sheet
    book = gc.open_by_key(spreadsheet_key)

    # full_df
    # takes str room and int week_num and returns the str room and a df with filled in gaps
    def full_df(room, week_num):
        room_week = (room + " (" + str(week_num) + ")") 
        worksheet = book.worksheet(room_week)
        table = worksheet.get_all_values() # fetch values from worksheet
        
        # Format Table in Pandas
        # Time      Mon   Tue ...
        # 7:00 AM   Josh   '' ...
        # 7:15 AM   Josh   '' ...
        # ...
        df = pd.DataFrame(table[3:67])
        df.columns = ['Time', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        # code to fill in gaps
        for day in df:
            series = df[day]
            for idx in range(len(series)):
                cell = series.iloc[idx]
                before_cell = series.iloc[idx-1]
                if cell == before_cell: # upper entry case
                    continue
                if cell != '':   # "if cell is not empty..."
                    diff = 1
                    for count in range(1,9):
                        if (idx + count) > (len(series) - 1):   # max bounds case
                            break
                        next_cell = series.iloc[idx + count]
                        if (next_cell != cell) and (next_cell != ''): # different entry case
                            break
                        if next_cell == cell:
                            if (idx + count + 1) > (len(series) - 1): # max bounds case
                                diff = count
                                break
                            next_next_cell = series.iloc[idx + count + 1]
                            if next_next_cell == next_cell:
                                break
                            diff = count
                            break
                    for i in range(diff):
                        df.loc[i + idx, day] = cell
                    
    df = df.set_index('Time').rename_axis('Time')
    return room, df

    # rooms
    rooms = ["Studio", "1401", "1407", "1409", "1413", "1414", "1416", "1417", "1418"]

    # compile dataframes, don't run too much or will overload page
    compiled_data = {}
    for room in rooms:
        room, df = full_df(room, week_num)
        compiled_data[room] = df

    return compiled_data

master = tk.Tk()

master.geometry("500x350")
master.title("Practice Log Data Collection")
wkNum_label = tk.Label(master, text="Enter the week number (1 or 2):")
wkNum_label.pack(pady=10)
wkNum_entry = tk.Entry(master)
wkNum_entry.pack(pady=5)
wkDate_label = tk.Label(master, text="Enter the week date (MM_DD_YY):")
wkDate_label.pack(pady=10)
wkDate_entry = tk.Entry(master)
wkDate_entry.pack(pady=5)
def submit():
    week_num = int(wkNum_entry.get())
    week_date = str(wkDate_entry.get())
    week_data = get_data(week_num)
    directory = Path(f'Documents/Python Scripts/Practice Log/data/{week_date}').mkdir(parents=True, exist_ok=True) # creates directory for week date if it doesn't exist, otherwise does nothing

    # write csv files and such to store compiled week data
    for room, df in week_data.items():
        df.to_csv("Documents/Python Scripts/Practice Log/data/"+ week_date + "/" + room + ".csv", index=True)
        print(room + " data for week " + str(week_num) + " has been written to csv.")

    success_label = tk.Label(master, text="Submission successful! Check the data folder for the csv files.")
    success_label.pack(pady=10)

button = tk.Button(master, text="Submit", command=submit)
button.pack(pady=10)

master.mainloop()