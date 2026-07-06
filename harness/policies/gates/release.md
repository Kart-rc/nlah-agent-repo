# Release Gate Checklist

Required before production launch. Verify the delivery artifact demonstrates:

- [ ] Tests pass (evidence recorded, not asserted)
- [ ] Build passes
- [ ] Migration plan reviewed (if data/schema is touched)
- [ ] Rollback plan exists and is concrete
- [ ] Monitoring exists for the changed behavior
- [ ] Known risks documented, not omitted
- [ ] Post-launch validation steps defined
- [ ] Rollout plan appropriate (feature flag / phased where warranted)
