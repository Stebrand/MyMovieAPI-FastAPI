from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


#@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15) ):
    db= Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    db = Session()
    MovieService(db).create_movie(movie)
    return  JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message":"Se ha modificado"})        
        
@movie_router.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message":"Se ha eliminado"}) 