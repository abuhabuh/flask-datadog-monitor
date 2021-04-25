import importlib
import sys


def _flask_app_from_module(module_name: str):
    return importlib.import_module(module_name).app


def main():
    module_name = sys.argv[1]
    flask_app = _flask_app_from_module(module_name)

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


if __name__ == '__main__':
    main()

