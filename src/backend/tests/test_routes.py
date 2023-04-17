from src.backend.config import SUCCESS


def test_index(client):
    response = client.get('/')
    assert response.data == b'Hello World!'
    assert response.status_code == SUCCESS


def test_health(client):
    response = client.get('/api/health')
    assert response.data == b'"success"\n'
    assert response.status_code == SUCCESS
