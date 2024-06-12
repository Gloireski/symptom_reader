import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    debug = True
    SECRET_KEY = 'cc0f7589be8f11e1082328d160892d8a'
    # SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
