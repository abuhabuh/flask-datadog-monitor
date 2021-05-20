"""Represents a DataDog Monitor
"""
from dataclasses import dataclass, field
from typing import Optional

from flask_datadog.generator import endpoint_util
from flask_datadog.shared.route_constants import MonitorType


@dataclass(frozen=True)
class AlertThresholds:
    critical_threshold: float
    critical_recovery: Optional[float] = None
    warning_threshold: Optional[float] = None
    warning_recovery: Optional[float] = None


@dataclass(frozen=True)
class DatadogMonitor:

    endpoint_path: str
    method: str
    monitor_type: MonitorType
    data_period: str
    alert_thresholds: Optional[AlertThresholds] = None

    @property
    def name(self) -> str:
        cleaned_endpoint_path: str = endpoint_util.clean_endpoint_for_naming(
            self.endpoint_path,
        )
        return f'{self.method}_{cleaned_endpoint_path}-{self.monitor_type.name}'

    @property
    def resource_name(self) -> str:
        """Datadog format resource name.

        Used for tagging a monitor.
        """
        return f'{self.method}_{self.endpoint_path}'.lower()

    def get_alert_thresholds(self) -> AlertThresholds:
        if self.alert_thresholds:
            return self.alert_thresholds
        return _make_default_threholds(self.monitor_type)


def _make_default_threholds(monitor_type: MonitorType) -> AlertThresholds:
    """Default alert thresholds for different monitor types
    """
    if monitor_type == MonitorType.ERROR_RATE_MONITOR:
        # Default error rate
        # - critical if above 10%
        # - warn if above 5%
        return AlertThresholds(
            critical_threshold=0.10,
            critical_recovery=None,
            warning_threshold=0.05,
            warning_recovery=None,
        )

    raise Exception(f'No default threshold found for monitor type: {monitor_type}')

