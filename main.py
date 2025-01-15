from uuid import uuid4
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

# Así se define el nombre de nestra aplicación app
app = FastAPI()
app.title = 'Primera APP en Fast API'
movie_router = APIRouter(prefix ="/api", tags=["Movies"])

class Movie(BaseModel):
    uuid: str = "123"
    title: str = "title"
    year: str = "2009"
    rating: str = "6"
    category: str = "Commedy"

movies = [
    {
        "uuid": "123",
        "title": "Pelicula Ejemplo",
        "year": "2015",
        "rating": "10",
        "category": "Action"
    },
    {
        "uuid": "234",
        "title": "Pelicula Ejemplo Dos",
        "year": "2013",
        "rating": "5",
        "category": "Drama"
    }
]

def findMovie(movies, searchKey: str, value: str):
    for movie in movies:
        if (movie[searchKey]).lower() == value.lower():
            return movie
    return None

@movie_router.get("/movies/all", name="Get all movies", description="Get all movies from a list")
def getMovies():
    return movies

@movie_router.get("/movies/getById/{id}", name="Get movie by ID ", description="Get a movie by id from a list of movies")
def getMovieById(id: str):
    movie = findMovie(movies, "uuid", id)
    if movie:
        return movie
    return {"message": "No such movie with id: %s" % id}

@movie_router.get("/movies/getByCategory/{category}", name="Get movies by category", description="Get all movies from a category of movies")
def getMoviesByCategory(category: str):
    movie = findMovie(movies, "category", category)
    if movie:
        return movie
    else:
        return { "message": "No such movie in that category: %s" % category }

@movie_router.post("/movies/addMovie", name="Add a new movie", description="Add a new movie to list of movies")
def addMovie(movie: Movie):
    if not movie.uuid:
        movie.uuid = str(uuid4())

    for existing in movies:
        if existing["title"] == movie.title:
            raise HTTPException(status_code=400, detail="A movie with the same title already exists")
        else:
            movies.append(movie.dict())
            return movie

app.include_router(movie_router)
