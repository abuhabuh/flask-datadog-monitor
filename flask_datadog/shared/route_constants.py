"""Shared constants shared between functionalies (e.g., generator, route tagger)
"""
import enum


class MonitorType(enum.Enum):
    ERROR_RATE_MONITOR = 1


class ThresholdTypes(enum.Enum):
    CRITICAL_THRESHOLD = 1
    CRITICAL_RECOVERY = 2
    WARNING_THRESHOLD = 3
    WARNING_RECOVERY = 4


ROUTE_INFO_KEY = '__flask_ddog_route_info__'


ROUTE_SCHEMA = {
    'type': 'object',
    'properties': {
        MonitorType.ERROR_RATE_MONITOR.name: {
            'type': 'object',
            'properties': {
                ThresholdTypes.CRITICAL_THRESHOLD.name: {
                    'type': 'number',
                },
                ThresholdTypes.CRITICAL_RECOVERY.name: {
                    'type': 'number',
                },
                ThresholdTypes.WARNING_THRESHOLD.name: {
                    'type': 'number',
                },
                ThresholdTypes.WARNING_RECOVERY.name: {
                    'type': 'number',
                },
            }
        },
    },
}

