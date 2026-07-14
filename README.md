# NLAH Magnetic Agentic Harness

A **magnetic harness** for repeatable delivery work — software changes,
proposals, technical decisions, architecture reviews, and (soon) roadmaps
and LOE estimates — built as a
[Natural-Language Agent Harness](https://arxiv.org/abs/2603.25723): all control
logic lives in editable natural-language documents, executed by Claude Code
acting as the harness runtime. There is no orchestration code to maintain;
changing the harness means editing a document.

## The magnetic metaphor

Workflows are composed from self-contained modules that **snap together and
apart with a one-line manifest edit**:

| Module | Library | What it contributes |
|---|---|---|
| **Stage** | `harness/stages/` | A unit of producer work with a contract: inputs, outputs, acceptance criteria |
| **Validator** | `harness/validators/` | An independent judgment task (adversarial review, red team, persona review, completeness) |
| **Knowledge adapter** | `harness/knowledge/` | An attachable knowledge source (enterprise MCP, second brain) |
| **Practice skill** | `harness/skillpacks/` | An engineering discipline the producer reads first (vendored [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)) |

A workflow is just a `workflow.yaml` manifest listing which modules attach
where. Adding, removing, reordering, or swapping any module never requires
structural changes — and `scripts/harness_lint.py` verifies every composition.

## Quickstart

Open Claude Code in this repo and describe a delivery task:

> add rate limiting to the API client in ~/code/my-service

The **agentic-delivery-router** skill classifies the request (work type + risk
level), selects a workflow, collects required inputs, and orchestrates it —
stage by stage, each in its own subagent context, each blocked by an
independent validation gate. High-risk work automatically gains extra
validators and human-approval checkpoints.

To create or modify a workflow:

> use the workflow-composer to build a roadmap workflow

## Why validation is the centerpiece

Every stage carries **acceptance criteria** and is judged by an **independent
validator subagent** — a different persona, in a fresh context that never sees
the producer's reasoning. Failing a gate triggers a bounded repair loop (fresh
producer + the failure report), then structured human escalation. Gates are
never silently skipped. Risk level (from the router's rubric) scales the rigor:
Critical work cannot start without explicit human approval.

## Repo map

| Path | What it is |
|---|---|
| `HARNESS.md` | **The constitution**: runtime charter, orchestration protocol, state semantics, prompt templates |
| `.claude/skills/agentic-delivery-router/` | Entry point: classify → select workflow → orchestrate |
| `.claude/skills/workflow-composer/` | Create/modify workflow manifests (scaffold, lint, dry-run) |
| `.claude/agents/` | Subagent personas: 3 producers, 4 validators (tool permissions = boundaries) |
| `harness/workflows/` | Composed workflows: `sdlc`, `proposal`, `tech-decision`, `architecture-review` |
| `harness/stages/` | Stage library (12 stages; `intake` is shared across workflows) |
| `harness/validators/` | Validator library (4 types, parameterizable) |
| `harness/knowledge/` | Knowledge adapters: `enterprise-mcp`, `second-brain` |
| `harness/policies/` | Risk policy (risk → validators + approvals) and gate checklists |
| `harness/skillpacks/` | Practice skills: vendored `addyosmani` (MIT, attributed) + original `tech-director` (director judgment disciplines) |
| [`docs/using-skills-standalone.md`](docs/using-skills-standalone.md) | Claude Code setup, handoff contract, and sequences for using practice skills without the harness |
| `harness/schema/` | JSON Schemas — the SDK-ready contracts for every document type |
| `scripts/harness_lint.py` | Validates schemas, cross-refs, validator coverage, topology |
| `runs/` | Externalized run state (gitignored; resumable via `task_state.json`) |
| `docs/` | Architecture (paper-concept mapping), failure taxonomy, how-tos, future workflows |

## Design lineage

- **NLAH paper** (arXiv 2603.25723): contracts, roles, stage structure,
  externalized state, failure taxonomy, adapters — mapped to repo components in
  [`docs/architecture.md`](docs/architecture.md).
- **agentic-delivery-router**: work-type taxonomy, risk rubric, mandatory
  gates, and approval discipline merged into the harness-native router skill.
- **addyosmani/agent-skills**: 24 practice skills vendored as an attachable
  skill pack.
