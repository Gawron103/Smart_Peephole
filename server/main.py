from flask import render_template, Blueprint, Response, url_for, abort, redirect
from flask_login import current_user

from queue import Queue

from .Camera import Camera
from .NormalStream import NormalStream
from .DetectionStream import DetectionStream
from .models import User
from . import db

import cv2

main = Blueprint('main', __name__)

normalFrames = Queue()
detectionFrames = Queue()
camera = Camera(cv2.VideoCapture(0), normalFrames, detectionFrames)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    if not current_user.is_authenticated:
        abort(403)

    return render_template('profile.html', name=current_user.name, detectionState=current_user.detectionState)

@main.route('/video_stream/')
def video_stream():
    if not current_user.is_authenticated:
        abort(403)
    
    global normalFrames
    global camera
    camera.startThread()
    return Response(gen(NormalStream(normalFrames)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/video_detection_stream/')
def video_detection_stream():
    if not current_user.is_authenticated:
        abort(403)

    global detectionFrames
    global camera
    camera.startThread()
    return Response(gen(DetectionStream(detectionFrames)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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

    return redirect(url_for('main.profile', name=current_user.name, detectionState=current_user.detectionState))

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403

def gen(stream):
    while True:
        frame = stream.getFrame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
