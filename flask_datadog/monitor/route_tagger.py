"""Module for decorator that tags flask endpoints with monitor params
"""
import functools
from typing import Optional

import jsonschema  # type: ignore

from flask_datadog.shared import datadog_constants
from flask_datadog.shared import route_tagger_constants


def validate_tag(tag_spec: dict):
    """Validate schema tagged on route fn is ok. Raises exception on errors."""
    jsonschema.validate(
            instance=tag_spec,
            schema=datadog_constants.DDOG_MONITOR_SCHEMA,
            )


def datadog_monitors(monitors: Optional[dict] = None):
    """Enable auto DataDog monitor spec generation on endpoint.

    Example:

    @datadog_monitors()
    @flask_app.route('/', methods=['GET'])
    def handle_root():
        pass

    """

    def decorator_fn(func):

        # tag_dict is the dictionary that is used to tag the route handler fn
        tag_dict: dict = {}
        if not monitors:
            tag_dict[datadog_constants.TAG_KEY_DEFAULT_MONITORS] = True
        else:
            tag_dict[datadog_constants.TAG_KEY_MONITORS] = monitors

        func.__dict__[route_tagger_constants.ROUTE_INFO_KEY] = tag_dict

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_fn

