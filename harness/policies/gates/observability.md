# Observability Gate Checklist

Required for production-facing changes. Verify:

- [ ] Structured logs for the new/changed paths
- [ ] Metrics for the key behaviors
- [ ] Traces where the change spans services (where applicable)
- [ ] Alerts based on user-visible symptoms
- [ ] Dashboards or queries to inspect the change in production
- [ ] Error visibility: failures are observable, not swallowed
- [ ] Latency visibility where the change affects a request path
- [ ] Owner and runbook identified (when production-facing)
- [ ] No sensitive data in telemetry
