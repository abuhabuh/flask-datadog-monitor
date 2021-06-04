"""Flask App for integration tests
"""
import flask

from flask_datadog.monitor import monitor_route
from flask_datadog.shared.ddog_constants import \
        MonitorSpec, \
        MonitorType, \
        MonitorThresholdType


flask_app = flask.Flask(__name__)


@flask_app.route('/null_case', methods=['GET'])
def null_case():
    """Route is not marked for monitoring so should not be included in output"""
    return 0


@monitor_route(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorThresholdType.CRITICAL_THRESHOLD: 0.8,
            MonitorThresholdType.CRITICAL_RECOVERY: 0.7,
            MonitorThresholdType.WARNING_THRESHOLD: 0.5,
            MonitorThresholdType.WARNING_RECOVERY: 0.3,
            MonitorSpec.ALERT_PERIOD: '10m',
            MonitorSpec.MSG: f"""
                /base_test error threshold of 0.8 reached
            """,
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


@monitor_route(
    monitors={
        MonitorType.APM_ERROR_RATE_ANOMALY: {
            MonitorThresholdType.CRITICAL_THRESHOLD: 0.3,
            MonitorSpec.ANOMALY_DEVIATION_DIR: 'both',
            MonitorSpec.ANOMALY_NUM_DEVIATIONS: 2,
            MonitorSpec.ANOMALY_ROLLUP_INTERVAL_SEC: 120,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/apm_error_rate_anomaly', methods=['GET'])
def apm_error_rate_anomaly_route():
    """Test route. Return value is unused"""
    return 0


"""
# Method specific configs should override overarching configs
PUT_SPECIFIC: {
    MonitorThresholdType.CRITICAL_THRESHOLD: 0.7,
    MonitorSpec.ALERT_PERIOD: '5m',
},
# Should be able to combine methods into a single monitor
COMBINE_METHODS: ['GET', 'POST'],
"""
@monitor_route(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorThresholdType.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/multiple_methods', methods=['GET', 'PUT', 'POST', 'PATCH'])
def multiple_methods():
    """Test route. Return value is unused"""
    return 0

