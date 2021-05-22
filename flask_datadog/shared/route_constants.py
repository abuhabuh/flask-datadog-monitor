"""Shared constants shared between functionalies (e.g., generator, route tagger)
"""
from flask_datadog.shared import ddog_constants


ROUTE_INFO_KEY = '__flask_ddog_route_info__'


ROUTE_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        ddog_constants.MonitorType.ERROR_RATE_MONITOR: {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                ddog_constants.ThresholdType.CRITICAL_THRESHOLD: {
                    'type': 'number',
                },
                ddog_constants.ThresholdType.CRITICAL_RECOVERY: {
                    'type': 'number',
                },
                ddog_constants.ThresholdType.WARNING_THRESHOLD: {
                    'type': 'number',
                },
                ddog_constants.ThresholdType.WARNING_RECOVERY: {
                    'type': 'number',
                },
            }
        },
    },
}

