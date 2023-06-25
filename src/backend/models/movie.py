from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    backdrop_path = Column(String(120), nullable=False)
    genre_ids = Column(String(120), nullable=False)
    original_language = Column(String(120), nullable=False)
    overview = Column(String(2**14), nullable=False)
    poster_path = Column(String(120), nullable=False)
    release_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"Movie(title={self.title})"
