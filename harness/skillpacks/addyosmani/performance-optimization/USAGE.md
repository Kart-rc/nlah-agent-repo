# Using `performance-optimization`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces measure-first performance work: establish a baseline, identify the
actual bottleneck, fix that specific thing, measure again, then guard against
regression — with Core Web Vitals targets, anti-pattern fixes, and
performance budgets as reference material.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Runs whose acceptance criteria include numbers: load-time budgets,
  response-time SLAs, Core Web Vitals thresholds.
- Requests phrased as "X is slow", "improve our Lighthouse score", "this
  endpoint times out", "I think that change caused a regression".
- Runs building features that handle large datasets or high traffic, where
  N+1 queries and unbounded fetching are likely to creep in.
- Do not attach speculatively: without evidence of a problem the skill
  itself says not to optimize.

**Default attachments:** none — ad hoc: attach it explicitly where the run's
work is performance-shaped — on the `implement` stage of the `sdlc` workflow
when the fix itself is performance work, or on `verify` when performance
acceptance criteria must be checked with measurements.

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
      - uses: skillpacks/addyosmani/performance-optimization
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/performance-optimization/SKILL.md fully,
then apply its measure-identify-fix-verify-guard workflow to <the reported
slowness>, recording before/after numbers.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer measures before changing anything, using the symptom-driven
  tree in SKILL.md → Where to Start Measuring, with both synthetic and RUM
  data where applicable.
- Fixes target a named bottleneck (N+1 query, unbounded fetch, oversized
  bundle, unnecessary re-renders) rather than shotgun micro-optimization.
- The stage output includes specific before/after numbers and, where
  configured, a CI guard (bundle-size check, Lighthouse CI).
- Done means SKILL.md → Verification passes: bottleneck identified and
  addressed, Web Vitals in "Good" thresholds, existing tests still green.
- Misapplication signs (SKILL.md → Red Flags): optimization with no
  profiling data, or `React.memo`/`useMemo` everywhere as reassurance.

## Worked example

Request: "Our dashboard takes 6 seconds to load; get LCP under 2.5s." An
sdlc run; use `workflow-composer` to add this skill to implement:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/performance-optimization
```

The builder records a Lighthouse baseline (LCP 6.1s), traces it to an
unoptimized hero image plus an N+1 stats query, fixes exactly those two,
re-measures (LCP 2.1s), and adds a bundle-size budget to CI — reporting the
numbers in its stage output under `runs/<run-id>/`.
