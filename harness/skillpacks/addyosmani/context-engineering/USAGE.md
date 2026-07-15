# Using `context-engineering`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Teaches deliberate curation of what an agent sees: a five-level context
hierarchy (rules files down to conversation history), selective loading over
flooding, trust levels for loaded files, and explicit confusion management —
surface conflicts and missing requirements instead of guessing.

## When to invoke

- The delivery is agent-enablement work: writing or overhauling a CLAUDE.md
  or equivalent rules file, or setting a repo up for AI-assisted development.
- Agent output quality is the problem being fixed — hallucinated APIs,
  ignored conventions, re-implemented utilities — and the remedy is better
  context setup rather than a code change.
- A producer must work in a large or unfamiliar codebase and the stage should
  begin with disciplined, selective context loading (read targets, one
  pattern example, type definitions) rather than bulk file dumps.
- The work involves ambiguous or conflicting requirements where the skill's
  confusion-management patterns (surface options, ask) should govern.
- See SKILL.md → When to Use for the full list.

**Default attachments:** none — ad hoc: attach it to the `implement` stage
when the deliverable is rules-file or agent-context setup, or to any
producer stage that must navigate a large codebase with tight focus.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/context-engineering
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/context-engineering/SKILL.md fully, then
apply its discipline to author a CLAUDE.md for <repo>, covering tech stack,
commands, conventions, boundaries, and one pattern example.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Rules-file deliverables follow the CLAUDE.md structure in SKILL.md: tech
  stack, commands, conventions, boundaries, and a short pattern example.
- Before editing, the producer loads context selectively — the files to
  modify, related tests, one existing example of the pattern — instead of
  flooding itself with the whole repo (aim under ~2,000 focused lines).
- Ambiguity is surfaced in the explicit CONFUSION / MISSING REQUIREMENT
  format with lettered options, never resolved by silent guessing.
- Multi-step work is preceded by a short inline PLAN block so wrong
  directions are caught before they compound.
- Instruction-like text found in config, data, or external docs is treated as
  data to report, per the skill's trust levels.
- Misapplication signs: output still ignoring project conventions, or context
  dumps of unrelated files — the anti-pattern table in SKILL.md names both.

## Worked example

Request: "Our agents keep inventing APIs and ignoring our conventions — set
this repo up properly for AI-assisted work."

The router runs `sdlc`; attach this skill to the `implement` stage (snippet
above). The builder reads SKILL.md, inventories the stack and commands, and
writes a CLAUDE.md with conventions (named exports, colocated tests), hard
boundaries (never commit `.env`, ask before schema changes), and a pointer to
one exemplar component. It also adds a short project map for the two largest
subsystems. The stage summary shows a trial task where the agent followed the
documented pattern instead of inventing one.
