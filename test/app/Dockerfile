# NOTE: Context for this build file is set by the docker-compose.yml file
FROM python:3.9

# Variables
ARG SRC_DIR=/var/www/src

# Copy flask-datadog up to container
# note: docker-compose will overwrite this with a bind mount when starting
RUN mkdir -p /var/www/src
COPY . /var/www/src

# env setup to the server
WORKDIR /var/www/src/test/app/
RUN pip install -r /var/www/src/test/app/requirements.txt

# Set Env vars -- additional env vars set in docker-compose
ENV PYTHONPATH=/var/www/src/test/app/
ENV FLASK_APP=app:app

# Starting the app with DataDog ddtrace-run
# - datadog env and service setup is specified in docker-compose file
ENTRYPOINT ["ddtrace-run", "flask", "run", "--port", "5000", "--host", "0.0.0.0", "--reload"]

