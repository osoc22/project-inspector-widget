from flask import Flask
from flask_migrate import Migrate
try:
    import config                           
except ImportError:
    from . import config
try:
    from src.models import db
except:
    from .src.models import db
    
from flask_cors import CORS
migrate = Migrate() # Initializing migrate.

# Create
def create_app():
#   Application factory pattern
    app = Flask(__name__)
    CORS(app)
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    migrate.init_app(app, db)

    return app