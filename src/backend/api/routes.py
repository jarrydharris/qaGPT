import logging as lg

from flask import Blueprint, make_response, request, jsonify

from src.backend.config import JSON_HEADER
from src.backend.service.agent import handle_message

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health')
def health():  # put application's code here
    return make_response(jsonify("success"), JSON_HEADER)


@api.route('/send_message', methods=['POST'])
def send_message():
    lg.info(f"User sent a message {request.data}")
    response = handle_message(request.data)
    return make_response(jsonify(response), JSON_HEADER)
