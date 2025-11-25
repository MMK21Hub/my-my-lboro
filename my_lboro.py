from datetime import datetime
from requests import Session

from my_lboro_types import CalendarEventsResponse


class MyLboro:
    """An API client, of sorts, for the myLboro app API"""

    class Endpoints:
        base = "https://my.lboro.ac.uk/campusm/sso"
        LogIn = f"{base}/ldap/2548"
        Calendars = f"{base}/calendars/CAL"

        # Calendar = lambda cal_type: f"{base}/cal2/{cal_type}"
        Calendar = f"{base}/cal2/{{cal_type}}"

    def __init__(self):
        self.USER_AGENT = "my-my-lboro/0.1"
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": self.USER_AGENT,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def log_in(self, username: str, password: str):
        res = self.session.post(
            self.Endpoints.LogIn,
            data={"username": username, "password": password},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            timeout=10,
        )
        res.raise_for_status()
        account_info = res.json()
        return account_info

    def get_calendars(self):
        res = self.session.get(self.Endpoints.Calendars)
        res.raise_for_status()
        data = res.json()
        return data["calendars"]

    def get_calendar_events(self, cal_type: str, start: datetime, end: datetime):
        res = self.session.get(
            url=self.Endpoints.Calendar.format(cal_type=cal_type),
            params={"start": start.isoformat(), "end": end.isoformat()},
        )
        res.raise_for_status()
        data = res.text
        return CalendarEventsResponse.model_validate_json(data).events

    def destroy(self):
        self.session.close()
