import logging as lg

from flask import Blueprint, make_response, request, jsonify, session, Response

from src.backend.config import JSON_HEADER, CorsConfig, BAD_REQUEST
from src.backend.service.agent import handle_message
from src.backend.service.ui_state import initialize_ui_state, handle_state_change

api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/init_session", methods=['POST', 'OPTIONS'])
def set_session() -> Response:
    lg.info(f"User requesting session.")
    initialization_successful = initialize_ui_state(session, request.json)
    if not initialization_successful:
        lg.info(f"Invalid schema, returning 400.")
        return make_response(jsonify("Invalid schema"), BAD_REQUEST)
    lg.debug(f"session obj: {session}")
    return make_response(jsonify(session["session_id"]), JSON_HEADER)


@api.route('/set_input_state', methods=['OPTIONS', 'POST'])
def set_input_state():
    lg.info(f"User updating state")
    handle_state_change(session, request.json)
    return make_response(jsonify("success"), JSON_HEADER)


@api.route('/get_input_state', methods=['GET'])
def get_input_state():
    lg.info(f"User requested checkbox state")
    return make_response(jsonify(session["state"]), JSON_HEADER)


@api.route('/health', methods=['GET'])
def health() -> Response:
    lg.info(f"User sent a health check.")
    return make_response(jsonify("success"), JSON_HEADER)


@api.route('/send_message', methods=['POST'])
def send_message() -> Response:
    lg.info(f"User sent a message {request.data}")
    return handle_message(request.data)


@api.after_request
def _cors(response):  # pragma: no cover
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', CorsConfig.CORS_ORIGIN)

        for header in CorsConfig.CORS_HEADERS:
            response.headers.add('Access-Control-Allow-Headers', header)

        for method in CorsConfig.CORS_METHODS:
            response.headers.add('Access-Control-Allow-Methods', method)

    else:
        response.headers.add('Access-Control-Allow-Origin', CorsConfig.CORS_ORIGIN)
    return response
