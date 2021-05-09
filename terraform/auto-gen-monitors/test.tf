resource "datadog_monitor" "test_service-GET__health-ERROR_RATE" {
  name               = "test_service-GET__health-ERROR_RATE"
  type               = "metric alert"
  message            = ""
  escalation_message = ""

  query = "sum(last_10m):(sum:trace.flask.request.errors{env:prod,service:test_service,resource_name:GET_/health}.as_count()/sum:trace.flask.request.hits{env:prod,service:test_service,resource_name:GET_/health}.as_count())>0.1"

  monitor_thresholds {
    
      warning = 0.05
    
    
    
      critical = 0.1
    
    
  }

  include_tags = true

  tags = [
    "service:test_service",
    "env:prod",
    "resource_name:get_/health"
  ]
}
