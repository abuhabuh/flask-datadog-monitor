"""Module for logic related to parsing Flask endpoints
"""
import flask
import werkzeug


def parse_endpoints(flask_app: flask.app.Flask):

    endpoints_info = {}
    for r in flask_app.url_map.iter_rules():
        if _is_default_endpoint(r):
            continue
        endpoints_info[r.rule] = {
            'methods': list(r.methods),
        }

    return endpoints_info


def _is_default_endpoint(endpoint_rule: werkzeug.routing.Rule):
    if endpoint_rule.rule == '/static/<path:filename>':
        return True
    return False

