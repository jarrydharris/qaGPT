import logging as lg

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from flask import Response
from flask import session
from flask_cors import CORS
from src.backend.config import BAD_REQUEST
from src.backend.config import CorsConfig
from src.backend.config import JSON_HEADER
from src.backend.config import SUCCESS
from src.backend.service.messaging import handle_message
from src.backend.service.ui_state import handle_state_change
from src.backend.service.ui_state import initialize_ui_state

api = Blueprint("api", __name__, url_prefix="/api")
CORS(api, supports_credentials=True)


def requires_session(func):
    def wrapper(*args, **kwargs):
        if "session_id" not in session:
            lg.error("Session not initialized, returning warning.")
            return make_response(
                jsonify("Session not initialized, try refreshing the page."),
                SUCCESS,
                JSON_HEADER,
            )
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@api.route("/init_session", methods=["POST", "OPTIONS"])
def set_session() -> Response:
    lg.info("User requesting session.")
    initialization_successful = initialize_ui_state(session, request.json)
    if not initialization_successful:
        lg.info("Invalid schema, returning 400.")
        return make_response(jsonify("Invalid schema"), BAD_REQUEST)
    lg.debug("session obj: {session}")
    return make_response(jsonify(session["session_id"]), JSON_HEADER)


@api.route("/set_input_state", methods=["POST", "OPTIONS"])
@requires_session
def set_input_state():
    lg.info("User updating state")
    if handle_state_change(session, request.json):
        return make_response(jsonify("success"), JSON_HEADER)
    else:
        return make_response(jsonify("Invalid schema"), BAD_REQUEST)


@api.route("/get_input_state", methods=["GET"])
@requires_session
def get_input_state():
    lg.debug("User requested checkbox state")
    return make_response(jsonify(session["state"]), JSON_HEADER)


@api.route("/send_message", methods=["POST"])
@requires_session
def send_message() -> Response:
    lg.info(f"User sent a message {request.json}")
    return handle_message(session, request.json)

@api.route("/products", methods=["GET"])
@requires_session
def get_products() -> Response:
    lg.info(f"User requested products")
    if "product_ids" not in session:
        return make_response(jsonify([]), JSON_HEADER)
    return make_response(jsonify(session["product_ids"]), JSON_HEADER)


@api.route("/health", methods=["GET"])
def health() -> Response:
    lg.info("User sent a health check.")
    return make_response(jsonify("success"), JSON_HEADER)


@api.after_request
def _cors(response):  # pragma: no cover
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", CorsConfig.CORS_ORIGIN)
        response.headers.add(
            "Access-Control-Allow-Credentials", CorsConfig.CORS_CREDENTIALS
        )

        for header in CorsConfig.CORS_HEADERS:
            response.headers.add("Access-Control-Allow-Headers", header)

        for method in CorsConfig.CORS_METHODS:
            response.headers.add("Access-Control-Allow-Methods", method)

    else:
        response.headers.add("Access-Control-Allow-Origin", CorsConfig.CORS_ORIGIN)
        response.headers.add(
            "Access-Control-Allow-Credentials", CorsConfig.CORS_CREDENTIALS
        )
    return response
