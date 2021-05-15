import datetime
import http
import json

import flask


def add_endpoints(flask_app, jinja_env):

    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render(), http.HTTPStatus.OK

    @flask_app.route('/date', methods=['GET'])
    def get_date():
        response_code = flask.request.args.get('resp')
        if not response_code:
            response_code = http.HTTPStatus.OK

        return json.dumps({
            'date':  str(datetime.datetime.now().date()),
            'response_code': response_code,
        }, indent=2), int(response_code)

    @flask_app.route('/health', methods=['GET'])
    def get_health():
        return json.dumps({'status': 'ok'}), http.HTTPStatus.OK

