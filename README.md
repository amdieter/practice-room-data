# practice-room-data
This project extracts the practice room data from the practice room reservation google sheet from the UW-Madison percussion studio and summarizes it to get a rough idea of the practice habits of people in the studio.

### Background
The google spreadsheet is grouped by room, and 15 minute intervals from 7am to 11pm are available to be signed out for each room, and the sheet is reset every week (data is not saved).
This program extracts this data weekly, reformats it, and saves it locally which can then be grouped with the rest of the data saved to eventually be summarized in several ways from most popular practice room to the person with the most practice time.
This program is not a perfect representation of the practice habits of the UW-Madison percussion studio, but it provides us with a good idea of their habits.

### How it works:
1. gspread is used to access data of each room
2. Data is compiled into dictionaries of pandas dataframes
3. Data is written locally into a folder labeled by the week
4. Data can then be summarized with several data points of interest such as entries_by_person, entries_by_room, and entries_by_time
5. This summarized data can be maniuplated in different ways to depict different relationships such as practice time to grade level and practice time to room. Below is a visualization of grade level versus average amount of entries for that grade level.

<img src="grade_vs_avg.png" alt="grade_vs_avg">
