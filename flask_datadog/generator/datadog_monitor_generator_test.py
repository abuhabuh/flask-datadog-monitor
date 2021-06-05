"""Unit tests
"""
import pytest

from flask_datadog.generator import datadog_monitor_generator


@pytest.mark.parametrize(
    'fe_methods,custom_methods,expected_methods',
    [
        ([], None, []),
        (None, None, []),
        (None, [], []),
        ([], ['GET'], []),
        (['GET', 'POST'], ['GET'], ['get']),
        (['GET', 'POST'], None, ['get', 'post']),
        (['GET', 'POST'], ['get', 'post', 'put'], ['get', 'post']),
    ],
)
def test_get_methods(fe_methods: list[str],custom_methods: list[str], expected_methods: list[str]):
    """Test get methods function returns appropriate methods.
    """
    assert expected_methods == datadog_monitor_generator._get_methods(fe_methods,custom_methods)