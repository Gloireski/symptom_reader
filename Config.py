import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    debug = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
