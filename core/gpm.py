
import requests
from config import *

def start_profile(profile_id, x, y):
    url = (
        f"http://127.0.0.1:{GPM_PORT}/api/v3/profiles/start/{profile_id}"
        f"?win_size={WIN_WIDTH},{WIN_HEIGHT}"
        f"&win_pos={x},{y}"
        f"&win_scale={WIN_SCALE}"
    )
    r = requests.get(url).json()
    if not r.get("success"):
        return None
    return r["data"]["remote_debugging_address"]

def close_profile(profile_id):
    try:
        requests.get(f"http://127.0.0.1:{GPM_PORT}/api/v3/profiles/close/{profile_id}", timeout=5)
    except:
        pass
