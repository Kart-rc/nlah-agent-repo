# Using `failure-domain-thinking`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer design and judge systems by their failure domains: the
reach of each component's failure stated, shared-fate dependencies
enumerated, an explicit brownout ladder (shed order, stale policy, refusal
point), bounded queues with overflow policies, end-to-end timeout/retry
budgets over idempotent operations, and — for incidents — lessons that fix
the class rather than the instance.

## When to invoke

- Designing anything that takes production traffic — the sdlc `design`
  stage's "failure modes and rollback" criterion is this skill's home
  ground.
- Reviewing an architecture whose operational story must be judged (the
  `assess` stage's failure-mode criterion).
- Turning an incident into systemic lessons rather than a patched
  instance.
- See SKILL.md → When to Use / When NOT to use; instrumentation choices
  belong to `addyosmani/observability-and-instrumentation`, and project
  risk registers to `tech-director/risk-mitigation`.

**Default attachments:** suggested by `stages/design` and `stages/assess`
`skill_refs`, and attached to the `design` stage of the shipped `sdlc`
workflow (where it pairs with that stage's SRE-flavored persona review at
gate time).

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/distinguished-engineer/failure-domain-thinking
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/failure-domain-thinking/SKILL.md
fully, then analyze <design/system> by failure domain: blast radius per
component, degradation ladder, backpressure, and recovery, before
reviewing anything else.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- Each component annotated with the largest thing its failure can reach;
  shared-fate dependencies (config, auth, DNS) enumerated and either
  justified or walled off.
- An explicit brownout ladder: what sheds first, what serves stale, what
  gets refused — decided in the design, not deferred to the incident.
- Every queue bounded with a stated overflow policy; timeout and retry
  budgets set end-to-end with idempotency where retries reach.
- A rollback story that has been exercised, not merely written.
- For incident-shaped work: contributing factors rather than a single
  root cause, and actions that change structure, not vigilance.
- Misapplication signs (from Red Flags): a failure-modes section written
  after the design was done, or fallback paths that exist only on paper.

## Worked example

Request: "Design the new checkout-payments integration." (sdlc run)

The shipped manifest attaches this skill at `design`, so no edit is
needed. Expected output shape: a design in `runs/<run-id>/` whose
failure-domain section states that a payment-provider outage reaches
checkout completion but not cart or browse (bulkhead: provider calls
isolated behind a bounded queue, 2s budget); the brownout ladder queues
authorizations for retry with user messaging at rung two and refuses new
checkouts only at rung three; retries carry idempotency keys end-to-end
so a double-submit cannot double-charge; the rollback plan (flag off,
drain queue) is exercised in staging as part of the design's acceptance;
and the shared-fate note flags that both the primary and fallback
providers resolve through the same DNS zone — a merged failure domain the
diagram had hidden.
