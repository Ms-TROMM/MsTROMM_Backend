import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

connexion_app = connexion.App(__name__, specification_dir='./')

connexion_app.add_api('swagger.yml')

app = connexion_app.app
CORS(app)

# Since you’re not creating an event-driven program, turn this feature off.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This causes SQLAlchemy to echo SQL statements it executes to the console.
app.config['SQLALCHEMY_ECHO'] = True

# Database URL received from heroku
if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL', None)

#  The db variable is what’s imported into the build_database.py
#  program to give it access to SQLAlchemy and the database.
db = SQLAlchemy(app)

# This initializes Marshmallow and allows it to introspect the SQLAlchemy components attached to the app.
ma = Marshmallow(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def root():
    return '<h1>Welcome to ms-tromm API</h1>'


