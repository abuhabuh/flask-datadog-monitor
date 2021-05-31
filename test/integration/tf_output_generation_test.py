"""Generate Terraform output from tagged endpoints in test app
"""
import difflib
import logging
import os
import sys

from flask_datadog.generator import flask_endpoint_parser
from flask_datadog.generator.flask_endpoint import FlaskEndpoint
from flask_datadog.generator import tf_spec_generator


logging.basicConfig(level=logging.DEBUG)


SERVICE_ENV = 'integration_test_env'
SERVICE_NAME = 'integration_test_service'
TF_FILE_PREFIX = 'integration_test'
EXPECTED_OUTPUT_DIR = 'expected_output'


def _get_full_fname(fname: str) -> str:
    return f'{sys.path[0]}/{EXPECTED_OUTPUT_DIR}/{fname}'


def _remove_fname(fname: str):
    os.remove(_get_full_fname(fname))


def _get_all_expected_output_files() -> list[str]:
    """Return file names of all expected output test files"""
    test_files = []
    for fname in os.listdir(f'{sys.path[0]}/{EXPECTED_OUTPUT_DIR}'):
        if fname.endswith('.tf'):
            test_files.append(fname)

    return test_files


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
        logging.info(f'')
        logging.info(f'Comparing expected outputs...')
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
                    logging.info(f' > Updated {fname}')
                else:
                    test_passed = False
        logging.info(f'Output check complete')

    # 3. write new output files
    if new_outputs:
        logging.info(f'')
        logging.info(f'New endpoints present - writing expected new expected output files')
        for full_file_path, contents in new_outputs.items():
            fname = full_file_path.split('/')[-1]
            with open(full_file_path, 'w+') as fp:
                fp.write(contents)
                logging.info(f' > Wrote new expected output for {fname}')

    # 4. delete any output files that are orphaned and don't match test endpoints
    #    this happens if we rename or delete a test endpoints
    all_expected_fnames = _get_all_expected_output_files()
    all_generated_fnames = [full_path.split('/')[-1] for full_path, _ in (existing_outputs | new_outputs).items()]
    delete_fnames = [f for f in all_expected_fnames if f not in all_generated_fnames]
    if delete_fnames:
        logging.info(f'')
        logging.info(f'Deleting any old orphaned output files. This happens if we rename or delete a test endpoints')
        for fname in delete_fnames:
            logging.info(f' > Removing output file that is no longer used: {fname}')
            _remove_fname(fname)

    logging.info(f'')

    return test_passed


if __name__ == '__main__':
    if run_integration_test():
        logging.info(f'Integration test passed. Test outputs in {_get_full_fname(".")}')
        sys.exit(0)
    logging.info(f'Integration test failed')
    sys.exit(1)

