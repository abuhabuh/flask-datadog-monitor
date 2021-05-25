# Progress

DONE
- App and DDog agent running and sending metrics
- ErrorRate monitor prototype working
- flask-datadog package working and usable by test app
- route tagging is working and carries through to TF outputs

TODO
- "trigger when metric is <above/below> the threshold <in total | on average | etc.> ...

# Issues

Need to be in the same venv as the target app we are generating for due to
import dependencies. i.e. need to source venv of target app

# Overview

Utility for auto generating terraform monitor specifications from endpoints for
a single service.

## Running

### Running the test app service against a test DataDog

Assumptions
- Test DataDog account is create and API Key is available

Running
1. Set DATADOG_API_KEY in env vars
1. Set DATADOG_APP_KEY in env vars
1. `make sync-datadog`: this applies monitoring configs to datadog acnt
1. `make local-up`: this builds app and dd-agent containers and runs them locally

Local setup
- Local docker compose environment runs test server in editable mode so you
  can modify python files while testing.


### Running auto terraform generator

Running
1. source the venv that the application runs in
  1. todo: need to make parser into an executable
1. python monitor_generator.py ../test-app/app:app

# Reference

- Flask App Object API: https://tedboy.github.io/flask/interface_api.application_object.html
