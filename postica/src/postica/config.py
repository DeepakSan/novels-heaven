import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO')
    LOG_LEVEL = os.environ.get('LOG_LEVEL')

class devConfig(Config):
    DEBUG = True

class prodConfig(Config):
    DEBUG = False
    FLASK_ENV = os.environ.get('FLASK_ENV')
