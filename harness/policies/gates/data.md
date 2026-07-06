# Data Gate Checklist

Required for: data pipelines, schema changes, event contracts, ETL/ELT,
streaming flows, analytics tables, backfills, migrations. Verify:

- [ ] Schema compatibility (backward/forward) is addressed
- [ ] Idempotency of processing is stated
- [ ] Reprocessing / replay behavior is defined
- [ ] Data quality checks exist
- [ ] Lineage: sources and consumers are identified
- [ ] Freshness expectations are stated
- [ ] Volume assumptions are explicit
- [ ] Partitioning / layout impact is considered
- [ ] Consumer impact (downstream breakage) is assessed
- [ ] Rollback or recovery plan exists
