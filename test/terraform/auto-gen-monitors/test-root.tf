# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_test-app-service_GET-root_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_test-app-service_GET-root_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_5m): ( sum:trace.flask.request.errors{ env:prod, service:test-app-service, resource_name:get_/ }.as_count() / sum:trace.flask.request.hits{ env:prod, service:test-app-service, resource_name:get_/ }.as_count() ) > 0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
      warning_recovery = 0.03
    
    
      critical = 0.1
    
    
      critical_recovery = 0.08
    
  }

  

  include_tags = true

  tags = [
    "service:test-app-service",
    "env:prod",
    "resource_name:get_/"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_test-app-service_GET-root_APM_LATENCY_THRESHOLD" {
  name               = "AUTOGEN_test-app-service_GET-root_APM_LATENCY_THRESHOLD"
  type               = "query alert"
  message            = "APM_LATENCY_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "avg(last_5m):avg:trace.flask.request{ env:prod, service:test-app-service, resource_name:get_/ } > 0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
      warning_recovery = 0.03
    
    
      critical = 0.1
    
    
      critical_recovery = 0.08
    
  }

  

  include_tags = true

  tags = [
    "service:test-app-service",
    "env:prod",
    "resource_name:get_/"
  ]
}



