"""Flask endpoint object
"""
import json

from werkzeug.routing import Rule

from flask_datadog.generator import endpoint_util


class FlaskEndpoint:

    def __init__(
            self,
            rule: Rule,
            monitor_specs: dict,
            ):
        self._rule = rule
        # Dictionary of monitor specifications as tagged via route_tagger
        self._monitor_specs = monitor_specs

    def get_endpoint(self) -> str:
        return self._rule.rule

    def get_endpoint_fname(self) -> str:
        """Convert endpoints like '/' and '/page/one' to 'root' and 'page_one'
        """
        return endpoint_util.clean_endpoint_for_naming(self.get_endpoint())

    def get_methods(self) -> list[str]:
        return list(_filter_methods(self._rule.methods))

    def get_specs(self) -> dict:
        """Return map of monitor types to their respective specifications.
        """
        return self._monitor_specs


def _filter_methods(methods: set) -> set:
    """Filter out HEAD and OPTIONS methods.

    Not instrumenting HEAD and OPTIONS methods by default.
    """
    return set(filter(
        lambda x: x not in {'HEAD', 'OPTIONS'},
        methods,
    ))

