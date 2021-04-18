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
        cords = (10, 25)
        font_scale = 0.6
        color = (100, 255, 0)
        thickness = 1

        return cv2.putText(
            frame,
            label,
            cords,
            self.__font,
            font_scale,
            color,
            thickness,
            cv2.cv2.LINE_AA
        )
