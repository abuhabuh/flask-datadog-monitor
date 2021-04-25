import importlib
import os
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader(
        'templates'
    ),
    autoescape=select_autoescape(['html', 'xml'])
)


def _flask_app_from_location(module_name: str):
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
    app_location: str = sys.argv[1]

    flask_app = _flask_app_from_location(app_location)

    endpoint = ''
    methods = []
    endpoints_info = {}
    for r in flask_app.url_map.iter_rules():
        endpoints_info[r.rule] = {
            'methods': r.methods,
        }

        endpoint = r.rule
        methods = r.methods

    print(endpoint)
    print(methods)
    print(jinja_env.get_template('datadog_monitor.tmpl').render(
        monitor_name='foo',
        monitor_name_pretty='foo me once',
        msg='asdfafd',
        escalation_msg='escalate_asdfasdf',
        monitor_query='select *',
    ))


if __name__ == '__main__':
    main()

