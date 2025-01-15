from uuid import uuid4
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

# Así se define el nombre de nestra aplicación app
app = FastAPI()
app.title = 'Learn Fast API'
app.description = 'This is a simple API to learn Fast API and start using it to develop applications in a near future.'
app.author = 'Systems Engineering: Yerson Andres Martinez Lopez'

# Define el router para las rutas de las películas
movie_router = APIRouter(prefix ="/api", tags=["Movies"])

# Define el modelo de datos para las películas
class ModelMovie(BaseModel):
    uuid: str
    title: str
    year: str
    rating: str
    category: str

class Movie(BaseModel):
    uuid: str = "67230031-df67-49fd-9f0d-2bcbafbee2b4"
    title: str = "title"
    year: str = "2009"
    rating: str = "6"
    category: str = "Commedy"
    
# Modelo para actualizar películas
class UpdateMovie(BaseModel):
    title: str
    year: str
    rating: str
    category: str
    
class ResponseModel(BaseModel):
    status: int
    message: str

class MovieResponse(BaseModel):
    response: ResponseModel
    data: ModelMovie

# Lista de películas iniciales para el ejemplo
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

# Función para buscar películas por un criterio
def findMovie(movies, searchKey: str, value: str):
    for movie in movies:
        if (movie[searchKey]).lower() == value.lower():
            return movie
    return None

# Rutas para las películas
@movie_router.get("/movies/all", name="Get all movies", description="Get all movies from a list")
def getMovies():
    return movies

@movie_router.get("/movies/getById/{id}", name="Get movie by ID ", description="Get a movie by id from a list of movies", response_model=MovieResponse)
def getMovieById(id: str):
    movie = findMovie(movies, "uuid", id)
    if movie:
        return  {
                    "response": {
                        "status": 200,
                        "message": "Movie found correctly"
                    },
                    "data": movie
                }
    return {"message": "No such movie with id: %s" % id}

@movie_router.get("/movies/getByCategory/{category}", name="Get movies by category", description="Get all movies from a category of movies", response_model=MovieResponse)
def getMoviesByCategory(category: str):
    movie = findMovie(movies, "category", category)
    if movie:
        return  {
                    "response": {
                        "status": 200,
                        "message": "Movie found correctly"
                    },
                    "data": movie
                }
    else:
        return { "message": "No such movie in that category: %s" % category }

@movie_router.post("/movies/addMovie", name="Add a new movie", description="Add a new movie to list of movies", response_model=MovieResponse)
def addMovie(movie: Movie):
    if not movie.uuid:
        movie.uuid = str(uuid4())

    for existing in movies:
        if existing["title"] == movie.title:
            raise HTTPException(status_code=400, detail="A movie with the same title already exists")
    movies.append(movie.model_dump())
    return  {
                "response": {
                    "status": 201,
                    "message": "Movie added correctly"
            }, 
                "data": movie
            }

@movie_router.put("/movies/updateMovie/{idMovie}", name="Update a movie", description="Update a movie in the list of movies", response_model=MovieResponse)
def updateMovie(idMovie: str, updateMovie: UpdateMovie):
    for movie in movies:
        if movie["uuid"] == idMovie:
            movie["title"] = updateMovie.title
            movie["year"] = updateMovie.year
            movie["rating"] = updateMovie.rating
            movie["category"] = updateMovie.category
            return  { 
                        "response": {
                            "status": 200, 
                            "message": "Movie updated correctly"
                        }, 
                        "data": movie
                    }

    raise HTTPException(status_code=404, detail="Movie not found")

app.include_router(movie_router)
