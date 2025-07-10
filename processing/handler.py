import time
from processing.fusion_engine import is_duplicate
from processing.message_queue import message_queue

def handle_detection(msg: dict):
    """Aplica deduplicação e mete na fila."""
    if is_duplicate(msg):
        return
    msg["queue_enter_ns"] = time.perf_counter_ns()
    message_queue.put(msg)
