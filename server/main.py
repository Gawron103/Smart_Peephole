from flask import render_template, Blueprint, Response, url_for, abort
from flask_login import current_user
from .CameraHandler import CameraHandler

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    if not current_user.is_authenticated:
        abort(403)

    return render_template('profile.html', name=current_user.name)

@main.route('/video_stream/')
def video_stream():
    if not current_user.is_authenticated:
        abort(403)

    return Response(gen(CameraHandler()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403

def gen(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
