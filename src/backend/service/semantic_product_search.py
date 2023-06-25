import os
from datetime import datetime
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

import weaviate
from dotenv import load_dotenv
from flask_session.sessions import ServerSideSession
from langchain import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents import create_vectorstore_agent
from langchain.agents.agent_toolkits import VectorStoreInfo
from langchain.agents.agent_toolkits import VectorStoreToolkit
from langchain.callbacks import AimCallbackHandler
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.vectorstores import VectorStore

load_dotenv()

VST = TypeVar("VST", bound="VectorStore")


class WeaviateMovieStore(VectorStore):
    def __init__(self, cluster_url, cluster_key, additional_headers, session):
        self._cluster_url = cluster_url
        self._cluster_key = weaviate.AuthApiKey(api_key=cluster_key)
        self._headers = additional_headers
        self._session = session
        self._client = self._init_client()

    def _init_client(self) -> weaviate.Client:
        return weaviate.Client(
            url=self._cluster_url,
            auth_client_secret=self._cluster_key,
            additional_headers=self._headers,
        )

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            **kwargs: Any,
    ) -> List[str]:
        raise NotImplementedError

    def _update_product_list(self, product_ids: List[int]) -> None:
        if "products" not in self._session:
            self._session["product_ids"] = product_ids
        self._session.update({"product_ids": product_ids})
        self._session.modified = True
        print(f"\n\nUpdated product list: {self._session}\n\n")

    def similarity_search(
            self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        response = (
            self._client.query.get("Movie", ["tmdb_id", "title", "overview"])
            .with_near_text({"concepts": [query]})
            .with_limit(k)
            .do()
        )
        response = response.get("data").get("Get").get("Movie")
        if response is None:
            return [Document(page_content='just return "I dont know" as the answer.',
                             metadata={"title": 'just return "I dont know" as the answer.',
                                       "source": 'just return "I dont know" as the answer.'})]
        response = [
            Document(
                page_content=m["overview"],
                metadata={"title": m["title"], "source": m["tmdb_id"]},
            )
            for m in response
        ]
        self._update_product_list([int(d.metadata["source"]) for d in response])
        return response

    @classmethod
    def from_texts(
            cls: Type[VST],
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            **kwargs: Any,
    ) -> VST:
        raise NotImplementedError


def init_semantic_searcher(session: ServerSideSession) -> AgentExecutor:
    additional_headers = {"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]}
    url = os.environ["CLUSTER_URL"]
    movie_db = WeaviateMovieStore(
        url, os.environ["CLUSTER_KEY"], additional_headers, session
    )
    vectorstore_info = VectorStoreInfo(
        name="Move database",
        description="A database of movies, pass in a query and get back similar movies",
        vectorstore=movie_db,
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    llm = OpenAI(temperature=0)
    session_time = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    aim_callback = AimCallbackHandler(
        repo=".", experiment_name=f"Semantic product search experiments: {session_time}"
    )
    callbacks = [StdOutCallbackHandler(), aim_callback]
    callback_manager = BaseCallbackManager(handlers=callbacks)
    agent_executor = create_vectorstore_agent(
        llm=llm, toolkit=toolkit, verbose=True, callback_manager=callback_manager
    )
    return agent_executor
