import queue
log_queue = queue.Queue()

def log(msg):
    log_queue.put(msg)
