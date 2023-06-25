import json
import logging as lg
import os

import redis
from dotenv import load_dotenv
from flask import session, make_response, jsonify

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

with open("src/backend/genre_schema.json") as f:
    STATE_SCHEMA = json.load(f)


def requires_session(func):
    def wrapper(*args, **kwargs):
        if "session_id" not in session:
            lg.error("Session not initialized, returning warning.")
            return make_response(
                jsonify("Session not initialized, try refreshing the page."),
                SUCCESS,
                JSON_HEADER,
            )
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


class FlaskConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url("redis://localhost:6379")
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "session:"
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_HTTPONLY = False
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
    CORS_ORIGIN = os.environ["CORS_ORIGIN"]
    CORS_HEADERS = ["Content-Type", "x-csrf-token", "Access-Control-Allow-Credentials"]
    CORS_METHODS = ["GET", "POST", "OPTIONS"]
    CORS_CREDENTIALS = "true"


config = {"development": DevelopmentConfig, "testing": TestConfig}
