from threading import Thread
from time import time, sleep

from .CameraHandler import CameraHandler

import cv2


class DetectionStream:
    def __init__(self, streamEvent, frames, fpsMeter, labelCreator, detector):
        self.__readyImg = None
        self.__frames = frames
        self.__event = streamEvent
        self.__fpsMeter = fpsMeter
        self.__labelCreator = labelCreator
        self.__detector = detector

        self.__processing_thread = Thread(target=self.__img_processing)
        self.__processing_thread.start()

        # Wait until frames are available
        while self.get_frame() is None:
            sleep(0)

    def __img_processing(self):
        print('Starting DetectionStream thread func')

        frame_skip_factor = 3
        frame_counter = 0

        while True:
            try:
                img = self.__frames.get(timeout=2)

                if frame_counter % frame_skip_factor == 0:
                    processed_img = self.__detector.detect_face(img)

                    fps = self.__fpsMeter.calculate_fps(time())
                    img = self.__labelCreator.apply_label(processed_img, fps)

                    self.__readyImg = cv2.imencode('.jpg', img)[1].tobytes()

                frame_counter += 1
            except Exception as error:
                print(f'Detection stream error: {repr(error)}')
                break

        self.__processing_thread = None
        print('DetectionStream thread set to none')

    def get_frame(self):
        CameraHandler.detection_stream_log_time(time())
        self.__event.wait()
        self.__event.clear()
        return self.__readyImg
