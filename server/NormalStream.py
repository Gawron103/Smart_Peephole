from threading import Thread
from time import time, sleep

from .Camera import Camera

import cv2

class NormalStream:
    def __init__(self, framesQue):
        self.frames = framesQue
        self.currentFrame = None

        self.thread = Thread(target=self.threadFunc)
        self.thread.start()

        while not self.getFrame():
            sleep(0)

        print('NormalStream init finished')

    def __del__(self):
        print('Normal Stream object deleted')

    def threadFunc(self):
        print('Starting NormalStream thread func')

        while True:
            frame = self.frames.get()
            self.currentFrame = cv2.imencode('.jpg', frame)[1].tobytes()

        self.thread = None
        print('NormalStream thread set to none')

    def getFrame(self):
        return self.currentFrame
        