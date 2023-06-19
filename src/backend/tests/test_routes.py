from copy import deepcopy
from uuid import UUID

from src.backend.config import BAD_REQUEST
from src.backend.config import STATE_SCHEMA
from src.backend.config import SUCCESS


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def test_index(client):
    response = client.get("/")
    assert response.data == b"Hello World!"
    assert response.status_code == SUCCESS


def test_health(client):
    response = client.get("/api/health")
    assert response.data == b'"success"\n'
    assert response.status_code == SUCCESS


def test_cors_headers(client):
    response = client.options("/")
    assert response.status_code == SUCCESS
    cors = response.headers.__str__()
    assert "text/html" in cors
    assert "utf-8" in cors
    assert "GET" in cors
    assert "OPTIONS" in cors
    assert "HEAD" in cors


def test_init_ui_state_rejects_bad_schema(client):
    invalid_state_schema = {
        "filter": {"id": "filter", "type": "text", "value": ""},
        "wildlife_checkbox": {
            "checked": False,
            "id": "wildlife-checkbox",
            "type": "checkbox",
        },
    }
    with client:
        response = client.post("/api/init_session", json=invalid_state_schema)
        assert response.status_code == BAD_REQUEST


def test_init_ui_state_retains_session_data(client):
    with client:
        response = client.post("/api/init_session", json=STATE_SCHEMA)
        assert response.status_code == SUCCESS
    expected_keys = ["session_id", "state"]
    with client.session_transaction() as sess:
        for key in expected_keys:
            assert key in sess
        assert is_valid_uuid(sess["session_id"])
        assert sess["state"] == STATE_SCHEMA


def test_init_ui_change_updates_session_state(client_session_a):  # , client_session_b
    with client_session_a:
        response = client_session_a.post("/api/init_session", json=STATE_SCHEMA)
        assert response.status_code == SUCCESS

    new_state = deepcopy(STATE_SCHEMA)

    with client_session_a.session_transaction() as sess:
        new_state["filter"]["value"] = "new value"
        response = client_session_a.post("/api/set_input_state", json=new_state)
        assert response.status_code == SUCCESS
        assert sess["state"]["filter"]["value"] == new_state["filter"]["value"]

    # with client_session_b:
    #     response = client_session_b.post('/api/init_session', json=STATE_SCHEMA)
    #     assert response.status_code == SUCCESS
    # with client_session_b.session_transaction() as sess:
    #     assert sess["state"]["filter"]["value"] != new_state["filter"]["value"]


def test_set_ui_state_expects_credentials(client):
    with client:
        response = client.post("/api/set_input_state", json=STATE_SCHEMA)
        assert response.status_code == BAD_REQUEST


def test_set_ui_state_with_credentials_updates(client):
    with client:
        response = client.post("/api/init_session", json=STATE_SCHEMA)
        assert response.status_code == SUCCESS
        response = client.post("/api/set_input_state", json=STATE_SCHEMA)
        assert response.status_code == SUCCESS
        print(response.headers.items())

    with client.session_transaction() as sess:
        assert "session_id" in sess
        print(sess)
