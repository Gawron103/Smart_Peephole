from threading import Thread
from time import time, sleep
from copy import deepcopy

from .StreamStatus import StreamStatus

import cv2


class CameraHandler:
    normal_stream_last_access = None
    detection_stream_last_access = None

    def __init__(self, cam, streamEvent, normalFramesQue, detectionFramesQue):
        self.__transmission_thread = None
        self.__currentImg = None
        self.__normalFrames = normalFramesQue
        self.__detectionFrames = detectionFramesQue
        self.__camera = cam
        self.__event = streamEvent

    def start_thread(self):
        if not self.__transmission_thread:
            self.__transmission_thread = Thread(target=self.__img_transmission)
            self.__transmission_thread.start()

            # Wait untill frames are available
            while self.__currentImg is None:
                sleep(0)

    def __capture_frames(self):
        if self.__camera.isOpened():
            while True:
                img = self.__camera.read()[1]
                img = cv2.resize(img, (640, 480))
                yield img

    def __img_transmission(self):
        print('Starting Camera img transmission')

        streams = {
            'NormalStream': StreamStatus.UNKNOWN,
            'DetectionStream': StreamStatus.UNKNOWN
        }

        imgs_iterator = self.__capture_frames()

        for img in imgs_iterator:
            self.__currentImg = img
            self.__event.set()

            if CameraHandler.normal_stream_last_access is not None:
                if time() - CameraHandler.normal_stream_last_access < 2:
                    self.__normalFrames.put(deepcopy(img))
                    streams['NormalStream'] = StreamStatus.ONLINE
                else:
                    print('Normal stream client disconnected')
                    CameraHandler.normal_stream_last_access = None
                    streams['NormalStream'] = StreamStatus.OFFLINE
                    self.__normalFrames.queue.clear()

            if CameraHandler.detection_stream_last_access is not None:
                if time() - CameraHandler.detection_stream_last_access < 2:
                    self.__detectionFrames.put(deepcopy(img))
                    streams['DetectionStream'] = StreamStatus.ONLINE
                else:
                    print('Detection stream client disconnected')
                    CameraHandler.detection_stream_last_access = None
                    streams['DetectionStream'] = StreamStatus.OFFLINE
                    self.__detectionFrames.queue.clear()

            stop_transmission = (
                any(val == StreamStatus.OFFLINE for val in streams.values())
                and all(val != StreamStatus.ONLINE for val in streams.values())
            )

            if stop_transmission:
                break

        self.__transmission_thread = None
        imgs_iterator.close()
        print('Camera img processing ended')

    @staticmethod
    def normal_stream_log_time(current_time):
        CameraHandler.normal_stream_last_access = current_time

    @staticmethod
    def detection_stream_log_time(current_time):
        CameraHandler.detection_stream_last_access = current_time
