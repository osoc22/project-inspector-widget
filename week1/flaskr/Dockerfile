# pull official base image
FROM python:3.10-bullseye

RUN mkdir /flaskr

# set work directory
WORKDIR /flaskr

# set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apt-get update && apt-get install curl gnupg -y \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends \
  && apt-get install -f \
  && rm -rf /var/lib/apt/lists/*


# install dependencies
COPY requirements.txt requirements.txt

# Install packages
RUN pip install -r requirements.txt

# copy project
COPY . /flaskr

# Make port 8500 available outside this container
#EXPOSE 8500

#CMD gunicorn app:app
# Run commands at start up
RUN chmod u+x ./docker-entrypoint.sh
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]