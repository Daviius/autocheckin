import threading
from web.state import STOP_EVENT
from web.logger import log
from core.slot_manager import init_slots
from core.worker import run_profile
from utils.excel import load_profiles

def start_automation(project_cls, excel_path, max_concurrent):
    STOP_EVENT.clear()
    init_slots()
    profiles = load_profiles(excel_path)
    sem = threading.Semaphore(max_concurrent)

    def task(profile):
        with sem:
            if STOP_EVENT.is_set():
                return
            project = project_cls()
            run_profile(profile, project)
            log(f"DONE {profile['profile_id']}")

    def runner():
        for p in profiles:
            if STOP_EVENT.is_set():
                break
            threading.Thread(target=task, args=(p,), daemon=True).start()
        log("ALL DONE")

    threading.Thread(target=runner, daemon=True).start()

def stop_automation():
    STOP_EVENT.set()
    log("STOP REQUESTED")
