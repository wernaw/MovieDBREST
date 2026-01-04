from fastapi import FastAPI, HTTPException
import requests
from typing import Any
from db_utils import (fetch_one, fetch_all, insert_item, update_item,
                      delete_item, delete_all_items, get_actors_for_movie)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sum")
def sum(x: int = 0, y: int = 10):
    return x+y


@app.get("/substract")
def substract(x: int = 0, y: int = 10):
    return x-y


@app.get("/multiply")
def multiply(x: int = 0, y: int = 10):
    return x*y


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/geocode")
def geocode(lat: float, lon: float):
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}'
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    return response.json()


@app.get('/movies')
def get_movies():
    movies = fetch_all('movie')

    return [{'id': movie[0], 'title': movie[1], 'director': movie[2],
             'year': movie[3], 'description': movie[4]} for movie in movies]


@app.get('/movies/{movie_id}')
def get_movie(movie_id: int):
    movie = fetch_one('movie', movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {'id': movie[0], 'title': movie[1], 'director': movie[2], 'year': movie[3], 'description': movie[4]}


@app.post('/movies')
def add_movie(params: dict[str, Any]):
    required_fields = ['title', 'director', 'year', 'description']
    missing = [f for f in required_fields if f not in params]

    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

    movie_id = insert_item('movie', required_fields, [params[f] for f in required_fields])

    return {"message": "Movie added successfully!", "id": movie_id}


@app.put('/movies/{movie_id}')
def update_movie(movie_id: int, params: dict[str, Any]):
    updates = {k: v for k, v in params.items() if k in ['title', 'director', 'year', 'description']}

    update_item('movie', movie_id, updates)

    return {"message": "Movie updated successfully!"}


@app.delete('/movies/{movie_id}')
def delete_movie(movie_id: int):
    delete_item('movie', movie_id)

    return {"message": "Movie deleted successfully!"}


@app.delete('/movies')
def delete_all_movies():
    count = delete_all_items('movie')

    return {"message": "All movies deleted successfully!", "deleted_count": count}


@app.get('/actors')
def get_actors():
    actors = fetch_all('actor')

    return [{'id': actor[0], 'name': actor[1], 'surname': actor[2]} for actor in actors]


@app.get('/actors/{actor_id}')
def get_actor(actor_id: int):
    actor = fetch_one('actor', actor_id)

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    return {'id': actor[0], 'name': actor[1], 'surname': actor[2]}


@app.post('/actors')
def add_actor(params: dict[str, Any]):
    required_fields = ['name', 'surname']
    missing = [f for f in required_fields if f not in params]

    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

    actor_id = insert_item('actor', required_fields, [params[f] for f in required_fields])

    return {"message": "Actor added successfully!", "id": actor_id}


@app.put('/actors/{actor_id}')
def update_actor(actor_id: int, params: dict[str, Any]):
    updates = {k: v for k, v in params.items() if k in ['name', 'surname']}
    update_item('actor', actor_id, updates)

    return {"message": "Actor updated successfully!"}


@app.delete('/actors/{actor_id}')
def delete_actor(actor_id: int):
    delete_item('actor', actor_id)

    return {"message": "Actor deleted successfully!"}


@app.get('/movies/{movie_id}/actors')
def get_actor_for_movie(movie_id: int):
    return get_actors_for_movie(movie_id)
