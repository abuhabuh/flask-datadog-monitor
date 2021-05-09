resource "datadog_monitor" "test_service-GET__health-ERROR_RATE" {
  name               = "test_service-GET__health-ERROR_RATE"
  type               = "metric alert"
  message            = ""
  escalation_message = ""

  query = "
            sum(last_10m): (
               sum:trace.flask.request.errors{
                   env:prod,
                   service:test_service,
                   resource_name:GET_/health
               }.as_count()
               /
               sum:trace.flask.request.hits{
                   env:prod,
                   service:test_service,
                   resource_name:GET_/health
               }.as_count()
            ) > 0.05
        "

  monitor_thresholds {
    warning           = 2
    warning_recovery  = 1
    critical          = 4
    critical_recovery = 3
  }

  notify_no_data    = false
  renotify_interval = 60

  notify_audit = false
  timeout_h    = 60
  include_tags = true

  # ignore any changes in silenced value; using silenced is deprecated in favor of downtimes
  lifecycle {
    ignore_changes = [silenced]
  }

  tags = ["foo:bar", "baz"]
}
