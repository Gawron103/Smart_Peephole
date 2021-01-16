from threading import Event, get_ident
from time import time


class StreamEvent:
    def __init__(self):
        self.__events = {}

    def clear(self):
        ident = get_ident()

        if ident in self.__events:
            self.__events[get_ident()][0].clear()

    def set(self):
        now = time()
        remove = None

        for ident, event in self.__events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 2:
                    remove = ident

        if remove:
            del self.__events[ident]

    def wait(self):
        ident = get_ident()

        if ident not in self.__events:
            self.__events[ident] = [Event(), time()]

        return self.__events[ident][0].wait()
