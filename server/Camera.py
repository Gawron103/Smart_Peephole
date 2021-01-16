from threading import Thread
from time import time, sleep
from copy import deepcopy

from .CameraState import CameraState

import cv2

class Camera:
    normalStreamLastAccess = None
    detectionStreamLastAccess = None

    def __init__(self, cam, streamEvent, normalFramesQue, detectionFramesQue):
        self.thread = None
        self.currentFrame = None
        self.normalFrames = normalFramesQue
        self.detectionFrames = detectionFramesQue
        self.camera = cam
        self.event = streamEvent

    def startThread(self):
        if not self.thread:
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()

            # Wait untill frames are available
            while self.currentFrame is None:
                sleep(0)

            print('Camera thread started')
        else:
            print('Camera thread already working')

    def captureFrames(self):
        if self.camera.isOpened():
            while True:
                _, img = self.camera.read()
                img = cv2.resize(img, (640, 480))
                yield img

    def getFrame(self):
        return self.currentFrame

    def threadFunc(self):
        print('Starting NewCamera thread func')

        streamsStates = {
            'NormalStream' : CameraState.NEVER_CONNECTED,
            'DetectionStream' : CameraState.NEVER_CONNECTED
        }

        framesIterator = self.captureFrames()

        for frame in framesIterator:
            self.currentFrame = frame
            self.event.set()

            if Camera.normalStreamLastAccess is not None:
                if time() - Camera.normalStreamLastAccess < 3:
                    self.normalFrames.put(deepcopy(frame))
                    streamsStates['NormalStream'] = CameraState.CONNECTED
                else:
                    print('2 sec elapsed. Normal stream client gone')
                    Camera.normalStreamLastAccess = None
                    streamsStates['NormalStream'] = CameraState.DISCONNECTED

            if Camera.detectionStreamLastAccess is not None:
                if time() - Camera.detectionStreamLastAccess < 3:
                    self.detectionFrames.put(deepcopy(frame))
                    streamsStates['DetectionStream'] = CameraState.CONNECTED
                else:
                    print('2 sec elapsed. Detection stream client gone')
                    Camera.detectionStreamLastAccess = None
                    streamsStates['DetectionStream'] = CameraState.DISCONNECTED

            if any(value == CameraState.DISCONNECTED for value in streamsStates.values()) and \
               all(value != CameraState.CONNECTED for value in streamsStates.values()):
                  print(f'Dict values: {streamsStates.values()}')
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
