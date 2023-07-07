from flask import Flask
from configuration import Configuration
from models import *
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config.from_object(Configuration)

if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
    create_database(Configuration.SQLALCHEMY_DATABASE_URI)

database.init_app(app)
migrate = Migrate(app, database)


@app.route("/users", methods=["GET"])
def users():
    return str(User.query.all())





