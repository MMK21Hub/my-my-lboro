from os import getenv
import requests
from dotenv import load_dotenv

load_dotenv()


class Endpoints:
    base = "https://my.lboro.ac.uk/campusm/sso"
    LogIn = f"{base}/ldap/2548"
    Calendars = f"{base}/calendars/CAL"


USER_AGENT = "my-my-lboro/0.0"

with requests.Session() as session:
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
        }
    )

    # Log in
    res = session.post(
        Endpoints.LogIn,
        data={"username": getenv("USERNAME"), "password": getenv("PASSWORD")},
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        timeout=10,
    )
    res.raise_for_status()
    account_info = res.json()
    print(account_info)

    res = session.get(Endpoints.Calendars)
    res.raise_for_status()
    data = res.json()
    print(data)
