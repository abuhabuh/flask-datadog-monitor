"""Flask App for integration tests
"""
import flask

from flask_datadog.monitor import monitor_route
from flask_datadog.shared.ddog_constants import \
        MonitorSpec, \
        MonitorType, \
        ThresholdType


flask_app = flask.Flask(__name__)


@monitor_route(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            ThresholdType.CRITICAL_THRESHOLD: 0.8,
            ThresholdType.CRITICAL_RECOVERY: 0.7,
            ThresholdType.WARNING_THRESHOLD: 0.5,
            ThresholdType.WARNING_RECOVERY: 0.3,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/base_test', methods=['GET'])
def base_test():
    """Test route. Return value is unused"""
    return 0


@monitor_route()
@flask_app.route('/base_test_all_monitors', methods=['GET'])
def base_test_all_monitors():
    """Test route. Return value is unused"""
    return 0


# @monitor_route(
#     monitors={
#         MonitorType.APM_ERROR_RATE_ANOMALY: {
#
#         },
#     },
# )
# @flask_app.route('/apm_error_rate_anomaly', methods=['GET'])
# def apm_error_rate_anomaly_route():
#     """Test route. Return value is unused"""
#     return 0
