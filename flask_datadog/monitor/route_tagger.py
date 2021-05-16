"""Module for decorator that tags flask endpoints with monitor params
"""
import functools


def tag_route(**kwargs):
    """Primary decorator for endpoints

    Example:

    @tag(arg1='foo')
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

