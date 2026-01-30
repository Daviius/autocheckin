
from queue import Queue
from config import *

slot_queue = Queue()

def init_slots():
    while not slot_queue.empty():
        slot_queue.get()
    for i in range(MAX_CONCURRENT_PROFILES):
        x = i * (WIN_WIDTH + WINDOW_PADDING)
        y = WIN_TOP
        slot_queue.put((x, y))

def acquire_slot():
    return slot_queue.get()

def release_slot(slot):
    slot_queue.put(slot)
