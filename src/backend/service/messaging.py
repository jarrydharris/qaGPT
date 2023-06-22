import json
import logging as lg

from dotenv import load_dotenv
from flask import Response
from flask import jsonify
from flask import make_response
from flask import session
from langchain.agents import AgentExecutor

from src.backend.config import BAD_REQUEST
from src.backend.config import JSON_HEADER
from src.backend.models.agent import movie_agent_v1
from src.backend.service.semantic_product_search import init_semantic_searcher

load_dotenv()


def decode_message(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


def validate_message(message: str) -> bool:
    if message is None:
        raise ValueError("Null message.")

    if message == "":
        raise ValueError("The message is an empty string.")

    if not isinstance(message, str):
        raise TypeError(f"The value for message is '{type(message)}' is not a string.")

    return True


def preprocessing(message: str, agent: AgentExecutor) -> None:
    chat_log = f"User: {message}"
    lg.info(chat_log)
    agent.run(chat_log)


def postprocessing(message: str, response: str, agent: AgentExecutor) -> None:
    chat_log = f"User: {message}\n TravelAgent: {response}"
    lg.info(chat_log)
    agent.run(chat_log)


def handle_message(
        session: session, data: dict, agent=movie_agent_v1, test: bool = False
) -> Response:
    lg.debug(f"User message: {data}")

    message = data.get("message")

    try:
        validate_message(message)
        lg.debug("User message validated.")
    except (ValueError, TypeError) as e:
        lg.error(f"Invalid message, returning warning. {e}")
        return make_response(
            jsonify(f"The data: '{data}' caused an error: '{e}'."),
            BAD_REQUEST,
            JSON_HEADER,
        )

    intent_detector = init_semantic_searcher(session)
    # preprocessing(message, intent_detector)

    if test:
        lg.info("Test mode, returning test response.")
        agent_response = f"DEBUG: This is a test response.{session['session_id']}"

    else:
        lg.info(f"Agent message: {message}")
        agent_response = agent.predict(human_input=message)
        postprocessing(message, agent_response, intent_detector)

    return make_response(jsonify(agent_response), JSON_HEADER)
