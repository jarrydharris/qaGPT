import os
import uuid

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains.base import Chain
from langchain.memory import ConversationBufferMemory, PostgresChatMessageHistory
from langchain.schema import BaseChatMessageHistory
from src.backend.config import config


def generate_session_id():
    return uuid.uuid4()


class TravelAgentV1:
    def __init__(
            self,
            chain: Chain,
            chat_history: BaseChatMessageHistory
    ):
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


travel_agent_v1 = TravelAgentV1(
    chain=LLMChain(
        llm=OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0),
        memory=ConversationBufferMemory(memory_key="chat_history"),
        prompt=PromptTemplate.from_file(template_file="./src/backend/prompts/travel_agent.prompt",
                                        input_variables=["chat_history", "human_input"]),
        verbose=False
    ),
    chat_history=PostgresChatMessageHistory(
        connection_string=os.environ["PG_URI"] + "/" + os.environ["APP_ENV"],
        session_id=generate_session_id().__str__(),
        table_name=f"chat_history_{os.environ['APP_ENV']}"
    )
)


# Lookup
# https://python.langchain.com/en/latest/modules/agents/agents/custom_llm_chat_agent.html
# https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html
# https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html
class TravelAgentV2(Chain):
    conversation_chain = LLMChain
    api_chain = LLMChain


agents = {
    "travel_agent_v1": travel_agent_v1
}
