import os

if not os.environ["DATABASE_URL"]:
    raise RuntimeError("DATABASE_URL is not set")

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = os.environ['DATABASE_URL']