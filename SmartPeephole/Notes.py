from flask import render_template, redirect, Blueprint, \
    url_for, abort, request
from flask_login import current_user

from . import db
from .Models import User, Note
from .Config import normal_stream, detection_stream, \
    snapped_frames

from base64 import b64encode
import numpy as np

notes = Blueprint('notes', __name__)

@notes.route('/snap')
def snap():
    if not current_user.is_authenticated:
        abort(403)

    frame = None

    if current_user.detectionState:
        frame = detection_stream.get_frame()
    else:
        frame = normal_stream.get_frame()

    snapped_frames[current_user.id] = frame

    frame = b64encode(frame).decode("utf-8")

    return render_template('add_note.html', frame=frame)


@notes.route('/save_note', methods=['POST'])
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


@notes.route('/user_notes')
def user_notes():
    if not current_user.is_authenticated:
        abort(403)

    notes = Note.query.filter_by(user_id=current_user.id).all()

    # need to convert binary data to img
    for note in notes:
        note.img = np.frombuffer(note.img, np.uint8)
        note.img = b64encode(note.img).decode("utf-8")

    return render_template('user_notes.html', notes=notes)


@notes.route('/delete_note', methods=['POST'])
def delete_note():
    if not current_user.is_authenticated:
        abort(403)

    id = request.form['note_id']
    note = Note.query.filter_by(user_id=current_user.id, id=id).first()

    if note:
        db.session.delete(note)
        db.session.commit()

    return redirect(url_for('notes.user_notes'))