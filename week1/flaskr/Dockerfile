# pull official base image
FROM --platform=linux/amd64 python:3.10-bullseye

RUN mkdir /flaskr

# set work directory
WORKDIR /flaskr

# set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apt-get update && apt-get install curl gnupg -y \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install chromium -y --no-install-recommends \
  && apt-get install -f \
  && rm -rf /var/lib/apt/lists/*


# install dependencies
COPY requirements.txt requirements.txt

# Install packages
RUN pip install -r requirements.txt

# copy project
COPY . /flaskr

EXPOSE 8500

CMD flask db upgrade

ENTRYPOINT flask run --host='0.0.0.0'