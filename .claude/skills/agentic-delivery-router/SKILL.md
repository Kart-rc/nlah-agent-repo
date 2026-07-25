---
name: agentic-delivery-router
description: Routes delivery requests to the right harness workflow. Classifies work type and delivery risk, applies approval gates and risk overlays, then orchestrates the workflow per HARNESS.md. Use at the beginning of any non-trivial engineering or delivery request, and to resume runs.
---

# Agentic Delivery Router

## Overview

Use this skill at the beginning of any non-trivial delivery request. It turns
a raw requirement into a safe, validated delivery path:

```text
1. Understand the request
2. Classify the work type
3. Classify the risk level
3b. Select the execution mode (standard / autonomous / interactive)
4. Select the workflow manifest
5. Apply the risk overlay (extra validators + approval checkpoints)
6. Surface assumptions; decide whether approval is needed
7. Orchestrate the workflow per HARNESS.md - small stages, blocking gates
8. Report with verification evidence
```

This skill decides *routing, risk, gates, and approval*. Execution discipline
lives in the harness itself: stage contracts, independent validators, and the
orchestration protocol in `HARNESS.md` §3 — which this skill executes but
never restates. Practice disciplines (TDD, incremental implementation, ...)
attach to stages as skill-pack references in the manifest.

Do not use the full router for trivial work: typo fixes, formatting-only
changes, tiny documentation edits. For those, keep scope limited, verify the
final diff, and skip the harness.

## Core rule

Do not start any run until this block is complete and (where required)
approved:

```text
REQUEST CLASSIFICATION
- Work type:
- Risk level:
- Execution mode:
- Selected workflow:
- Mandatory gates (from risk policy):
- Assumptions:
- Files/areas likely involved:
- Verification plan:
- Approval needed before starting: Yes/No
```

Record this block in the run's `task_state.json` → `classification`.

## Step 1: Understand the request

Determine: what is the user trying to accomplish; does it change behavior;
does it touch production, users, data, infrastructure, cost, security, or
public contracts; is there an existing spec/issue/failing test; is it isolated
or cross-system. If unclear, ask the smallest number of clarifying questions
required to route safely. If context suffices, state assumptions and proceed.

## Step 2: Classify work type

Choose the closest primary type (multiple may apply; the primary drives
routing):

| Work type | Description |
|---|---|
| vague-requirement | Goal unclear or underspecified |
| idea-refinement | User wants options, tradeoffs, direction |
| new-feature | Adds behavior or capability |
| bug-fix | Corrects broken or unintended behavior |
| api-interface-change | Endpoint, SDK, contract, schema, public behavior |
| data-change | Pipeline, ETL, streaming, analytics, table, event, ML data |
| infrastructure-change | Cloud, deployment, networking, CI/CD, secrets, permissions, runtime |
| security-sensitive-change | Auth, PII, secrets, permissions, sensitive input/output |
| performance-cost-change | Latency, throughput, memory, query efficiency, cost, scale |
| refactor-simplification | Preserves behavior, improves structure |
| migration-deprecation | Moves users/data/systems or removes old behavior |
| observability-change | Logs, metrics, traces, dashboards, alerts, SLOs |
| production-launch | Releases or rolls out to users/production |
| proposal | Argues for a decision: business case, recommendation |
| technical-decision | Chooses between named technical options and records the call, time-bound |
| architecture-review | Judges an existing or proposed architecture with an evidence-cited verdict |

## Step 3: Classify risk level

**Low** — small doc updates, test-only improvements, localized bug fix with
clear tests, minor copy, small behavior-preserving refactor. *Behavior:*
proceed after stating assumptions; keep scope limited; verify the final diff.

**Medium** — new internal feature with contained blast radius, multi-file
change with clear ownership, non-breaking schema change, internal API change,
CI update not affecting production deployment. *Behavior:* run the workflow;
ask for approval only if assumptions materially affect behavior.

