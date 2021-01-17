from queue import Queue

from .StreamEvent import StreamEvent
from .CameraHandler import CameraHandler
from .NormalStream import NormalStream
from .DetectionStream import DetectionStream
from .FPSMeter import FPSMeter
from .LabelCreator import LabelCreator
from .FaceDetector import FaceDetector

import cv2


video_source = 0

face_cascade = 'haarcascade_frontalface_default.xml'

normal_frames = Queue()

detection_frames = Queue()

stream_event = StreamEvent()

cam = CameraHandler(
    cv2.VideoCapture(video_source),
    stream_event,
    normal_frames,
    detection_frames
)

normal_stream = NormalStream(
    stream_event,
    normal_frames,
    FPSMeter(),
    LabelCreator(
        cv2.FONT_HERSHEY_SIMPLEX
    )
)

detection_stream = DetectionStream(
    stream_event,
    detection_frames,
    FPSMeter(),
    LabelCreator(
        cv2.FONT_HERSHEY_SIMPLEX
    ),
    FaceDetector(
        cv2.CascadeClassifier(
            cv2.data.haarcascades + face_cascade
        )
    )
)
