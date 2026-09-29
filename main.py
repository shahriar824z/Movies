from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from models import Movies, MovieCreate, MovieUpdate
from typing import Annotated, Literal
from database import engine, SessionLocal
from fastapi.responses import JSONResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/movies')
def read_movies(db : db_dependency):
    return db.query(Movies).all()

@app.get('/movies/sort')
def sort_movies(db : db_dependency,
                sort_by : Literal['duration', 'rating'] = 'rating',
                order : Literal['asc', 'desc'] = 'desc'):

    column = getattr(Movies, sort_by)

    if order == 'asc':
        return db.query(Movies).order_by(column.asc()).all()
    return db.query(Movies).order_by(column.desc()).all()

@app.get('/movies/{movie_id}')
def read_specific_movie(db : db_dependency, movie_id : int):
    specific_movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()
    if specific_movie is not None:
        return specific_movie
    else:
        raise HTTPException(status_code=404, detail='Movie not found')

@app.post('/create_movies', status_code=201)
def create_movie(db : db_dependency, new_movie : MovieCreate):

    existing_movie = db.query(Movies).filter(Movies.movie_id == new_movie.movie_id).first()
    if existing_movie is not None:
        raise HTTPException(status_code=400, detail='Movie with this movie_id already exists')

    movie_model = Movies(**new_movie.model_dump())
    db.add(movie_model)
    db.commit()
    db.refresh(movie_model)

    return movie_model

@app.put('/movies/{movie_id}')
def update_movie(db : db_dependency, movie_id : int, update_movie : MovieUpdate):

    movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    update_data = update_movie.model_dump()

    for key,value in update_data.items():
        setattr(movie,key,value)

    db.commit()
    db.refresh(movie)

    return movie

@app.delete('/movies/{movie_id}')
def delete_movie(db : db_dependency, movie_id : int):

    movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    db.query(Movies).filter(Movies.movie_id == movie_id).delete()

    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Movie deleted successfully'})