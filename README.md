# Overview

Utility for auto generating terraform monitor specifications from endpoints for
a single service.

# Running

## Running the test app service against a test DataDog account

Assumptions
- Test DataDog account is created; API and APP key are known

Running
1. Set DATADOG_API_KEY in env vars
1. Set DATADOG_APP_KEY in env vars
1. `make sync-datadog`: this applies monitoring configs to datadog acnt
1. `make local-up`: this builds app and dd-agent containers and runs them locally

Local setup
- Local docker compose environment runs test server in editable mode so you
  can modify python files while testing.


## Running auto terraform generator

Running
1. source the venv that the application runs in
1. python monitor_generator.py ../test-app/app:app

# Testing

1. Ensure venv is created. From root dir: `python -m venv venv`
2. Install testing dependencies: `./venv/bin/pip install .[testing]` (setup.cfg has `testing` extras_require)
3. `make test`

# Reference

- Flask App Object API: https://tedboy.github.io/flask/interface_api.application_object.html

# TODO

- Allow specification of just the monitors you want to default to
- "trigger when metric is <above/below> the threshold <in total | on average | etc.> ...
- test with different versions of Flask
- make terraform file generator into a cmd line executable

