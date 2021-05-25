"""Module for generating Terraform monitor specifications
"""
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape

from flask_datadog.generator import datadog_monitor_generator
from flask_datadog.generator.datadog_monitor import AlertThresholds, DatadogMonitor
from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.shared import ddog_constants


jinja_env = Environment(
    loader=FileSystemLoader(
        str(pathlib.Path(__file__).parent.absolute()) + '/../templates',
    ),
    autoescape=select_autoescape(['html', 'xml'])
)


class TFSpecGeneratorException(Exception):
    pass


def get_tf_fname(tf_file_prefix: str, endpoint: str) -> str:
    return f'{tf_file_prefix}-{endpoint}.tf'


def get_tf_contents_from_flask_endpoint(
        fe: FlaskEndpoint,
        service_env: str,
        service_name: str,
        ) -> str:
    """Generate Terraform file contents for monitors for endpoint

    Terraform file includes specifications for all monitors for the endpoint
    provided.
    """
    monitors: list[DatadogMonitor] = \
        datadog_monitor_generator.monitors_from_flask_endpoint(fe)

    tf_file_str = ''
    for mon in monitors:
        tf_spec: str = _get_monitor_spec(
                mon, service_env, service_name)
        tf_file_str += tf_spec + '\n\n\n'

    return tf_file_str


def _get_monitor_spec(monitor: DatadogMonitor, env: str, service_name: str) -> str:
    """Generate a terraform spec for a particular monitor
    """
    service_monitor_name: str = _get_service_monitor_name(service_name, monitor)
    at: AlertThresholds = monitor.get_alert_thresholds()

    query_str: str = _get_tf_query(
            monitor_type=monitor.monitor_type,
            env=env,
            service_name=service_name,
            endpoint_path=monitor.endpoint_path,
            method=monitor.method,
            alert_period=monitor.alert_period,
            threshold=at.critical_threshold,
    )

    spec_str: str = jinja_env.get_template('datadog_monitor.tmpl').render(
        service_name=service_name,
        env=env,
        resource_name=monitor.resource_name,
        monitor_name=service_monitor_name,
        monitor_name_pretty=service_monitor_name,
        terraform_monitor_type=monitor.terraform_monitor_type,
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
    return f'AUTOGEN_{service_name}_{monitor.name}'


def _get_tf_query(
        monitor_type: ddog_constants.MonitorType,
        env: str,
        service_name: str,
        endpoint_path: str,
        method: str,
        alert_period: str,
        threshold: float,
) -> str:
    """
    :param alert_period: e.g. '15m' for "15 minutes"
    """
    method = method.lower()
    resource_name: str = f'{method}_{endpoint_path}'
    if monitor_type == ddog_constants.MonitorType.APM_ERROR_RATE_THRESHOLD:
        return f"""
            sum(last_{alert_period}): (
               sum:trace.flask.request.errors{{
                   env:{env},
                   service:{service_name},
                   resource_name:{resource_name}
               }}.as_count()
               /
               sum:trace.flask.request.hits{{
                   env:{env},
                   service:{service_name},
                   resource_name:{resource_name}
               }}.as_count()
            ) > {threshold}
        """.replace(' ', '').replace('\n', '')

    if monitor_type == ddog_constants.MonitorType.APM_LATENCY_THRESHOLD:
        return f"""
            avg(last_{alert_period}):avg:trace.flask.request{{
                env:{env},
                service:{service_name},
                resource_name:{resource_name}
            }} > {threshold}
        """.replace(' ', '').replace('\n', '')

    raise TFSpecGeneratorException(f'Monitor type ({monitor_type}) not supported.')
