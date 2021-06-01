# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-base_test_all_monitors_APM_ERROR_RATE_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-base_test_all_monitors_APM_ERROR_RATE_THRESHOLD"
  type               = "query alert"
  message            = ""
  escalation_message = ""

  query = "sum(last_5m):(sum:trace.flask.request.errors{env:integration_test_env,service:integration_test_service,resource_name:get_/base_test_all_monitors}.as_count()/sum:trace.flask.request.hits{env:integration_test_env,service:integration_test_service,resource_name:get_/base_test_all_monitors}.as_count())>0.1"

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
    "resource_name:get_/base_test_all_monitors"
  ]
}



# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-base_test_all_monitors_APM_LATENCY_THRESHOLD" {
  name               = "AUTOGEN_integration_test_service_GET-base_test_all_monitors_APM_LATENCY_THRESHOLD"
  type               = "query alert"
  message            = ""
  escalation_message = ""

  query = "avg(last_5m):avg:trace.flask.request{env:integration_test_env,service:integration_test_service,resource_name:get_/base_test_all_monitors}>0.1"

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
    "resource_name:get_/base_test_all_monitors"
  ]
}



