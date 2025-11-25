from datetime import datetime, timedelta

from my_lboro import MyLboro
from config import config

client = MyLboro()
user = client.log_in(config.lboro_username, config.lboro_password)
print(user)
calendars = client.get_calendars()
print(calendars)
cal_start = datetime.now() + timedelta(days=0)
cal_end = datetime.now() + timedelta(days=7)
course_timetable = client.get_calendar_events("course_timetable", cal_start, cal_end)
print(course_timetable)
