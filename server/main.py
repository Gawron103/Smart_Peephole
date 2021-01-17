from flask import render_template, Blueprint, Response, \
    url_for, abort, redirect
from flask_login import current_user

from queue import Queue

from .StreamEvent import StreamEvent
from .CameraHandler import CameraHandler
from .NormalStream import NormalStream
from .DetectionStream import DetectionStream
from .FPSMeter import FPSMeter
from .LabelCreator import LabelCreator
from .FaceDetector import FaceDetector
from .models import User
from . import db

import cv2

main = Blueprint('main', __name__)

normal_frames = Queue()
detection_frames = Queue()
stream_event = StreamEvent()
cam = CameraHandler(
                    cv2.VideoCapture(0),
                    stream_event,
                    normal_frames,
                    detection_frames
                )


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    if not current_user.is_authenticated:
        abort(403)

    return render_template('profile.html')


@main.route('/video_stream/')
def video_stream():
    if not current_user.is_authenticated:
        abort(403)

    cam.start_thread()

    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    response = gen(
        NormalStream(
            stream_event,
            normal_frames,
            FPSMeter(),
            LabelCreator(
                cv2.FONT_HERSHEY_SIMPLEX
            )
        )
    )

    return Response(response=response, mimetype=mimetype)


@main.route('/video_detection_stream/')
def video_detection_stream():
    if not current_user.is_authenticated:
        abort(403)

    cam.start_thread()

    face_cascade = 'haarcascade_frontalface_default.xml'
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    response = gen(
        DetectionStream(
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
    )

    return Response(response=response, mimetype=mimetype)


@main.route('/detection')
def detection():
    if not current_user.is_authenticated:
        abort(403)

    if current_user.detectionState:
        current_user.detectionState = False
    else:
        current_user.detectionState = True

    user = User.query.filter_by(id=current_user.id)
    user.detectionState = current_user.detectionState

    db.session.commit()

    return redirect(url_for('main.profile'))


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


def gen(stream):
    while True:
        frame = stream.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
