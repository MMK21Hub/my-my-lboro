from os import getenv
import requests
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
