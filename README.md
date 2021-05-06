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

Datadog agent should be up:

docker run -d --name dd-agent -p 8126:8127/tcp -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=<api-key> -e DD_SITE="datadoghq.com" gcr.io/datadoghq/agent:7


1. Source venv of target app (need to make flask ddog parser a package)
1. cd monitor-generator/
1. python flask_endpoint_parser.py ../test-app/app:app

