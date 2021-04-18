from flask import render_template, Blueprint, Response, \
    url_for, abort, redirect, request
from flask_login import current_user

from . import db
from .Models import User, Note
from .Config import cam, normal_stream, detection_stream, \
    snapped_frames

from base64 import b64encode
import numpy as np

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


@main.route('/snap')
def snap():
    if not current_user.is_authenticated:
        abort(403)

    frame = None

    if current_user.detectionState:
        frame = detection_stream.get_frame()
    else:
        frame = normal_stream.get_frame()

    snapped_frames[current_user.id] = frame

    print(f'In snap: {type(frame)}')
    frame = b64encode(frame).decode("utf-8")

    return render_template('add_note.html', frame=frame)


@main.route('/save_note', methods=['POST'])
def save_note():
    if not current_user.is_authenticated:
        abort(403)

    if 'Save' == request.form['action']:
        text = request.form['img_desc']

        if current_user.id in snapped_frames:
            frame = snapped_frames.pop(current_user.id)

            user = User.query.filter_by(email=current_user.email).first()

            if user:
                user.notes.append(Note(desc=text, img=frame, user_id=user.id))
                db.session.commit()

    return redirect(url_for('main.profile'))


@main.route('/notes')
def notes():
    if not current_user.is_authenticated:
        abort(403)

    notes = Note.query.filter_by(user_id=current_user.id).all()

    # need to convert binary data to img
    for note in notes:
        note.img = np.frombuffer(note.img, np.uint8)
        note.img = b64encode(note.img).decode("utf-8")

    return render_template('notes.html', notes=notes)


@main.route('/delete_note', methods=['POST'])
def delete_note():
    if not current_user.is_authenticated:
        abort(403)

    id = request.form['note_id']
    note = Note.query.filter_by(user_id=current_user.id, id=id).first()

    if note:
        db.session.delete(note)
        db.session.commit()

    return redirect(url_for('main.notes'))


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
