from flask import Flask
from config.authConfig import Configuration
from authModels import *
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Configuration)

database.init_app(app)

migrate = Migrate(app)

