"""Monitors are auto-gen'd for these API endpoints and sync'd to DataDog
"""
import datetime
import http
import json
import time

import flask

from flask_datadog.monitor import monitor_route
from flask_datadog.shared.ddog_constants import \
        MonitorSpec, \
        MonitorType, \
        MonitorThresholdType


def add_endpoints(flask_app, jinja_env):

    @monitor_route()
    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render(), http.HTTPStatus.OK

    @monitor_route(
        monitors={
            MonitorType.APM_ERROR_RATE_THRESHOLD: {
                MonitorThresholdType.CRITICAL_THRESHOLD: 0.8,
                MonitorThresholdType.CRITICAL_RECOVERY: 0.7,
                MonitorThresholdType.WARNING_THRESHOLD: 0.5,
                MonitorThresholdType.WARNING_RECOVERY: 0.4,
                MonitorSpec.ALERT_PERIOD: '10m',
            },
        },
    )
    @flask_app.route('/error', methods=['GET'])
    def get_date():
        response_code = flask.request.args.get('resp')
        if not response_code:
            response_code = http.HTTPStatus.OK

        return json.dumps({
            'date':  str(datetime.datetime.now().date()),
            'response_code': response_code,
        }, indent=2), int(response_code)

    @monitor_route()
    @flask_app.route('/latency', methods=['GET'])
    def get_health_baby():
        sleep_sec = int(flask.request.args.get('sleep'))
        if sleep_sec:
            time.sleep(sleep_sec)
        else:
            sleep_sec = 0

        return json.dumps({'status': 'ok', 'slept': sleep_sec}), http.HTTPStatus.OK
