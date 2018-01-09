# Rest API using Falcon

Falcon is a bare-metal Python web API framework used for building fast app backends and microservices. A bare-metal server is single-tenant physical server completely dedicated for single customer.

As per the official [Falcon website](https://falconframework.org/)

```
“When it comes to building HTTP APIs, other frameworks weigh you down with tons of dependencies and unnecessary abstractions. Falcon cuts to the chase with a clean design that embraces HTTP and the REST architectural style.”
``` 	

In this article, we will create a RESTful API for our application using Falcon. It is a simple application having one table Note with following fields:

* Title
* Description
* Created At
* Created By
* Priority

Main tasks performed by this app:
1. Create a note (POST request)
2. Get a note (GET request)
3. Edit a note (PUT request)
4. Delete a note (DELETE request)

We will use SQLAlchemy as our resource provider for the APIs and gunicorn to serve those APIs.

### Set up Falcon
Set up and activate a virtual environment using python3. Install Falcon, SQLAlchemy and gunicorn

```
pip install falcon
pip install SQLAlchemy
pip install gunicorn
```

or clone the github [repository](https://github.com/vibhash1083/falcon-note) and install the requirements

```
pip install -r requirements.txt
```

### Models

Once the package installation is done, we will set up SQLAlchemy as our resource provider in models.py file:

```
if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
```

After that, we add a Note model class for creating note objects in models.py

```
class Note(Base):
    __tablename__ = 'notes'
    id      = Column(Integer, primary_key=True)
    title    = Column(String(50))
    description     = Column(String(50))
    created_at     = Column(String(50))
    created_by     = Column(String(50))
    priority     = Column(Integer)

```

In resources.py file we define Note resources based on Note model. 
```
class NoteCollectionResource(CollectionResource):
    model = Note
    methods = ['GET', 'POST']


class NoteResource(SingleResource):
    model = Note
```


After defining models and resources, we add API urls in app.py.
```
db_engine = create_engine('sqlite:///stuff.db')

app = falcon.API(
    middleware=[Middleware()],
)

app.add_route('/notes', NoteCollectionResource(db_engine))
app.add_route('/notes/{id}', NoteResource(db_engine))
```

## Running the app
Create database by executing following in terminal
```
python models.py
```

Run the server
```
gunicorn --reload app:app
```
We can view list of all requests at http://127.0.0.1:8000/notes.

### Using APIs for notes
Open python shell and execute following requests:

requests.post('http://localhost:8000/notes/',
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({'title': 'sample note five' , 'description': 'sample notes',
                                    'created_at': '2017-08-18 00:00:00', 'created_by': 'apcelent',
                                    'priority': 3}))

requests.put('http://localhost:8000/notes/2',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'title': 'sample note five' , 'description': 'sample notes edit',
                                    'created_at': '2017-08-18 00:00:00', 'created_by': 'apcelent',
                                    'priority': 3}))

requests.delete('http://localhost:8000/notes/2')

### Performance
Benchmark results for Falcon on official website shows that Falcon performs better than some other popular python frameworks with ability to handle much larger requests in lesser time making it fast and reliable for large-scale microservices and backends.