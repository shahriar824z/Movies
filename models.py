from database import Base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field
from typing import Literal

class Movies(Base):

    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    genre = Column(String)
    duration = Column(Integer)
    rating = Column(Float)

class MovieCreate(BaseModel):
    movie_id : int
    title : str
    director : str
    genre : Literal['action', 'comedy', 'drama', 'thriller']
    duration : int = Field(gt=0)
    rating : float = Field(ge=0, le=5)


class MovieUpdate(BaseModel):
    title : str
    director : str
    genre : Literal['action', 'comedy', 'drama', 'thriller']
    duration : int = Field(gt=0)
    rating : float = Field(ge=0, le=5)