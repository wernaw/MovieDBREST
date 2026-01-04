from fastapi import FastAPI, HTTPException
import requests
import sqlite3
from typing import Any


app = FastAPI()
DB_PATH = 'movies-extended.db'

def get_db_cursor():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    return db, cursor

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
    output = []

    db, cursors = get_db_cursor()
    cursors.execute('select * from movie')

    for movie in cursors:
        movie = {'id': movie[0], 'title': movie[1], 'director': movie[2],
                 'year': movie[3], 'decription': movie[4]}
        output.append(movie)

    return output

@app.get('/movies/{movie_id}')
def get_movie(movie_id: int):
    db, cursor = get_db_cursor()

    movie = cursor.execute("select * from movie where id=?", (movie_id,)).fetchone()

    if movie is None:
        return {"message": "Movie not found"}

    return {'id': movie[0], 'title': movie[1], 'director': movie[2],
            'year': movie[3], 'decription': movie[4]}

@app.post('/movies')
def add_movie(params: dict[str, Any]):
    required_fields = ['title', 'director', 'year', 'description']
    missing_fields = [f for f in required_fields if f not in params]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    db, cursor = get_db_cursor()

    cursor.execute(
        'INSERT INTO movie (title, director, year, description) VALUES (?, ?, ?, ?)',
        (
            params['title'],
            params['director'],
            params['year'],
            params['description']
        )
    )

    movie_id = cursor.lastrowid

    db.commit()
    db.close()

    return {"message": f"Movie added successfully!", "id": movie_id}

@app.put('/movies/{movie_id}')
def update_movie(movie_id: int, params: dict[str, Any]):
    fields = []
    values = []

    for key in ['title', 'director', 'year', 'description']:
        if key in params:
            fields.append(f"{key} = ?")
            values.append(params[key])

    if not fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    values.append(movie_id)

    try:
        db, cursor = get_db_cursor()

        cursor.execute(
            f'UPDATE movie SET {", ".join(fields)} WHERE id = ?',
            tuple(values)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Movie not found")

        db.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        db.close()

    return {"message": "Movie updated successfully!"}

@app.delete('/movies/{movie_id}')
def delete_movie(movie_id: int):
    try:
        db, cursor = get_db_cursor()

        cursor.execute('DELETE FROM movie WHERE id = ?', (movie_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        db.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        db.close()

    return {"message": "Movie deleted successfully!"}


@app.delete('/movies')
def delete_all_movies():
    try:
        db, cursor = get_db_cursor()

        cursor.execute('DELETE FROM movie')
        deleted_count = cursor.rowcount

        db.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        db.close()

    return {
        "message": "All movies deleted successfully!",
        "deleted_count": deleted_count
    }

@app.get('/actors')
def get_actors():
    output = []

    db, cursors = get_db_cursor()
    cursors.execute('select * from actor')

    for actor in cursors:
        actors = {'id': actor[0], 'name': actor[1], 'surname': actor[2]}
        output.append(actors)

    return output

@app.get('/actors/{actor_id}')
def get_actor(actor_id: int):
    db, cursor = get_db_cursor()

    actor = cursor.execute("select * from actor where id=?", (actor_id,)).fetchone()

    if actor is None:
        return {"message": "Actor not found"}

    return {'id': actor[0], 'name': actor[1], 'surname': actor[2]}

@app.post('/actors')
def add_actor(params: dict[str, Any]):
    required_fields = ['name', 'surname']
    missing_fields = [f for f in required_fields if f not in params]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    db, cursor = get_db_cursor()

    cursor.execute(
        'INSERT INTO actor (name, surname) VALUES (?, ?)',
        (
            params['name'],
            params['surname']
        )
    )

    actor_id = cursor.lastrowid

    db.commit()
    db.close()

    return {"message": f"Actor added successfully!", "id": actor_id}

@app.put('/actors/{actor_id}')
def update_actor(actor_id: int, params: dict[str, Any]):
    fields = []
    values = []

    for key in ['name', 'surname']:
        if key in params:
            fields.append(f"{key} = ?")
            values.append(params[key])

    if not fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    values.append(actor_id)

    try:
        db, cursor = get_db_cursor()

        cursor.execute(
            f'UPDATE actor SET {", ".join(fields)} WHERE id = ?',
            tuple(values)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Actor not found")

        db.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        db.close()

    return {"message": "Actor updated successfully!"}

@app.delete('/actors/{actor_id}')
def delete_actor(actor_id: int):
    try:
        db, cursor = get_db_cursor()

        cursor.execute('DELETE FROM actor WHERE id = ?', (actor_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Actor not found")
        db.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        db.close()

    return {"message": "Actor deleted successfully!"}

@app.get('/movies/{movie_id}/actors')
def get_actor_for_movie(movie_id: int):
    db, cursor = get_db_cursor()

    actors = cursor.execute("select name, surname from actor a "
                           "join movie_actor_through atm on a.id = atm.actor_id "
                           "where atm.movie_id = ?;", (movie_id,)).fetchall()

    if actors is None:
        return {"message": "No actors found for this movie"}

    output = [
        {"name": name, "surname": surname}
        for name, surname in actors
    ]

    return output
