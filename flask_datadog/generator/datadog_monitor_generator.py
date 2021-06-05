"""DataDog monitor generator logic
"""

from flask_datadog.generator.datadog_monitor import DatadogMonitor
from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.monitor import route_tagger
from flask_datadog.shared import datadog_constants


def monitors_from_flask_endpoint(
        fe: FlaskEndpoint,
) -> list[DatadogMonitor]:
    """Generate a list of DatadogMonitor objects for a single flask endpoint.
    """
    default_mon_types: list[datadog_constants.MonitorType] = [
        datadog_constants.MonitorType.APM_ERROR_RATE_THRESHOLD,
        datadog_constants.MonitorType.APM_LATENCY_THRESHOLD,
    ]

    endpoint: str = fe.get_endpoint()
    monitor_specs: dict = fe.get_specs()

    route_tagger.validate_tag(monitor_specs)

    # Generate monitors for endpoint
    monitors = []
    if monitor_specs.get(datadog_constants.TAG_KEY_DEFAULT_MONITORS, None):
        # If generating all default monitors, add all monitors in default list
        # for each method
        for mon_type in default_mon_types:
            for method in _get_methods(fe.get_methods()):
                monitors.append(
                    DatadogMonitor(
                        monitor_type=mon_type,
                        endpoint_path=endpoint,
                        method=method,
                        mon_spec=dict(),
                    )
                )
    else:
        monitor_map: dict = monitor_specs.get(datadog_constants.TAG_KEY_MONITORS, {})
        for mon_type, mon_spec in monitor_map.items():

            for method in _get_methods(
                fe.get_methods(),
                mon_spec.get(datadog_constants.MonitorSpec.METHODS, []),
            ):
                monitors.append(DatadogMonitor(
                    monitor_type=datadog_constants.MonitorType(mon_type),
                    endpoint_path=endpoint,
                    method=method,
                    mon_spec=mon_spec,
                    ))

    return monitors


def _get_methods(fe_methods: list[str], custom_methods: list[str] = None) -> list[str]:
    """Return http methods derived from flask end point and monitor specs.

    A flask endpoint has methods bound to it during endpoint definitions.
    Monitor specs also could have methods specified to override default
    methods spec'd by the flask endpoint. Monitor specs have methods specified
    when the use only wants monitors generated for a certain set of methods on
    the flask endpoint.

    :param fe_methods: list of methods bound to the flask endpoint
    :param custom_methods: list of custom methods specified in monitor spec
    """
    if not fe_methods:
        return []
    if not custom_methods:
        custom_methods = []

    fe_methods_set: set[str] = {s.lower() for s in fe_methods}
    custom_methods_set: set[str] = {s.lower() for s in custom_methods}

    methods_set: set = fe_methods_set
    if custom_methods:
        methods_set = custom_methods_set.intersection(fe_methods_set)

    return sorted(list(methods_set))
