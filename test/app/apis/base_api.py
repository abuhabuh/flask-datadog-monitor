"""Monitors are auto-gen'd for these API endpoints and sync'd to DataDog
"""
import datetime
import http
import json
import time

import flask

from flask_datadog.monitor import datadog_monitors
from flask_datadog.shared.datadog_constants import \
        MonitorType, \
        MonitorSpec


def add_endpoints(flask_app, jinja_env):

    @datadog_monitors()
    @flask_app.route('/', methods=['GET'])
    def get_root():
        return jinja_env.get_template('index.html').render(), http.HTTPStatus.OK

    @datadog_monitors(
        monitors={
            MonitorType.APM_ERROR_RATE_THRESHOLD: {
                MonitorSpec.CRITICAL_THRESHOLD: 0.8,
                MonitorSpec.CRITICAL_RECOVERY_THRESHOLD: 0.7,
                MonitorSpec.WARNING_THRESHOLD: 0.5,
                MonitorSpec.WARNING_RECOVERY_THRESHOLD: 0.4,
                MonitorSpec.ALERT_PERIOD: '10m',
            },
            MonitorType.APM_ERROR_RATE_ANOMALY: {
                MonitorSpec.CRITICAL_THRESHOLD: 0.7,
                MonitorSpec.ANOMALY_DEVIATION_DIR: 'above',
                MonitorSpec.ANOMALY_NUM_DEVIATIONS: 1,
                MonitorSpec.ANOMALY_ROLLUP_INTERVAL_SEC: 120,
                MonitorSpec.ALERT_PERIOD: '10m',
            },
        },
    )
    @flask_app.route('/base-test', methods=['GET'])
    def get_error():
        response_code = flask.request.args.get('resp')
        if not response_code:
            response_code = http.HTTPStatus.OK

        try:
            sleep_sec = int(flask.request.args.get('sleep', ''))
            time.sleep(sleep_sec)
        except ValueError:
            sleep_sec = 0

        return json.dumps({
            'date':  str(datetime.datetime.now().date()),
            'response_code': response_code,
            'slept': sleep_sec,
        }, indent=2), int(response_code)
