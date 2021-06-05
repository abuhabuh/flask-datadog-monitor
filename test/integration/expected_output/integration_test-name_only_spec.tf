# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-name_only_spec_APM_ERROR_RATE_ANOMALY" {
  name               = "AUTOGEN_integration_test_service_GET-name_only_spec_APM_ERROR_RATE_ANOMALY"
  type               = "query alert"
  message            = "APM_ERROR_RATE_ANOMALY triggered."
  escalation_message = "Alert escalated"

  query = "avg(last_12h):anomalies( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:get_/name_only_spec }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:get_/name_only_spec }.as_count(), 'basic', 2, direction='both', alert_window='last_5m', interval=120, count_default_zero='true' ) >= 0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
      warning_recovery = 0.03
    
    
      critical = 0.1
    
    
      critical_recovery = 0.08
    
  }

  
  # Anomaly monitors have threshold windows
  monitor_threshold_windows {
    
      recovery_window = "last_5m"
    
      trigger_window = "last_5m"
    
  }
  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/name_only_spec"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-name_only_spec_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-name_only_spec_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_5m): ( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:get_/name_only_spec }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:get_/name_only_spec }.as_count() ) > 0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
      warning_recovery = 0.03
    
    
      critical = 0.1
    
    
      critical_recovery = 0.08
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/name_only_spec"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-name_only_spec_APM_LATENCY_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-name_only_spec_APM_LATENCY_THRESHOLD"
  type               = "query alert"
  message            = "APM_LATENCY_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "avg(last_5m):avg:trace.flask.request{ env:integration_test_env, service:integration_test_service, resource_name:get_/name_only_spec } > 0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
      warning_recovery = 0.03
    
    
      critical = 0.1
    
    
      critical_recovery = 0.08
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/name_only_spec"
  ]
}



