import datetime
import json

import flask


def add_endpoints(flask_app, jinja_env):

    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render()

    @flask_app.route('/date', methods=['GET'])
    def get_date():
        return json.dumps({
            'date':  str(datetime.datetime.now().date())
        })

    @flask_app.route('/health', methods=['GET'])
    def get_health():
        return json.dumps({'status': 'ok'})

