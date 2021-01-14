from threading import Event, get_ident
from time import time

class StreamEvent:
    def __init__(self):
        self.events = {}

    def clear(self):
        ident = get_ident()

        if ident in self.events:
            self.events[get_ident()][0].clear()

    def set(self):
        now = time()
        remove = None

        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 2:
                    remove = ident

        if remove:
            del self.events[ident]

    def wait(self):
        ident = get_ident()

        if ident not in self.events:
            self.events[ident] = [Event(), time()]

        return self.events[ident][0].wait()
