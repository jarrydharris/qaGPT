import logging as lg
import uuid

from flask import session, make_response, jsonify, Response

from src.backend.config import STATE_SCHEMA, JSON_HEADER, BAD_REQUEST


def handle_get_state(session: session) -> Response:
    return make_response(jsonify(session["state"]), JSON_HEADER)


def state_schema_is_valid(state: dict) -> bool:
    state_keys = set(state.keys())
    schema_keys = set(STATE_SCHEMA.keys())

    if state_keys != schema_keys:
        return False

    for key in state_keys:
        if state[key]["id"] != STATE_SCHEMA[key]["id"]:
            return False

    return True


def handle_state_change(session: session, new_state: dict) -> Response:
    if not state_schema_is_valid(new_state):
        return make_response(jsonify("Invalid schema"), BAD_REQUEST)
    session["state"] = new_state
    return make_response(jsonify("success"), JSON_HEADER)


def handle_initialization_request(current_session: session, input_state: dict) -> Response:
    if not state_schema_is_valid(input_state):
        lg.info("Invalid schema, returning 400.")
        return make_response(jsonify("Invalid schema"), BAD_REQUEST)
    ui_state = {"session_id": str(uuid.uuid4()), "state": input_state, "product_ids": []}
    current_session.update(ui_state)
    lg.debug(f"session obj: {session}")
    return make_response(jsonify(session["session_id"]), JSON_HEADER)


def handle_product_request(session):
    # if "product_ids" not in session:
    #     return make_response(jsonify([]), JSON_HEADER)
    return make_response(jsonify(session["product_ids"]), JSON_HEADER)
