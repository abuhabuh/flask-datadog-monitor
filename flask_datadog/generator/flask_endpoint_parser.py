"""Module for logic related to parsing Flask endpoints
"""
import flask
import werkzeug

from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.shared import route_tagger_constants


def parse_endpoints(flask_app: flask.app.Flask) -> list[FlaskEndpoint]:
    """Parse out relevant endpoints to monitor from a Flask app

    Endpoints that are not tagged are still processed. Their Terraform output
    will just be empty.
    """

    fe_list = []

    for r in flask_app.url_map.iter_rules():
        if _is_default_endpoint(r):
            continue
        # NOTE: flask_app.view_functions is a mapping of a route handler
        # function's name (r.endpoint) to the actual function
        specs: dict = \
                flask_app.view_functions[r.endpoint].__dict__.get(
                       route_tagger_constants.ROUTE_INFO_KEY, {})

        fe_list.append(FlaskEndpoint(
            rule=r,
            monitor_specs=specs,
        ))

    return fe_list


def _is_default_endpoint(endpoint_rule: werkzeug.routing.Rule) -> bool:
    """Eliminate Flask's default /static/* endpoint.

    Flask's default /static endpoint serves static data. Eliminate this by
    default.

    :param endpoint_rule: endpoint rule that has associated path
    """
    if endpoint_rule.rule == '/static/<path:filename>':
        return True
    return False

