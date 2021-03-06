"""Fake client that polls different API endpoints
"""
import datetime
import logging
import time

import requests


logging.basicConfig(level=logging.DEBUG)


def run_requests():
    host = 'http://test-app:5000'
    paths = [
        '/',
        '/',
        '/base-test?resp=200',
        '/base-test?resp=500',
        '/base-test?resp=500',
        '/base-test?sleep=1',
        '/base-test?sleep=2',
    ]

    logging.info(f'*** Starting Request Batch ***')

    for p in paths:
        req_url: str = f'{host}{p}'
        r = requests.get(req_url)
        logging.info(f'Response from {req_url}: {r.status_code}')

    logging.info(f'--')
    logging.info(f'--')
    logging.info(f'--')

    sleep_sec = 60
    logging.info(f'>>>>>>> sleeping for {sleep_sec}s at {datetime.datetime.now()}')
    logging.info(f'...')
    logging.info(f'...')
    logging.info(f'...')
    time.sleep(sleep_sec)


if __name__ == '__main__':
    run_requests()
