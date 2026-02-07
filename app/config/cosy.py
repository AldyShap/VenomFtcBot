from dotenv import load_dotenv
from os import getenv
import base64

load_dotenv()
token = getenv("BOT_TOKEN")
ftc_username = getenv("FTC_USER_NAME")
ftc_token = getenv("FTC_TOKEN")

USERNAME= getenv("FTC_USER_NAME") # your user name
API_KEY = getenv("FTC_TOKEN") # your token

BASE_URL ="https://ftc-api.firstinspires.org/v2.0"

auth_str = f"{USERNAME}:{API_KEY}"
encoded = base64.b64encode(auth_str.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {encoded}",
    "Accept": "application/json"
}

FTC_SEASON = 2025