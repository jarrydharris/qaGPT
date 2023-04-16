import logging as lg
import os

JSON_HEADER = {"Content-type": "application/json"}

SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
METHOD_NOT_ALLOWED = 405
NOT_IMPLEMENTED = 501

PG_HOST = os.environ.get("PG_HOST")
PG_PORT = os.environ.get("PG_PORT")
PG_USER = os.environ.get("PG_USER")
PG_SECRET = os.environ.get("PG_SECRET")
PG_URI = f"postgresql://{PG_USER}:{PG_SECRET}@{PG_HOST}:{PG_PORT}/development"

class FlaskConfig:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(FlaskConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = PG_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.INFO


class TestConfig(FlaskConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = PG_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.DEBUG


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig
}
