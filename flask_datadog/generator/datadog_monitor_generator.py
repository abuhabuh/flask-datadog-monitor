"""DataDog monitor generator logic
"""

from flask_datadog.generator.datadog_monitor import DatadogMonitor
from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.monitor import route_tagger
from flask_datadog.shared import ddog_constants


def monitors_from_flask_endpoint(
        fe: FlaskEndpoint,
) -> list[DatadogMonitor]:
    """Generate a list of DatadogMonitor objects for a single flask endpoint.
    """
    default_mon_types: list[ddog_constants.MonitorType] = [
        ddog_constants.MonitorType.APM_ERROR_RATE_THRESHOLD,
        ddog_constants.MonitorType.APM_LATENCY_THRESHOLD,
        # TODO: Anomaly not finished
        ddog_constants.MonitorType.APM_ERROR_RATE_ANOMALY,
    ]

    endpoint: str = fe.get_endpoint()
    methods: list[str] = fe.get_methods()
    monitor_specs: dict = fe.get_specs()

    route_tagger.validate_tag(monitor_specs)

    # Generate monitors for endpoint
    monitors = []
    method: str = methods[0]
    if monitor_specs.get(ddog_constants.TAG_KEY_DEFAULT_MONITORS, None):
        # If generating all default monitors, add all monitors in default list
        for mon_type in default_mon_types:
            monitors.append(
                DatadogMonitor(
                    monitor_type=mon_type,
                    endpoint_path=endpoint,
                    method=method,
                    mon_spec=dict(),
                )
            )
    else:
        monitor_map: dict = monitor_specs.get(ddog_constants.TAG_KEY_MONITORS, {})
        for mon_type, mon_spec in monitor_map.items():
            monitors.append(DatadogMonitor(
                monitor_type=ddog_constants.MonitorType(mon_type),
                endpoint_path=endpoint,
                method=method,
                mon_spec=mon_spec,
                ))

    return monitors

