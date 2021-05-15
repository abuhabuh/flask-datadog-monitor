"""Module for decorator that tags flask endpoints with monitor params
"""
import functools


def monitor_tag(**kwargs):
    """Primary decorator for endpoints

    Example:

    @monitor_tag(arg1='foo')
    def foo():
        print(f'bar')
    print(foo.__dict__)

    """

    def decorator_fn(func):

        func.__dict__['foo'] = 'bar'
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_fn

