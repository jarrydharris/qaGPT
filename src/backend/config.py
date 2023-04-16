import logging as lg


class FlaskConfig:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(FlaskConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.INFO


class TestConfig(FlaskConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = lg.DEBUG


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig
}
