# Using `explain-your-work`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes the producer emit `EXPLAIN.md` (what I did / why / what I assumed /
what alternatives I rejected / what you should check / questions for you)
alongside its declared outputs, so every human checkpoint has a teaching
artifact to present — and the producer's open questions reach the human
instead of dissolving into silent assumptions.

## When to invoke

- The workflow runs in interactive mode (`sdlc-interactive` attaches this
  skill to every stage by default).
- Any stage whose output a human must approve, or where the requester's
  stated goal includes understanding the process or the code.
- Subagents cannot ask questions mid-stage; this skill's "Questions for
  you" section is the harness's translation of clarifying-questions-ON —
  attach it wherever unresolved ambiguity should reach the human at the
  next checkpoint.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest, and pair it with the
enforcement `extra_check` on that stage's completeness-check — the skill
instructs the producer, but the gate is what guarantees the artifact:

```yaml
stages:
  - id: design
    uses: stages/design
    validators:
      - uses: validators/completeness-check
        with:
          extra_check: "artifacts/EXPLAIN.md exists with sections: What I did, Why, What I assumed, What alternatives I rejected, What you should check, Questions for you. EXPLAIN.md is an allowed, expected artifact for this stage."
    skills:
      - uses: skillpacks/teaching/explain-your-work
```

The `extra_check` both **requires and allows** EXPLAIN.md: completeness-check
flags undeclared artifacts as scope drift (failure class F4), so attaching
the skill without the extra_check makes the gate fail on the very artifact
the skill produced.

### Standalone (no harness run)

```text
Read harness/skillpacks/teaching/explain-your-work/SKILL.md fully, then
write EXPLAIN.md for the work you just completed, following its six-section
contract.
```

## What to expect

- One extra artifact per attached stage: `EXPLAIN.md` in the stage's
  artifact directory.
- At notify checkpoints the orchestrator presents it and continues; at
  block checkpoints it is the core of the approval evidence.
- Non-empty "Questions for you" sections are the signal to watch: they are
  the producer's unresolved ambiguities, surfaced instead of assumed away.
- Pairs with `skillpacks/provenance/context-register`: EXPLAIN.md cites
  `[context: CR-n]` entries when a register exists, making the "why" section
  auditable back to sources.
