from dataclasses import dataclass
from typing import Optional

from flask_datadog.generator import endpoint_util
from flask_datadog.shared.ddog_constants import MonitorSpec, MonitorType, ThresholdType


class DatadogMonitorFormatException(Exception):
    pass


@dataclass(frozen=True)
class AlertThresholds:
    critical_threshold: float
    critical_recovery: Optional[float] = None
    warning_threshold: Optional[float] = None
    warning_recovery: Optional[float] = None


@dataclass(frozen=True)
class DatadogMonitor:
    """Represents a DataDog Monitor"""

    endpoint_path: str
    method: str
    monitor_type: MonitorType
    mon_spec: dict

    DEFAULT_ALERT_PERIOD: str = '5m'

    @property
    def alert_period(self) -> str:
        if self.is_default_monitor():
            return DatadogMonitor.DEFAULT_ALERT_PERIOD
        if not MonitorSpec.ALERT_PERIOD in self.mon_spec:
            raise DatadogMonitorFormatException(f'{MonitorSpec.ALERT_PERIOD} required')
        return self.mon_spec[MonitorSpec.ALERT_PERIOD]

    @property
    def name(self) -> str:
        cleaned_endpoint_path: str = endpoint_util.clean_endpoint_for_naming(
            self.endpoint_path,
        )
        return f'{self.method}-{cleaned_endpoint_path}_{self.monitor_type.name}'

    @property
    def resource_name(self) -> str:
        """Datadog format resource name.

        Used for tagging a monitor.
        """
        return f'{self.method}_{self.endpoint_path}'.lower()

    @property
    def terraform_monitor_type(self) -> str:
        """Map the DataDog Monitor to the proper monitor type for Terraform specs.

        Different monitor types: https://docs.datadoghq.com/api/latest/monitors/#create-a-monitor
        """
        if self.monitor_type in [MonitorType.APM_ERROR_RATE_THRESHOLD, MonitorType.APM_LATENCY_THRESHOLD]:
            return 'query alert'
        raise DatadogMonitorFormatException(
            f'MonitorType [{self.monitor_type}] has no matching terraform monitor type string')

    def get_alert_thresholds(self) -> AlertThresholds:
        """Alert thresholds with defaults
        """
        critical_threshold: float = self.mon_spec.get(ThresholdType.CRITICAL_THRESHOLD, None)
        critical_recovery: float = self.mon_spec.get(ThresholdType.CRITICAL_RECOVERY, None)
        warning_threshold: float = self.mon_spec.get(ThresholdType.WARNING_THRESHOLD, None)
        warning_recovery: float = self.mon_spec.get(ThresholdType.WARNING_RECOVERY, None)

        if all(x is None for x in [
            critical_recovery,
            critical_threshold,
            warning_recovery,
            warning_threshold]
            ):
            critical_threshold = .1
            critical_recovery = .08
            warning_threshold = .05
            warning_recovery = .03

        return AlertThresholds(
            critical_threshold=critical_threshold,
            critical_recovery=critical_recovery,
            warning_threshold=warning_threshold,
            warning_recovery=warning_recovery,
        )

    def is_default_monitor(self):
        """A monitor is a default monitor if it has no specifications"""
        return len(self.mon_spec) == 0
