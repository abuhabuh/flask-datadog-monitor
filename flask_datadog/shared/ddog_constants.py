"""Shared constants for DataDog domain
"""
import enum


class MonitorType(enum.Enum):
    ERROR_RATE_MONITOR = 1


class ThresholdType(enum.Enum):
    CRITICAL_THRESHOLD = 1
    CRITICAL_RECOVERY = 2
    WARNING_THRESHOLD = 3
    WARNING_RECOVERY = 4

