import logging as lg
import os

from dotenv import load_dotenv

load_dotenv()

JSON_HEADER = {"Content-type": "application/json"}

SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
METHOD_NOT_ALLOWED = 405
NOT_IMPLEMENTED = 501

PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_USER = os.environ["PG_USER"]
PG_SECRET = os.environ["PG_SECRET"]
APP_ENV = os.environ["APP_ENV"]
PG_URI = f"postgresql://{PG_USER}:{PG_SECRET}@{PG_HOST}:{PG_PORT}/${APP_ENV}"


class FlaskConfig:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(FlaskConfig):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = PG_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.INFO


class TestConfig(FlaskConfig):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = PG_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.DEBUG


class CorsConfig:
    CORS_ORIGIN = os.environ['CORS_ORIGIN']
    CORS_HEADERS = ['Content-Type', 'x-csrf-token']
    CORS_METHODS = ["GET", "POST", "OPTIONS"]


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig
}
