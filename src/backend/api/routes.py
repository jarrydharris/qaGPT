from flask import Blueprint, make_response
from src.backend.config import JSON_HEADER

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health')
def health():  # put application's code here
    return make_response("success", JSON_HEADER)