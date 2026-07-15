# Using `idea-refine`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Turns a raw idea into a sharp, buildable concept via three phases (expand,
stress-test, converge), ending in a markdown one-pager: problem statement,
recommended direction, assumptions, MVP scope, and a "Not Doing" list.

## When to invoke

SKILL.md has no "When to Use" section, so route on these cues:

- The request contains a concept that is real but underspecified: "explore
  options for X", "we're thinking about building Y", "stress-test my plan".
- Intent is confirmed (via `interview-me`) but the shape of the solution is
  open: several plausible directions, none yet compared.
- The router classified the work as a tech decision, architecture review,
  or proposal — their research/options stages widen the option space.
- Do not attach it when requirements are already spec-ready
  (`spec-driven-development` comes next) or intent is still unknown
  (`interview-me` comes first); its sharpening questions expect a live
  user, so autonomous stages record unanswered ones as assumptions.

**Default attachments:** suggested by `stages/research` and `stages/options`
`skill_refs`; attached to the `research` stage of the `tech-decision`,
`architecture-review`, and `proposal` workflows, and to the `options` stage
of the `tech-decision` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: research
    uses: stages/research
    skills:
      - uses: skillpacks/addyosmani/idea-refine
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/idea-refine/SKILL.md fully, then run an
ideation session on <idea>, producing the one-pager it specifies.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Per SKILL.md → Process: restate as a "How Might We" problem, ask 3–5
  sharpening questions, generate 5–8 variations, converge on 2–3
  stress-tested directions.
- Supporting files are consulted along the way: `frameworks.md` (Phase 1
  ideation lenses), `refinement-criteria.md` (Phase 2 rubric),
  `examples.md` (model sessions), plus the optional
  `scripts/idea-refine.sh` helper that initializes an ideas directory.
- Done means SKILL.md → Verification passes: a one-pager with assumptions,
  validation strategies, and a "Not Doing" list — written to
  `runs/<run-id>/` in a harness run, not `docs/ideas/`.
- Misapplication signs (SKILL.md → Red Flags): 20+ shallow variations, no
  assumptions surfaced, or jumping straight to the one-pager.

## Worked example

Request: "Should we build a plugin system for our CLI?" The router starts
a `tech-decision` run, whose manifest already attaches it at `research`:

```yaml
  - id: research
    uses: stages/research
    skills:
      - uses: skillpacks/addyosmani/idea-refine
```

The research producer explores variations (full plugin API, config-driven
hooks, "do nothing"), stress-tests them against `refinement-criteria.md`,
and writes a one-pager into the run directory — recommended direction,
assumptions to validate, "Not Doing" list — for the `options` stage to compare.
