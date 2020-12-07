from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Check if email exists in db
    user = User.query.filter_by(email=email).first()

    # Check if password for user is correct
    if not user or not check_password_hash(user.password, password):
        flash('Wrong login data. Try again', category='error')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile', user_name=user.name))

@auth.route('/logout')
def logout():
    logout_user()

    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']

    redirect(url_for('main.index'))
