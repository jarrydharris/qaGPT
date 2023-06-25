import logging as lg

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from flask import Response
from flask import session
from src.backend.config import CorsConfig
from src.backend.config import JSON_HEADER
from src.backend.config import requires_session
from src.backend.service.messaging import handle_message
from src.backend.service.ui_state import handle_get_state
from src.backend.service.ui_state import handle_initialization_request
from src.backend.service.ui_state import handle_product_request
from src.backend.service.ui_state import handle_state_change

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/init_session", methods=["POST", "OPTIONS"])
def set_session() -> Response:
    lg.info("User requesting session.")
    return handle_initialization_request(session, request.json)


@api.route("/set_input_state", methods=["POST"])
@requires_session
def set_input_state():
    lg.info("set_input_state called.")
    return handle_state_change(session, request.json)


@api.route("/get_input_state", methods=["GET"])
@requires_session
def get_input_state():
    lg.debug("User requested checkbox state")
    return handle_get_state(session)


@api.route("/send_message", methods=["POST"])
@requires_session
def send_message() -> Response:
    lg.info(f"User sent a message {request.json}")
    return handle_message(session, request.json)


@api.route("/products", methods=["GET"])
@requires_session
def get_products() -> Response:
    lg.info(f"User requested products: {session}")
    return handle_product_request(session)


@api.route("/session", methods=["GET"])
@requires_session
def get_session() -> Response:
    lg.info(f"DEBUG: session: {session}")
    return make_response(jsonify(session), JSON_HEADER)


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
