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
| **Practice skill** | `harness/skillpacks/` | An engineering discipline the producer reads first (vendored and first-party packs) |

A workflow is just a `workflow.yaml` manifest listing which modules attach
where. Adding, removing, reordering, or swapping any module never requires
structural changes — and `scripts/harness_lint.py` verifies every composition.

## How to use this repo

There are four approaches, from fully harnessed to fully manual. Pick by how
much enforcement the work needs:

| # | Approach | Use when | Entry point |
|---|---|---|---|
| 1 | **Run a delivery workflow** | You have a delivery task and want risk-scaled rigor: blocking gates, repair loops, approvals, resumable state | Just describe the task — the `agentic-delivery-router` skill routes it |
| 2 | **Compose or modify a workflow** | The work type has no matching workflow, or you want to attach/detach/reorder modules | `workflow-composer` skill |
| 3 | **Use practice skills standalone** | You want one discipline or a lightweight sequence and will manage handoffs and review yourself | [`docs/using-skills-standalone.md`](docs/using-skills-standalone.md) |
| 4 | **Bootstrap Claude context in another repo** | A different repository needs Claude Code onboarding and layered project instructions | `bootstrap-claude-context` skill |

### 1. Run a delivery workflow (the default)

Open Claude Code in this repo and describe a delivery task:

> add rate limiting to the API client in ~/code/my-service

The **agentic-delivery-router** skill classifies the request (work type + risk
level), selects a workflow by matching the manifests' `intent` blocks, collects
required inputs, and orchestrates it per `HARNESS.md` §3 — stage by stage, each
in its own subagent context, each blocked by an independent validation gate.
High-risk work automatically gains extra validators and human-approval
checkpoints via `harness/policies/risk-policy.yaml`.

Four workflows ship in v1:

| Workflow | Deliverable | Key input |
|---|---|---|
| `sdlc` | Verified, delivered code change | `target_repo` — path to the codebase to change |
| `proposal` | Audience-ready business/technical case | `audience` |
| `tech-decision` | Time-bound decision record with rationale, dissent, revisit triggers | `audience`, optional `decision_deadline` |
| `architecture-review` | Evidence-cited verdict: approve / approve-with-conditions / reject | `subject` — path to the design doc, RFC, or codebase |

Run state externalizes to `runs/<run-id>/`; after any interruption or context
reset, say **"resume run \<run-id\>"** and the run continues losslessly from
`task_state.json`. Trivial work (typos, tiny doc edits) deliberately skips the
harness — the router keeps scope limited and verifies the diff instead.

To try it safely, point an SDLC run at the bundled toy target
(`examples/toy-cli/`), or read a trimmed snapshot of a real completed run —
including a gate failure → repair → pass cycle — in
[`docs/examples/sample-run/`](docs/examples/sample-run/README.md).

### 2. Compose or modify a workflow

> use the workflow-composer to build a roadmap workflow

The **workflow-composer** skill creates or edits `workflow.yaml` manifests by
composing existing stages, validators, knowledge adapters, and practice-skill
packs — then lints (`python3 scripts/harness_lint.py`) and dry-runs the result.
New machinery is the exception, not the rule: see
[`docs/future-workflows.md`](docs/future-workflows.md) for the work-type →
workflow mapping and worked composition examples, and
[`docs/adding-a-stage.md`](docs/adding-a-stage.md) when a genuinely new stage
is needed.

### 3. Use practice skills standalone (no harness)

The 35 practice skills in `harness/skillpacks/` (addyosmani, tech-director,
geoffreylitt, and review-debt packs) work directly in Claude Code — either
loaded by path from this repo or installed once into `~/.claude/skills/` for
`/skill-name` invocation across projects.
[`docs/using-skills-standalone.md`](docs/using-skills-standalone.md) provides
the setup, a manual invocation contract, and per-task sequences (feature, bug
fix, technical decision, architecture review, people/org work).

Standalone mode trades enforcement for lightness: no automatic risk routing,
no blocking validators, no repair loops, no resumable state — you manage
handoffs and review points yourself. Switch to approach 1 when the process
must be enforced rather than recommended.

### 4. Bootstrap Claude context in another repo

The **bootstrap-claude-context** skill installs a layered, self-improving
Claude Code instruction scaffold (project instructions, rules, learning loop)
into a target repository. It previews every write with a dry-run installer and
never mutates existing instructions without explicit approval.

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
| `harness/skillpacks/` | Practice skills: vendored `addyosmani` (MIT, attributed), original `tech-director` (director judgment disciplines), `geoffreylitt` (understanding AI-written code), and `review-debt` (evidence-backed code-review burden) |
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
- **review-debt**: first-party code-review guidance adapted from Sachin Gupta's
  “Your Coding Agent Is Creating Review Debt” talk, focused on reviewability
  and human understanding without penalizing AI assistance.
