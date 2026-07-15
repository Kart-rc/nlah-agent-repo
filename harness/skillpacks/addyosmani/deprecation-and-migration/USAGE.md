# Using `deprecation-and-migration`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Treats code as a liability and disciplines its removal: a decision framework
for whether to deprecate, advisory-vs-compulsory classification, and a
four-step migration process (build the replacement, announce, migrate
consumers incrementally, remove at verified zero usage), with named patterns
(strangler, adapter, feature-flag migration).

## When to invoke

- The request removes or replaces something with consumers: "sunset the v1
  API", "migrate everyone off OldService", "kill this legacy module".
- Duplicate implementations need consolidating, or zombie code (no owner,
  active consumers) needs a maintain-or-remove decision.
- A design stage for a new system should plan its eventual removal — the
  skill insists deprecation planning starts at design time.
- A maintain-vs-migrate judgment call needs the skill's cost framing
  (ongoing maintenance versus one-time migration cost).
- See SKILL.md → When to Use for the full list.

**Default attachments:** none — ad hoc: attach it to the `plan` and
`implement` stages of an `sdlc` run whose deliverable is a migration, or to
the `assess`/`decide` stages of `architecture-review`/`tech-decision` runs
weighing whether to sunset a system.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: plan
    uses: stages/plan
    skills:
      - uses: skillpacks/addyosmani/deprecation-and-migration
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/deprecation-and-migration/SKILL.md fully,
then apply its process to plan the deprecation of <old system>, including the
decision questions, a migration guide, and an incremental consumer rollout.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer answers the five deprecation-decision questions (unique value,
  consumer count, replacement readiness, migration cost, cost of not
  deprecating) before proposing removal.
- The plan classifies the deprecation as advisory or compulsory (defaulting
  to advisory) and includes a written deprecation notice with a migration
  guide in the format SKILL.md shows.
- Migration proceeds consumer by consumer per the Churn Rule — the owner
  migrates users or ships backward-compatible updates, not just a deadline.
- Removal happens only after metrics/logs confirm zero active consumers, and
  takes tests, docs, config, and the notices with it.
- Done matches SKILL.md → Verification: replacement production-proven, all
  consumers migrated, no references to the old system remain.
- Misapplication signs: deprecating with no replacement available, or new
  features still landing on the deprecated system (SKILL.md → Red Flags).

## Worked example

Request: "We have two task services — retire `LegacyTaskService` and move all
callers to `NewTaskService`."

The router runs `sdlc`; attach this skill to `plan` and `implement` (snippet
above). The plan producer answers the decision questions (11 consumers,
replacement already in production), chooses advisory deprecation with a
feature-flag migration, and drafts the notice plus migration guide into
`runs/<run-id>/plan/`. The implement stage flips consumers one at a time
behind `new-task-service` flags; the final commit removes the legacy class,
its tests, and the notice once logs show zero calls for the observation
window.
