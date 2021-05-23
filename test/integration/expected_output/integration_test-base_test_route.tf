resource "datadog_monitor" "integration_test_service-GET_base_test_route-ERROR_RATE_MONITOR" {
  name               = "integration_test_service-GET_base_test_route-ERROR_RATE_MONITOR"
  type               = "metric alert"
  message            = ""
  escalation_message = ""

  query = "sum(last_10m):(sum:trace.flask.request.errors{env:integration_test_env,service:integration_test_service,resource_name:get_/base_test_route}.as_count()/sum:trace.flask.request.hits{env:integration_test_env,service:integration_test_service,resource_name:get_/base_test_route}.as_count())>0.8"

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
    "resource_name:get_/base_test_route"
  ]
}



