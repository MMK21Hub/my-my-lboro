from collections import deque
from datetime import datetime, timedelta
from math import ceil
from time import monotonic

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from config import config
from convert_to_ical import convert_events_to_ical
from my_lboro import MyLboro

# The calendar that we're interested in (i.e. the one that contains the timetable)
# We _could_ fetch available calendars from the API, but I don't think that would
# meaningly improve reliability of this program.
MAIN_CALENDAR_ID = "Student Timetable"

client = MyLboro(auth_token=config.lboro_auth_token, contact_email=config.contact_email)

app = FastAPI(
    title="My myLboro (timetable API)",
    description="""
A service that provides your Loughborough University timetable in [iCalendar format](https://icalendar.org/), ready to be imported into Google Calendar, Thunderbird, or any other calendar app!

Source code: [GitHub - MMK21Hub/my-my-lboro](https://github.com/MMK21Hub/my-my-lboro)
""",
)


request_times: deque[float] = deque()
last_upstream_success: float | None = None
RATE_LIMIT = 30
RATE_WINDOW_SECONDS = 60


async def enforce_rate_limit():
    now = monotonic()
    while request_times and now - request_times[0] >= RATE_WINDOW_SECONDS:
        request_times.popleft()
    if len(request_times) >= RATE_LIMIT:
        retry_after = ceil(RATE_WINDOW_SECONDS - (now - request_times[0]))
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )
    request_times.append(now)


@app.get("/")
async def root():
    return HTMLResponse("""
<p>Hello!</p>
                        
<p>You have reached the My myLboro timetable API.</p>
                        
<p>Perhaps you'd like to <a href="/docs">take a look at the documentation page</a> for more info.</p>
""")


@app.get("/health")
async def health_check():
    global last_upstream_success
    functioning = (
        last_upstream_success is not None
        and monotonic() - last_upstream_success < RATE_WINDOW_SECONDS
    )
    if not functioning:
        await enforce_rate_limit()
        start = datetime.now()
        end = start + timedelta(days=1)
        try:
            client.get_calendar_events(MAIN_CALENDAR_ID, start, end)
            last_upstream_success = monotonic()
            functioning = True
        except Exception:  # noqa: BLE001
            functioning = False
    alive = client.alive
    ok = alive and functioning
    status_code = 200 if ok else 503
    return JSONResponse(
        {
            "ok": ok,
            "alive": alive,
            "functioning": functioning,
        },
        status_code,
    )


@app.get("/timetables", dependencies=[Depends(enforce_rate_limit)])
async def get_timetables():
    """Provides a list of available timetables."""
    global last_upstream_success
    calendars = client.get_calendars()
    last_upstream_success = monotonic()
    return {"timetables": calendars}


@app.get("/lboro.ics", dependencies=[Depends(enforce_rate_limit)])
async def get_calendar_ics(
    timetable: str = MAIN_CALENDAR_ID, days_ahead: int = 90, days_behind: int = 7
):
    """Provides your timetable in iCalendar format.

    Query parameters:
    - `timetable`: The timetable to fetch (default: `Student Timetable`)
    - `days_ahead`: How many days events should be fetched for, starting from today (default: `90`)
    - `days_behind`: How many extra days of events should be fetched from before today (default: `7`)
    """
    global last_upstream_success
    events = client.get_calendar_events(
        timetable,
        datetime.now() + timedelta(days=-days_behind),
        datetime.now() + timedelta(days=days_ahead),
    )
    last_upstream_success = monotonic()
    ical = convert_events_to_ical(events)
    return StreamingResponse(content=ical, media_type="text/calendar")
