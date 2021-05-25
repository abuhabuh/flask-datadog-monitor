"""Shared constants for DataDog domain
"""
import enum


class MonitorSpec(enum.Enum):
    ALERT_PERIOD = 1


class MonitorType(enum.Enum):
    """Different monitor types supported.

    Value of enums are used in generating terraform specs and should be kept constant if possible.
    """
    APM_ERROR_RATE_THRESHOLD = 'APM_ERROR_RATE_THRESHOLD'
    APM_LATENCY_THRESHOLD = 'APM_LATENCY_THRESHOLD'

    APM_ERROR_RATE_ANOMALY = 'APM_ERROR_RATE_ANOMALY'


class ThresholdType(enum.Enum):
    CRITICAL_THRESHOLD = 1
    CRITICAL_RECOVERY = 2
    WARNING_THRESHOLD = 3
    WARNING_RECOVERY = 4


TAG_KEY_DEFAULT_MONITORS = 'default_monitors'
TAG_KEY_MONITORS = 'monitors'


DDOG_MONITOR_SCHEMA = {
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
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        ThresholdType.CRITICAL_THRESHOLD: {
                            'type': 'number',
                        },
                        ThresholdType.CRITICAL_RECOVERY: {
                            'type': 'number',
                        },
                        ThresholdType.WARNING_THRESHOLD: {
                            'type': 'number',
                        },
                        ThresholdType.WARNING_RECOVERY: {
                            'type': 'number',
                        },
                        MonitorSpec.ALERT_PERIOD: {
                            'type': 'string',
                        },
                    },
                },
            },
        },
    },
}

