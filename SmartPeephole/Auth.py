from flask import Blueprint, render_template, redirect, \
    url_for, session, request, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from .Models import User

auth = Blueprint('auth', __name__)

from . import db

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Check if email exists in db
    user = User.query.filter_by(email=email).first()

    # Check if password for user is correct
    if not user or not check_password_hash(user.password, password):
        flash('Wrong login data. Try again', category='error')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    # Check if user has admin rights
    if user.superUser:
        return redirect(url_for('admin.index'))

    return redirect(url_for('main.profile', user_name=user.name))


@auth.route('/logout')
def logout():
    logout_user()

    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']

    return redirect(url_for('main.index'))


# Temporary for crearing admin user
@auth.route('/reg')
def reg():
    email = 'admin@admin.pl'
    name = 'admin'
    password = 'admin'
    isAdmin = True
    detection = False

    new_user = User(email=email, name=name, superUser=isAdmin, detectionState=detection, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    print('User created')

    return redirect(url_for('main.index'))