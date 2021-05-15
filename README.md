# Progress

DONE
- Endpoint generator output is hooked up.
- App container sending to Datadog
- Terraform specs generating and writable to Datadog

TODO
- Creating Make commands for easily running things -- .phony and test target not working
- Test alert thresholds on Datadog and ensure they are working
- Turn program into

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
1. Update docker-compose.yml in test-app directory and set API Key for dd-agent
1. Build and run docker compose: docker-compose build && docker-compose up


### Running auto terraform generator

Running
1. source the venv that the application runs in
  1. todo: need to make parser into an executable
1. python monitor_generator.py ../test-app/app:app

