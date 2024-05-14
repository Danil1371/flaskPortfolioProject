import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_DIR = dirname(__file__)
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    PASSWORD_SALT = os.environ['PASSWORD_SALT']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_BLACKLIST_ENABLED = True

    PROPAGATE_EXCEPTIONS = True

    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')

    FLASK_CONFIG = os.environ['FLASK_CONFIG']


class LocalConfig(Config):
    TESTING = True
    BACKEND_URL = 'http://127.0.0.1:5000'
    DEBUG = True
    PROPAGATE_EXCEPTIONS = False
