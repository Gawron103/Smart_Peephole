from flask import render_template, Blueprint, Response, \
    url_for, abort, redirect
from flask_login import current_user

from . import db
from .Models import User
from .Config import cam, normal_stream, detection_stream

main = Blueprint('main', __name__)


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

    mimetype = 'multipart/x-mixed-replace; boundary=frame'

    cam.start_thread()
    normal_stream.start_thread()

    return Response(response=gen(normal_stream), mimetype=mimetype)


@main.route('/video_detection_stream/')
def video_detection_stream():
    if not current_user.is_authenticated:
        abort(403)

    mimetype = 'multipart/x-mixed-replace; boundary=frame'

    cam.start_thread()
    detection_stream.start_thread()

    return Response(response=gen(detection_stream), mimetype=mimetype)


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
