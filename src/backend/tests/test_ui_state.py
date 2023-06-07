import pytest

from src.backend.config import STATE_SCHEMA
from src.backend.service.ui_state import state_schema_is_valid


def test_valid_state_schema_returns_true_with_valid_schema():
    assert state_schema_is_valid(STATE_SCHEMA)


def test_state_schema_is_valid_returns_false_with_extra_key():
    invalid_state_schema = {
        "filter": {"id": "filter", "type": "text", "value": ""},
        "slider": {"id": "slider", "type": "range", "value": "5000"},
        "wildlife_checkbox": {"checked": False, "id": "wildlife-checkbox", "type": "checkbox"},
        "extra_key": {"checked": False, "id": "wildlife-checkbox", "type": "checkbox"}
    }
    assert not state_schema_is_valid(invalid_state_schema)


def test_state_schema_is_valid_returns_false_with_missing_key():
    invalid_state_schema = {
        "filter": {"id": "filter", "type": "text", "value": ""},
        "slider": {"id": "slider", "type": "range", "value": "5000"}
    }
    assert not state_schema_is_valid(invalid_state_schema)


def test_state_schema_is_valid_returns_false_with_spelling_error():
    invalid_state_schema = {
        "filter": {"id": "filter", "type": "text", "value": ""},
        "slider": {"id": "slier", "type": "range", "value": "5000"},
        "wildlife_checkbox": {"checked": False, "id": "wildlife-checkbox", "type": "checkbox"}
    }
    assert not state_schema_is_valid(invalid_state_schema)


@pytest.mark.skip("Not implemented")
def test_state_schema_is_valid_returns_false_with_incorrect_type():
    invalid_state_schema = {
        "filter": {"id": "filter", "type": "text", "value": ""},
        "slider": {"id": "slider", "type": "text", "value": "5000"},
        "wildlife_checkbox": {"checked": False, "id": "wildlife-checkbox", "type": "checkbox"}
    }
    assert not state_schema_is_valid(invalid_state_schema)
