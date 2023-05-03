import logging as lg

from flask import Blueprint, make_response, request, jsonify

from src.backend.config import JSON_HEADER, CorsConfig
from src.backend.service.agent import handle_message

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health', methods=['GET'])
def health():  # put application's code here
    lg.info(f"User sent a health check.")
    return make_response(jsonify("success"), JSON_HEADER)


@api.route('/send_message', methods=['POST'])
def send_message():
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