**High** — public API change, data pipeline change with downstream consumers,
auth/authz logic, PII handling, infrastructure or deployment change,
cost-sensitive path, migration or backfill, large refactor, cross-service
behavior change. *Behavior:* do not start producing stages until the plan is
approved; risk overlay adds security/release validators and an approval
checkpoint before implementation; rollback plan and blast-radius assessment
are required evidence.

**Critical** — data deletion, permission escalation, secret/credential
handling, payment/billing/compliance/regulated workflows, emergency production
mitigation, irreversible migration, customer-facing outage risk, broad
infrastructure change. *Behavior:* stop and request explicit human approval
before ANY producing stage; overlay adds a skeptical persona reviewer to every
stage; provide step-by-step execution and rollback plans; attach
`skillpacks/addyosmani/doubt-driven-development` to the implement stage.

The risk → validators/checkpoints mapping is data, not prose:
`harness/policies/risk-policy.yaml`.

## Step 3b: Select the execution mode

Software-change work types are served by a workflow family (`sdlc`,
`sdlc-autonomous`, `sdlc-interactive`); this step chooses among them. For
work types served by a single workflow, the mode is **standard** — skip
ahead.

- **standard** (default): the `sdlc` composition — validated stages, human
  contact at escalations and risk-overlay checkpoints only.
- **autonomous** (`sdlc-autonomous`): choose ONLY when the user asked for
  hands-off delivery AND ALL three hold:
  (a) a strong, spec-aligned deterministic verifier exists — the target repo
  has a runnable test suite and the request has testable acceptance
  criteria; (b) every planned action is reversible — git-revertible, no
  data migration, production deploy, or external side effects; (c) blast
  radius is contained — one repo/service, no public contract. High or
  Critical risk is never autonomous.
- **interactive** (`sdlc-interactive`): choose when the user wants to
  understand, approve, or learn from each stage ("walk me through",
  "teach me", "I approve each step") — or when the user asked for autonomy
  but a rubric condition fails and they still want stage-level involvement
  rather than standard mode.

User phrasing overrides the rubric **in the safe direction only**: a user
may always demand interactive; autonomous is granted only when the rubric
agrees. When a rubric condition fails an autonomy request, say which one and
offer interactive or standard.

Record the mode (and the rubric outcome that justified it) in the REQUEST
CLASSIFICATION block; in `task_state.json` it is carried as a
`classification.assumptions` entry — e.g. `"execution mode: autonomous
(verifier strong, actions reversible, blast radius contained)"`.

## Step 4: Select the workflow

1. Glob `harness/workflows/*/workflow.yaml`; read ONLY each manifest's
   `workflow.intent` block (summary, triggers, signals, work_types).
2. Match the classified work type and the request's language against those
   intent blocks.
3. Confidence rubric:
   - **One clear match** → select it.
   - **Multiple plausible** → ask the user to choose; never guess-and-run.
   - **No match** (routing failure, F7) → offer the `workflow-composer` skill,
     suggesting a stage composition for the unmapped work type (see the
     current mapping in `docs/future-workflows.md`); never force a request
     through the wrong workflow.
4. `vague-requirement` and `idea-refinement` route to intake-led workflows
   (v1: `proposal` for persuasion-shaped asks, `tech-decision` for
   decision-shaped asks with a nameable option set; otherwise clarify first —
   intake exists to convert vagueness into requirements).
5. `sdlc`, `sdlc-autonomous`, and `sdlc-interactive` share their work types
   deliberately: they are one family disambiguated by Step 3b's execution
   mode, never treated as a multiple-match ambiguity.

## Step 5: Collect inputs and initialize the run

1. Read the selected manifest's `inputs`; collect any missing required input
   from the user before starting. Inputs whose description marks them as
   orchestrator-resolved (e.g. `run_dir`) are filled at initialization and
   never requested from the user.
2. Initialize the run per `HARNESS.md` §3.0: create `runs/<run-id>/`, write
   `request.md` + `inputs.json`, apply the risk overlay from
   `harness/policies/risk-policy.yaml` while writing `workflow.lock.yaml`
   (append `additional_validators` to matching stages — `at_stage: "*"` means
   every stage; skip entries naming stages this workflow lacks; record
   `approval_checkpoints`), and initialize `task_state.json` with the
   REQUEST CLASSIFICATION.

