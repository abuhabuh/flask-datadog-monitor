# Overview

Utility for auto generating DataDog terraform monitor specifications from flask
endpoints.

1. Setup DataDog Terraform integration
1. Decorate flask endpoints you want to monitor
1. Run the `flask-datadog` cmd line util to generate terraform files for the monitors
1. Apply Terraform changes

# Usage Examples

## Decorate Flask endpoints you want to monitor

```
# Decorating with `datadog_monitors` will generate default monitors for each
# method on the route
@datadog_monitors()
@flask_app.route('/foo', methods=['GET', 'POST'])
def handle_foo():
    return ''

# Specifying a particular monitor will allow you to tweak thresholds (and
# other parameters) but will only generate that particular monitor for
# that route
@datadog_monitors(
    monitors={
        MonitorType.APM_ERROR_RATE_THRESHOLD: {
            MonitorSpec.CRITICAL_THRESHOLD: 0.8,
            MonitorSpec.ALERT_PERIOD: '10m',
        },
    },
)
@flask_app.route('/foo', methods=['GET', 'POST'])
def handle_foo():
    return ''
```


## Generate Terraform for monitors with cmd line utility

```
flask-datadog gen-terraform --env prod --service my_service path/to/flask_app:app output_dir
```

# Running This Project Locally

Info on running the test service locally against a DataDog test account.

Assumptions
- You have a DataDog test account created

Steps to standup local test env
1. Set DATADOG_API_KEY in env vars
1. Set DATADOG_APP_KEY in env vars
1. `make sync-datadog`: this applies monitoring configs to datadog acnt
1. `make local-up`: this builds app and runs them locally with the dd-agent
containers

Once the local env is up, an automatic script in the `fake-client` service
should ping the `test-app` service periodically to generate fake traffic.

The `test-app` service and `fake-client` service both have mount points so
you can edit the code and have changes reflected directly without rebuilding
containers.


# Unit / Integration Testing

1. Ensure venv is created. From root dir: `python -m venv venv`
1. Install testing dependencies: `./venv/bin/pip install .[testing]` (setup.cfg has `testing` extras_require)
1. `make test`


# Reference

Flask API interface
- Flask App Object API: https://tedboy.github.io/flask/interface_api.application_object.html


# TODO

- Allow specification of just the monitors you want to default to
- "trigger when metric is <above/below> the threshold <in total | on average | etc.> ...
- test with different versions of Flask
- make terraform file generator into a cmd line executable

