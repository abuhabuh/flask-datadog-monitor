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

    endpoint: str = fe.get_endpoint()
    methods: list[str] = fe.get_methods()
    monitor_specs: dict = fe.get_specs()

    print(f'*** mon from fe - {endpoint}: {monitor_specs}')

    route_tagger.validate_tag(monitor_specs)

    # TODO: only doing 1 method right now
    method: str = methods[0]
    monitors = []
    for mon_type, mon_spec in monitor_specs.items():
        monitors.append(DatadogMonitor(
            monitor_type=ddog_constants.MonitorType(mon_type),
            endpoint_path=endpoint,
            method=method,
            data_period='10m',
            ))

    return monitors

