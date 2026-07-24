# Mapping: Executable-Agent-Skills Proposal → Harness Components

How [the proposal](2026-07-23-executable-agent-skills-sdlc.md) was
implemented in this repository. The proposal specifies skill *contracts* in
its own vocabulary (STATE_ROOT, task packets, AGENTS.md adapters); this
harness already had first-class equivalents for much of it, so the
implementation **translates** the proposal into the harness idiom rather
than duplicating machinery. `HARNESS.md` remains the constitution;
everything below composes under it.

## Scenario A — autonomous catalog (A0–A10)

| Proposal skill | Harness realization |
|---|---|
| A0 `sdlc-orchestrator` | Already present: `agentic-delivery-router` skill + the orchestration protocol in `HARNESS.md` §3. No new component. |
| A1 `context-acquisition` | Already present: `stages/intake` (+ `stages/research` in research-led workflows). **Added:** `skillpacks/provenance/context-register` for source visibility (see below). |
| A2 `architecture-and-adr` | `stages/design` already outputs `decisions` (`decisions.json`, machine-readable ADR list). **Added:** `skillpacks/addyosmani/documentation-and-adrs` attached to design in the new workflows; the new `stages/document` materializes the decisions as ADRs in the target repo. |
| A3 `planning-decomposition` | Already present: `stages/plan` (traceability `extra_check` in the manifests). |
| A4 `implementation` | Already present: `stages/implement` (+ TDD / incremental-implementation skillpacks). |
| A5 `test-generation-and-test-of-tests` | Split deliberately: test *generation* stays in `stages/implement` (TDD discipline); the *gate on the tooling itself* is the new **`validators/test-of-tests`** (mutation-style: seeded faults must make the suite fail), run by the new **`test-auditor` persona** (Bash, mutate-only-in-throwaway-copies, mandatory restoration proof). Attached to `implement` in both new workflows — `diff_manifest.json` gives the exact mutation target set, and a failed gate repairs the tests in the stage that owns them. |
| A6 `fresh-context-verification` | Already the harness's core architecture: every validator runs as a fresh subagent, different persona, no producer reasoning (HARNESS.md §3.1, §6, §7.2). `stages/verify` produces the evidence; validators judge it. |
| A7 `security-and-quality-gates` | Already present: `validators/red-team` + `policies/gates/security.md` + the risk overlay (`policies/risk-policy.yaml`). |
| A8 `documentation` | **New stage `stages/document`** (builder): repo docs + ADR materialization; `docs_manifest.json` restricted to documentation paths; judged by a new-team-member persona review. |
| A9 `deployment-readiness` | **New stage `stages/readiness`** (builder): concrete rollback procedure (missing/vague = blocking failure), health signals with rollback-trigger thresholds, per-concern go/no-go with evidence, judged against `policies/gates/release.md` + an on-call SRE persona. |
| A10 `retrospective-and-self-evolution` | **New stage `stages/retrospect`** (analyst): replays `events.jsonl`/`gate.json` against `docs/failure-taxonomy.md`, computes run metrics + context-usage stats, and proposes harness edits as **candidate diffs marked NOT APPLIED** — human ratification required, safety-critical proposals (HARNESS.md, personas, permissions, risk policy, approval logic) prominently flagged. The stage is forbidden from modifying the harness itself. |

Composed as **`harness/workflows/sdlc-autonomous`**: intake → design → plan
→ implement → verify → document → readiness → deliver → retrospect. No
manifest checkpoints; the risk overlay still merges its own at lock time, so
**risk trumps mode by construction** (High/Critical keep their approval
gates even in autonomous mode).

## Scenario B — human-in-the-loop catalog (B1–B11)

The proposal's B-catalog decomposes the same skills and adds a teaching +
approval layer. Implemented as **`harness/workflows/sdlc-interactive`**
(same nine stages) plus two mechanisms:

| Proposal mechanism | Harness realization |
|---|---|
| Teaching output (`EXPLAIN.md` per skill) | **`skillpacks/teaching/explain-your-work`** attached to every stage; the artifact is *required and allowed* by each stage's completeness-check `extra_check` (without which the harness's F4 scope-drift rule would reject the undeclared file). |
| Three-tier gating (auto / notify / block) | **Manifest-declared `approval_checkpoints`** — an additive `workflow-manifest.schema.json` extension. No checkpoint entry = auto (intake); `mode: notify` presents evidence and continues; `mode: block` stops for sign-off (before `implement` and `deliver`). Merged with the risk overlay at lock time — union by `before`, block wins, overlay checkpoints are always block-tier. Per-stage grants land in the new `classification.approvals` map (`task-state.schema.json`). |
| Clarifying questions ON | Producer subagents cannot interact mid-stage, so this is translated: EXPLAIN.md's mandatory **"Questions for you"** section surfaces at the next checkpoint, and the router asks more aggressively at input collection. A deliberate deviation, recorded below. |
| Human approves each stage (B1–B11 checkpoints) | The checkpoint tiers above + `max_repair_attempts: 1` in the interactive manifest, so failures reach the human fast instead of burning repair budget silently. |

