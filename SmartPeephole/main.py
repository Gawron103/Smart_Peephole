from flask import render_template, Blueprint, abort
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    if not current_user.is_authenticated:
        abort(403)

    return render_template('profile.html')


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403
