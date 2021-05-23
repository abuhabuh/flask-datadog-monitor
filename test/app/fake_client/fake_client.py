"""Fake client that polls different API endpoints
"""
import logging

import requests


logging.basicConfig(level=logging.DEBUG)


def run_requests():
    host = 'http://test-app:5000'
    paths = [
        '/',
        '/',
        '/error?resp=500',
        '/error?resp=200',
        '/latency?sleep=0',
        '/latency?sleep=2',
    ]

    logging.info(f'*** Starting Request Batch ***')

    for p in paths:
        req_url: str = f'{host}{p}'
        r = requests.get(req_url)
        logging.info(f'Response from {req_url}: {r.status_code}')

    logging.info(f'--')
    logging.info(f'--')
    logging.info(f'--')


if __name__ == '__main__':
    run_requests()
