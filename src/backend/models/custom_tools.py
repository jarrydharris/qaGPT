from typing import Any
from typing import Callable

from flask_session.sessions import ServerSideSession
from pydantic import BaseModel
from pydantic import Field


class FlaskSessionTool(BaseModel):
    user_input: str = Field(None, alias="input")
    session: ServerSideSession = Field(default_factory=ServerSideSession)
    func: Callable = Field(default_factory=lambda: Any | None)

    def run(self, user_input) -> str:
        return self.func(user_input=user_input, session=self.session)
