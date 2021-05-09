"""Represents a DataDog Monitor
"""
import enum


class MonitorType(enum.Enum):
    ERROR_RATE = 1


class DatadogMonitor:

    def __init__(
            self,
            endpoint_path: str,
            method: str,
            monitor_type: MonitorType,
            data_period: str,
    ):
        self.endpoint_path = endpoint_path
        self.method = method
        self.monitor_type = monitor_type
        self.data_period = data_period

    @property
    def name(self) -> str:
        cleaned_endpoint_path: str = self.endpoint_path.replace('/', '_')
        return f'{self.method}_{cleaned_endpoint_path}-{self.monitor_type.name}'

