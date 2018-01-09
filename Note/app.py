
from sqlalchemy import create_engine
import falcon
from resources import *
from falcon_autocrud.middleware import Middleware

db_engine = create_engine('sqlite:///stuff.db')

app = falcon.API(
    middleware=[Middleware()],
)

app.add_route('/notes', NoteCollectionResource(db_engine))
app.add_route('/notes/{id}', NoteResource(db_engine))