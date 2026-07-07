# Skill Pack: tech-director

Practice skills for **Technology Director judgment work**: making and
recording technical decisions, judging architectures, building cross-org
buy-in, managing risk, communicating upward, and leading people. Original
content authored for this harness (not vendored).

- **Contents:** 7 skills, each a `<skill-name>/SKILL.md`
- **Format:** same as the other packs — `name`/`description` frontmatter,
  practice-discipline body the producer reads before working

## What this pack is for

These are **practice skills**: judgment discipline documents that a stage's
producer subagent reads before doing its work. They are attached to workflow
stages via the manifest:

```yaml
stages:
  - id: decide
    uses: stages/decide
    skills:
      - uses: skillpacks/tech-director/timeboxed-decision-making
      - uses: skillpacks/tech-director/executive-communication
```

Attaching, detaching, or swapping a practice skill is a one-line manifest
edit. The orchestrator passes attached skill *paths* to the producer subagent
with an instruction to read them before starting (see `HARNESS.md` → Prompt
Templates).

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `options-and-tradeoffs` | Decision-grade option matrices: weighted drivers, TCO, reversibility, sensitivity | `stages/options` (skill_refs) |
| `timeboxed-decision-making` | One-way/two-way doors, the 70% rule, disagree-and-commit, revisit triggers | `stages/decide` (skill_refs) |
| `executive-communication` | BLUF, one-page decision briefs, calibrated uncertainty, altitude tailoring | `stages/decide` (skill_refs); `finalize` stage of the tech-decision, architecture-review, and proposal workflows |
| `architectural-judgement` | Judging designs: reversibility first, boring-technology bias, TCO over elegance, verdict discipline | `stages/assess` (skill_refs) |
| `influence-without-authority` | Stakeholder maps, minimum winning coalition, pre-wiring, designed escalation | `draft` stage of the proposal workflow |
| `risk-mitigation` | Risk registers: concrete events, mitigation vs contingency, owners, triggers, pre-mortems | none (ad hoc — see below) |
| `people-leadership` | Delegation levels, SBI feedback, coaching, team-health signals | none (ad hoc — see below) |

`risk-mitigation` and `people-leadership` are deliberately standalone:
attach them ad hoc with a one-line manifest edit wherever the work calls for
them — e.g. `risk-mitigation` on a `decide` or `assess` stage when the
decision is risk-dominated, `people-leadership` on `draft` when the proposal
is a reorg, growth plan, or team-shaped change. `influence-without-authority`
likewise fits any stage whose output must move other teams.

## Relationship to workflows

The `tech-decision` and `architecture-review` workflows (see
`harness/workflows/`) attach these skills per the map above; the `proposal`
workflow attaches `influence-without-authority` (draft) and
`executive-communication` (finalize). Stage documents suggest defaults in
their `skill_refs` frontmatter; the workflow-composer materializes those into
new manifests, where you can freely override them.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
