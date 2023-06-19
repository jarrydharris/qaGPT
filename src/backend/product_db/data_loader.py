import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.backend.models.movie import Movie

load_dotenv()


def create_tables() -> None:
    engine = create_engine(os.environ["PG_URI"] + "/movies", echo=True, future=True)
    Movie.metadata.create_all(engine)


def connect_to_postgres() -> Session:
    engine = create_engine(os.environ["PG_URI"] + "/movies", echo=True, future=True)
    session = Session(engine)
    return session


def load_data_to_model(path: str = "out/movies.json") -> list[dict]:
    with open(path) as f:
        movies_json = json.load(f)
    movies = [Movie(**movie) for movie in movies_json]
    return movies


def commit_movie_data(session, movies) -> None:
    with session:
        session.add_all(movies)
        session.commit()


if __name__ == "__main__":
    session = connect_to_postgres()
    movies = load_data_to_model()
    commit_movie_data(session, movies)
