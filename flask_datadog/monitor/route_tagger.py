"""Module for decorator that tags flask endpoints with monitor params
"""
import functools

import jsonschema  # type: ignore

from flask_datadog.shared import route_constants


def _validate_tag(tag_spec: dict) -> bool:
    print(f'tag_spec: {tag_spec}')
    ret_val = jsonschema.validate(instance=tag_spec, schema=route_constants.ROUTE_SCHEMA)
    print(f'validate returned {ret_val}')
    return True


def tag_route(**kwargs):
    """Primary decorator for endpoints

    Example:

    @tag(monitors={})
    def foo():
        print(f'bar')

    """

    def decorator_fn(func):

        if 'monitors' in kwargs:
            func.__dict__[route_constants.ROUTE_INFO_KEY] = kwargs['monitors']

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_fn


# TODO: remove this test code
@tag_route(
    monitors={
        route_constants.MonitorType.ERROR_RATE_MONITOR.name: {
            route_constants.ThresholdTypes.CRITICAL_THRESHOLD.name: 0.1,
        },
    },
)
def foo():
    print('bar')
foo()

print(f'call with {foo.__dict__}')
_validate_tag(foo.__dict__[route_constants.ROUTE_INFO_KEY])

