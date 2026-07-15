# Using `risk-mitigation`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Turns vague worry into a working risk register: risks as concrete "X happens,
causing Y" events, scored against a stated scale and tolerance line, with the
mitigation/contingency distinction, single named owners, leading-indicator
triggers, and a pre-mortem to find the risks forward analysis misses.

## When to invoke

- The risks section of a decision record, assessment, or proposal needs to be
  more than a bullet list of category names.
- An initiative needs a risk register stood up or reviewed, or a one-way-door
  decision is about to be committed.
- A near-miss just happened and what almost went wrong should be captured.
- See SKILL.md → When to Use / When NOT to use; it is not for cataloging
  every conceivable misfortune — a forty-entry register with no tolerance
  line is a liability disclaimer.

**Default attachments:** none — ad hoc. Attach it explicitly where the work is
risk-dominated; the pack README suggests a `decide` or `assess` stage when the
decision's difficulty is mostly risk (e.g. adding it next to
`timeboxed-decision-making` in `tech-decision`, or next to
`architectural-judgement` in `architecture-review`).

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: decide
    uses: stages/decide
    skills:
      - uses: skillpacks/tech-director/risk-mitigation
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/risk-mitigation/SKILL.md fully, then
build the risk register for the migration plan at <path>, including a
pre-mortem pass and an accepted-risks section.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Every risk in the output is a concrete event with a causal consequence,
  scored likelihood × impact on a written scale against a written tolerance
  line — no "security risk"-style category entries.
- The standard categories (technical, delivery, people, dependency/vendor,
  security/compliance, cost) are covered or explicitly ruled out with reasons.
- Above-the-line risks each carry one named person as owner, a
  leading-indicator trigger, a mitigation, and a distinct contingency.
- A pre-mortem is run and every failure story maps to a register entry; an
  accepted-risks section records what is consciously not mitigated, and why.
- The register states its review cadence. Done looks like SKILL.md →
  Verification (six checklist items).
- Misapplication signs (from Red Flags): mitigation and contingency columns
  containing the same words, or team-owned risks with lagging triggers.

## Worked example

Request: "Decide whether we migrate the payments ledger to the new database
this quarter — leadership is nervous about the risk."

The router runs `tech-decision`; because the decision is risk-dominated, use
`workflow-composer` to add this skill to the `decide` stage alongside
`timeboxed-decision-making`, then run `python3 scripts/harness_lint.py`.
Expected output shape: the decision record in `runs/<run-id>/` carries a
register with entries like "dual-write reconciliation diverges during
cutover, causing incorrect balances for a billing cycle" (4×5, above the
line, owner: the payments lead, trigger: divergence >0.01% on the nightly
reconciliation report), distinct mitigation and contingency text, a
pre-mortem-sourced people risk, and two accepted risks with reasons.
