from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PeepholeDB.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .Models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    class MyMV(ModelView):
        def on_model_change(self, form, model, is_created):
            model.password = generate_password_hash(
                model.password,
                method='sha256'
            )

        def is_accessible(self):
            if not current_user.is_authenticated:
                return False

            return current_user.is_admin()

    class LoginMenuLink(MenuLink):
        def is_accessible(self):
            return not current_user.is_authenticated

    class LogoutMenuLink(MenuLink):
        def is_accessible(self):
            return current_user.is_authenticated

    admin = Admin(
                app,
                name='Administrators panel',
                template_mode='bootstrap3',
                base_template='/admin/admin.html'
            )
    admin.add_view(MyMV(User, db.session))
    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))

    from .main import page_forbidden, page_not_found
    app.register_error_handler(403, page_forbidden)
    app.register_error_handler(404, page_not_found)

    # Blueprint for auth routes
    from .Auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Blueprint for notes parts of app
    from .Notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)

    return app
