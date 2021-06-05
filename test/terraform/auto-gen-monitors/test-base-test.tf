# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_test-app-service_GET-base-test_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_test-app-service_GET-base-test_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_10m): ( sum:trace.flask.request.errors{ env:prod, service:test-app-service, resource_name:get_/base-test }.as_count() / sum:trace.flask.request.hits{ env:prod, service:test-app-service, resource_name:get_/base-test }.as_count() ) > 0.8"

  monitor_thresholds {
    
      warning = 0.5
    
    
      warning_recovery = 0.4
    
    
      critical = 0.8
    
    
      critical_recovery = 0.7
    
  }

  

  include_tags = true

  tags = [
    "service:test-app-service",
    "env:prod",
    "resource_name:get_/base-test"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_test-app-service_GET-base-test_APM_ERROR_RATE_ANOMALY" {
  name               = "AUTOGEN_test-app-service_GET-base-test_APM_ERROR_RATE_ANOMALY"
  type               = "query alert"
  message            = "APM_ERROR_RATE_ANOMALY triggered."
  escalation_message = "Alert escalated"

  query = "avg(last_12h):anomalies( sum:trace.flask.request.errors{ env:prod, service:test-app-service, resource_name:get_/base-test }.as_count() / sum:trace.flask.request.hits{ env:prod, service:test-app-service, resource_name:get_/base-test }.as_count(), 'basic', 1, direction='above', alert_window='last_10m', interval=120, count_default_zero='true' ) >= 0.7"

  monitor_thresholds {
    
    
    
      critical = 0.7
    
    
  }

  
  # Anomaly monitors have threshold windows
  monitor_threshold_windows {
    
      recovery_window = "last_10m"
    
      trigger_window = "last_10m"
    
  }
  

  include_tags = true

  tags = [
    "service:test-app-service",
    "env:prod",
    "resource_name:get_/base-test"
  ]
}



