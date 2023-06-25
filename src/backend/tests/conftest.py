import pytest
from src.backend.app_factory import create_app
from src.backend.config import config


@pytest.fixture()
def app():
    return create_app("testing", config)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def client_session_a():
    return create_app("testing", config).test_client()


@pytest.fixture()
def client_session_b():
    return create_app("testing", config).test_client()
