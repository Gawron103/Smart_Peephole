from threading import get_ident

import threading
import time

class CameraEvent:
    def __init__(self):
        self.__events = {}

    def wait(self):
        # Invoked for each clients thread to wait for next frame
        ident = get_ident()

        if ident not in self.__events:
            # New client connected
            self.__events[ident] = [threading.Event(), time.time()]

        return self.__events[ident][0].wait()

    def set(self):
        # Invoke by the camera thread, when a new frame is available
        now = time.time()
        remove = None

        for ident, event in self.__events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident

        if remove:
            del self.__events[remove]

    def clear(self):
        # Invoke for each clients thread after a frame was processed
        self.__events[get_ident()][0].clear()