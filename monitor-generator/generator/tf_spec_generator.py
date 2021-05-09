"""Module for generating Terraform monitor specifications
"""
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape

from datadog_monitor import AlertThresholds, DatadogMonitor

jinja_env = Environment(
    loader=FileSystemLoader(
        str(pathlib.Path(__file__).parent.absolute()) + '/../templates',
    ),
    autoescape=select_autoescape(['html', 'xml'])
)


def get_tf_spec(monitor: DatadogMonitor, env: str, service_name: str) -> str:

    at: AlertThresholds = monitor.get_alert_threholds()

    query_str: str = _get_tf_query(
            env=env,
            service_name=service_name,
            endpoint_path=monitor.endpoint_path,
            method=monitor.method,
            data_period=monitor.data_period,
            threshold=at.critical_threshold,
    )

    service_monitor_name: str = _get_service_monitor_name(service_name, monitor)

    spec_str: str = jinja_env.get_template('datadog_monitor.tmpl').render(
        service_name=service_name,
        env=env,
        resource_name=monitor.resource_name,
        monitor_name=service_monitor_name,
        monitor_name_pretty=service_monitor_name,
        msg='',
        escalation_msg='',
        monitor_query=query_str,
        critical_threshold=at.critical_threshold,
        critical_recovery=at.critical_recovery,
        warning_threshold=at.warning_threshold,
        warning_recovery=at.warning_recovery,
    )

    return spec_str


def _get_service_monitor_name(service_name: str, monitor: DatadogMonitor) -> str:
    return f'{service_name}-{monitor.name}'


def _get_tf_query(
        env: str,
        service_name: str,
        endpoint_path: str,
        method: str,
        data_period: str,
        threshold: str,
):
    """
    :param data_period: e.g. '15m' for "15 minutes"
    """
    return f"""
            sum(last_{data_period}): (
               sum:trace.flask.request.errors{{
                   env:{env},
                   service:{service_name},
                   resource_name:{method}_{endpoint_path}
               }}.as_count()
               /
               sum:trace.flask.request.hits{{
                   env:{env},
                   service:{service_name},
                   resource_name:{method}_{endpoint_path}
               }}.as_count()
            ) > {threshold}
        """.replace(' ', '').replace('\n', '')

