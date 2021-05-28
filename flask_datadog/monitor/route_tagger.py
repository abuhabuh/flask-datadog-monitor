"""Module for decorator that tags flask endpoints with monitor params
"""
import functools
from typing import Optional

import jsonschema  # type: ignore

from flask_datadog.shared import ddog_constants
from flask_datadog.shared import route_tagger_constants


def validate_tag(tag_spec: dict):
    """Validate schema tagged on route fn is ok. Raises exception on errors."""
    jsonschema.validate(
            instance=tag_spec,
            schema=ddog_constants.DDOG_MONITOR_SCHEMA,
            )


def monitor_route(monitors: Optional[dict] = None):
    """Primary decorator for endpoints

    Example:

    @tag(monitors={})
    def foo():
        pass

    """

    def decorator_fn(func):

        # tag_dict is the dictionary that is used to tag the route handler fn
        tag_dict: dict = {}
        if not monitors:
            tag_dict[ddog_constants.TAG_KEY_DEFAULT_MONITORS] = True
        else:
            tag_dict[ddog_constants.TAG_KEY_MONITORS] = monitors

        func.__dict__[route_tagger_constants.ROUTE_INFO_KEY] = tag_dict

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_fn

