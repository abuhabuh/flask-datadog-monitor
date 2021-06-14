"""
Commandline functionality for package

e.g., Generate terraform templates
"""
import logging

import click

from flask_datadog.generator import main_generator_logic


logging.basicConfig(level=logging.INFO)


@click.group()
def main():
    """Main flask-datadog cmdline group
    """
    pass


@main.command()
@click.argument('flask_app')
@click.argument('output_dir')
@click.option('--service', required=True, help='Name of service: e.g., user_service')
@click.option('--env', required=True, help='Environment: e.g., production')
@click.option('--prefix', default='', help='Prefix of output terraform files')
def gen_terraform(
        flask_app: str,
        output_dir: str,
        service: str,
        env: str,
        prefix: str,
        ):
    """
    FLASK_APP is the path to the flask application object
    - e.g., path/to/run_app:app
    """
    main_generator_logic.gen_tf(flask_app, output_dir, service, env, prefix)


if __name__ == '__main__':
    """Run cmd line"""
    main()

