from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
from . import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
db.init_app(app)
db.create_all()

