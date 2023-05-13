import json
import logging as lg

from dotenv import load_dotenv
from flask import jsonify, make_response, Response

from src.backend.config import JSON_HEADER, BAD_REQUEST
from src.backend.models.agent import travel_agent_v1

load_dotenv()


def handle_message(data: bytes, agent=travel_agent_v1) -> Response:
    lg.debug(f"User message: {data}")
    data_str = data.decode("utf-8")
    data_json = json.loads(data_str)
    message = data_json.get("message")
    if message is None:
        lg.error("No message, returning warning.")
        return make_response(jsonify(f"JSON incorrectly formated: {data}"), BAD_REQUEST, JSON_HEADER)
    elif message == "":
        lg.error("Blank message, returning warning.")
        return make_response(jsonify("Please enter a message."), BAD_REQUEST, JSON_HEADER)

    agent_response = agent.predict(human_input=message)

    lg.info(f"Agent message: {agent_response}")
    return make_response(jsonify(agent_response), JSON_HEADER)
