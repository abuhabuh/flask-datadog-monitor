"""Module for decorator that tags flask endpoints with monitor params
"""
import functools

import jsonschema  # type: ignore

from flask_datadog.shared import ddog_constants
from flask_datadog.shared import route_constants


def validate_tag(tag_spec: dict) -> bool:
    ret_val = jsonschema.validate(
            instance=tag_spec,
            schema=ddog_constants.DDOG_MONITOR_SCHEMA,
            )
    return True


def tag_route(**kwargs):
    """Primary decorator for endpoints

    Example:

    @tag(monitors={})
    def foo():
        print(f'bar')

    """

    # TODO: create a "gen_all_monitors" arg that specifies generating all monitors by default
    def decorator_fn(func):

        if 'monitors' in kwargs:
            func.__dict__[route_constants.ROUTE_INFO_KEY] = kwargs['monitors']

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_fn

