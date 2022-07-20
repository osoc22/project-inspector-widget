#!/bin/sh

flask db init
flask db migrate
flask db upgrade

gunicorn app:app -b 0.0.0.0:8500 #run on port if param env is
#gunicorn app:app #run on port if param env is