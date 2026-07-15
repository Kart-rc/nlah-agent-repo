# Using `workflow-composer`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Creates and modifies harness workflow manifests
(`harness/workflows/<id>/workflow.yaml`) by composing existing modules —
stages, validators, knowledge adapters, and practice skills — then proves the
result with `scripts/harness_lint.py` and a dry-run. Workflow changes are
manifest edits, never new machinery.

## When to invoke

- You want a new workflow for a work type the shipped manifests (`sdlc`,
  `tech-decision`, `architecture-review`, `proposal`) do not cover.
- You want to add, remove, or reorder stages; swap validators or their
  persona/`with` parameters; or attach/detach knowledge adapters or practice
  skills on an existing workflow (SKILL.md → Modify mode).
- The `agentic-delivery-router` hit a routing failure (no workflow matches)
  and offered composition.
- Per `CLAUDE.md`, all workflow creation and modification goes through this
  skill. It does not *run* workflows (that is the router) and it never edits
  stage contracts to fit one workflow (SKILL.md → Anti-patterns).

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it on requests to create or change workflows, stages,
validators, or attachments.

## How to invoke

### In conversation

Explicit invocation:

```text
/workflow-composer Create an incident-postmortem workflow.
```

Natural-language requests that trigger it via the frontmatter description:

```text
Add the red-team validator to the implement stage of the sdlc workflow.
```

```text
Detach idea-refine from the proposal workflow's research stage.
```

### Requirements

Run it with this repository as the working directory: it needs the four
module libraries under `harness/`, the manifest schema
(`harness/schema/workflow-manifest.schema.json`), and
`scripts/harness_lint.py`. Per `CLAUDE.md`, lint must run after any edit
under `harness/`.

## What to expect

- In create mode: a short interview (id, goal, intent triggers, work types,
  inputs), then a proposed stage composition built from stage frontmatter
  only — with an explicit callout if a needed capability has no stage.
- A new or minimally edited `harness/workflows/<id>/workflow.yaml` with
  default validators materialized per stage (completeness-check first) and
  `skill_refs` practice skills adjusted to the domain.
- A clean `python3 scripts/harness_lint.py` run — a manifest that does not
  lint clean does not exist to the router.
- A dry-run printout (stage order, resolved bindings, validator roster,
  knowledge and skill attachments, gate policy, applicable risk-overlay
  entries) and a confirmation step before the workflow is declared ready.
- In-flight runs are unaffected; they execute their frozen
  `workflow.lock.yaml` (HARNESS.md §3.0.3).
- Warning signs it is misapplied: a manifest declared ready without lint and
  a confirmed dry-run, or validators written by hand instead of materialized
  from stage defaults (SKILL.md → Anti-patterns).

## Worked example

You say: "We need a workflow for security incident postmortems." The
composer interviews you (id `incident-postmortem`, triggers like "write a
postmortem for the outage", work type `proposal`-adjacent), reads the stage
catalog frontmatter, and proposes intake → research → draft → finalize with
input bindings. It scaffolds `harness/workflows/incident-postmortem/workflow.yaml`
with materialized validators and skills, runs the linter to a clean pass,
prints the dry-run, and asks you to confirm before calling it ready.
