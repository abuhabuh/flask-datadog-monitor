"""Main executable for generating DataDog monitors from flask endpoints
"""
import importlib
import json
import os
import sys

import flask

from flask_endpoint import FlaskEndpoint
from datadog_monitor import DatadogMonitor
import datadog_monitor_generator
import flask_endpoint_parser
import tf_spec_generator


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


def _gen_and_write_monitors(output_file: str, fe_list: list[FlaskEndpoint]):
    print([str(x) for x in fe_list])

    fe = fe_list[0]
    monitors: list = datadog_monitor_generator.monitors_from_flask_endpoint(fe)

    # todo: only looking at 1st monitor
    monitor: DatadogMonitor = monitors[0]

    env: str = 'prod'
    service_name: str = 'test_service'

    tf_spec: str = tf_spec_generator.get_tf_spec(monitor, env, service_name)
    print('**** tf spec ****')
    print(f'{tf_spec}')

#    with open(output_file, 'w') as fp:
#
#        out_str = jinja_env.get_template('datadog_monitor.tmpl').render(
#            monitor_name='foo',
#            monitor_name_pretty='foo me once',
#            msg='asdfafd',
#            escalation_msg='escalate_asdfasdf',
#            monitor_query='select *',
#        )
#
#        print(out_str)
#        fp.write(out_str)


def main():
    app_location: str = sys.argv[1]
    output_file: str = 'endpoints.tf'

    flask_app: flask.app.Flask = _flask_app_from_location(app_location)

    fe_list: list[FlaskEndpoint] = flask_endpoint_parser.parse_endpoints(
        flask_app,
    )

    _gen_and_write_monitors(output_file, fe_list)


if __name__ == '__main__':
    main()

