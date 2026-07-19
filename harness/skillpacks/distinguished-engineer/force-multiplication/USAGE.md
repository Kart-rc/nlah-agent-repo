# Using `force-multiplication`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer scale judgment through artifacts instead of presence:
repeated guidance promoted into paved paths, exemplars, lint rules, or
guides; paved paths built as working scaffolding with priced escape
hatches and measured adoption; review output written as principle plus
instance with severity distinguished; and delegation that hands over the
problem, constraints, and context while the solve stays with its new
owner.

## When to invoke

- The output must change how *other engineers* work: a standards
  proposal, a golden-path definition, a review guide, a platform
  template.
- The same guidance is being dispensed one-to-one repeatedly, or the same
  review comment recurs across authors.
- A practice needs adoption across teams nobody can mandate.
- See SKILL.md → When to Use / When NOT to use; management-flavored
  delegation and feedback belong to `tech-director/people-leadership`,
  and coalition-building for one proposal to
  `tech-director/influence-without-authority`.

**Default attachments:** none (ad hoc). Natural home: any stage whose
output is a standard, template, or practice meant to spread — e.g. the
`draft` stage of a proposal for a golden path.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: draft
    uses: stages/draft
    skills:
      - uses: skillpacks/distinguished-engineer/force-multiplication
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/force-multiplication/SKILL.md
fully, then design how <standard/practice> spreads without a mandate:
the paved path, the exemplar, the checks, and the adoption measures.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- The standard exists as working scaffolding — template repo, generator,
  CI check — not only as prose; the doc explains the path rather than
  substituting for it.
- Escape hatches open and priced: leaving the path is allowed and the
  cost of leaving is explicit and owned by the leaver.
- Adoption measured, with abandonment treated as a bug report on the
  path; no compliance-by-decree anywhere in the design.
- Judgment encoded in checkable form where possible (lint rules, scaffold
  defaults) instead of remembered form.
- Delegation framed as problem + constraints + context, with the short
  list of decisions the delegator still wants a say in made explicit.
- Misapplication signs (from Red Flags): a standard that exists only as a
  doc, or an adoption plan that begins with an enforcement deadline.

## Worked example

Request: "Every team wires observability differently; propose how we
standardize."

Attach this skill at the proposal's `draft` stage (alongside its default
`influence-without-authority`, which handles the stakeholder side).
Expected output shape: a proposal in `runs/<run-id>/` whose core is a
paved path, not a policy — a service scaffold where tracing, metrics, and
log correlation come wired by default, plus a migration codemod for the
top framework; an exemplar service named and kept current; a CI check
that warns (not blocks) on unstructured logs, with the block reserved
until adoption crosses 60%; escape-hatch pricing (teams off the path own
their own dashboard maintenance and integration upkeep); adoption
measured by scaffold usage and correlated-log coverage, reviewed
monthly; and the rollout delegated per-org as a problem statement with
constraints — not as a task list from the author.
