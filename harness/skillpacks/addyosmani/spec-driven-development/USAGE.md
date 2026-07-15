# Using `spec-driven-development`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Requires a structured, human-validated specification before any code exists,
via a gated Specify → Plan → Tasks → Implement workflow in which assumptions
are surfaced explicitly and vague requirements are reframed as testable
success criteria.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Any sdlc run — it is a default at both intake (spec skeleton) and design
  (full validated spec), so the router rarely needs to add it.
- Requests starting a new project, feature, or multi-file change with no
  written spec, or with ambiguous requirements ("make it faster").
- Runs about to make an architectural decision that should be pinned down
  in writing before implementation.
- Skip single-line fixes and typos (per SKILL.md). Its Plan and Tasks
  phases defer to `planning-and-task-breakdown` as canonical — in the sdlc
  workflow those phases belong to the separate plan stage.

**Default attachments:** suggested by `stages/intake` and `stages/design`
`skill_refs`; attached to the `intake` stage (alongside `interview-me`) and
the `design` stage (alongside `api-and-interface-design`) of the `sdlc`
workflow.

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
      - uses: skillpacks/addyosmani/spec-driven-development
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/spec-driven-development/SKILL.md fully,
then write a spec for <feature> covering its six core areas, surfacing your
assumptions before drafting.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer opens with an "ASSUMPTIONS I'M MAKING" block and asks
  clarifying questions before writing spec content; vague requirements come
  back reframed as measurable success criteria.
- The spec covers the six core areas of SKILL.md's template — Objective,
  Commands, Project Structure, Code Style, Testing Strategy, Boundaries —
  and its phase gates map to the workflow's approval gates in a harness run.
- The spec is a living artifact: scope or decision changes update it first;
  in a harness run it lives under `runs/<run-id>/` as the stage artifact
  the plan and implement stages consume.
- Done means SKILL.md → Verification passes: six areas covered, human
  approval given, success criteria specific and testable, spec saved.
- Misapplication signs (SKILL.md → Red Flags): code starting before any
  written requirements, or features appearing that no spec mentions.

## Worked example

Request: "We need commenting on shared documents." The router starts an
sdlc run; the shipped manifest attaches this skill at intake and design:

```yaml
  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/addyosmani/spec-driven-development
      - uses: skillpacks/addyosmani/api-and-interface-design
```

The design producer lists its assumptions (threaded vs. flat, notification
behavior, permissions), gets them corrected, then writes the six-area spec
with boundaries like "Ask first: schema changes". The approved spec becomes
the input the plan stage decomposes.
