from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from Config import Config


def create_app():
    pass
    # app = Flask(__name__)
    # db = SQLAlchemy(app)
    # db.init_app(app)
    # app.config.from_object(Config)
    #
    # with app.app_context():
    #     db.create_all()
    # return app
