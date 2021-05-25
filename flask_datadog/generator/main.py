"""Main executable for generating DataDog monitors from flask endpoints
"""
import importlib
import logging
import os
import sys

# TODO: flask is an important dependency -- need to test how this works with
# different versions of flask
import flask

from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.generator import flask_endpoint_parser
from flask_datadog.generator import tf_spec_generator


logging.basicConfig(level=logging.DEBUG)


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


def main():
    logging.info(f'Started Terraform spec generation.')
    app_location: str = sys.argv[1]
    output_dir: str = sys.argv[2]
    tf_file_prefix: str = sys.argv[3]

    service_name = os.environ['DD_MONITOR_GEN_SERVICE']
    service_env = os.environ['DD_MONITOR_GEN_SERVICE_ENV']

    flask_app: flask.app.Flask = _flask_app_from_location(app_location)

    fe_list: list[FlaskEndpoint] = flask_endpoint_parser.parse_endpoints(
        flask_app,
    )

    for fe in fe_list:
        fname: str = tf_spec_generator.get_tf_fname(tf_file_prefix, fe.get_endpoint_fname())
        contents: str = tf_spec_generator.get_tf_contents_from_flask_endpoint(
                fe, service_env, service_name)
        with open(f'{output_dir}/{fname}', 'w') as fp:
            fp.write(contents)
        logging.info(f' > wrote output for {output_dir}/{fname}')


if __name__ == '__main__':
    main()
