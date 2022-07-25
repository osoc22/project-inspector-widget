#!/bin/sh

flask db init
flask db migrate
flask db upgrade

if [[ $FLASK_ENV = "development" ]]
then
    gunicorn app:app -b 0.0.0.0:8500
else 
    gunicorn app:app
fi