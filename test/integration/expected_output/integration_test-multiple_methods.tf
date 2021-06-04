# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-multiple_methods_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-multiple_methods_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_10m): ( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:get_/multiple_methods }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:get_/multiple_methods }.as_count() ) > 0.8"

  monitor_thresholds {
    
    
    
      critical = 0.8
    
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/multiple_methods"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_PUT-multiple_methods_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_PUT-multiple_methods_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_10m): ( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:put_/multiple_methods }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:put_/multiple_methods }.as_count() ) > 0.8"

  monitor_thresholds {
    
    
    
      critical = 0.8
    
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:put_/multiple_methods"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_POST-multiple_methods_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_POST-multiple_methods_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = "APM_ERROR_RATE_THRESHOLD triggered."
  escalation_message = "Alert escalated"

  query = "sum(last_10m): ( sum:trace.flask.request.errors{ env:integration_test_env, service:integration_test_service, resource_name:post_/multiple_methods }.as_count() / sum:trace.flask.request.hits{ env:integration_test_env, service:integration_test_service, resource_name:post_/multiple_methods }.as_count() ) > 0.8"

  monitor_thresholds {
    
    
    
      critical = 0.8
    
    
  }

  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:post_/multiple_methods"
  ]
}



