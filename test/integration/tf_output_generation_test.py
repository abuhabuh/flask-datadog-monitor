"""Generate Terraform output from tagged endpoints in test app
"""
import difflib
import os
import sys

from flask_datadog.generator import flask_endpoint_parser
from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.generator import tf_spec_generator


SERVICE_ENV = 'integration_test_env'
SERVICE_NAME = 'integration_test_service'
TF_FILE_PREFIX = 'integration_test'
EXPECTED_OUTPUT_DIR = 'expected_output'


def _get_full_fname(fname: str) -> str:
    return f'{sys.path[0]}/{EXPECTED_OUTPUT_DIR}/{fname}'


def _generate_test_results(flask_endpoint_list: list[FlaskEndpoint]) -> tuple[dict, dict]:
    """Generate terraform outputs for a list of flask endpoints
    """
    existing_outputs = dict()
    new_outputs = dict()
    for fe in flask_endpoint_list:
        contents: str = tf_spec_generator.get_tf_contents_from_flask_endpoint(
                fe, SERVICE_ENV, SERVICE_NAME)
        fname: str = tf_spec_generator.get_tf_fname(TF_FILE_PREFIX, fe.get_endpoint_fname())
        fname_full_path: str = _get_full_fname(fname)
        if os.path.isfile(fname_full_path):
            existing_outputs[fname_full_path] = contents
        else:
            new_outputs[fname_full_path] = contents
    return existing_outputs, new_outputs


def run_integration_test() -> bool:
    """
    :return: bool - True if tests passed or diffs were expected
    """
    # import the flask app to test
    from test.integration.integration_test_app import flask_app

    test_passed = True

    # 1. generate output from API end points
    fe_list: list[FlaskEndpoint] = flask_endpoint_parser.parse_endpoints(
        flask_app,
    )
    existing_outputs, new_outputs = _generate_test_results(fe_list)

    # 2. compare with actual output files
    if existing_outputs:
        for full_file_path, contents in existing_outputs.items():
            fname = full_file_path.split('/')[-1]
            with open(full_file_path, 'r') as fp:
                expected_contents = fp.read()

            # if contents different, prompt user to overwrite
            if not contents == expected_contents:
                sys.stdout.writelines(difflib.unified_diff(contents, expected_contents))
                ans: str = ''
                while ans.lower() not in ['y', 'n']:
                    ans = input(
                        f'\n'
                        f'Diff found for {fname}. \n'
                        f' > Replace expected output (y/n)? '
                    )
                ans = ans.lower()
                if ans == 'y':
                    with open(full_file_path, 'w+') as fp:
                        fp.write(contents)
                    print(f' > updated {fname}')
                else:
                    test_passed = False

    if new_outputs:
        for full_file_path, contents in new_outputs.items():
            fname = full_file_path.split('/')[-1]
            with open(full_file_path, 'w+') as fp:
                fp.write(contents)
                print(f'Wrote new expected output for {fname}')

    return test_passed


if __name__ == '__main__':
    if run_integration_test():
        sys.exit(0)
    sys.exit(1)

