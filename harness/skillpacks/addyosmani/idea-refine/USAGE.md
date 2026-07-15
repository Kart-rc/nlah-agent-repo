# Using `idea-refine`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Turns a raw or vague idea into a sharp, buildable concept through a
three-phase divergent/convergent process (expand, stress-test, converge),
ending in a markdown one-pager with a problem statement, recommended
direction, explicit assumptions, MVP scope, and a "Not Doing" list.

## When to invoke

SKILL.md has no "When to Use" section, so route on these cues:

- The request contains a concept that is real but underspecified: "explore
  options for X", "we're thinking about building Y", "stress-test my plan".
- Intent is already confirmed (via `interview-me`) but the *shape* of the
  solution is open — several plausible directions exist and none has been
  compared.
- The router classifies the work as a tech decision, architecture review, or
  proposal, where the research/options stages must widen the option space
  before anything converges.
- Do not attach it when requirements are already concrete enough to spec
  (`spec-driven-development` is the next step then), or when the user has
  not yet said what they actually want (`interview-me` comes first).
- It expects a live user for its sharpening questions; in a fully autonomous
  stage the producer should treat unanswered questions as recorded
  assumptions rather than blocking.

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
  sharpening questions, then generates 5–8 variations before converging on
  2–3 stress-tested directions (see SKILL.md → Process).
- The skill folder carries supporting files the producer is told to consult:
  `frameworks.md` (extra ideation lenses, applied selectively in Phase 1),
  `refinement-criteria.md` (the full evaluation rubric for Phase 2), and
  `examples.md` (model ideation sessions for tone and depth).
- `scripts/idea-refine.sh` is an optional helper that initializes an ideas
  directory; it is not required for the skill to work.
- Done means the Verification checklist passes: a one-pager exists with
  assumptions listed alongside validation strategies and an explicit
  "Not Doing" list — in a harness run it lands in `runs/<run-id>/`, not
  `docs/ideas/`.
- Misapplication signs (from SKILL.md → Red Flags): 20+ shallow variations,
  no assumptions surfaced, or output jumping straight to the one-pager
  without the divergent phases.

## Worked example

Request: "Should we build a plugin system for our CLI, or is that
overkill?" The router starts a `tech-decision` run; the shipped manifest
already attaches `idea-refine` to its `research` stage:

```yaml
  - id: research
    uses: stages/research
    skills:
      - uses: skillpacks/addyosmani/idea-refine
```

The research producer reads SKILL.md plus `frameworks.md`, explores
variations (full plugin API, config-driven hooks, fork-friendly
architecture, "do nothing"), stress-tests them against
`refinement-criteria.md`, and writes a one-pager into the run directory
naming a recommended direction, the assumptions to validate, and what is
explicitly not being built — input the `options` stage then compares.
