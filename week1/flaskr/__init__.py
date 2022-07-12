from flask import Flask
from flask_migrate import Migrate
from . import config
from .src.models import db

migrate = Migrate() # Initializing migrate.

# Create
def create_app():
#   Application factory pattern
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    migrate.init_app(app, db)

    return app