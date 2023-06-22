import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from langchain import LLMChain
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.callbacks import AimCallbackHandler
from langchain.chains.base import Chain
from langchain.memory import ConversationBufferMemory
from langchain.memory import PostgresChatMessageHistory
from langchain.schema import BaseChatMessageHistory

load_dotenv()


def generate_session_id() -> str:
    return uuid.uuid4().__str__()


class TravelAgentV1:
    def __init__(self, chain: Chain, chat_history: BaseChatMessageHistory):
        self.chain = chain
        self.chat_history = chat_history

    def predict(self, human_input: str) -> str:
        self._save_user_message(human_input)
        response = self.chain.predict(human_input=human_input)
        self._save_ai_message(response)
        return response

    def _save_user_message(self, human_input: str) -> None:
        self.chat_history.add_user_message(human_input)

    def _save_ai_message(self, ai_output: str) -> None:
        self.chat_history.add_ai_message(ai_output)


def init_agent_v1() -> TravelAgentV1:
    session = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    if os.environ["APP_ENV"] == "dev":
        callbacks = [
            AimCallbackHandler(repo=".", experiment_name=f"Travel Agent V1: {session}")
        ]
    else:
        callbacks = []
    llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    prompt = PromptTemplate.from_file(
        template_file=f"{os.environ['PROMPT_TEMPLATE_PATH']}/travel_agent.prompt",
        input_variables=["chat_history", "human_input"],
    )
    chain = LLMChain(
        llm=llm, memory=memory, prompt=prompt, callbacks=callbacks
    )  # , callbacks=callbacks
    chat_history = PostgresChatMessageHistory(
        connection_string=f"{os.environ['PG_URI']}/{os.environ['APP_ENV']}",
        session_id=generate_session_id(),
        table_name=f"chat_history_{os.environ['APP_ENV']}",
    )
    return TravelAgentV1(chain=chain, chat_history=chat_history)

def init_agent_v2() -> TravelAgentV1:
    session = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    if os.environ["APP_ENV"] == "dev":
        callbacks = [
            AimCallbackHandler(repo=".", experiment_name=f"Movie agent V1: {session}")
        ]
    else:
        callbacks = []
    llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    prompt = PromptTemplate.from_file(
        template_file=f"{os.environ['PROMPT_TEMPLATE_PATH']}/movie_agent.prompt",
        input_variables=["chat_history", "human_input"],
    )
    chain = LLMChain(
        llm=llm, memory=memory, prompt=prompt, callbacks=callbacks
    )  # , callbacks=callbacks
    chat_history = PostgresChatMessageHistory(
        connection_string=f"{os.environ['PG_URI']}/{os.environ['APP_ENV']}",
        session_id=generate_session_id(),
        table_name=f"chat_history_{os.environ['APP_ENV']}_movie",
    )
    return TravelAgentV1(chain=chain, chat_history=chat_history)


travel_agent_v1 = init_agent_v1()
movie_agent_v1 = init_agent_v2()

agents = {
    "travel_agent_v1": init_agent_v1(),
    "movie_agent_v1": init_agent_v1(),
}
