# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-apm_error_rate_anomaly_APM_ERROR_RATE_ANOMALY" {
  name               = "AUTOGEN_integration_test_service_GET-apm_error_rate_anomaly_APM_ERROR_RATE_ANOMALY"
  type               = "query alert"
  message            = ""
  escalation_message = ""

  query = "avg(last_12h):anomalies(sum:trace.flask.request.errors{env:integration_test_env,service:integration_test_service,resource_name:get_/apm_error_rate_anomaly}.as_count()/sum:trace.flask.request.hits{env:integration_test_env,service:integration_test_service,resource_name:get_/apm_error_rate_anomaly}.as_count(),'basic',2,direction='both',alert_window='last_10m',interval=120,count_default_zero='true')>=0.3"

  monitor_thresholds {
    
    
    
      critical = 0.3
    
    
  }

  
    # Anomaly monitors have threshold windows
    monitor_threshold_windows {
      
        recovery_window = "last_10m"
      
        trigger_window = "last_10m"
      
    }
  

  include_tags = true

  tags = [
    "service:integration_test_service",
    "env:integration_test_env",
    "resource_name:get_/apm_error_rate_anomaly"
  ]
}