## §4 decision framework

| Proposal element | Harness realization |
|---|---|
| A-vs-B decision rule | Router **Step 3b** (`.claude/skills/agentic-delivery-router/SKILL.md`): autonomous ONLY when the user asked for hands-off AND a strong spec-aligned verifier exists AND actions are reversible AND blast radius is contained; High/Critical risk is never autonomous; user phrasing overrides in the safe direction only. |
| Same skills, two modes | One stage library, three sdlc-family manifests sharing `work_types` deliberately; the router disambiguates by mode, never as a multiple-match ambiguity. |
| Threshold triggers that flip A→B mid-run | Router Step 7 "Mid-run mode flip": verifier cannot discriminate, irreversible action reached, repair budget exhausted (F5), or novelty — stop via §3.1 mechanics, `mode_flipped` event, tighten the lock per HARNESS.md §5 (block checkpoints before all remaining stages). One-way: never loosen mid-run. |

## Context visibility (user-raised requirement)

Visibility into *which gathered context is actually used* — the proposal's
A1 observability contract and its §5.1 handoff-recall warning (NLAH measured
information-handoff recall as low as 0.32 under parent-child execution):

| Layer | Harness realization |
|---|---|
| What each stage received | Already present: `stages/<id>/inputs.json` (file-level), knowledge-adapter citation rules (claim-level for adapter-sourced knowledge). |
| What was gathered | **`skillpacks/provenance/context-register`**: intake emits `context-register.md` — id (CR-n), source, provenance, relevance, key claim — including discarded sources. |
| What was used | Downstream stages cite `[context: CR-n]` on load-bearing decisions (design/plan `extra_check`s); the register itself is never mutated downstream. |
| The difference | `stages/retrospect` reports cited vs never-cited entries (wasted retrieval) and uncited load-bearing claims (fabrication risk) as run metrics. |

## Deliberate deviations from the proposal's letter

| Proposal convention | Harness equivalent | Why |
|---|---|---|
| `STATE_ROOT/` + `artifacts/manifest.json` | `runs/<run-id>/` + `task_state.json` (HARNESS.md §4) | Identical semantics (file-backed, path-addressable, compaction-stable state) already constitutional; two state models would violate Principle 1. |
| `children/<id>/TASK.md` task packets | HARNESS.md §7 prompt templates (producer/validator/repair) | Same mechanism — fresh context, file-path handoff, no reasoning leakage — already specified exactly once in the constitution. |
| AGENTS.md deterministic adapters | Knowledge adapters (`harness/knowledge/`) + stage contracts naming real commands + per-repo conventions | The harness binds mechanism per target repo through stage contracts and personas; a parallel adapter registry would drift. The proposal's "map, not manual" discipline is honored by this repo's own minimal `CLAUDE.md`. |
| `fork_context=true/false` | All producers and validators run fresh (`defaults.producer_context: fresh`; validators always fresh by §3.1.5) | The harness never inherits parent context; the proposal's stricter option is the only option here. |
| Retry cap default 5 | `max_repair_attempts` default 2 (3 on implement, 1 in interactive mode) | Harness budgets are per-gate with human escalation after exhaustion — cheaper failure surfacing than deep autonomous retry; caps remain one-line manifest edits. |
| Multi-candidate search (K=5, "used sparingly") | Not implemented | The proposal's own evidence (NLAH RQ3) shows it can hurt; nothing was built. |
| Self-evolution applies its own harness edits | `retrospect` proposals are NOT APPLIED by contract | Both the proposal (§A10 gates) and HARNESS.md demand human ratification for safety/permission logic; the harness extends that to all self-proposed edits. |

## Files added/changed (implementation index)

- `harness/schema/workflow-manifest.schema.json`, `harness/schema/task-state.schema.json` — additive `approval_checkpoints` / `classification.approvals`
- `HARNESS.md` §3.0.3, §3.1.1, §5, §6 — merge semantics, notify tier, tighten-only lock edits, test-auditor rules
- `.claude/agents/test-auditor.md`; `harness/validators/test-of-tests/`
- `harness/stages/document/`, `harness/stages/readiness/`, `harness/stages/retrospect/`; `harness/stages/deliver/` (optional `readiness_report` input)
- `harness/skillpacks/teaching/explain-your-work/`, `harness/skillpacks/provenance/context-register/`
- `harness/workflows/sdlc-autonomous/`, `harness/workflows/sdlc-interactive/`
- `.claude/skills/agentic-delivery-router/` — Step 3b, family disambiguation, mid-run flip
- `scripts/harness_lint.py` — manifest checkpoint validation
