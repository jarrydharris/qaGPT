from src.backend.app_factory import initialize_logging
from src.backend.config import config
import logging as lg


def test_fixture_has_test_config(client):
    assert client.application.testing is True


def test_logging_for_each_environment(app):
    testing_level = initialize_logging(app, "testing", config)
    development_level = initialize_logging(app, "development", config)
    assert testing_level == lg.DEBUG
    assert development_level == lg.INFO

def test_index(client):
    response = client.get('/')
    assert response.data == b'Hello World!'
    assert response.status_code == 200

def test_health(client):
    response = client.get('/api/health')
    assert response.data == b'success'
    assert response.status_code == 200