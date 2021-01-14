from threading import Thread
from time import time, sleep
from datetime import datetime

from .Camera import Camera

import cv2

class NormalStream:
    def __init__(self, streamEvent, framesQue):
        self.frames = framesQue
        self.currentFrame = None
        self.lastGivenFrameTime = None
        self.event = streamEvent

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.newFrameTime = 0
        self.prevFrameTime = 0

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
            # if frame is not None:
                # self.lastGivenFrameTime = time()
            # else:
                # print(f'time not logged')
                # print(f'Current time difference: {time() - self.lastGivenFrameTime}')

                fps = self.calculateFPS()
                currentData = datetime.now()
                time = currentData.strftime("%d/%m/%Y %H:%M:%S")
                info = "".join([time, ' ', 'FPS:', ' ', fps])
                frame = cv2.putText(frame, info, (7, 30), self.font, 1, (100, 255, 0), 1, cv2.LINE_AA)

                self.currentFrame = cv2.imencode('.jpg', frame)[1].tobytes()

                # if time() - self.lastGivenFrameTime > 2:
                #         print('2 sec elapsed and normal stream client didnt get any frames')
                #         break
            except:
                print('2 sec elapsed and normal stream didnt get any frame')
                break

        self.thread = None
        # self.frames = None
        # self.currentFrame = None
        # self.event = None
        print('NormalStream thread set to none')

        # self.thread.join()

    def getFrame(self):
        Camera.normalStreamLogTime(time())
        self.event.wait()
        self.event.clear()
        return self.currentFrame

    def calculateFPS(self):
        self.newFrameTime = time()
        fps = 1 / (self.newFrameTime - self.prevFrameTime)
        self.prevFrameTime = self.newFrameTime
        return str(int(fps))