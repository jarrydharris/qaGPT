from flask import Flask, make_response
import logging as lg
from src.backend.config import config


def create_app(environment: str, config: dict = config) -> Flask:
    app = Flask(__name__)
    initialize_logging(app, environment, config)

    @app.route('/')
    def index():  # put application's code here
        return 'Hello World!'

    @app.route('/api/health')
    def health():  # put application's code here
        return make_response("success")

    return app


def initialize_logging(app: Flask, environment: str, config: dict) -> int:
    with app.app_context():
        log_format = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        lg.basicConfig(format=log_format)
        log_level = config[environment].LOG_LEVEL
        lg.getLogger().setLevel(log_level)
        lg.info(f"Logging configured to: {log_level}")
    return log_level
