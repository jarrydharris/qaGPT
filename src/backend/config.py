import json
import logging as lg
import os

import redis
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

# STATE_SCHEMA = {
#     "filter": {"id": "filter", "type": "text", "value": ""},
#     "slider": {"id": "slider", "type": "range", "value": "5000"},
#     "wildlife-checkbox": {
#         "checked": False,
#         "id": "wildlife-checkbox",
#         "type": "checkbox",
#     },
# }

with open("src/backend/genre_schema.json", "r") as f:
    STATE_SCHEMA = json.load(f)

class FlaskConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url("redis://localhost:6379")
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    PROMPT_TEMPLATE_PATH = os.environ["PROMPT_TEMPLATE_PATH"]

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
    LOG_LEVEL = lg.DEBUG
    # LOG_LEVEL = lg.INFO


class TestConfig(FlaskConfig):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = PG_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.DEBUG


class CorsConfig:
    CORS_ORIGIN = os.environ["CORS_ORIGIN"]
    CORS_HEADERS = ["Content-Type", "x-csrf-token"]
    CORS_METHODS = ["GET", "POST", "OPTIONS"]
    CORS_CREDENTIALS = "true"


config = {"development": DevelopmentConfig, "testing": TestConfig}
