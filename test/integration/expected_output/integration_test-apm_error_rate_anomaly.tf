# NOTE: this resource is auto generated via flask-datadog

resource "datadog_monitor" "AUTOGEN_integration_test_service_GET-apm_error_rate_anomaly_APM_ERROR_RATE_ANOMALY" {
  name               = "AUTOGEN_integration_test_service_GET-apm_error_rate_anomaly_APM_ERROR_RATE_ANOMALY"
  type               = "query alert"
  message            = ""
  escalation_message = ""

  query = "avg(last_12h):anomalies(avg:trace.flask.request{env:integration_test_env,service:integration_test_service,resource_name:get_/apm_error_rate_anomaly},'basic',2,direction='both',alert_window='last_10m',interval=120,count_default_zero='true')>=1"

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
    "resource_name:get_/apm_error_rate_anomaly"
  ]
}


