"""Module for logic related to parsing Flask endpoints
"""
import flask
import werkzeug

from flask_endpoint import FlaskEndpoint


def parse_endpoints(flask_app: flask.app.Flask) -> list[FlaskEndpoint]:

    fe_list = []
    for r in flask_app.url_map.iter_rules():
        if _is_default_endpoint(r):
            continue
        fe_list.append(FlaskEndpoint(
            rule=r
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

