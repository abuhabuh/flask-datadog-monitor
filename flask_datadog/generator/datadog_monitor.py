from dataclasses import dataclass
from typing import Optional

from flask_datadog.generator import endpoint_util
from flask_datadog.shared.ddog_constants import MonitorSpec, MonitorType, MonitorThresholdType


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
        """Return name of DataDog monitor name
        """
        cleaned_endpoint_path: str = endpoint_util.clean_endpoint_for_naming(
            self.endpoint_path,
        )
        # Use MonitorType.value because we can keep the enum value the same
        # while we we maintain flexibility to refactor the enum name in the code
        return f'{self.method}-{cleaned_endpoint_path}_{self.monitor_type.value}'

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
        if self.monitor_type in [
                MonitorType.APM_ERROR_RATE_THRESHOLD,
                MonitorType.APM_LATENCY_THRESHOLD,
                MonitorType.APM_ERROR_RATE_ANOMALY,
        ]:
            return 'query alert'
        raise DatadogMonitorFormatException(
            f'MonitorType [{self.monitor_type}] has no matching terraform monitor type string')

    def get_alert_thresholds(self) -> AlertThresholds:
        """Alert thresholds with defaults
        """
        critical_threshold: float = self.mon_spec.get(MonitorThresholdType.CRITICAL_THRESHOLD, None)
        critical_recovery: float = self.mon_spec.get(MonitorThresholdType.CRITICAL_RECOVERY, None)
        warning_threshold: float = self.mon_spec.get(MonitorThresholdType.WARNING_THRESHOLD, None)
        warning_recovery: float = self.mon_spec.get(MonitorThresholdType.WARNING_RECOVERY, None)

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


    def get_query_str(
        self,
        env: str,
        service_name: str,
    ) -> str:
        """
        :param env: alert env (e.g., 'staging', 'prod')
        :param service_name: name of service (e.g., 'authentication_service')
        """

        at: AlertThresholds = self.get_alert_thresholds()

        resource_name: str = f'{self.method.lower()}_{self.endpoint_path}'
        # flask_req_filter is the common filter to apply to flask request traces
        flask_req_filter: str = f"""
               env:{env},
               service:{service_name},
               resource_name:{resource_name}
            """
        if self.monitor_type == MonitorType.APM_ERROR_RATE_THRESHOLD:
            return f"""
                sum(last_{self.alert_period}): (
                   sum:trace.flask.request.errors{{
                       {flask_req_filter}
                   }}.as_count()
                   /
                   sum:trace.flask.request.hits{{
                       {flask_req_filter}
                   }}.as_count()
                ) > {at.critical_threshold}
            """.replace(' ', '').replace('\n', '')

        if self.monitor_type == MonitorType.APM_LATENCY_THRESHOLD:
            return f"""
                avg(last_{self.alert_period}):avg:trace.flask.request{{
                       {flask_req_filter}
                }} > {at.critical_threshold}
            """.replace(' ', '').replace('\n', '')

        if self.monitor_type == MonitorType.APM_ERROR_RATE_ANOMALY:
            # TODO: only basic supported for now -- other's are 'agile', 'robust'
            anomaly_algo = 'basic'
            anomaly_deviation_direction = 'both'  # TODO: config --> above, below, both
            anomaly_num_deviations = 2  # TODO: config
            anomaly_rollup_interval_sec = 120  # TODO: config
            # TODO: turn query period into a multiple of alert period
            return f"""
                avg(last_4h):anomalies(
                    avg:trace.flask.request{{ {flask_req_filter} }},
                    '{anomaly_algo}',
                    {anomaly_num_deviations},
                    direction='{anomaly_deviation_direction}',
                    alert_window='last_{self.alert_period}',
                    interval={anomaly_rollup_interval_sec},
                    count_default_zero='true'
                ) >= 1
            """

        raise DatadogMonitorFormatException(f'Monitor type ({self.monitor_type}) not supported.')
