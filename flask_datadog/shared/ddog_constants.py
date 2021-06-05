"""Shared constants for DataDog domain
"""
import enum


class MonitorType(enum.Enum):
    """Different monitor types supported.

    Value of enums are used in generating terraform specs and should be kept constant if possible.
    """
    # Thresholds
    APM_ERROR_RATE_THRESHOLD = 'APM_ERROR_RATE_THRESHOLD'
    APM_LATENCY_THRESHOLD = 'APM_LATENCY_THRESHOLD'
    # Anomalies
    APM_ERROR_RATE_ANOMALY = 'APM_ERROR_RATE_ANOMALY'

    @staticmethod
    def anomaly_monitors() -> list['MonitorType']:
        return [
            MonitorType.APM_ERROR_RATE_ANOMALY,
        ]


class MonitorThresholdType(enum.Enum):
    CRITICAL_THRESHOLD = 1
    CRITICAL_RECOVERY = 2
    WARNING_THRESHOLD = 3
    WARNING_RECOVERY = 4


class MonitorSpec(enum.Enum):
    ALERT_PERIOD = 1
    MSG = 2
    METHODS = 3

    ANOMALY_DEVIATION_DIR = 100
    ANOMALY_NUM_DEVIATIONS = 101
    ANOMALY_ROLLUP_INTERVAL_SEC = 102


TAG_KEY_DEFAULT_MONITORS = 'default_monitors'
TAG_KEY_MONITORS = 'monitors'


DDOG_MONITOR_SCHEMA = {
    # Base monitor specifications that are common to all monitors
    'definitions': {
        'base_monitor_properties': {
            'type': 'object',
            # additionalProperties has to be True because we are combining
            # base schema with other attributes
            'additionalProperties': True,
            'properties': {
                MonitorThresholdType.CRITICAL_THRESHOLD: {
                    'type': 'number',
                },
                MonitorThresholdType.CRITICAL_RECOVERY: {
                    'type': 'number',
                },
                MonitorThresholdType.WARNING_THRESHOLD: {
                    'type': 'number',
                },
                MonitorThresholdType.WARNING_RECOVERY: {
                    'type': 'number',
                },
                MonitorSpec.ALERT_PERIOD: {
                    'type': 'string',
                },
                MonitorSpec.MSG: {
                    'type': 'string',
                },
            },
        }
    },

    # Actual schema definitions
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        TAG_KEY_DEFAULT_MONITORS: {
            'type': 'boolean',
            'enum': [True]
        },
        TAG_KEY_MONITORS: {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                MonitorType.APM_ERROR_RATE_THRESHOLD: {
                    'allOf': [
                        {
                            '$ref': '#/definitions/base_monitor_properties',
                        },
                        {},
                    ],
                },
                MonitorType.APM_ERROR_RATE_ANOMALY: {
                    'allOf': [
                        {
                            '$ref': '#/definitions/base_monitor_properties',
                        },
                        {
                            'type': 'object',
                            'properties': {
                                MonitorSpec.ANOMALY_DEVIATION_DIR: {
                                    'type': 'string',
                                    'enum': [ 'below', 'above', 'both', ],
                                },
                                MonitorSpec.ANOMALY_NUM_DEVIATIONS: {
                                    'type': 'number',
                                },
                                MonitorSpec.ANOMALY_ROLLUP_INTERVAL_SEC: {
                                    'type': 'number',
                                },
                            },
                        },
                    ],
                },
            },
        },
    },
}

