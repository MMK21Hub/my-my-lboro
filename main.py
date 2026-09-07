from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from config import config
from convert_to_ical import convert_events_to_ical
from my_lboro import MyLboro

# The calendar that we're interested in (i.e. the one that contains the timetable)
# We _could_ fetch available calendars from the API, but I don't think that would
# meaningly improve reliability of this program.
CALENDAR_ID = "Student Timetable"

client = MyLboro(contact_email=config.contact_email)
cal_start = datetime.now() + timedelta(days=0)
cal_end = datetime.now() + timedelta(days=7)
course_timetable = client.get_calendar_events(CALENDAR_ID, cal_start, cal_end)

app = FastAPI(
    title="My myLboro (timetable API)",
    description="""
A service that provides your Loughborough University timetable in [iCalendar format](https://icalendar.org/), ready to be imported into Google Calendar, Thunderbird, or any other calendar app!

Source code: [GitHub - MMK21Hub/my-my-lboro](https://github.com/MMK21Hub/my-my-lboro)
""",
)


@app.get("/")
async def root():
    return HTMLResponse("""
<p>Hello!</p>
                        
<p>You have reached the My myLboro timetable API.</p>
                        
<p>Perhaps you'd like to <a href="/docs">take a look at the documentation page</a> for more info.</p>
""")


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running.

    Note that a more accurate health check would be to GET `/timetables`, as
    that actually verifies connection to the myLboro API. But this at least
    shows that the service is alive.
    """
    alive = client.alive
    # TODO improve
    ok = alive
    return JSONResponse(
        {
            "ok": ok,
            "alive": alive,
        }
    )


@app.get("/timetables")
async def get_timetables():
    """Provides a list of available timetables."""
    return {"timetables": client.get_calendars()}


@app.get("/lboro.ics")
async def get_calendar_ics(
    timetable: str = "course_timetable", days_ahead: int = 90, days_behind: int = 7
):
    """Provides your timetable in iCalendar format.

    Query parameters:
    - `timetable`: The timetable to fetch (e.g. `course_timetable`, `sports_timetable`) (default: `course_timetable`)
    - `days_ahead`: How many days events should be fetched for, starting from today (default: `90`)
    - `days_behind`: How many extra days of events should be fetched from before today (default: `7`)
    """
    events = client.get_calendar_events(
        timetable,
        datetime.now() + timedelta(days=-days_behind),
        datetime.now() + timedelta(days=days_ahead),
    )
    ical = convert_events_to_ical(events)
    return StreamingResponse(content=ical, media_type="text/calendar")
