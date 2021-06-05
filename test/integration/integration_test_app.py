"""Flask App for integration tests
"""
import flask

from flask_datadog.monitor import datadog_monitors
from flask_datadog.shared.ddog_constants import \
        MonitorType, \
        MonitorSpec


flask_app = flask.Flask(__name__)


@flask_app.route('/null_case', methods=['GET'])
def null_case():
    """Route is not marked for monitoring so should not be included in output"""
    return 0


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.CRITICAL_RECOVERY_THRESHOLD: 0.7,
            MonitorSpec.WARNING_THRESHOLD: 0.5,
            MonitorSpec.WARNING_RECOVERY_THRESHOLD: 0.3,
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


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
        MonitorType.APM_LATENCY_THRESHOLD: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.7,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/two-specs', methods=['GET'])
def two_specs():
    """Test tag with more than one specification.
    """
    return 0


@datadog_monitors()
@flask_app.route('/base_test_all_monitors', methods=['GET'])
def base_test_all_monitors():
    """Test route. Return value is unused"""
    return 0


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_ANOMALY: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.3,
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


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/multiple_methods', methods=['GET', 'PUT', 'POST', 'PATCH'])
def multiple_methods():
    """Test route with multiple methods.

    Monitors for all methods should be generated.
    """
    return 0


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorSpec.METHODS: ['GET'],
            MonitorSpec.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/multiple_methods_get_only', methods=['GET', 'PUT', 'POST', 'PATCH'])
def multiple_methods_get_only():
    """Test multiple methods route with single method spec'd.

    Only GET monitor should be generated
    """
    return 0


@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_ANOMALY: {},
        MonitorType.APM_ERROR_RATE_THRESHOLD: {},
        MonitorType.APM_LATENCY_THRESHOLD: {},
    }
)
@flask_app.route('/name_only_spec', methods=['GET'])
def name_only_spec():
    """Test specifying names of monitors only.

    Specifying only the names of the monitors should get you the monitors you
    want.
    """
    return 0
