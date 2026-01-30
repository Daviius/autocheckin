from core.slot_manager import acquire_slot, release_slot
from core.gpm import start_profile, close_profile
from core.driver import attach_driver
from core.control import STOP_EVENT

def run_profile(profile, project):
    if STOP_EVENT.is_set():
        return
    slot = acquire_slot()
    x, y = slot
    driver = None
    try:
        if STOP_EVENT.is_set():
            return
        debug = start_profile(profile['profile_id'], x, y)
        if not debug or STOP_EVENT.is_set():
            return
        driver = attach_driver(debug)
        driver.set_window_position(x, y)
        if STOP_EVENT.is_set():
            return
        project.run(driver, profile)
    finally:
        try:
            if driver:
                driver.quit()
        except:
            pass
        close_profile(profile['profile_id'])
        release_slot(slot)
