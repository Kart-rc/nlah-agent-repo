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
- Do not attach it when requirements are already concrete enough to spec
  (`spec-driven-development` comes next) or intent itself is still unknown
  (`interview-me` comes first). Its sharpening questions expect a live
  user; in autonomous stages unanswered questions become recorded
  assumptions.

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

- The producer restates the idea as a "How Might We" problem, asks 3–5
  sharpening questions, generates 5–8 variations, then converges on 2–3
  stress-tested directions (SKILL.md → Process).
- Supporting files in the skill folder are consulted along the way:
  `frameworks.md` (extra ideation lenses for Phase 1),
  `refinement-criteria.md` (the Phase 2 evaluation rubric), `examples.md`
  (model sessions for tone and depth), plus the optional
  `scripts/idea-refine.sh` helper that initializes an ideas directory.
- Done means SKILL.md → Verification passes: a one-pager with assumptions,
  validation strategies, and a "Not Doing" list — written to
  `runs/<run-id>/` in a harness run, not `docs/ideas/`.
- Misapplication signs (SKILL.md → Red Flags): 20+ shallow variations, no
  assumptions surfaced, or jumping straight to the one-pager without the
  divergent phases.

## Worked example

Request: "Should we build a plugin system for our CLI, or is that
overkill?" The router starts a `tech-decision` run, whose shipped manifest
already attaches `idea-refine` to the `research` stage:

```yaml
  - id: research
    uses: stages/research
    skills:
      - uses: skillpacks/addyosmani/idea-refine
```

The research producer explores variations (full plugin API, config-driven
hooks, "do nothing"), stress-tests them against `refinement-criteria.md`,
and writes a one-pager into the run directory naming a recommended
direction, assumptions to validate, and a "Not Doing" list — input the
`options` stage then compares.
