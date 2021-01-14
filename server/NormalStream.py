from threading import Thread
from time import time, sleep

from .Camera import Camera

import cv2

class NormalStream:
    def __init__(self, streamEvent, framesQue, fpsMeter, labelCreator):
        self.frames = framesQue
        self.currentFrame = None
        self.lastGivenFrameTime = None
        self.event = streamEvent
        self.fpsMeter = fpsMeter
        self.labelCreator = labelCreator

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
            try:
                frame = self.frames.get(timeout=2)
        
                fps = self.fpsMeter.calculateFPS(time())
                frame = self.labelCreator.addLabelToFrame(frame, fps)

                self.currentFrame = cv2.imencode('.jpg', frame)[1].tobytes()

            except:
                print('2 sec elapsed and normal stream didnt get any frame')
                break

        self.thread = None
        print('NormalStream thread set to none')

    def getFrame(self):
        Camera.normalStreamLogTime(time())
        self.event.wait()
        self.event.clear()
        return self.currentFrame
