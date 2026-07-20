# Using `deep-system-debugging`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer diagnose by method instead of familiarity: system
invariants listed and tested to find the first broken promise, verified
facts separated from assumptions in writing, a hypothesis tree with
recorded kills, experiments chosen by information-per-cost with one
variable each, bisection across time/space/data/config, and a minimal
reproduction (or instrumented falsifiable narrative) delivered as the
diagnosis artifact.

## When to invoke

- A bug spans services, layers, or codebases nobody fully owns, or is
  intermittent and environment-dependent.
- Routine debugging has already stalled — the escalation-tier situation
  this skill is built for; on an sdlc run, attach it at `verify` when a
  hard bug emerges, alongside or replacing
  `addyosmani/debugging-and-error-recovery`.
- The symptom and cause are plausibly far apart: corruption, clock skew,
  partial deploys, cache coherence.
- See SKILL.md → When to Use / When NOT to use; a failing test with a
  clear stack trace does not need this skill.

**Default attachments:** none (ad hoc). Natural home: sdlc `verify` when a
hard bug emerges.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: verify
    uses: stages/verify
    skills:
      - uses: skillpacks/distinguished-engineer/deep-system-debugging
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/deep-system-debugging/SKILL.md
fully, then diagnose <failure>: list the invariants, build the hypothesis
tree, and bisect - do not propose a fix until the mechanism from cause to
symptom is evidenced.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- An invariant list with test results — the first violated invariant
  named, usually upstream of the symptom.
- A written split of verified facts versus assumptions, updated as the
  investigation moves.
- A hypothesis tree where killed branches carry their killing evidence;
  no hypothesis investigated twice.
- Experiments that change one variable and are chosen for how much of the
  tree they cut, not for which favorite they confirm.
- A minimal repro whose every element is load-bearing — or, where
  impossible, a rate-repro or an evidenced timeline plus shipped
  instrumentation for the next occurrence.
- A fix that explains the full mechanism; mitigation (restarts, rollbacks)
  clearly labeled as not-diagnosis.
- Misapplication signs (from Red Flags): fixes attempted before any
  hypothesis was written, or victory declared after changing two things.

## Worked example

Situation: checkout intermittently double-charges — once or twice a week,
no pattern, three prior attempts stalled.

Attach this skill at `verify` (or run standalone). Expected output shape:
an investigation log in `runs/<run-id>/` listing invariants (an order id
maps to at most one captured payment; retries carry idempotency keys) and
finding the first violation — duplicate captures share an order id but
differ in idempotency key. The hypothesis tree kills "provider retry bug"
(provider logs show distinct requests) and "client double-submit" (UI
disabled), leaving key regeneration; time-bisection lands on a deploy that
moved key generation inside a retry wrapper. The minimal repro is a
five-line script: force a timeout on first capture, observe a fresh key on
retry, double-charge one in one. The fix (hoist key generation) explains
the full mechanism, and the rate — "once or twice a week" — matches the
measured timeout rate, closing the loop.
