from fastapi import HTTPException
from orm.models import db, Movie, Actor, ActorMovie
from typing import Any, Dict, List, Type
from peewee import Model, DoesNotExist


def fetch_one(model: Type[Model], item_id: int) -> Model:
    try:
        return model.get_by_id(item_id)
    except DoesNotExist:
        return None


def fetch_all(model: Type[Model]) -> List[Model]:
    return list(model.select())


def insert_item(model: Type[Model], data: Dict[str, Any]) -> int:
    obj = model.create(**data)
    return obj.id


def update_item(model: Type[Model], item_id: int, updates: Dict[str, Any]) -> None:
    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    rows = (
        model
        .update(**updates)
        .where(model.id == item_id)
        .execute()
    )

    if rows == 0:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} not found"
        )


def delete_item(model: Type[Model], item_id: int) -> None:
    rows = (
        model
        .delete()
        .where(model.id == item_id)
        .execute()
    )

    if rows == 0:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} not found"
        )


def delete_all_items(model: Type[Model]) -> int:
    return model.delete().execute()


def get_actors_for_movie_orm(movie_id: int) -> list[dict]:
    if db.is_closed():
        db.connect()

    try:
        movie = Movie.get(Movie.id == movie_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")

    actors_query = (
        Actor
        .select(Actor.name, Actor.surname)
        .join(ActorMovie)
        .where(ActorMovie.movie == movie)
    )

    if not actors_query.exists():
        raise HTTPException(status_code=404, detail="There are no actors for this movie")

    return [{"name": actor.name, "surname": actor.surname} for actor in actors_query]
