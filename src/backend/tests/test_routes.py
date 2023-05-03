from src.backend.config import SUCCESS


def test_index(client):
    response = client.get('/')
    assert response.data == b'Hello World!'
    assert response.status_code == SUCCESS


def test_health(client):
    response = client.get('/api/health')
    assert response.data == b'"success"\n'
    assert response.status_code == SUCCESS


def test_cors_headers(client):
    response = client.options('/')
    assert response.status_code == SUCCESS
    cors = response.headers.__str__()
    assert "text/html" in cors
    assert "utf-8" in cors
    assert "GET" in cors
    assert "OPTIONS" in cors
    assert "HEAD" in cors
