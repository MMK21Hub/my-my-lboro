from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv

from my_lboro import MyLboro

load_dotenv()

client = MyLboro()
username = getenv("USERNAME")
password = getenv("PASSWORD")
if username is None:
    raise ValueError("USERNAME environment variable not set")
if password is None:
    raise ValueError("PASSWORD environment variable not set")
user = client.log_in(username, password)
print(user)
calendars = client.get_calendars()
print(calendars)
cal_start = datetime.now() + timedelta(days=0)
cal_end = datetime.now() + timedelta(days=7)
course_timetable = client.get_calendar_events("course_timetable", cal_start, cal_end)
print(course_timetable)
