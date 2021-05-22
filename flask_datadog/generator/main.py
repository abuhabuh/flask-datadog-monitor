"""Main executable for generating DataDog monitors from flask endpoints
"""
import importlib
import json
import os
import sys

# TODO: flask is an important dependency -- need to test how this works with
# different versions of flask
import flask

from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.generator.datadog_monitor import DatadogMonitor
from flask_datadog.generator import datadog_monitor_generator
from flask_datadog.generator import endpoint_util
from flask_datadog.generator import flask_endpoint_parser
from flask_datadog.generator import tf_spec_generator


def _flask_app_from_location(module_name: str) -> flask.app.Flask:
    """
    :param module_name: String specifying path and module name as well as
      actual flask app attribute. e.g., /path/to/module:flask_app
    """
    module_and_app_name: str = (module_name.split('/')[-1])
    module_file: str = module_and_app_name.split(':')[0]
    flask_app_obj: str = module_and_app_name.split(':')[1]

    path = '/'.join(module_name.split('/')[0:-1])
    sys.path.append(path)

    flask_app_module = importlib.import_module(module_file)

    return getattr(flask_app_module, flask_app_obj)


def _gen_and_monitors(
        fe_list: list[FlaskEndpoint],
        ) -> dict[str, list[DatadogMonitor]]:

    print(f'Endpoints: {[str(x) for x in fe_list]}')
    return {
            endpoint_util.clean_endpoint_for_naming(fe.get_endpoint()):
                datadog_monitor_generator.monitors_from_flask_endpoint(fe)
                    for fe in fe_list}


def _write_tf_output(
        output_dir: str,
        tf_file_prefix: str,
        endpoint_to_monitors: dict[str, list[DatadogMonitor]],
        service_name: str,
        service_env: str,
        ):
    for endpoint, monitors in endpoint_to_monitors.items():
        if not monitors:
            continue

        monitor: DatadogMonitor = monitors[0]

        tf_spec: str = tf_spec_generator.get_tf_spec(monitor, service_env, service_name)

        output_file: str = _get_output_file_name(tf_file_prefix, output_dir, endpoint)
        with open(output_file, 'w') as fp:
            fp.write(tf_spec)

        print(f'wrote output to {output_file}')


def _get_output_file_name(prefix: str, output_dir: str, endpoint: str) -> str:
    if output_dir.endswith('/'):
        output_dir = output_dir[:-1]

    return f'{output_dir}/{prefix}-{endpoint}.tf'


def main():
    app_location: str = sys.argv[1]
    output_dir: str = sys.argv[2]
    tf_file_prefix: str = sys.argv[3]

    service_name = os.environ['DD_MONITOR_GEN_SERVICE']
    service_env = os.environ['DD_MONITOR_GEN_SERVICE_ENV']

    flask_app: flask.app.Flask = _flask_app_from_location(app_location)

    fe_list: list[FlaskEndpoint] = flask_endpoint_parser.parse_endpoints(
        flask_app,
    )

    endpoint_to_monitors: dict[str, list[DatadogMonitor]] = \
            _gen_and_monitors(fe_list)

    _write_tf_output(
            output_dir,
            tf_file_prefix,
            endpoint_to_monitors,
            service_name,
            service_env,
            )


if __name__ == '__main__':
    main()

