# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-base_test_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-base_test_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "/base_test error threshold of 0.8 reached"
  escalation_message = "Alert escalated"

  query = "sum(last_10m): ( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:get_/base_test }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:get_/base_test }.as_count() ) > 0.8"

  monitor_thresholds {
    
      warning = 0.5
    
    
      warning_recovery = 0.3
    
    
      critical = 0.8
    
    
      critical_recovery = 0.7
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/base_test"
  ]
}



