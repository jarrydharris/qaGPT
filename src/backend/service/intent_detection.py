from datetime import datetime

from flask_session.sessions import RedisSession
from flask_session.sessions import ServerSideSession
from langchain import LLMChain
from langchain import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents import ZeroShotAgent
from langchain.callbacks import AimCallbackHandler
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.tools import Tool
from src.backend.models.custom_tools import FlaskSessionTool

CRED = "\33[31m"
CEND = "\33[0m"


def update_destination(session: ServerSideSession, user_input: str) -> str:
    print(f"{CRED}\nCheckbox API called, input: {user_input}\n{CEND}")
    session["state"]["filter"]["value"] = user_input
    return "Showing destinations"


def update_budget(session: RedisSession, user_input: str):
    print(f"{CRED}\nBudget API called, input: {user_input}\n{CEND}")
    if user_input.isnumeric():
        session["state"]["slider"]["value"] = user_input
        return "Showing budget"
    else:
        return "Please provide a numerical value"


def update_wildlife(session: ServerSideSession, user_input: str) -> str:
    print(f"{CRED}\nCheckbox API called, input: {user_input}\n{CEND}")
    session["state"]["wildlife-checkbox"]["checked"] = True
    return "Showing wildlife"


def call_other(user_input: str):
    print(f"{CRED}\nOther API called, input: {user_input}\n{CEND}")
    return "The users needs are met, no further action required"


def init_intent_executor(session: ServerSideSession) -> AgentExecutor:
    checkbox = FlaskSessionTool(session=session, func=update_wildlife)
    destination = FlaskSessionTool(session=session, func=update_destination)
    budget = FlaskSessionTool(session=session, func=update_budget)

    prefix = """Use the tools below to show the user things they are interested in.
    You have access to the following tools:"""
    suffix = """
    Chat log: {input}
    {agent_scratchpad}"""
    tools = [
        Tool(
            func=checkbox.run,
            name="wildlife_checkbox",
            description=(
                "Only use this tool if the user indicates they want to see animals or wildlife."
                "provide one word to indicate the type of wildlife"
            ),
        ),
        Tool(
            func=destination.run,
            name="destination_textbox",
            description=(
                "Only use this tool if the user indicates interest in seeing a destination."
                "Provide one word to indicate the destination"
            ),
        ),
        Tool(
            func=budget.run,
            name="budget",
            description="Only use this tool if the user specifies a budget."
            "Provide a number to indicate the budget",
        ),
        Tool(
            func=call_other,
            name="other",
            description="Use this tool if the other tools are not applicable.",
        ),
    ]
    tool_names = [tool.name for tool in tools]
    input_variables = ["input", "agent_scratchpad"]
    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )
    llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
    session = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    aim_callback = AimCallbackHandler(
        repo=".", experiment_name=f"Tool Agent Experiments V1 -> Datetime: {session}"
    )
    callbacks = [StdOutCallbackHandler(), aim_callback]
    callback_manager = BaseCallbackManager(handlers=callbacks)
    agent = ZeroShotAgent(
        llm_chain=llm_chain, allowed_tools=tool_names, callbacks=callbacks
    )
    return AgentExecutor(
        agent=agent, tools=tools, verbose=True, callbackManager=callback_manager
    )
