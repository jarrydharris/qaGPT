import logging as lg

import dotenv
from flask import Flask
from flask_session import Session

from src.backend.config import config


def create_app(environment: str, config: dict = config) -> Flask:
    app = Flask(__name__)
    initialize_logging(app, environment, config)
    lg.info(f"Creating app under {environment}.")
    apply_configs(app, environment, config)
    Session(app)
    setup_basic_routes(app)
    register_blueprints(app)
    return app


def initialize_logging(app: Flask, environment: str, config: dict) -> int:
    with app.app_context():
        log_format = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        filename = f"./logs/{environment}.log"
        filemode = "a"
        lg.basicConfig(filename=filename,
                       filemode=filemode,
                       format=log_format)
        log_level = config[environment].LOG_LEVEL
        lg.getLogger().setLevel(log_level)
        lg.info(f"Logging configured to: {log_level}")
    return log_level


def apply_configs(app: Flask, environment: str, config: dict):
    dotenv_path = dotenv.find_dotenv()
    dotenv.set_key(dotenv_path, "APP_ENV", environment)
    app.config.from_object(config[environment])
    config[environment].init_app(app)
    lg.info(f'Config applied: "{environment}" -> {config[environment]}')
    # Resetting back to default
    default_environment = "development"
    dotenv.set_key(dotenv_path, "APP_ENV", default_environment)


def setup_basic_routes(app: Flask):
    @app.route("/")
    def index() -> str:
        lg.info("User visited index")
        return "Hello World!"


def register_blueprints(app: Flask):
    with app.app_context():
        from src.backend.api.routes import api
        app.register_blueprint(api)
        blueprint_names = app.blueprints.keys()
        lg.info(f'Registered Blueprints: {", ".join(blueprint_names)}')
