from os import getenv
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://my.lboro.ac.uk/campusm/sso/ldap/2548"
data = {"username": getenv("USERNAME"), "password": getenv("PASSWORD")}  # <- replace
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

with requests.Session() as session:
    # session preserves cookies (equivalent to credentials: include)
    response = session.post(url, data=data, headers=headers, timeout=10)
    response.raise_for_status()
    print(response.status_code)
    print(response.text)
    print(response.headers)
