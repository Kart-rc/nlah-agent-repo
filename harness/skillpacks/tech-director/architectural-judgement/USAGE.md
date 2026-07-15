# Using `architectural-judgement`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Equips a producer to judge an architecture rather than design one: reversibility
first, boring-technology bias, total cost of ownership over elegance, and a
verdict discipline that ends in exactly one of approve / approve-with-conditions
/ reject with evidence-cited, severity-ranked findings.

## When to invoke

- The request is "review/assess this design doc, RFC, or system" — the router
  classifies this as assessment work and routes it to the `architecture-review`
  workflow, whose `assess` stage carries this skill by default.
- Two teams' competing designs need arbitration, or a pattern is proposed as a
  platform standard.
- An approval must carry conditions that someone can later verify.
- See SKILL.md → When to Use / When NOT to use for the full boundary; the key
  exclusion is producing the design yourself — attach a design-side skill
  (e.g. `addyosmani/api-and-interface-design`) for that instead.

**Default attachments:** suggested by `stages/assess` `skill_refs` (alongside
`addyosmani/documentation-and-adrs`), and attached to the `assess` stage of
the shipped `architecture-review` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: assess
    uses: stages/assess
    skills:
      - uses: skillpacks/tech-director/architectural-judgement
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/architectural-judgement/SKILL.md fully,
then apply its discipline to review the design doc at <path> and deliver a
verdict with severity-ranked, evidence-cited findings.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The assessment opens by classifying the design's key decisions as one-way or
  two-way doors before any quality judgment.
- Each novel-technology choice is weighed against a boring alternative, and
  the operational story (3am ownership, failure diagnosis, upgrade path) is
  assessed explicitly.
- Output ends in exactly one verdict — approve / approve-with-conditions /
  reject — stated first, with decidable conditions (what, verified how, by when).
- Every finding cites a location in the artifact under review and carries a
  blocker/major/minor severity; blockers drive the verdict.
- Done looks like SKILL.md → Verification: all six checklist boxes satisfiable
  from the assessment document alone.
- Misapplication signs (from Red Flags): unverifiable conditions attached to an
  "approval" (a hidden reject), or findings citing principles with no location
  in the subject.

## Worked example

Request: "Assess the proposed event-sourced billing redesign in
`docs/rfc-billing-v2.md` before the platform review board meets."

The router runs the `architecture-review` workflow; its `assess` stage already
attaches this skill via the shipped manifest, so no manifest edit is needed.
Expected output shape: an assessment in `runs/<run-id>/` that opens with a
reversibility classification (the event-store schema flagged as a one-way
door), challenges the two novel technologies against the incumbent Postgres
path, and closes with "approve-with-conditions" — each condition decidable,
e.g. "replay-from-snapshot benchmark under production volume before GA,
verified in the capacity review."
