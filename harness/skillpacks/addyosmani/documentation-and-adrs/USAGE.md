# Using `documentation-and-adrs`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes producers document the *why*, not just the code: Architecture Decision
Records with alternatives and consequences, why-not-what comments, API docs,
README and changelog structure, and rules-file upkeep so future humans and
agents inherit the reasoning behind decisions.

## When to invoke

- A run makes a significant, expensive-to-reverse technical choice — the
  `tech-decision` and `architecture-review` workflows attach it for exactly
  this, so their written decisions land as proper ADRs.
- A delivery adds or changes a public API and needs typed documentation, or
  ships user-facing behavior that needs a changelog entry.
- The request is documentation itself: "write up why we chose X", "document
  this module", "make the README explain how to run the project".
- A proposal or draft needs decision-record rigor (context, alternatives
  considered, consequences) rather than free-form prose.
- See SKILL.md → When to Use / When NOT to use — skip it for throwaway
  prototypes and self-explanatory code.

**Default attachments:** suggested by `skill_refs` on `stages/deliver`,
`stages/assess`, `stages/decide`, and `stages/draft`; attached to the
`decide` stage of the `tech-decision` workflow, the `assess` stage of
`architecture-review`, and the `draft` stage of `proposal`. (The shipped
`sdlc` manifest's `deliver` stage omits it — add it there when a delivery
warrants an ADR or changelog.)

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
      - uses: skillpacks/addyosmani/documentation-and-adrs
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/documentation-and-adrs/SKILL.md fully,
then write an ADR for <decision> using its template, including alternatives
considered and consequences.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Significant decisions come out as numbered ADRs (`docs/decisions/`) with
  Status, Context, Decision, Alternatives Considered, and Consequences —
  superseded ADRs are kept and referenced, never deleted.
- Inline comments explain intent and gotchas only; comments that restate the
  code, commented-out code, and lingering TODOs are removed.
- Public API functions gain parameter/return/throws documentation (or
  OpenAPI definitions for REST endpoints).
- Shipped features get curated changelog entries and README updates covering
  quick start, commands, and architecture pointers.
- Done matches SKILL.md → Verification: ADRs for all significant decisions,
  documented gotchas, current rules files, no commented-out code.
- Misapplication signs: docs that restate the code instead of explaining
  intent, or decisions recorded with no rationale (SKILL.md → Red Flags).

## Worked example

Request: "Should we move task search to Elasticsearch or stay on Postgres
full-text? Decide and record it."

The router runs the `tech-decision` workflow; its `decide` stage already
carries this skill. After research and options stages, the decide producer
reads SKILL.md and writes `runs/<run-id>/decide/adr-007-task-search.md`:
Status Accepted, the load and ops-capacity context, the decision to stay on
Postgres full-text, Elasticsearch and Meilisearch as rejected alternatives
with reasons, and consequences (no new infra; revisit past 10M tasks). The
finalize stage then communicates a decision future agents can find instead
of re-litigating.
