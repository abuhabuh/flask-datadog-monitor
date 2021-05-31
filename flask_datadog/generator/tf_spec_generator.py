"""Module for generating Terraform monitor specifications
"""
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape

from flask_datadog.generator import datadog_monitor_generator
from flask_datadog.generator.datadog_monitor import AlertThresholds, DatadogMonitor
from flask_datadog.generator.flask_endpoint import FlaskEndpoint


jinja_env = Environment(
    loader=FileSystemLoader(
        str(pathlib.Path(__file__).parent.absolute()) + '/../templates',
    ),
    autoescape=select_autoescape(['html', 'xml'])
)


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

    spec_str: str = jinja_env.get_template('datadog_monitor.tmpl').render(
        service_name=service_name,
        env=env,
        resource_name=monitor.resource_name,
        monitor_name=service_monitor_name,
        monitor_name_pretty=service_monitor_name,
        terraform_monitor_type=monitor.terraform_monitor_type,
        msg='',
        escalation_msg='',
        monitor_query=monitor.get_query_str(env, service_name),
        critical_threshold=at.critical_threshold,
        critical_recovery=at.critical_recovery,
        warning_threshold=at.warning_threshold,
        warning_recovery=at.warning_recovery,
    )

    return spec_str


def _get_service_monitor_name(service_name: str, monitor: DatadogMonitor) -> str:
    return f'AUTOGEN_{service_name}_{monitor.name}'
