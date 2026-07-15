# Using `people-leadership`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Applies leadership practice to people-shaped work: calibrated delegation
levels with explicit decision rights, SBI feedback tied to observable
behavior, coaching over prescribing, and leading team-health indicators —
growing decision-makers instead of dependents.

## When to invoke

- The request is a growth plan, feedback notes, a difficult-conversation
  opener, or a delegation decision.
- A proposal or plan under review is really a reorg, team split, ownership
  change, or growth plan — its dominant risks are human, not technical.
- A capable team is deciding slowly or shipping timidly and the request is to
  diagnose why.
- See SKILL.md → When to Use / When NOT to use; it explicitly excludes
  compensation, performance-management process, and legal matters, which
  follow the organization's HR frameworks.

**Default attachments:** none — ad hoc. Attach it explicitly where the work is
team-shaped; the pack README suggests the `draft` stage (e.g. of the
`proposal` workflow) when the proposal is a reorg, growth plan, or other
team-shaped change. It also pairs naturally with `risk-mitigation` on an
`assess` stage when an initiative's risks are organizational.

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
      - uses: skillpacks/tech-director/people-leadership
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/people-leadership/SKILL.md fully, then
apply its discipline to review the reorg plan at <path> for delegation,
ownership, and team-health risks.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Delegations in the output state their level (task / outcome / area),
  explicit decision rights (decide alone / decide-and-inform / consult), and
  a check-in cadence — problems delegated, not pre-baked solutions.
- Feedback content is in SBI form (situation, behavior, impact), describing
  observable behavior rather than character.
- Plans push decisions to the lowest level that can safely make them, and
  distinguish recoverable two-way-door mistakes from ones needing intervention.
- Team-health signals — decision latency, dissent frequency, attrition risk,
  bus factor — are assessed, and people risks land on the initiative's risk
  register rather than staying implicit.
- Done looks like SKILL.md → Verification (five checklist items).
- Misapplication signs (from Red Flags): growth plans that are promotion
  checklists, or "delegated" outcomes with hourly check-ins.

## Worked example

Request: "Draft the proposal to split the 14-person platform team into two
teams with separate on-call rotations."

The router runs the `proposal` workflow; since this skill has no default
attachment, use `workflow-composer` to add it to the `draft` stage alongside
the manifest's existing skills, then run `python3 scripts/harness_lint.py`.
Expected output shape: a draft in `runs/<run-id>/` whose ownership section
names area-level delegation for each new lead with explicit decision rights,
flags the single engineer who can operate the billing pipeline as a bus-factor
risk on the register, and includes SBI-form talking points for the two
engineers whose scope shrinks in the split.
