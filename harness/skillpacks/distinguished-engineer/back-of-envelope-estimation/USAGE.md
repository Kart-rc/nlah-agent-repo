# Using `back-of-envelope-estimation`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer do the arithmetic before the argument: quantities
decomposed into anchored factors, powers-of-ten results bounded from both
sides, the dominating assumption flagged for measurement, results checked
against physical and platform ceilings, and the envelope published in the
artifact with its consequence stated — so designs are sanity-checked by
sums, not adjectives.

## When to invoke

- A design implies a latency, throughput, storage, or cost profile nobody
  has computed — most `options` and `design` stage work at scale.
- Options in a decision differ mainly by a number, so the option matrix's
  cost rows need defensible arithmetic behind them.
- A claim like "it won't scale" or "the cache will save us" is steering a
  review unquantified.
- See SKILL.md → When to Use / When NOT to use; skip it when the real
  number is cheaply measurable — measure instead.

**Default attachments:** suggested by `stages/options` `skill_refs`
(alongside `tech-director/options-and-tradeoffs`), and attached to the
`options` stage of the shipped `tech-decision` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: options
    uses: stages/options
    skills:
      - uses: skillpacks/distinguished-engineer/back-of-envelope-estimation
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/back-of-envelope-estimation/SKILL.md
fully, then estimate <quantity> for <design/claim>, writing out factors,
anchors, and assumptions so the arithmetic can be attacked.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- Quantities decomposed into factors, each traced to an anchor or a
  written assumption — no bare conclusions.
- Powers-of-ten results with optimistic and pessimistic bounds; no
  four-significant-figure fiction.
- The dominating assumption identified, with a recommendation to measure
  or spike it before committing.
- Claims checked against platform ceilings (partition throughput, rate
  limits, line rate); any design needing a component to exceed its
  documented limits flagged.
- The envelope appears in the artifact with a stated so-what tying the
  number to the decision it drives.
- Misapplication signs (from Red Flags): precision theater on guessed
  inputs, or an estimate whose assumptions were never written down.

## Worked example

Request: "Build or buy a feature-flag service?" (tech-decision run)

The shipped manifest attaches this skill at `options`, so no edit is
needed. Expected output shape: the option matrix's cost and capacity rows
backed by envelopes in `runs/<run-id>/` — e.g. flag-check traffic
estimated at clients × checks/request × requests/s ≈ 10^5 checks/s,
pessimistic 5×10^5; a self-hosted option needing one cache tier at that
rate (within a single node's ceiling, with headroom stated); the SaaS
option's per-seat + per-MAU pricing multiplied out to ~$10^5/year
pessimistic; and the dominating assumption (checks per request) flagged
with a one-day measurement plan against the current codebase. The
sensitivity note can then say which factor flips the build/buy ranking.
