# Using `shipping-and-launch`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes deployments reversible, observable, and incremental: a multi-section
pre-launch checklist, feature-flag and staged-rollout strategy with explicit
advance/hold/rollback thresholds, and a documented rollback plan for every
release.

## When to invoke

See SKILL.md → When to Use for the full criteria. Harness routing cues:

- Any sdlc run reaching its deliver stage — this is the default attachment
  there, so the router rarely needs to add it.
- Requests phrased as "deploy this", "prepare the release", "plan the
  rollout", "we need a rollback plan", or "open the beta".
- Runs the router tags as high delivery risk (data migrations,
  infrastructure changes): staged rollout and rollback are the
  risk-reduction mechanics.
- For the underlying telemetry work attach
  `observability-and-instrumentation` at implement instead; this skill
  consumes those signals for launch-day monitoring.

**Default attachments:** suggested by `stages/deliver` `skill_refs`
(alongside `documentation-and-adrs`); attached to the `deliver` stage of
the `sdlc` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: deliver
    uses: stages/deliver
    skills:
      - uses: skillpacks/addyosmani/shipping-and-launch
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/shipping-and-launch/SKILL.md fully, then
prepare <feature/release> for production: work the pre-launch checklist,
propose a staged rollout, and write the rollback plan.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer works the pre-launch checklist section by section (code
  quality, security, performance, accessibility, infrastructure,
  documentation) and reports gaps rather than glossing over them.
- Risky features get a feature-flag plan with an owner and expiration date;
  the rollout follows the staged sequence (staging → flag-off deploy →
  team → 5% canary → gradual → full) with the decision-threshold table
  governing advance/hold/rollback.
- A written rollback plan (trigger conditions, steps, database
  considerations, time-to-rollback) exists before any deploy, plus a
  first-hour post-launch verification routine.
- Done means SKILL.md → Verification passes, both before and after deploy;
  the deliver artifacts land in `runs/<run-id>/`.
- Misapplication signs (SKILL.md → Red Flags): deploying without a rollback
  plan, big-bang releases skipping staging, or nobody watching the first hour.

## Worked example

Request: "The workspace feature is merged — get it into production." The
shipped sdlc manifest already attaches this skill at deliver:

```yaml
  - id: deliver
    uses: stages/deliver
    skills:
      - uses: skillpacks/addyosmani/shipping-and-launch
```

The deliver producer emits a launch package into the run directory: the
completed pre-launch checklist (flagging the missing DB index found under
Performance), a rollout plan gated on the error-rate/latency thresholds
from SKILL.md's table, and a rollback plan naming the flag kill-switch
(<1 min) and the migration rollback command (<15 min).
