import logging as lg

from src.backend.app_factory import initialize_logging
from src.backend.config import config, TestConfig


def test_fixture_has_test_config(client):
    assert client.application.testing is True


def test_logging_for_each_environment(app):
    testing_level = initialize_logging(app, "testing", config)
    development_level = initialize_logging(app, "development", config)
    assert testing_level == lg.DEBUG
    assert development_level == lg.INFO


def test_apply_config_to_app(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == TestConfig.SQLALCHEMY_DATABASE_URI
    assert app.config["TESTING"] is TestConfig.TESTING
    assert app.config["LOG_LEVEL"] is lg.DEBUG
