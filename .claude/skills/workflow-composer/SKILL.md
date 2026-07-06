---
name: workflow-composer
description: Create, modify, and validate harness workflow manifests by composing existing stages, validators, knowledge adapters, and practice skills. Use when the user wants a new workflow, wants to add/remove/reorder stages, swap validators, or attach/detach knowledge or skill packs.
---

# Workflow Composer

## Overview

This skill is the "magnetic" UX of the harness: every workflow is a
`workflow.yaml` manifest composing modules from four libraries —

- stages (`harness/stages/`)
- validators (`harness/validators/`)
- knowledge adapters (`harness/knowledge/`)
- practice skills (`harness/skillpacks/`)

Creating or changing a workflow NEVER means new machinery — it means editing
a manifest, then proving it with lint + dry-run. The manifest schema is
`harness/schema/workflow-manifest.schema.json`; the reference example is
`harness/workflows/sdlc/workflow.yaml`.

## Create mode

### 1. Interview

Collect: workflow id (slug) and name; the goal and final deliverables; intent
triggers (example request phrasings) and signal keywords; which router work
types it serves; required workflow inputs (name, format, description).
Smallest number of questions — propose defaults from context where possible.

### 2. Catalog

Read ONLY the frontmatter of every `harness/stages/*/stage.md` (id, summary,
inputs, outputs, knowledge_slots, skill_refs). Propose a stage composition:
which existing stages, in what order, with what input bindings. Almost every
workflow starts with `stages/intake`.

If a needed capability has no stage, say so explicitly and point to
`docs/adding-a-stage.md` — do not force a stage to do work outside its
contract (its acceptance criteria will fail the run).

### 3. Scaffold

Write `harness/workflows/<id>/workflow.yaml`:

- `workflow.intent` from the interview (summary, triggers, signals, work_types).
- `inputs` from the interview.
- `defaults.gate`: `max_repair_attempts: 2`, `on_exhaustion: escalate` unless
  the user asks otherwise; `producer_context: fresh` always.
- Stages in order, each with:
  - `needs` (previous stage id, or several for genuine DAG needs),
  - `inputs` bound as `workflow:<input>` or `<stage>:<output>` — outputs come
    from the source stage's frontmatter, nothing else,
  - `validators` **materialized from the stage's `default_validators`**
    (copy them in, completeness-check FIRST), then apply workflow-specific
    `with` parameters (personas, focus, checklists from
    `harness/policies/gates/`),
  - `skills` **materialized from the stage's `skill_refs`**, adjusted to the
    workflow's domain.
- `outputs` bound to the deliverable stage outputs.

Defaults are consumed exactly once — here, at scaffold time. The runtime
reads only the manifest.

### 4. Attach knowledge

Read each adapter's frontmatter (`harness/knowledge/*/adapter.md`): its
`capabilities` must intersect the stage's `knowledge_slots` to be useful. Ask
which apply; attach at workflow level (all stages may use) or stage level
(additive). Each attachment is one line: `- uses: knowledge/<id>`.

### 5. Lint

Run `python3 scripts/harness_lint.py`. Fix every finding. A manifest that
does not lint clean does not exist as far as the router is concerned.

### 6. Dry-run

Without executing anything, print: stage order; per stage — the resolved
input bindings, validator roster (with parameters), knowledge attachments,
and practice skills; the gate policy per stage; which risk-overlay entries
from `harness/policies/risk-policy.yaml` would apply at each risk level.
Confirm with the user before declaring the workflow ready.

## Modify mode

For an existing manifest — add/remove/reorder stages, swap validators, change
`with` parameters, attach/detach knowledge adapters or practice skills:

1. Read the current manifest.
2. Make the minimal edit. Typical one-liners:
   - detach a practice skill: delete its `- uses: skillpacks/...` line
   - attach org context: add `- uses: knowledge/enterprise-mcp`
   - swap a persona gate: change the `persona:` parameter
   - remove a stage: delete its block AND fix any `needs`/bindings that
     referenced it (lint will catch stragglers)
3. Rules that hold under any edit:
   - every stage keeps ≥1 validator, completeness-check first
     (schema + lint enforce this),
   - bindings only reference `workflow:` inputs or outputs of stages in the
     stage's transitive `needs`,
   - a stage's producer persona never validates its own output.
4. Always finish with **Lint (step 5) + Dry-run (step 6)**.
5. In-flight runs are unaffected: they execute their frozen
   `workflow.lock.yaml` (HARNESS.md §3.0.3). New runs pick up the edit.

## Anti-patterns

Avoid: writing a manifest without materializing default validators; attaching
a knowledge adapter to a stage with no matching knowledge_slot (it will be
ignored — lint warns via capabilities mismatch in review); editing stage
contracts to fit one workflow (parameterize via `with` instead — stage docs
are shared); declaring a workflow ready without a clean lint and a confirmed
dry-run; deleting the intake stage to "save time" (every downstream gate
loses its requirements anchor).
