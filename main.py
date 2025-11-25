from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from convert_to_ical import convert_events_to_ical
from my_lboro import MyLboro
from config import config

client = MyLboro()
user = client.log_in(config.lboro_username, config.lboro_password)
calendars = client.get_calendars()
cal_start = datetime.now() + timedelta(days=0)
cal_end = datetime.now() + timedelta(days=7)
course_timetable = client.get_calendar_events("course_timetable", cal_start, cal_end)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lboro.ics")
async def get_calendar_ics():
    events = client.get_calendar_events(
        "course_timetable",
        datetime.now() + timedelta(days=0),
        datetime.now() + timedelta(days=7),
    )
    ical = convert_events_to_ical(events)
    return StreamingResponse(content=ical, media_type="text/calendar")
