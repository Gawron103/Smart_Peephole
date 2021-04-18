from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    superUser = db.Column(db.Boolean, default=False)
    detectionState = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def is_admin(self):
        return self.superUser


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    img = db.Column(db.BLOB(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
