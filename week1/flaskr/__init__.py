from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import json
try:
    import config                           
except ImportError:
    from . import config
try:
    from src.models import db, TokenBlocklist
except ImportError:
    from .src.models import db, TokenBlocklist
    
from flask_cors import CORS
from datetime import timedelta
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
    app.config["JWT_SECRET_KEY"] =  config.SECRET_KEY or 'top-secret'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.app_context().push()
    
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return json.dumps({
            'succes': False,
            'message': 'The token has expired'
        }), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_on_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.find_by_jti(jti)

        return token is not None

    @jwt.unauthorized_loader
    def missing_token_callback(callback):
        return json.dumps({
            'succes': False,
            'message': 'Missing auth header'
        }), 401
    
    db.init_app(app)
    migrate.init_app(app, db)

    return app

