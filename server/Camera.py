from threading import Thread
from time import time, sleep
from copy import deepcopy

import cv2

class Camera:
    normalStreamLastAccess = None
    detectionStreamLastAccess = None

    def __init__(self, cam, normalFramesQue, detectionFramesQue):
        self.thread = None
        self.currentFrame = None
        self.normalFrames = normalFramesQue
        self.detectionFrames = detectionFramesQue
        self.camera = cam
        self.lastGainedPhoto = None

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
        self.lastGainedPhoto = time()
        return self.currentFrame

    def threadFunc(self):
        print('Starting NewCamera thread func')
        streamsStates = {'NormalStream' : None, 'DetectionStream' : None}
        framesIterator = self.captureFrames()

        for frame in framesIterator:
            self.currentFrame = frame

            if Camera.normalStreamLastAccess is not None:
                if time() - Camera.normalStreamLastAccess < 5:
                    self.normalFrames.put(deepcopy(frame))
                    streamsStates['NormalStream'] = True
                else:
                    print('5 sec elapsed. Normal stream client gone')
                    Camera.normalStreamLastAccess = None
                    streamsStates['NormalStream'] = False

            if Camera.detectionStreamLastAccess is not None:
                if time() - Camera.detectionStreamLastAccess < 5:
                    self.detectionFrames.put(deepcopy(frame))
                    streamsStates['DetectionStream'] = True
                else:
                    print('5 sec elapsed. Detection stream client gone')
                    Camera.detectionStreamLastAccess = None
                    streamsStates['DetectionStream'] = False

            if all(value == False for value in streamsStates.values()):
                print('No clients connected. Dont need to read new frames')
                break

        self.thread = None
        self.normalFrames.queue.clear()
        self.detectionFrames.queue.clear()
        framesIterator.close()
        print('Stopped camera thread due to inactivity')

    @staticmethod
    def normalStreamLogTime(currentTime):
        Camera.normalStreamLastAccess = currentTime

    @staticmethod
    def detectionStreamLogTime(currentTime):
        Camera.detectionStreamLastAccess = currentTime
