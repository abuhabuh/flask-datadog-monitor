"""Represents a DataDog Monitor
"""
from dataclasses import dataclass, field
from typing import Optional
import enum


class MonitorType(enum.Enum):
    ERROR_RATE = 1


@dataclass(frozen=True)
class AlertThresholds:
    critical_threshold: Optional[float] = None
    critical_recovery: Optional[float] = None
    warning_threshold: Optional[float] = None
    warning_recovery: Optional[float] = None


@dataclass(frozen=True)
class DatadogMonitor:

    endpoint_path: str
    method: str
    monitor_type: MonitorType
    data_period: str
    alert_threholds: Optional[AlertThresholds] = None

    @property
    def name(self) -> str:
        cleaned_endpoint_path: str = self.endpoint_path.replace('/', '_')
        return f'{self.method}_{cleaned_endpoint_path}-{self.monitor_type.name}'

    @property
    def resource_name(self) -> str:
        """Datadog format resource name.

        Used for tagging a monitor.
        """
        return f'{self.method}_{self.endpoint_path}'.lower()

    def get_alert_threholds(self) -> AlertThresholds:
        if self.alert_threholds:
            return self.alert_threholds
        return _make_default_threholds(self.monitor_type)


def _make_default_threholds(monitor_type: MonitorType) -> AlertThresholds:
    """Default alert thresholds for different monitor types
    """
    at = AlertThresholds()
    if monitor_type == MonitorType.ERROR_RATE:
        # Default error rate
        # - critical if above 10%
        # - warn if above 5%
        at = AlertThresholds(
            critical_threshold=0.10,
            critical_recovery=None,
            warning_threshold=0.05,
            warning_recovery=None,
        )
    return at

