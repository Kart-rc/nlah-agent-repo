# Using `large-scale-migration-design`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer design migrations as sequences of small, observable,
reversible steps: strangler slices that each pay for themselves, a
parallel run with dual-write/shadow-read and a divergence budget defined
before cutover, tested rollbacks with explicit data-consistency stories, a
named point of no return, and an end state with observable exit criteria
that includes decommissioning the old path.

## When to invoke

- The work is a datastore swap, API platform move, monolith strangling,
  auth/identity migration, or multi-team dependency shift — anywhere a
  big-bang cutover would be unrecoverable. On an sdlc run, attach at
  `design` and `plan`.
- A migration plan needs review for survivability: ramps, rollbacks,
  divergence handling, exit criteria.
- See SKILL.md → When to Use / When NOT to use; sunset policy and user
  communication belong to `addyosmani/deprecation-and-migration`, and
  in-codebase refactors to `addyosmani/code-simplification`.

**Default attachments:** none (ad hoc). Natural home: sdlc `design` and
`plan` when the work type is a migration.

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
      - uses: skillpacks/distinguished-engineer/large-scale-migration-design
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/large-scale-migration-design/SKILL.md
fully, then design the migration from <old> to <new> as reversible slices
with a parallel-run verification plan and explicit exit criteria.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- The migration decomposed into slices that each deliver value alone, with
  the first slice chosen to falsify the design cheaply.
- The system left coherent at every intermediate state — a pause at any
  step strands no data and orphans no dependents.
- A parallel-run design: dual-write/shadow-read, continuous
  reconciliation, alerting on divergence, and a divergence budget defined
  before the run starts.
- Every step paired with an exercised rollback and a data story for writes
  accepted since the step; the point of no return named and gated.
- Exit criteria in observables (dependents at zero, parity confirmed),
  decommissioning scoped with an owner and date, and the long tail
  enumerated by name.
- Misapplication signs (from Red Flags): a cutover date with no ramp plan,
  or value backloaded to the final step.

## Worked example

Request: "Move checkout from the legacy Postgres cluster to the new
partitioned store."

Attach this skill at sdlc `design` and `plan`. Expected output shape: a
design in `runs/<run-id>/` that strangles by tenant cohort — internal
tenants first (falsifies cheapest), the two whale tenants last; dual-write
begins at step one with shadow-reads compared continuously and a
divergence budget of zero on money fields, 0.01% on timestamps (clock
semantics documented); each ramp (1% → 10% → 50% → 100% of reads per
cohort) carries an exercised rollback whose data story is "writes dual-run,
so rollback is a read-path flag flip"; the point of no return —
stopping dual-writes — is gated on two weeks' parity and a daylight
decision; and exit criteria name legacy reader count at zero, the shim
deleted, and the cluster decommissioned by a dated owner, with the four
known laggard services listed and owned.
