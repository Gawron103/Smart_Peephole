from flask import render_template, Blueprint, Response
from flask_login import current_user
from .CameraHandler import CameraHandler

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/video_stream/')
def video_stream():
    return Response(gen(CameraHandler()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
