from threading import Lock

status_data = {
    "fps": 0,
    "roi_count": 0,
    "enter_count": 0,
    "exit_count": 0,
    "current_person_count": 0,
    "total_unique_ids": 0,
    "events": []
}

status_lock = Lock()

def update_status(data):
    with status_lock:
        status_data.update(data)

def get_status():
    with status_lock:
        return status_data.copy()