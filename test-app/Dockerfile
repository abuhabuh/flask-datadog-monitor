FROM frolvlad/alpine-python3

### create app directory, copy app, install
### note: docker-compose will overwrite this with a bind mount when starting
RUN mkdir -p /var/www/server/client-server
COPY . /var/www/server/client-server
RUN pip install -r /var/www/server/client-server/requirements.txt

### env setup to the server
WORKDIR /var/www/server/
ENV PYTHONPATH=/var/www/server/client-server
ENV FLASK_APP=client-server/app:app

ENTRYPOINT ["flask", "run", "--port", "5000", "--host", "0.0.0.0", "--reload"]