## Step 6: Decide whether approval is needed

Approval is required before producing stages when: risk is High or Critical;
the requirement is ambiguous and assumptions materially affect behavior; the
work touches sensitive data, secrets, auth, access, billing, compliance, or
production; the change is irreversible or hard to roll back; it affects
multiple teams or downstream consumers; it introduces a new dependency or
platform pattern; it modifies public contracts; or you cannot verify the
change safely.

When approval is required, present:

```text
Approval required before starting because this is [High/Critical] risk.

Plan:            [stage order from the locked manifest + what each will do]
Rollback:        [strategy]
Verification:    [how the verify stage + gates will prove it]

Please approve or adjust the plan.
```

Record approval in `classification.approval.granted_at` before proceeding.

## Step 7: Orchestrate

Execute the locked manifest exactly per **`HARNESS.md` §3** (the orchestration
protocol — single source of truth). Honor `awaiting_approval` checkpoints from
the risk overlay.

**Context discipline (you are the orchestrator):**
- Never read stage artifacts — only `task_state.json` and `summary.md` files.
- Never paste artifact content into subagent prompts — pass file paths.
- Compose producer/validator/repair prompts from the HARNESS.md §7 templates,
  adding nothing.
- After an escalation, or every few stages on long runs, re-read state and
  drop accumulated context; the run resumes losslessly from disk.

**Resume:** on "resume run <run-id>", follow `HARNESS.md` §3.2 — trust
`task_state.json`, never conversation memory; never re-execute passed stages.

**Mid-run mode flip (autonomous → human-in-the-loop):** on any of these
triggers, stop treating the run as autonomous —
- the verifier cannot discriminate (the test-of-tests or verify gate shows
  the suite passes over broken code);
- an action outside the declared reversible set is reached (data migration,
  deploy, external side effect);
- a repair budget exhausts (failure class F5);
- the work drifts outside its classified type (novelty the classification
  did not anticipate).

Do not continue autonomously past the trigger: stop through the existing
§3.1 escalation/approval mechanics, append a `mode_flipped` event to
`events.jsonl`, and — with the user's consent — tighten the lock per
`HARNESS.md` §5 (add `mode: block` checkpoints before all remaining stages).
Never loosen the lock mid-run; the flip has one direction.

## Step 8: Report

On completion, deliver the SUMMARY block (HARNESS.md §7.5) filled from real
artifacts:

```text
SUMMARY
- What changed:
- Why:
- Files changed:
- Tests/verification:
- Risks or follow-ups:
```

If verification could not run: state what, why, what alternative evidence was
gathered, and the recommended next validation. On escalation, surface the
escalation report and the specific human decision needed.

## Response patterns

**Requirements clear** → "Proceeding with these assumptions, using the
<workflow> workflow: [stages]. Scope: [scope]. Verification: [plan]."

**Requirements ambiguous** → ask the single most valuable question, with why
it matters. Smallest number of questions possible.

**Requested approach is risky** → "I would not recommend that approach
because [concrete risk]. Safer alternative: [alternative]. If you still want
the original, confirm the tradeoff and I will proceed within agreed
constraints."

## Anti-patterns

Avoid: starting a run before the classification block is complete; skipping
assumptions for non-trivial work; guessing a workflow on an ambiguous match;
reading stage artifacts into orchestrator context; restating the HARNESS.md
protocol instead of referencing it; letting a gate failure pass silently;
mixing refactor and feature work without approval; claiming completion
without verification evidence; treating subagent output as inherently correct
(that is what gates are for).

## Final checklist

- [ ] Work type, risk, and execution mode classified; classification recorded in run state
- [ ] Workflow selected by intent match (or composer offered on F7)
- [ ] Risk overlay applied at lock time; approval obtained if required
- [ ] All stages passed their gates (or escalation surfaced honestly)
- [ ] SUMMARY delivered with verification evidence
