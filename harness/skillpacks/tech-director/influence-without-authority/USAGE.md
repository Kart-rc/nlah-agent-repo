# Using `influence-without-authority`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer plan cross-org buy-in for initiatives no one can mandate:
evidence-based stakeholder maps, a named minimum winning coalition, pre-wired
1:1 sequencing before any decision forum, and escalation as a designed move —
all in the open, trading in genuine interests.

## When to invoke

- The request is proposal-shaped and its success depends on teams outside the
  requester's authority — the router sends this to the `proposal` workflow,
  whose `draft` stage carries this skill by default.
- A decision meeting is approaching with positions unknown or opposed, or a
  previous attempt at the same initiative died for non-technical reasons.
- Ad hoc: attach it to any stage whose output must move other teams (the pack
  README calls this out explicitly) — e.g. a `decide` stage on a contested
  cross-team standard.
- See SKILL.md → When to Use / When NOT to use; skip it for decisions inside
  your own scope, or when the real gap is substance rather than alignment.

**Default attachments:** attached to the `draft` stage of the `proposal`
workflow (alongside `addyosmani/documentation-and-adrs`). It is not in any
stage's `skill_refs` suggestions, so other workflows pick it up only via an
explicit manifest edit.

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
      - uses: skillpacks/tech-director/influence-without-authority
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/influence-without-authority/SKILL.md
fully, then build a stakeholder map and influence plan for the proposal at
<path>, naming the minimum winning coalition and the pre-wiring sequence.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The draft gains a stakeholder map covering everyone who can block, fund, or
  must execute — each with a stake in their terms, a position on the
  champion-to-opponent spectrum, and cited evidence or a marked assumption.
- A named minimum winning coalition (which positions must move) plus the
  oppositions explicitly accepted as unresolved.
- A pre-wiring sequence of dated, owned 1:1s, each with an explicit ask and a
  fallback, so the decision meeting ratifies rather than decides.
- The strongest opponent's objection steelmanned and answered with substance
  (a concession, pilot, or scope change); escalation criteria defined upfront.
- Done looks like SKILL.md → Verification: all six checklist items evidenced
  in the plan.
- Misapplication signs (from Red Flags): position reads based on hope with no
  marked assumptions, or tactics you would not show to their targets.

## Worked example

Request: "Draft a proposal to consolidate our three internal CI systems onto
one platform — the two teams that own the others will resist."

The router runs the `proposal` workflow; its `draft` stage already attaches
this skill in the shipped manifest. Expected output shape: the proposal draft
in `runs/<run-id>/` plus an influence plan mapping both owning teams' leads
(one marked "opponent — said so in the June platform sync", one "assumed
neutral — verify first"), a coalition of the infra VP and one owning lead,
a concession offering the displaced team the migration-tooling charter, and
dated 1:1s scheduled before the platform council that ratifies the decision.
