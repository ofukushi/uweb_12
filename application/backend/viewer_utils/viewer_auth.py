
# chart_viewer/utils/auth.py

import os
import logging
import requests
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load credentials from env
JQ_USER = os.getenv("G_MAIL_ADDRESS")
JQ_PASS = os.getenv("J_QUANTS_PASSWORD")

def get_refresh_token() -> str:
    """Fetch refresh token using email and password."""
    data = {"mailaddress": JQ_USER, "password": JQ_PASS}
    res = requests.post(
        "https://api.jquants.com/v1/token/auth_user",
        data=json.dumps(data)
    )
    if res.status_code != 200 or "refreshToken" not in res.json():
        logging.error("Failed to get refresh token: %s", res.text)
        return None
    return res.json()["refreshToken"]

from time import sleep

def get_id_token(retries=3) -> str:
    for attempt in range(retries):
        refresh_token = get_refresh_token()
        if not refresh_token:
            continue
        res = requests.post(
            f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}"
        )
        if res.status_code == 200 and "idToken" in res.json():
            return res.json()["idToken"]
        logging.warning("Retrying ID token fetch... (%d/%d)", attempt + 1, retries)
        sleep(1)
    logging.error("Failed to get ID token after retries.")
    return None

