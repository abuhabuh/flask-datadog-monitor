"""Shared constants for DataDog domain
"""
import enum


class MonitorSpec(enum.Enum):
    ALERT_PERIOD = 1


class MonitorType(enum.Enum):
    ERROR_RATE_MONITOR = 1


class ThresholdType(enum.Enum):
    CRITICAL_THRESHOLD = 1
    CRITICAL_RECOVERY = 2
    WARNING_THRESHOLD = 3
    WARNING_RECOVERY = 4


DDOG_MONITOR_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        MonitorType.ERROR_RATE_MONITOR: {
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
}

