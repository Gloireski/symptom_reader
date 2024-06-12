import os
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager

from .extensions import db, bcrypt


# Create app function to create our app and make
# all the configurations and app registration
def create_app():
    app_ = Flask(__name__, static_folder='static')
    basedir = os.path.abspath(os.path.dirname(__file__))
    # sqlite db path, point to current project folder path
    app_.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app_.config["SECRET_KEY"] = 'cc0f7589be8f11e1082328d160892d8a'
    # help logout user after 15 minutes
    app_.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app_)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # app_.config.from_object(Config)
    db.init_app(app_)
    bcrypt.init_app(app_)
    return app_