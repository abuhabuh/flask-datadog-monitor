# Progress

Endpoint generator output is hooked up. Need to get sample Docker metrics
working so I can try to test this.

Current error is that ddtrace is trying to send metrics to the agent but it
cannot find the agent on localhost:8126 or whatever. Probably not able to get
through to the other Docker container.


# Issues

Need to be in the same venv as the target app we are generating for due to
import dependencies. i.e. need to source venv of target app

# Overview

Utility for auto generating terraform monitor specifications from endpoints.

## Running

Running the test app service against a test DataDog

Assumptions
- Test DataDog account is create and API Key is available

Running
1. Update docker-compose.yml in test-app directory and set API Key for dd-agent
1. Build and run docker compose: docker-compose build && docker-compose up

