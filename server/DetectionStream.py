from threading import Thread
from time import time, sleep

from .Camera import Camera

import cv2

class DetectionStream:
    def __init__(self, streamEvent, framesQue):
        self.frames = framesQue
        self.currentFrame = None
        self.lastGivenFrameTime = None
        self.event = streamEvent
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.thread = Thread(target=self.threadFunc)
        self.thread.start()

        # Wait until frames are available
        while self.getFrame() is None:
            sleep(0)

        print('DetectionStream init finished')

    def __del__(self):
        print('Detection Stream object deleted')

    def threadFunc(self):
        print('Starting DetectionStream thread func')
        frameSkipFactor = 3
        frameCounter = 0

        while True:
            try:
                frame = self.frames.get(timeout=2)
            # if frame is not None:
                # self.lastGivenFrameTime = time()

                if frameCounter % frameSkipFactor == 0:
                    self.currentFrame = self.detectFace(frame)
                # else:
                #     print('ignoring frames')

                frameCounter+=1

            # if time() - self.lastGivenFrameTime > 2:
            #     print('2 sec elapsed and detection stream client didnt get any frames')
            #     break
            except:
                print('2 sec elapsed and detection stream client didnt get any frames')
                break

        self.thread = None
        print('DetectionStream thread set to none')

    def getFrame(self):
        Camera.detectionStreamLogTime(time())
        self.event.wait()
        self.event.clear()
        return self.currentFrame

    def detectFace(self, inputImg):
        grayImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(grayImg, 1.5, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(inputImg, (x, y), (x + w, y + h), (255, 0, 0), 2)

        retImg = cv2.imencode('.jpg', inputImg)[1].tobytes()

        return retImg if retImg is not None else inputImg
