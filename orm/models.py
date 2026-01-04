from peewee import *
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase('orm/movies_extended_orm.db')

class BaseModel(Model):
    class Meta:
        database = db

    def to_dict(self, recurse=False):
        return model_to_dict(self, recurse=recurse)


class Actor(BaseModel):
    name = CharField()
    surname = CharField()

    class Meta:
        table_name = 'actor'


class Movie(BaseModel):
    title = CharField()
    director = CharField()
    year = IntegerField()
    description = TextField()
    actors = ManyToManyField(Actor, backref="movies")

    class Meta:
        table_name = 'movie'

ActorMovie = Movie.actors.get_through_model()

db.connect()
db.create_tables([Actor, Movie, ActorMovie])
db.close()
