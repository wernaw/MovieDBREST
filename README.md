# FastAPI Movies Manager

This is a simple FastAPI application that allows you to manage movies in an SQLite database. It also includes some basic arithmetic and geocoding endpoints.

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Endpoints with Example curl Commands
### Root
```bash
curl http://127.0.0.1:8000/
```

#### Response
```json
{"message": "Hello World"}
```
### Greeting
```bash
curl http://127.0.0.1:8000/hello/Weronika
```
#### Response
```json
{"message": "Hello Weronika"}
```
<br>

### Arithmetic
#### Sum
```bash
curl "http://127.0.0.1:8000/sum?x=5&y=7"
```
#### Response
```json
12
```

#### Subtract
```bash
curl "http://127.0.0.1:8000/substract?x=16&y=3"
```
#### Response
```json
13
```

#### Multiply
```bash
curl "http://127.0.0.1:8000/multiply?x=3&y=5"
```
#### Response
```json
15
```
<br>

### Geocoding
```bash
curl "http://127.0.0.1:8000/geocode?lat=50.0680275&lon=19.9098668"
```
#### Response
```json
{"place_id":171151821,"licence":"Data Â© OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
  "osm_type":"node","osm_id":9253022633,"lat":"50.0680109","lon":"19.9098257","category":"amenity",
  "type":"fast_food","place_rank":30,"importance":7.936751354233642e-05,"addresstype":"amenity",
  "name":"p1zzeria","display_name":"p1zzeria, Kawiory, Cichy KÄ…cik, Czarna WieÅ›, Krowodrza, KrakÃ³w, wojewÃ³dztwo maÅ‚opolskie, 30-056, Polska",
  "address":{"amenity":"p1zzeria","road":"Kawiory","neighbourhood":"Cichy KÄ…cik","quarter":"Czarna WieÅ›", 
    "suburb":"Krowodrza","city_district":"Krowodrza","city":"KrakÃ³w","state":"wojewÃ³dztwo maÅ‚opolskie",
    "ISO3166-2-lvl4":"PL-12","postcode":"30-056","country":"Polska","country_code":"pl"},
  "boundingbox":["50.0679609","50.0680609","19.9097757","19.9098757"]}
```
<br>

### Movies CRUD
#### Get all movies
```bash
curl http://127.0.0.1:8000/movies
```

#### Get movie by ID
```bash
curl http://127.0.0.1:8000/movies/1
```

#### Add a movie
```bash
curl -X POST http://127.0.0.1:8000/movies \
     -H "Content-Type: application/json" \
     -d '{"title": "Severance", "director": "Ben Stiller", "year": 2020, 
     "description": "Severance is a dark sci-fi thriller about office workers who undergo a procedure that completely separates their work memories from their personal lives, uncovering a chilling corporate conspiracy."}'
```

#### Response
```json
{"message": "Movie added successfully!", "id": 9}
```

#### Update a movie
```bash
curl -X PUT http://127.0.0.1:8000/movies/6 \
     -H "Content-Type: application/json" \
     -d '{"title": "New Title", "year": 2020}'
```
#### Response
```json
{"message": "Movie updated successfully!"}
```

#### Delete a movie
```bash
curl -X DELETE http://127.0.0.1:8000/movies/7
```

#### Response
```json
{"message": "Movie deleted successfully!"}
```

#### Delete all movies
```bash
curl -X DELETE http://127.0.0.1:8000/movies
```

#### Response
```json
{"message": "All movies deleted successfully!", "deleted_count": 4}
```

<br>

### Actors CRUD
#### Get all actors
```bash
curl http://127.0.0.1:8000/actors
```

#### Get actor by ID
```bash
curl http://127.0.0.1:8000/actors/1
```

#### Add an actor
```bash
curl -X POST http://127.0.0.1:8000/actors \
     -H "Content-Type: application/json" \
     -d '{"name": "Adam", "surname": "Scott"}'
```

#### Response
```json
{"message": "Actor added successfully!", "id": 19}
```

#### Update an actor
```bash
curl -X PUT http://127.0.0.1:8000/actors/18 \
     -H "Content-Type: application/json" \
     -d '{"name": "Billy"}'
```
#### Response
```json
{"message": "Actor updated successfully!"}
```

#### Delete an actor
```bash
curl -X DELETE http://127.0.0.1:8000/actors/5
```

#### Response
```json
{"message": "Actor deleted successfully!"}
```

### Retrieve actors by movie ID
```bash
curl http://127.0.0.1:8000/movies/4/actors
```
<br>

## ORM Version
The orm folder contains the same movies and actors functionality but implemented using Peewee ORM instead of raw SQL queries.
- Models for Movie and Actor are defined in orm/models.py.
- Many-to-many relationships between movies and actors are handled via ManyToManyField.
- CRUD operations are performed using Peewee methods.

Example structure inside orm/:
```
orm/
├─ models.py       # Peewee ORM models
├─ db_utils.py     # CRUD helpers using ORM
└─ movies_extended_orm.db  # SQLite database for ORM
```

## Notes
- SQLite database file: movies-extended.db
- Error handling implemented with HTTP status codes:
  - 400: Bad request / missing fields
  - 404: Movie not found
  - 500: Database error
