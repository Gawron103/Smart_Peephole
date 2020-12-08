from .CameraEvent import CameraEvent

import threading
import time
import cv2

class CameraHandler:
    event = CameraEvent()
    frame = None
    thread = None
    lastAccess = 0
    detectionEnabled = False

    def __init__(self):
        # Start camera thread if not running
        if CameraHandler.thread is None:
            CameraHandler.lastAccess = time.time()
            CameraHandler.thread = threading.Thread(target=self.__threadFunc)
            CameraHandler.thread.start()

            # Wait untill frames are available
            while self.getFrame() is None:
                time.sleep(0)
        
    @classmethod
    def __threadFunc(cls):
        print('Starting camera thread')
        frames_iterator = cls.frames()

        for frame in frames_iterator:
            CameraHandler.frame = frame

            CameraHandler.event.set()
            time.sleep(0)

            if time.time() - CameraHandler.lastAccess > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity')
                break

        self.__thread = None
        print('CameraHandler thread set to none')
    
    def getFrame(self):
        CameraHandler.lastAccess = time.time()
        CameraHandler.event.wait()
        CameraHandler.event.clear()
        return CameraHandler.frame

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)

        if camera.isOpened():
            while True:
                _, img = camera.read()

                yield cv2.imencode('.jpg', img)[1].tobytes()

    