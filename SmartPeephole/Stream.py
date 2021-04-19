from flask import Blueprint, Response, url_for, \
    abort, redirect
from flask_login import current_user

from . import db
from .Models import User
from .Config import cam, normal_stream, \
    detection_stream, mimetype

stream = Blueprint('stream', __name__)


@stream.route('/stream_normal_video/')
def stream_normal_video():
    if not current_user.is_authenticated:
        abort(403)

    cam.start_thread()
    normal_stream.start_thread()

    return Response(response=gen(normal_stream), mimetype=mimetype)


@stream.route('/stream_video_with_detection/')
def stream_video_with_detection():
    if not current_user.is_authenticated:
        abort(403)

    cam.start_thread()
    detection_stream.start_thread()

    return Response(response=gen(detection_stream), mimetype=mimetype)


@stream.route('/detection_state_change')
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


def gen(stream):
    while True:
        frame = stream.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')