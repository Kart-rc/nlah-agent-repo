# Using `options-and-tradeoffs`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer build a decision-grade option matrix: decision drivers derived
and weighted from requirements before options are scored, TCO and reversibility
per option, fair advocacy for do-nothing and the boring choice, and a
sensitivity note — so the eventual call can be defended or overturned on
evidence.

## When to invoke

- The request is a technology selection, build-vs-buy, vendor evaluation, or
  architectural-direction question — the router classifies these as
  decision-shaped work and runs the `tech-decision` workflow, whose `options`
  stage carries this skill by default.
- A decision is expensive enough that someone will later ask "what else did
  you consider?", and the matrix must feed a decision record.
- See SKILL.md → When to Use / When NOT to use; skip it when there is one
  viable path, the choice is trivially reversible, or the decision was already
  made above your head.

**Default attachments:** suggested by `stages/options` `skill_refs` (alongside
`addyosmani/idea-refine`), and attached to the `options` stage of the shipped
`tech-decision` workflow.

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
      - uses: skillpacks/tech-director/options-and-tradeoffs
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/options-and-tradeoffs/SKILL.md fully,
then build the option matrix for <decision>, deriving weighted drivers from
the requirements in <path> before enumerating options.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Drivers and their explicit weights appear first, each traced to a
  requirement — before any option is named or scored.
- Every option scored against every driver with a one-line, evidence-citing
  justification (or a labeled assumption); a do-nothing row is present and
  fairly advocated.
- Each option carries TCO (build + run + opportunity cost), a one-way/two-way
  door classification with reasoning, and its named dominant risk.
- A sensitivity note states which single weight or assumption change would
  flip the ranking.
- The matrix ranks but does not recommend — the `decide` stage (and its
  skills) makes the call. Done looks like SKILL.md → Verification.
- Misapplication signs (from Red Flags): weights adjusted after scoring began,
  or every driver conveniently favoring the same option.

## Worked example

Request: "Should we build our own feature-flag service or buy LaunchDarkly?"

The router runs `tech-decision`; the shipped manifest attaches this skill at
the `options` stage, so no edit is needed. Expected output shape: a matrix in
`runs/<run-id>/` with weighted drivers (fitness, TCO, operational load,
reversibility, time to value) traced to intake requirements; rows for build,
buy, and do-nothing (keep config-file flags); per-cell justifications citing
the research stage; the buy option flagged as a two-way door and build as
one-way once SDKs spread; and a sensitivity note that halving the
time-to-value weight flips build above buy.
