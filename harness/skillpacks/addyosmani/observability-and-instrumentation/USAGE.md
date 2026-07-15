# Using `observability-and-instrumentation`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes production behavior visible and diagnosable by driving instrumentation
from on-call questions: structured logs with correlation IDs, RED/USE metrics
with bounded cardinality, OpenTelemetry traces, and symptom-based alerts —
written alongside the feature, not after it.

## When to invoke

See SKILL.md → When to Use / NOT for the full criteria. Harness routing cues:

- Feature runs whose implement stage adds a service, endpoint, background
  job, queue, retry logic, or external integration — anything that will run
  in production and need evidence it works.
- Requests explicitly about telemetry: "add logging/metrics/tracing",
  "set up alerting", "we couldn't tell what happened in production".
- Post-incident hardening work where diagnosis was too slow.
- Do not attach for live incident diagnosis (`debugging-and-error-recovery`)
  or measured-slowness work (`performance-optimization`); launch-day
  monitoring checklists belong to `shipping-and-launch`.

**Default attachments:** none — ad hoc: attach it explicitly where the work
produces production-facing code, most naturally alongside the defaults on
the `implement` stage of the `sdlc` workflow (instrumentation is written
with the feature), or on `verify` when auditing existing telemetry.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/observability-and-instrumentation
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/observability-and-instrumentation/SKILL.md
fully, then apply its discipline to instrument <feature or service>, starting
from the on-call questions it requires.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Before touching code, the producer writes down 2–4 questions an on-call
  engineer will ask about the feature; every signal added must map to one
  (SKILL.md → Process step 1).
- Logs become structured JSON events with stable names and a correlation ID
  on every line; secrets and PII are excluded by allowlisting fields.
- New endpoints and external dependencies get RED metrics with
  small-fixed-set labels and latency histograms (percentiles, not averages).
- Any new alerts are symptom-based, actionable, runbook-linked, and
  test-fired once.
- Done means SKILL.md → Verification passes, including locating an induced
  staging failure via telemetry alone; the at-a-glance list is in the pack's
  `references/observability-checklist.md`.
- Misapplication signs (from SKILL.md → Red Flags): a PR adding retries or
  external calls with zero new telemetry, or metrics labeled with user IDs
  or raw URLs (cardinality bomb).

## Worked example

Request: "Add a payment-retry mechanism to checkout — and make sure we can
actually see what it's doing in prod." Use `workflow-composer` to add this
skill to the sdlc `implement` stage for the run:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/observability-and-instrumentation
```

The builder first records the on-call questions ("what fraction succeed
after retry?", "why do permanent failures happen?"), then ships the retry
logic with `payment_failed` structured events, RED metrics on the provider
call, and one symptom-based alert — verifying the telemetry by forcing a
failure in staging and finding it by `requestId`.
