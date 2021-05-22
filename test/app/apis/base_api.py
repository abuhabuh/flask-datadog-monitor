import datetime
import http
import json

import flask

from flask_datadog.monitor import tag_route
from flask_datadog.shared.ddog_constants import MonitorType, ThresholdType


def add_endpoints(flask_app, jinja_env):

    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render(), http.HTTPStatus.OK

    @tag_route(
        monitors={
            MonitorType.ERROR_RATE_MONITOR: {
                ThresholdType.CRITICAL_THRESHOLD: 0.1,
                ThresholdType.WARNING_THRESHOLD: 0.05,
            },
        },
    )
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
    def get_health_baby():
        return json.dumps({'status': 'ok'}), http.HTTPStatus.OK

