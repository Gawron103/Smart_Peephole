from threading import Thread
from time import time, sleep

from .Camera import Camera

import cv2

class NormalStream:
    def __init__(self, framesQue):
        self.frames = framesQue
        self.currentFrame = None
        self.lastGivenFrameTime = None

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
            if frame is not None:
                self.lastGivenFrameTime = time()

            self.currentFrame = cv2.imencode('.jpg', frame)[1].tobytes()

            if time() - self.lastGivenFrameTime > 5:
                print('5 sec elapsed and normal stream client didnt get any frames')
                break

        self.thread = None
        print('NormalStream thread set to none')

    def getFrame(self):
        Camera.normalStreamLogTime(time())
        return self.currentFrame
