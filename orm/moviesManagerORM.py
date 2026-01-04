from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from orm.models import Movie, Actor
from orm.db_utils_orm import (fetch_one, fetch_all, insert_item,
update_item, delete_item, delete_all_items, get_actors_for_movie_orm)


app = FastAPI()

@app.get("/movies")
def get_movies():
    movies = fetch_all(Movie)

    return [movie.to_dict() for movie in movies]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = fetch_one(Movie, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie.to_dict()


@app.post("/movies")
def add_movie(payload: Dict[str, Any]):
    movie_id = insert_item(Movie, payload)

    return {"message": "Movie added", "id": movie_id}


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, payload: Dict[str, Any]):
    update_item(Movie, movie_id, payload)

    return {"message": "Movie updated"}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    delete_item(Movie, movie_id)

    return {"message": "Movie deleted"}


@app.delete("/movies")
def delete_movies():
    count = delete_all_items(Movie)

    return {"message": "All movies deleted", "deleted_count": count}


@app.get("/actors")
def get_actors():
    actors = fetch_all(Actor)

    return [actor.to_dict() for actor in actors]


@app.get("/actors/{actor_id}")
def get_actor(actor_id: int):
    actor = fetch_one(Actor, actor_id)

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    return actor.to_dict()


@app.post("/actors")
def add_actor(payload: Dict[str, Any]):
    actor_id = insert_item(Actor, payload)

    return {"message": "Actor added", "id": actor_id}


@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, payload: Dict[str, Any]):
    update_item(Actor, actor_id, payload)

    return {"message": "Actor updated"}


@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    delete_item(Actor, actor_id)

    return {"message": "Actor deleted"}

@app.get('/movies/{movie_id}/actors')
def get_actor_for_movie(movie_id: int):
    return get_actors_for_movie_orm(movie_id)
