# pull official base image
FROM python:3.10-bullseye

RUN mkdir /flaskr

# set work directory
WORKDIR /flaskr

# set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# install dependencies
COPY requirements.txt requirements.txt

# Install packages
RUN pip install -r requirements.txt

# copy project
COPY . /flaskr

EXPOSE 8500

ENTRYPOINT flask run --host='0.0.0.0'