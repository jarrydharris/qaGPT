import json
import logging as lg
import os

from dotenv import load_dotenv
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferWindowMemory

load_dotenv()

tools = []
llm = OpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    temperature=0)
memory = ConversationBufferWindowMemory(k=10)

agent = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)


def handle_message(data: bytes, agent=agent) -> str:
    lg.debug(f"Handle message: {data}")
    data_str = data.decode("utf-8")
    data_json = json.loads(data_str)
    message = data_json["message"]
    agent_response = agent.predict(input=message)

    lg.debug(f"Agent message: {agent_response}")
    return agent_response
