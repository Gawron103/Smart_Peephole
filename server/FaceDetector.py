import cv2


class FaceDetector:
    def __init__(self, cascade):
        self.__faceCascade = cascade

    def detect_face(self, img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.__faceCascade.detectMultiScale(gray_img, 1.5, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return img
