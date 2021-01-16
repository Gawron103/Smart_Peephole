from datetime import datetime

import cv2


class LabelCreator:
    def __init__(self, font):
        self.__font = font

    def __create_label(self, fps):
        parsed_data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return "".join([parsed_data, ' ', 'FPS:', ' ', fps])

    def apply_label(self, frame, fps):
        label = self.__create_label(fps)
        return cv2.putText(frame,
                           label,
                           (7, 30),
                           self.__font,
                           1,
                           (100, 255, 0),
                           1,
                           cv2.cv2.LINE_AA)
