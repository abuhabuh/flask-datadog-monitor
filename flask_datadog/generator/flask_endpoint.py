"""Flask endpoint object
"""
import json

import werkzeug


class FlaskEndpoint:

    def __init__(self, rule: werkzeug.routing.Rule):
        self._rule = rule

    def get_endpoint(self) -> str:
        return self._rule.rule

    def get_methods(self) -> list[str]:
        return list(_filter_methods(self._rule.methods))

    def __str__(self) -> str:
        """todo: remove this - only for testing
        """
        return json.dumps({
            self.get_endpoint(): self.get_methods(),
        })


def _filter_methods(methods: set) -> set:
    """Filter out HEAD and OPTIONS methods.

    Not instrumenting HEAD and OPTIONS methods by default.
    """
    return set(filter(
        lambda x: x not in {'HEAD', 'OPTIONS'},
        methods,
    ))

