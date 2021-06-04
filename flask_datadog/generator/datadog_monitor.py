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

    # endpoint_path example: /base_test
    endpoint_path: str
    # method example: GET
    method: str
    monitor_type: MonitorType
    # mon_spec: dictionary of monitor specifications
    mon_spec: dict

    DEFAULT_ALERT_PERIOD: str = '5m'
    # For anomaly monitors: mapping of rollup intervals for aggregation to the
    # avg() time period for the anomaly query
    ROLLUP_TO_AVG_TIME_MAP = {
        7600: '2w',
        3600: '1w',
        1800: '1w',
        600: '2d',
        300: '1d',
        120: '12h',
        60: '4h',
        20: '1h',
    }

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

    def get_alert_escalation_msg(self) -> str:
        """Return escalation message

        TODO: not sure where escalation msg is applicable
        """
        return 'Alert escalated'

    def get_alert_msg(self) -> str:
        """Return alert msg for monitor
        """
        if self.mon_spec.get(MonitorSpec.MSG, ''):
            return ' '.join(self.mon_spec[MonitorSpec.MSG].split())

        return f"""{self.monitor_type.value} triggered."""

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

    def get_anomaly_threshold_windows(self) -> dict[str, str]:
        """Return anomaly monitor threshold windows.

        Threshold windows match the alert_window.
        """
        if self.is_anomaly_monitor():
            return  {
                'recovery_window': f'last_{self.alert_period}',
                'trigger_window': f'last_{self.alert_period}',
            }
        return {}

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
            query = f"""
                sum(last_{self.alert_period}): (
                   sum:trace.flask.request.errors{{
                       {flask_req_filter}
                   }}.as_count()
                   /
                   sum:trace.flask.request.hits{{
                       {flask_req_filter}
                   }}.as_count()
                ) > {at.critical_threshold}
            """

        elif self.monitor_type == MonitorType.APM_LATENCY_THRESHOLD:
            query = f"""
                avg(last_{self.alert_period}):avg:trace.flask.request{{
                       {flask_req_filter}
                }} > {at.critical_threshold}
            """

        elif self.monitor_type == MonitorType.APM_ERROR_RATE_ANOMALY:
            # TODO: only basic supported for now -- other's are 'agile',
            #   'robust' and have more associated configs
            anomaly_algo = 'basic'
            anomaly_deviation_direction = self.mon_spec[MonitorSpec.ANOMALY_DEVIATION_DIR]
            anomaly_num_deviations = self.mon_spec[MonitorSpec.ANOMALY_NUM_DEVIATIONS]
            anomaly_rollup_interval_sec = self.mon_spec[MonitorSpec.ANOMALY_ROLLUP_INTERVAL_SEC]
            if anomaly_rollup_interval_sec not in DatadogMonitor.ROLLUP_TO_AVG_TIME_MAP:
                raise DatadogMonitorFormatException(f'Rollup interval ({anomaly_rollup_interval_sec}) not supported.')

            query = f"""
                avg(last_{DatadogMonitor.ROLLUP_TO_AVG_TIME_MAP[anomaly_rollup_interval_sec]}):anomalies(
                
                    sum:trace.flask.request.errors{{
                        {flask_req_filter}
                    }}.as_count()
                    /
                    sum:trace.flask.request.hits{{
                        {flask_req_filter}
                    }}.as_count(),
                    
                    '{anomaly_algo}',
                    {anomaly_num_deviations},
                    direction='{anomaly_deviation_direction}',
                    alert_window='last_{self.alert_period}',
                    interval={anomaly_rollup_interval_sec},
                    count_default_zero='true'
                ) >= {at.critical_threshold}
            """

        else:
            raise DatadogMonitorFormatException(f'Monitor type ({self.monitor_type}) not supported.')

        return ' '.join(query.split())

    def is_anomaly_monitor(self) -> bool:
        """Return whether or not this is an anomaly monitor
        """
        return self.monitor_type in MonitorType.anomaly_monitors()

    def is_default_monitor(self) -> bool:
        """A monitor is a default monitor if it has no specifications"""
        return len(self.mon_spec) == 0
