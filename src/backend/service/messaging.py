import json
import logging as lg

from dotenv import load_dotenv
from flask import jsonify, make_response, Response, session

from src.backend.config import JSON_HEADER, BAD_REQUEST
from src.backend.models.agent import travel_agent_v1
from src.backend.service.intent_detection import init_intent_executor
from langchain.agents import AgentExecutor
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


def handle_message(session: session, data: dict, agent=travel_agent_v1, test: bool = False) -> Response:
    lg.debug(f"User message: {data}")

    message = data.get("message")

    try:
        validate_message(message)
        lg.debug(f"User message validated.")
    except (ValueError, TypeError) as e:
        lg.error(f"Invalid message, returning warning. {e}")
        return make_response(jsonify(f"The data: '{data}' caused an error: '{e}'."), BAD_REQUEST, JSON_HEADER)

    if test:
        lg.info(f"Test mode, returning test response.")
        agent_response = f"DEBUG: This is a test response.{session['session_id']}"

    else:
        lg.info(f"Agent message: {message}")
        agent_response = agent.predict(human_input=message)

    intent_detector = init_intent_executor(session)
    postprocessing(message, agent_response, intent_detector)

    return make_response(jsonify(agent_response), JSON_HEADER)
