"""Primary application module. This is where the app is run out of.
"""
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

import bootstrap


jinja_env = Environment(
    loader=FileSystemLoader(
        os.path.join(
            os.path.dirname(__file__),
            'templates'
        )
    ),
    autoescape=select_autoescape(['html', 'xml'])
)

# `flask run` references this app object
app = bootstrap.bootstrap_app(jinja_env)

