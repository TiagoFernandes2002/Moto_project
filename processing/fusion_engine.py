import time
recent_events = {}

def is_duplicate(data):
    event_id = data["MessageID"]
    now = time.time()
    if event_id in recent_events and now - recent_events[event_id] < 3:
        return True
    recent_events[event_id] = now
    return False
