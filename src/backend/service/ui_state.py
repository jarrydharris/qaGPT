import uuid

from flask import session
from src.backend.config import STATE_SCHEMA


def state_schema_is_valid(state: dict) -> bool:
    state_keys = set(state.keys())
    schema_keys = set(STATE_SCHEMA.keys())

    if state_keys != schema_keys:
        return False

    for key in state_keys:
        if state[key]["id"] != STATE_SCHEMA[key]["id"]:
            return False

    return True


def handle_state_change(session: session, new_state: dict) -> bool:
    if not state_schema_is_valid(new_state):
        print("Invalid state")
        return False
    session["state"] = new_state
    return True


def initialize_ui_state(current_session: session, input_state: dict) -> bool:
    if not state_schema_is_valid(input_state):
        return False
    ui_state = {"session_id": str(uuid.uuid4()), "state": input_state}
    current_session.update(ui_state)
    return True
