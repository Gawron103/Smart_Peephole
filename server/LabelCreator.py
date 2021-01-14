from datetime import datetime

import cv2

class LabelCreator:
    def __init__(self, font):
        self.font = font

    def createLabel(self, fps):
        parsedData = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return "".join([parsedData, ' ', 'FPS:', ' ', fps])

    def addLabelToFrame(self, frame, fps):
        label = self.createLabel(fps)
        return cv2.putText(frame, label, (7, 30), self.font, 1, (100, 255, 0), 1, cv2.cv2.LINE_AA)
