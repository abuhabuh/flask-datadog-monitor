import json

import flask


def add_endpoints(flask_app, jinja_env):

    @flask_app.route('/health', methods=['GET'])
    def get_health():
        return json.dumps({'status': 'ok'})

    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render()

