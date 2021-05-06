# FROM frolvlad/alpine-python3
FROM python:3

# create app directory, copy app, install
# note: docker-compose will overwrite this with a bind mount when starting
RUN mkdir -p /var/www/server/client-server
COPY . /var/www/server/client-server
RUN pip install -r /var/www/server/client-server/requirements.txt

# env setup to the server
WORKDIR /var/www/server/
ENV PYTHONPATH=/var/www/server/client-server
ENV FLASK_APP=client-server/app:app

# Datadog setup
ENV DD_SERVICE="test_app_service"
ENV DD_ENV="prod"
ENV DD_LOGS_INJECTION=true

ENTRYPOINT ["ddtrace-run", "flask", "run", "--port", "5000", "--host", "0.0.0.0", "--reload"]

