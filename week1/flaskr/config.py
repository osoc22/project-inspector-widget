import os
from dotenv import load_dotenv

mode = os.environ.get('FLASK_ENV')

if mode == 'production':
    APP_ROOT = os.path.join(os.path.dirname(__file__))
    dotenv_path = os.path.join(APP_ROOT, '.env.prod')
    load_dotenv(dotenv_path)
    os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].replace("postgres", "postgresql") # Add regex, make sure it only does that for production

elif mode == 'development':
    load_dotenv()

if not os.environ["DATABASE_URL"]:
    raise RuntimeError("DATABASE_URL is not set")

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']