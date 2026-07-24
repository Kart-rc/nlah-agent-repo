# HARNESS.md — Runtime Charter

This document is the **constitution** of the NLAH magnetic harness. It is the
single source of truth for how workflows execute. Skills, stages, validators,
and personas *reference* this protocol; none of them may restate or override it.

The design follows the NLAH model ("Natural-Language Agent Harnesses",
arXiv 2603.25723): **natural language carries policy; the runtime carries
mechanism.** Claude Code is the runtime (the paper's "Intelligent Harness
Runtime"): it executes tools, launches subagents, and reads/writes files. The
documents in this repository carry all control logic — stage topology, roles,
contracts, validation gates, state semantics, and failure recovery.

---

## 1. Principles

1. **Text is the harness.** Changing harness behavior means editing a document,
   never writing orchestration code. The workflow manifest (`workflow.yaml`) is
   the single runtime source of truth for a workflow: every stage, validator,
   knowledge adapter, practice skill, and gate policy is literally visible in it.
   There is no implicit inheritance at execution time.
2. **State lives on disk, not in context.** Every run externalizes its state to
   path-addressable artifacts under `runs/<run-id>/`. The orchestration loop is
   a pure function of `task_state.json` — any context reset, compaction, or
   restart can resume the run losslessly from disk.
3. **Subagents for context management.** Each stage executes in its own
   fresh subagent context. The orchestrator never reads stage artifacts — only
   `task_state.json` and per-stage `summary.md` files (≤200 words each).
   Handoffs happen via files, never via context.
4. **Validation is independent and blocking.** A stage is not complete until an
   independent validator subagent — a *different persona* than the producer,
   with a fresh context that never contains the producer's reasoning — passes
   the stage's acceptance criteria. Failures trigger a bounded repair loop,
   then structured human escalation. Gates are never silently skipped.
5. **Magnetic composition.** Stages, validators, knowledge adapters, and
   practice skills are self-contained modules. Attaching, detaching, swapping,
   or reordering any of them is a manifest edit validated by
   `scripts/harness_lint.py`. Creating a workflow means composing existing
   modules, not writing new machinery.
6. **Risk drives rigor.** The `agentic-delivery-router` classifies every request
   (work type + risk level) before any run starts. The risk level materializes
   additional validators and human-approval checkpoints into the run's locked
   manifest via `harness/policies/risk-policy.yaml`.

## 2. Component model

| Component | Location | Contract | Role |
|---|---|---|---|
| Workflow manifest | `harness/workflows/<id>/workflow.yaml` | `harness/schema/workflow-manifest.schema.json` | Composition: stage order, attachments, gate policy |
| Stage | `harness/stages/<id>/stage.md` | frontmatter ↔ `stage-contract.schema.json` | Self-contained unit of producer work with acceptance criteria |
| Validator | `harness/validators/<id>/validator.md` | frontmatter ↔ `validator-contract.schema.json` | Independent judgment task producing a verdict |
| Knowledge adapter | `harness/knowledge/<id>/adapter.md` | frontmatter ↔ `adapter-contract.schema.json` | Attachable knowledge source (enterprise MCP, second brain, …) |
| Practice skill pack | `harness/skillpacks/<pack>/<skill>/SKILL.md` | path existence (linted) | Attachable engineering discipline read by producers |
| Persona | `.claude/agents/<name>.md` | Claude Code agent format | WHO executes: tool permissions + voice. Producers ≠ validators |
| Policies | `harness/policies/` | `risk-policy.yaml` + gate checklists | Risk → validators/approvals; gate checklists for validators |
| Router | `.claude/skills/agentic-delivery-router/` | — | Entry point: classify → select → orchestrate this protocol |
| Composer | `.claude/skills/workflow-composer/` | — | Create/modify manifests; lint + dry-run |
| Run state | `runs/<run-id>/` | `task-state.schema.json` | Externalized, resumable execution state |

**Two-layer persona model.** Personas (`.claude/agents/`) define WHO — tool
permissions and voice. Stage and validator documents define WHAT — the task,
contract, and criteria. A producer prompt = stage doc + inputs; a validator
prompt = validator doc + criteria + artifact paths. No document plays both roles.

## 3. Orchestration protocol

The router (or any orchestrator) executes this loop. It is the only place this
protocol is defined.

### 3.0 Run initialization

1. Create `runs/<run-id>/` where `run-id` = `YYYYMMDD-HHMM-<workflow-id>-<slug>`.
2. Write `request.md` (the user's request, verbatim) and `inputs.json`
   (resolved workflow-level inputs, collected from the user if missing).
3. Resolve the manifest: copy `harness/workflows/<id>/workflow.yaml`, apply the
   risk overlay from `harness/policies/risk-policy.yaml` for the classified
   risk level (append `additional_validators` to the named stages; merge the
   overlay's `approval_checkpoints` with any the manifest itself declares —
   union by `before`; overlay checkpoints carry no `mode` and are always
   block-tier, and `block` wins over `notify` for the same stage), and write
   the result to `workflow.lock.yaml`.
   **The lock file is the only manifest read for the rest of the run.**
4. Initialize `task_state.json` (all stages `pending`; `classification` block
   recorded from the router's REQUEST CLASSIFICATION).
5. Append a `run_initialized` event to `events.jsonl`.

### 3.1 Per-stage loop

Execute stages in `needs` order (v1: sequentially; a stage runs only after all
stages in its `needs` are `passed`). For each stage:

1. **Approval checkpoint.** If the lock file declares an approval checkpoint
   `before` this stage, act on its tier (`mode`, default `block`):
   - `block` — if no grant is recorded for this checkpoint: set run status
     `awaiting_approval`, present the plan, rollback strategy, and
     verification approach to the user (see §7 templates), and STOP. Resume
     only on explicit user approval; record the grant in
     `classification.approvals.<stage>` (`classification.approval` remains
     the run-level pre-start approval).
   - `notify` — never stops the run and records no grant: present the same
     evidence, append a `checkpoint_notified` event to `events.jsonl`, and
     continue.
2. **Resolve.** Look up each input binding (`workflow:<input>` in `inputs.json`;
   `<stage>:<output>` in `task_state.json → stages.<stage>.artifacts`). Write
   `stages/<id>/inputs.json` mapping input names to file paths. An unresolvable
   binding is failure class **F1 at the harness level**: halt the run and
   report — this is a harness bug, not a repair case.
3. **Produce.** Set stage `in_progress`. Launch a subagent whose type is the
   stage's `producer` persona, with the Producer Prompt (§7.1). The producer
   writes artifacts to `stages/<id>/artifacts/` and `stages/<id>/summary.md`,
   then returns a single line.
4. **Record.** Read `summary.md` ONLY (never artifacts). Update
   `task_state.json`: artifact paths (from the stage contract's declared
   outputs), status `validating`. Append event.
5. **Gate.** For each validator in the lock file's order (completeness-check is
   always first, by composer convention and lint): resolve the attachment's
   `with` block — a value that is exactly an input binding (`workflow:<input>`
   or `<stage>:<output>`) resolves to its path as in step 2, all other values
   pass verbatim; this is how a validator that must inspect the target repo
   (e.g. `test-of-tests`) receives `workflow:target_repo`, and an unresolvable
   binding is F1 at the harness level, as in step 2. Then launch a fresh
   subagent whose type is the validator's `agent` persona, with the Validator
   Prompt (§7.2). The validator RETURNS its verdict JSON as its final message —
   validator personas are mechanically read-only — and the orchestrator
   persists it to
   `stages/<id>/validation/attempt-<n>/<validator>.verdict.json`.
   **Fail fast:** the first `fail` verdict ends the gate. Write `gate.json`.
6. **Decide.**
   - All verdicts `pass` → stage `passed`; continue to the next stage.
   - A verdict is `fail` and attempts ≤ `max_repair_attempts` → stage
     `repairing`; go to step 3 with the Repair Prompt (§7.3). Repair attempts
     use a **fresh producer context**: the failure verdicts and the prior
     artifacts are the ONLY feedback channel. Never resume or replay the prior
     producer's conversation.
   - Attempts exhausted → apply the gate's `on_exhaustion`:
     - `escalate` (default): write `escalations/<stage>.md` (§7.4), set run
       `escalated`, STOP, and surface the escalation to the user. The run
       remains resumable after human input.
     - `abort`: set run `aborted`, STOP.
7. **Complete.** After the last stage passes: assemble the manifest's `outputs`
   (name → artifact path) and report to the user using the SUMMARY format
   (§7.5). Set run `complete`.

### 3.2 Resume protocol

On any restart, context reset, or the instruction "resume run <id>":

1. Read `runs/<run-id>/task_state.json` and `workflow.lock.yaml`. Trust only
   these — not conversation memory.
2. Continue from the first stage whose status is not `passed`:
   `pending` → run it; `in_progress` → re-run from step 3 (produce);
   `validating` → re-run from step 5 (gate); `repairing` → step 3 with repair
   prompt; `escalated`/`awaiting_approval` → present the pending report or
   approval request to the user.
3. Never re-execute a `passed` stage.

The orchestrator may treat itself as freshly resumed at any time (after an
escalation, or every few stages on long workflows): re-read state, drop
accumulated context. This is always safe because of Principle 2.

## 4. State semantics

```
runs/<run-id>/
├── task_state.json          # resume anchor (schema: task-state.schema.json)
├── events.jsonl             # append-only: {ts, stage, event, detail}
├── request.md               # user request, verbatim
├── inputs.json              # resolved workflow-level inputs
├── workflow.lock.yaml       # frozen manifest incl. risk overlay
├── stages/<stage-id>/
│   ├── inputs.json          # input name → file path
│   ├── artifacts/           # producer outputs — validators read ONLY this
│   ├── summary.md           # ≤200 words — orchestrator reads ONLY this
│   ├── gate.json            # {status, attempts: [{n, verdicts, outcome}]}
│   └── validation/attempt-<n>/<validator-id>.verdict.json
└── escalations/<stage-id>.md
```

Stage statuses: `pending → in_progress → validating → (passed | repairing → in_progress … | escalated)`.
Run statuses: `running | awaiting_approval | escalated | complete | aborted`.

`task_state.json` shape (see schema for the full contract):

```json
{
  "run_id": "20260706-1430-sdlc-add-auth",
  "workflow": { "id": "sdlc", "lock": "workflow.lock.yaml" },
  "status": "running",
  "created_at": "2026-07-06T14:30:00Z",
  "updated_at": "2026-07-06T15:02:11Z",
  "classification": {
    "work_type": "new-feature",
    "risk": "high",
    "gates_applied": ["security", "release"],
    "assumptions": ["..."],
    "approval": { "required": true, "granted_at": null }
  },
  "current_stage": "design",
  "stages": {
    "intake": { "status": "passed", "attempts": 1,
                "artifacts": { "requirements": "stages/intake/artifacts/requirements.md" },
                "summary": "stages/intake/summary.md" },
    "design": { "status": "repairing", "attempts": 2, "artifacts": {}, "summary": null }
  }
}
```

## 5. Gate & repair policy

- Default gate policy comes from the manifest's `defaults.gate`; per-stage
  `gate` blocks override it. Default: `max_repair_attempts: 2`,
  `on_exhaustion: escalate`.
- Validators run in manifest order; `completeness-check` first (cheap contract
  conformance before expensive judgment). First failure short-circuits.
- A repair attempt = fresh producer subagent + failed verdicts + prior
  artifacts. Producer context never accumulates across attempts.
- Failure classes and their recovery policies are defined in
  `docs/failure-taxonomy.md` (F1–F7). Notably: tool/environment failures (F3)
  are retried once and do NOT consume the repair budget — they are not the
  producer's fault.
- Approval checkpoints (from the risk policy or the manifest) are gates owned
  by the human: the run cannot pass block-tier ones without explicit user
  approval.
- At any stop (an escalation or an approval checkpoint), a human may
  **tighten** the remainder of the run — adding approval checkpoints or
  validators to the lock file, recorded as a `lock_tightened` event in
  `events.jsonl`. Loosening the lock mid-run is never allowed.

## 6. Permission boundaries

Enforced by persona tool restrictions (mechanism) and document rules (policy):

- **Producers** write only inside `runs/<run-id>/stages/<their-stage>/`.
  Exception: the `builder` persona additionally modifies the target repo as
  directed by stage contracts that declare `target_repo` in
  `permissions.writes` (implement, document).
- **Validators** are mechanically read-only: their personas carry no Write
  tool, so they cannot alter anything (the `red-team` and `test-auditor`
  personas may execute commands to probe; `test-auditor` may additionally
  apply temporary mutations — in throwaway copies of the target repo, or as
  git-revertible edits it MUST fully restore before returning; neither may
  leave any persisted change). They return their
  verdict JSON as their final message; the orchestrator persists it.
  Validators read the stage's `artifacts/` directory and any paths the
  artifacts reference — never `summary.md`, never other stages' summaries,
  never producer reasoning.
- **The orchestrator** writes only run-state files (`task_state.json`,
  `events.jsonl`, `gate.json`, `inputs.json`, lock file, escalations) and reads
  only state + summaries.
- Known limitation (accepted for v1): these boundaries are policy-enforced, not
  sandbox-enforced. An SDK runtime executing the same manifests can enforce
  them with filesystem scoping.

## 7. Prompt templates

The orchestrator composes subagent prompts from these templates EXACTLY —
adding nothing else. What is absent from a template is deliberately absent.

### 7.1 Producer Prompt

```
You are executing stage <stage-id> of run <run-id>.

<full body of harness/stages/<stage>/stage.md, including frontmatter>

INPUTS (read these files):
<input name>: <path>   # one line per resolved input

OUTPUT DIRECTORY (write artifacts ONLY here):
runs/<run-id>/stages/<stage-id>/artifacts/

<if practice skills attached:>
PRACTICE SKILLS — read each of these files fully BEFORE starting, and apply
their disciplines to your work:
- <path to skillpacks/.../SKILL.md>

<if knowledge adapters attached:>
KNOWLEDGE ADAPTERS — these describe knowledge sources available to you:
<full body of each attached adapter.md>

When done: write summary.md (≤200 words: what was produced, key decisions,
open concerns) to runs/<run-id>/stages/<stage-id>/, then reply with exactly
one line confirming completion.
```

### 7.2 Validator Prompt

```
You are validating stage <stage-id> of run <run-id>. You are independent of
whoever produced these artifacts; judge only what is on disk.

<full body of harness/validators/<validator>/validator.md>

PARAMETERS:
<key>: <value>          # the `with` block, if any; binding values arrive resolved to paths (§3.1.5)
<if with.checklist:> CHECKLIST (apply every item):
<full body of harness/policies/gates/<gate>.md>

ACCEPTANCE CRITERIA (the contract you judge against):
<acceptance_criteria list from the stage frontmatter>

ARTIFACTS TO VALIDATE:
<path to runs/<run-id>/stages/<stage-id>/artifacts/ and its declared files>

Return your verdict as your final message: the complete verdict JSON in a
```json fenced block, followed by exactly one line: PASS or FAIL plus a
one-clause reason. You write no files — the orchestrator persists your verdict
to runs/<run-id>/stages/<stage-id>/validation/attempt-<n>/<validator-id>.verdict.json.
```

### 7.3 Repair Prompt

The Producer Prompt (§7.1), plus — inserted after INPUTS — the following block.
Nothing from the previous producer's conversation is ever included.

```
REPAIR ATTEMPT <n> of <max>.
A previous attempt produced artifacts that FAILED validation.

PRIOR ARTIFACTS (start from these; fix, don't restart unless criteria demand it):
runs/<run-id>/stages/<stage-id>/artifacts/

FAILURE REPORTS (address every finding):
<full contents of each failed verdict.json from attempt <n-1>>
```

### 7.4 Escalation report (`escalations/<stage>.md`)

```
# Escalation: <stage-id> — run <run-id>
## What was attempted        # one paragraph per attempt
## Verdict digest            # per attempt: validator → verdict, top findings
## Unresolved findings       # deduplicated, with evidence paths
## Decision needed           # the specific question(s) only a human can answer
## How to resume             # e.g. "relax criterion X / provide input Y, then: resume run <run-id>"
```

### 7.5 Final SUMMARY (reported to the user on completion)

```
SUMMARY
- What changed:
- Why:
- Files changed:            # or deliverable paths from manifest outputs
- Tests/verification:       # evidence, with paths to verification artifacts
- Risks or follow-ups:
```

If verification could not be run:
```
I could not run [test/check] because [reason].
I verified the change by [alternative evidence].
Recommended next validation: [specific command or check].
```

## 8. Versioning

- `manifest_version: "1.0"` — breaking manifest schema changes bump this and
  `workflow-manifest.schema.json` together.
- Locked runs are immune to library edits by construction (§3.0.3). A run
  started under one manifest version completes under it.
- Schema files are the SDK contract: an SDK runtime must execute any manifest
  this repo's lint accepts, implementing §3 exactly.
