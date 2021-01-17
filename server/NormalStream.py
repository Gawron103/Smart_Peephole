from threading import Thread
from time import time, sleep

from .CameraHandler import CameraHandler

import cv2


class NormalStream:
    def __init__(self, streamEvent, frames, fpsMeter, labelCreator):
        self.__readyImg = None
        self.__frames = frames
        self.__event = streamEvent
        self.__fpsMeter = fpsMeter
        self.__labelCreator = labelCreator

        self.__processing_thread = Thread(target=self.__img_processing)
        self.__processing_thread.start()

        # Waint until frames are available
        while not self.get_frame():
            sleep(0)

    def __img_processing(self):
        print('Starting NormalStream img processing')

        while True:
            try:
                img = self.__frames.get(timeout=2)

                fps = self.__fpsMeter.calculate_fps(time())
                img = self.__labelCreator.apply_label(img, fps)

                self.__readyImg = cv2.imencode('.jpg', img)[1].tobytes()

            except Exception as error:
                print(f'Normal stream error: {repr(error)}')
                break

        self.__processing_thread = None
        print('NormalStream img processing ended')

    def get_frame(self):
        CameraHandler.normal_stream_log_time(time())
        self.__event.wait()
        self.__event.clear()
        return self.__readyImg
