import os
import uuid
from typing import Union, Any

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.agents import BaseSingleActionAgent, Tool, tool
from langchain.chains.base import Chain
from langchain.memory import ConversationBufferMemory, PostgresChatMessageHistory
from langchain.retrievers import WeaviateHybridSearchRetriever
from langchain.schema import BaseChatMessageHistory, AgentAction, AgentFinish

from src.backend.config import config

from langchain.utilities import BingSearchAPIWrapper


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

#
# class TravelAgentV2(BaseSingleActionAgent):
#     """This travel agent can search local documents"""
#     @property
#     def input_keys(self):
#         return ["input"]
#
#     def plan(
#             self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
#     ) -> Union[AgentAction, AgentFinish]:
#         """Given input, decided what to do.
#
#         Args:
#             intermediate_steps: Steps the LLM has taken to date,
#                 along with observations
#             **kwargs: User inputs.
#
#         Returns:
#             Action specifying what tool to use.
#         """
#         return AgentAction(tool="Search", tool_input=kwargs["input"], log="")
#
#     async def aplan(
#             self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
#     ) -> Union[AgentAction, AgentFinish]:
#         """Given input, decided what to do.
#
#         Args:
#             intermediate_steps: Steps the LLM has taken to date,
#                 along with observations
#             **kwargs: User inputs.
#
#         Returns:
#             Action specifying what tool to use.
#         """
#         return AgentAction(tool="Search", tool_input=kwargs["input"], log="")
#
#
# weaviate_client = weaviate.Client(
#     url=os.environ["CLUSTER_URL"],
# )
#
# retriever = WeaviateHybridSearchRetriever(weaviate_client, index_name="LangChain", text_key="text")
#
# tools = [
#     Tool(
#         name = "Search",
#         func=weaviate_client.run,
#         description="useful for when you need to answer questions about current events",
#         return_direct=True
#     )
# ]
#
# class TravelAgentApiInteraction(BaseSingleActionAgent):
#     """This travel agent can call an API"""
#     @property
#     def input_keys(self):
#         return ["chat_history", "human_input"]
#
#     @tool("set_wildlife", return_direct=True, args_schema="should be called if the client shows interest wildlife")
#     def set_wildlife(self):
#         return "wildlife"
#
#
#     def plan(
#             self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
#     ) -> Union[AgentAction, AgentFinish]:
#         """Given input, decided what to do.
#
#         Args:
#             intermediate_steps: Steps the LLM has taken to date,
#                 along with observations
#             **kwargs: User inputs.
#
#         Returns:
#             Action specifying what tool to use.
#         """
#         return AgentAction(tool="Search", tool_input=kwargs["input"], log="")
#
#     async def aplan(
#             self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
#     ) -> Union[AgentAction, AgentFinish]:
#         """Given input, decided what to do.
#
#         Args:
#             intermediate_steps: Steps the LLM has taken to date,
#                 along with observations
#             **kwargs: User inputs.
#
#         Returns:
#             Action specifying what tool to use.
#         """
#         return AgentAction(tool="Search", tool_input=kwargs["input"], log="")

agents = {
    "travel_agent_v1": travel_agent_v1
}
