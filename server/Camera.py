from threading import Thread
from time import time, sleep
from copy import deepcopy

import cv2

class Camera:
    def __init__(self, cam, normalFramesQue, detectionFramesQue):
        self.thread = None
        self.currentFrame = None
        self.normalFrames = normalFramesQue
        self.detectionFrames = detectionFramesQue
        self.camera = cam

    def startThread(self):
        if not self.thread:
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()

            # Wait untill frames are available
            while self.getFrame() is None:
                sleep(0)

            print('Camera thread started')
        else:
            print('Camera thread already working')

    def captureFrames(self):
        if self.camera.isOpened():
            while True:
                _, img = self.camera.read()
                yield img

    def getFrame(self):
        return self.currentFrame

    def threadFunc(self):
        print('Starting NewCamera thread func')
        framesIterator = self.captureFrames()

        for frame in framesIterator:
            self.currentFrame = frame

            self.normalFrames.put(deepcopy(frame))
            self.detectionFrames.put(deepcopy(frame))

        self.thread = None
        self.normalFrames.queue.clear()
        self.detectionFrames.queue.clear()
        framesIterator.close()
        print('Stopped camera thread due to inactivity')
        