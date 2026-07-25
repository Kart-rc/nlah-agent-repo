# Executable Agent Skills for Autonomous and Human-in-the-Loop SDLC: An NLAH-Grounded Proposal

## TL;DR

- **Use one shared harness for the two modes, not two codebases:** for a fully autonomous SDLC (Scenario A), compose the skills under a single end-to-end harness with a parent orchestrator and fresh-context child workers; for the human-in-the-loop SDLC (Scenario B), decompose the *same* skills into human-invoked, stage-by-stage units that add teaching outputs (`EXPLAIN.md`) and three-tier approval gates. Both inherit one runtime charter and one file-backed state model taken directly from NLAH (Pan et al., arXiv:2603.25723).
- **Design priorities are set by NLAH’s empirical findings:** acceptance-gated **self-evolution** was the strongest module (SWE-bench 73.0→78.8, OSWorld 44.4→52.8), **file-backed state** was the most reliable structural module (+2.6 SWE, +13.9 OSWorld),  and modules that don’t tighten alignment to the final acceptance condition (multi-candidate search, aggressive context compression) can *hurt* — so more structure is not automatically better.
- **Default to full autonomy only when a strong, spec-aligned deterministic verifier exists AND the action is reversible AND blast radius is contained;** absent any one of those, decompose into human-invoked skills with approval gates. Keep each catalog small and role-routed — skill-selection accuracy collapses past a critical library size due to semantic confusability (Li, arXiv:2601.04748), and curated focused skills (2–3 modules) outperform exhaustive bundles (SkillsBench, arXiv:2602.12670).

-----

## Key Findings

1. **The harness is the durable, model-independent asset — not the prompt.** NLAH externalizes harness policy (roles, contracts, stages, state, recovery, stopping) as editable natural language executed by an Intelligent Harness Runtime (IHR), keeping exact mechanisms (tests, parsers, sandboxing, validators) in code. SKILL.md bundles are the natural-language instruction carriers this proposal treats as NLAH modules with deterministic script/adapter hooks. NLAH compressed a 60.1k-token code harness to a 2.9k-token readable policy on Live-SWE while matching task performance — evidence that policy belongs in inspectable text and mechanism belongs in code.
1. **Self-evolution and file-backed state are the high-ROI modules; branching and compression are traps.** In NLAH’s RQ3 ablation, self-evolution (acceptance-gated retry, default cap 5) and file-backed state gave the largest, most reliable gains, while multi-candidate search dropped SWE performance (73.0→71.4) despite 5× more agent calls, and context compression hurt both benchmarks (OSWorld 44.4→36.1). The lesson: instrument the acceptance loop hard, externalize state to paths, and add branching/compression only when they demonstrably tighten the path to acceptance.
1. **Fresh-context, independent verification is non-negotiable and is the one place multi-agent structure always pays.** A model reviewing its own work in-context confirms its own assumptions; independent review with a fresh context (ideally a different model family), receiving only the diff + spec + static-scan results and running fail-closed, disrupts systematic errors. This is the concrete realization of the user’s “independently verifiable by a different agent with no development context” pillar.
1. **Curated skills help measurably but self-generated skills don’t, and libraries have a hard scaling ceiling.** SkillsBench found curated skills raise average pass rate by 16.2 percentage points (range +4.5 pp software engineering to +51.9 pp healthcare; 86 tasks / 11 domains; 7,308 trajectories / 7 agent-model configs), self-generated skills give no benefit on average, and focused 2–3-module skills beat exhaustive ones. Selection accuracy degrades sharply past a critical library size due to semantic confusability — bounding catalog growth and motivating hierarchical routing.
1. **Context-file discipline is empirically load-bearing.** ETH Zurich’s evaluation (Gloaguen et al., arXiv:2602.11988, Feb 2026) found context files gave “no improvement in task success rates, while also increasing inference cost by over 20%”; LLM-generated files reduced success in 5 of 8 settings and developer-written files added only ~+4 pp — so AGENTS.md must be minimal, high-signal, and human-authored. OpenAI’s Codex field report echoes this: “AGENTS.md should be a map, not a manual… Keep it short (~100 lines),” and the repository is the system of record (“if knowledge isn’t in the repository, it doesn’t exist for agents”).

-----

## Details

## 1. Shared Runtime Charter and Workspace Conventions

This charter is the fixed, cross-skill layer both scenarios inherit — the analog of NLAH’s “runtime policy / charter” that turns a base agent into IHR. It is stack-agnostic: every deterministic operation is named as a generic *adapter* bound per project.

### 1.1 Roles (non-overlapping responsibilities)

- **Orchestrator (parent):** interprets the active skill/NLAH, launches children, supervises handoffs, enforces gates and stopping, and records the ledger. Per NLAH’s runtime-only-parent rule, the parent does **not** do substantive task work; even a nominally single-agent run is realized as “parent + one executor child” so the control/execution boundary stays inspectable. 
- **Solver (executor child):** performs the actual work (research, design, code, tests) inside its own workspace.
- **Verifier (fresh-context child):** checks a candidate against the spec/rubric with the lightest sufficient materials, runs at least one independent check, and returns exactly one verdict label plus a report. It does **not** repair the work.
- **Researcher (child):** gathers internal/external context, distills, and returns only the relevant findings by path (context-pollution control).

### 1.2 Canonical workspace (adapted from NLAH Appendix B/C/F)

```
/workspace
  STATE_ROOT/                 # durable runtime state, separate from deliverables
    RESPONSE.md               # stable run-level status file
    NLAH.md                   # active harness policy (the composed skill set)
    task_history.jsonl        # append-only launch/promotion ledger
    memory.md                 # markdown memory (stable headings)
    children/<id>/
      TASK.md                 # task packet handed to a child
      NLAH.md                 # optional child-specific policy overlay
      RESPONSE.md             # child's written-back result
  artifacts/
    manifest.json             # index of promoted, judgeable deliverables
    evidence/<stage>.md       # evidence documents (evidence-backed answering)
    adr/NNNN-*.md             # architecture decision records
  src/, tests/, docs/         # project tree (per-project)
```

**State semantics (the load-bearing convention).** Nothing counts as “transferred” until it exists as a named file under `STATE_ROOT` — TASK.md, NLAH.md, RESPONSE.md, or a promoted artifact.  State is file-backed, path-addressable, and compaction-stable: later agents reopen files by path before planning, verification, handoff, or final reporting.  Durable intermediate state lives under `STATE_ROOT`; judgeable deliverables live under `artifacts/`.  This mirrors Anthropic’s long-running-agent harness (an initializer writes a durable environment;  each session leaves clear artifacts and a `claude-progress.txt`-style status for the next fresh context) and OpenAI’s Codex “map, not a manual” principle.

**Task packets.** Parent→child handoff is exactly the `children/<id>/TASK.md` prompt string plus referenced paths. Claude Code subagents start with a fresh context window; the only channel from parent to child is that packet, so it must contain every path, error message, and decision the child needs. Children write `RESPONSE.md`; the parent promotes results into `artifacts/manifest.json`. This is the concrete mechanism for context-pollution control: a child may read dozens of files, but the main conversation only receives a summary.

**Context semantics.** Following IHR: `fork_context=true` means a child inherits the parent’s accumulated context; `fork_context=false` means a fresh, independent child that receives only its task packet. Verifiers and independent researchers MUST run `fork_context=false` to preserve adversarial independence.

### 1.3 Deterministic adapters (bound per project via AGENTS.md)

Named generic hooks — never hardcode a language/cloud: **test-runner**, **linter**, **static-analyzer/type-checker**, **build-tool**, **formatter**, **security-scanner (SAST/dependency/secret)**, **coverage-tool**, **retrieval/search adapter**, **parser**, **artifact-validator**, **deploy/readiness checker**. Bindings live in a repo-root `AGENTS.md` — the cross-tool open standard released August 2025, donated to the Linux Foundation’s Agentic AI Foundation in December 2025,  and adopted by more than 60,000 open-source projects and agent frameworks (Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, VS Code). Keep AGENTS.md minimal and high-signal: commands, non-standard constraints, and “never touch” rules — ETH Zurich research (Gloaguen et al., arXiv:2602.11988) found context files gave no success-rate improvement while raising inference cost by over 20%, and that human-written files should “describe only minimal requirements.”

### 1.4 Failure taxonomy (drives recovery in every skill)

|Failure mode    |Detection                             |Recovery action                                                          |
|----------------|--------------------------------------|-------------------------------------------------------------------------|
|Missing artifact|Expected path absent in manifest      |Re-open ledger; re-run producing stage; if absent, fail-closed           |
|Wrong path      |Read returns nothing / schema mismatch|Normalize path via adapter; reconcile against manifest                   |
|Verifier failure|Verdict = FAIL                        |Enter self-evolution repair loop (reflect → redesign → retry)            |
|Tool error      |Non-zero adapter exit                 |Classify (transient vs deterministic); retry transient once; else surface|
|Timeout         |Wall-clock/step budget exceeded       |Write compaction-stable state; stop honestly; report incomplete          |
|Contract breach |Output fails format/validation gate   |Reject; return to solver with the specific gate that failed              |

### 1.5 Runtime defaults

Retry cap default 5 (self-evolution); candidate budget K default 5 (used sparingly — see §5); honest-stop semantics (never claim success on the last failed attempt); contract-first completion (benchmark/spec output is the primary gate); permission/sandbox enforced in code, not prose (NLAH keeps safety, permissions, evaluation, and parsing logic in code by design).

-----

## 2. Scenario A — Fully Autonomous SDLC Skill Catalog

Scenario A composes all skills under **one end-to-end harness** with the orchestrator driving the plan → execute → verify → repair topology across the SDLC, minimizing human touchpoints. Each skill below is fully specified in SKILL.md-bundle style.

### A0. `sdlc-orchestrator` (meta-skill / harness entry)

- **Role(s):** Orchestrator.
- **Trigger:** A high-level goal is submitted for autonomous delivery (“build/ship X end to end”).
- **Inputs (contract):** goal statement; repo root + AGENTS.md adapter bindings; risk tier; budget caps.
- **Outputs (contract):** populated `STATE_ROOT` + `artifacts/manifest.json`; final RESPONSE.md with deliverable paths and evidence links; retrospective.
- **Stage structure:** clarify → research → architect(ADR) → plan/decompose → implement → test+test-of-tests → fresh-context verify → security/quality gates → docs → deployment-readiness → retrospective/self-evolution.
- **Adapters:** all (delegated to child skills).
- **State:** owns `task_history.jsonl` and `manifest.json`; writes stage-boundary compaction-stable state.
- **Gates:** each stage must write its evidence artifact before the next stage starts; a failed gate routes to repair, not forward.
- **Retry/stop:** per-stage self-evolution loop (cap 5); global honest-stop on budget exhaustion.
- **Failure taxonomy:** all six modes; orchestrator owns routing.
- **Observability:** emits per-stage LLM/tool call counts, tokens, wall-clock, gate pass/fail, retry counts, and % work delegated to children (NLAH observed ~90% of tokens in child agents on SWE-bench).

### A1. `context-acquisition` (requirements + internal/external research)

- **Role(s):** Researcher (children, `fork_context=false`), Orchestrator.
- **Trigger:** Start of run, or whenever the goal/spec is underspecified.
- **Inputs:** goal; access to internal knowledge (repo, docs, ADRs) and external retrieval adapter.
- **Outputs:** `artifacts/evidence/context.md` — distilled findings, confirmed goal, tooling/language/framework expectations bound to work type, and an explicit assumptions/open-questions list. In autonomous mode, ambiguities are resolved by documented assumption (logged) rather than blocking.
- **Stage structure:** scope → retrieve (internal, then external) → distill → write context evidence.
- **Adapters:** retrieval/search, parser.
- **State:** writes `context.md`; appends sources to manifest with provenance.
- **Gates:** every release-critical claim must be cited (evidence-backed answering); uncited claims block downstream design.
- **Retry/stop:** re-research if verifier flags unsupported assumptions.
- **Failure taxonomy:** wrong path / missing artifact on retrieval; tool error on search adapter.
- **Observability:** # sources retrieved vs cited, distillation ratio (tokens in child vs surfaced), unresolved-assumption count.
- **Systems note:** *Inflow*: raw internal+external knowledge. *Outflow*: distilled, cited context. *Hidden assumption*: retrieval adapter coverage is adequate. *Cost of inaction*: building on a wrong goal — the most expensive SDLC error.

### A2. `architecture-and-adr` (design decisions + ADR generation)

- **Role(s):** Solver (child), Verifier (design review).
- **Trigger:** After context is accepted, before planning; or when a change affects overall architecture.
- **Inputs:** `context.md`; constraints (NFRs, security, performance).
- **Outputs:** design doc + one `artifacts/adr/NNNN-*.md` per significant decision in MADR format (title, context, decision, consequences, alternatives considered). ADR criteria: document if a decision affects multiple modules OR has multiple viable alternatives with significant trade-offs.
- **Stage structure:** derive options → evaluate trade-offs → decide → record ADR → design-review gate.
- **Adapters:** static-analyzer (feasibility probes), parser.
- **State:** ADRs are immutable point-in-time records; supersession creates a new ADR.
- **Gates:** ADR “why/context” must be grounded in `context.md`, not fabricated (agent-generated ADRs risk fabricating rationale — flag inferred rationale explicitly).
- **Retry/stop:** design-review verifier can reject and force re-decision.
- **Failure taxonomy:** contract breach (missing consequences/alternatives).
- **Observability:** # ADRs, # alternatives evaluated per decision, review verdicts.

### A3. `planning-decomposition`

- **Role(s):** Solver (child), Orchestrator.
- **Trigger:** After architecture accepted.
- **Inputs:** design doc + ADRs.
- **Outputs:** a tree-structured task plan (write-todos style) in `STATE_ROOT/plan.md`, each task with a non-overlapping responsibility and an explicit success condition; independence flags for parallelizable branches.
- **Stage structure:** classify task shape → decompose → assign success conditions → mark independence.
- **State:** plan.md is reopened before each implementation task.
- **Gates:** every task must have a testable acceptance condition before implementation begins.
- **Retry/stop:** re-plan on repeated downstream verifier failure.
- **Failure taxonomy:** contract breach (task without acceptance condition).
- **Observability:** task count, dependency depth, parallelizable fraction.

### A4. `implementation`

- **Role(s):** Solver (executor child).
- **Trigger:** A planned task with an acceptance condition is ready.
- **Inputs:** task packet (`children/<id>/TASK.md`), relevant paths, coding conventions from AGENTS.md.
- **Outputs:** code changes; updated `RESPONSE.md` with changed paths and rationale; entry in ledger.
- **Stage structure:** inspect → edit → self-check (lint/build) → write response.
- **Adapters:** build-tool, linter, formatter, test-runner (local).
- **State:** all changes land as files; no change is “done” until written and manifest-indexed.
- **Gates:** must pass build + lint before handing to verification.
- **Retry/stop:** self-evolution loop on failed local checks (cap 5).
- **Failure taxonomy:** tool error, timeout, wrong path.
- **Observability:** files touched, build/lint status, retry count.

### A5. `test-generation-and-test-of-tests`

- **Role(s):** Solver (child) for tests; Verifier (fresh child) for the test-of-tests.
- **Trigger:** After (or, in TDD mode, before) implementation of a task.
- **Inputs:** acceptance condition; spec/rubric; code under test.
- **Outputs:** test suite; `artifacts/evidence/test_quality.md` documenting coverage and a **test-of-tests** result — verifying the verification tooling itself (mutation-style: confirm tests fail on deliberately broken code; confirm the test-runner adapter actually executes and reports).
- **Stage structure:** derive cases from spec → write tests → run against correct code (expect pass) → run against seeded fault (expect fail) → record.
- **Adapters:** test-runner, coverage-tool.
- **State:** test-quality evidence in manifest.
- **Gates:** a test suite that passes against a seeded fault is rejected (the verifier tooling is broken).
- **Retry/stop:** regenerate tests if test-of-tests fails.
- **Failure taxonomy:** verifier failure (tests don’t discriminate), tool error.
- **Observability:** coverage %, mutation/seeded-fault catch rate, false-negative count.
- **Systems note:** this is the “verify the tooling itself” pillar. *Cost of inaction*: green tests that certify nothing — the most dangerous false signal in autonomous mode.

### A6. `fresh-context-verification`

- **Role(s):** Verifier (fresh child, `fork_context=false`, ideally a different model family).
- **Trigger:** After implementation + tests pass locally; before any gate promotion.
- **Inputs:** ONLY the diff + spec/acceptance criteria + static-scan results — no builder reasoning, no shared context.
- **Outputs:** JSON verdict (`passed: true/false`) + report naming checks run; fail-closed (unparseable = fail; any security or logic finding ⇒ fail).
- **Stage structure:** identify claim → break into subclaims → audit completeness/correctness → run ≥1 independent check → verdict.
- **Adapters:** test-runner, static-analyzer, security-scanner.
- **State:** verdict written to `artifacts/evidence/verification-<task>.md`.
- **Gates:** verdict must remain close to the *final* acceptance criterion (NLAH: verifiers help only when their local object of judgment tracks the true gate — otherwise gains can diverge; verifier gave only +0.2 on SWE but +8.4 on OSWorld precisely because alignment differed).
- **Retry/stop:** FAIL routes to self-evolution repair; a third fresh context does the fix (not builder, not verifier).
- **Failure taxonomy:** verifier failure; contract breach on unparseable output.
- **Observability:** verdict, subclaims checked, independent checks run, escapes caught.
- **Systems note:** independence is the value. *Hidden assumption*: the verifier’s spec is the true spec. *Alternative*: same-model self-review — rejected, because a model reviewing its own work in-context confirms its own assumptions.

### A7. `security-and-quality-gates`

- **Role(s):** Verifier (child), Orchestrator.
- **Trigger:** Before deployment-readiness.
- **Inputs:** full diff, dependencies, config.
- **Outputs:** `artifacts/evidence/security.md` — SAST, dependency/secret scan, quality thresholds (baseline-relative: fail only on NEW regressions vs a pre-change snapshot).
- **Adapters:** security-scanner, static-analyzer, coverage-tool.
- **Gates:** any hardcoded secret, injection vector, or new critical regression = hard block.
- **Retry/stop:** auto-fix loop (cap 2) on specific findings, then re-scan.
- **Failure taxonomy:** contract breach, tool error.
- **Observability:** findings by severity, regressions introduced vs baseline, fix-loop iterations.

### A8. `documentation`

- **Role(s):** Solver (child).
- **Trigger:** After verification passes.
- **Inputs:** code, ADRs, evidence artifacts.
- **Outputs:** updated README/API docs; changelog; AGENTS.md updates if conventions changed (treat context files as version-controlled config reviewed in PRs).
- **Gates:** docs must reference actual artifact paths.
- **Observability:** doc coverage of public surface, staleness flags.

### A9. `deployment-readiness`

- **Role(s):** Verifier + Orchestrator.
- **Trigger:** All prior gates green.
- **Inputs:** build artifacts, deployment config, readiness checklist.
- **Outputs:** `artifacts/evidence/readiness.md` — build reproducibility, rollback plan, health checks, feature-flag/exit-code contracts.
- **Adapters:** build-tool, deploy/readiness checker.
- **Gates:** rollback path and health/heartbeat contract must exist (guarding the “silent failure” mode where an agent process green-dashboards while doing nothing).
- **Retry/stop:** block on missing rollback.
- **Observability:** readiness checklist pass rate, rollback presence.

### A10. `retrospective-and-self-evolution`

- **Role(s):** Orchestrator + Verifier.
- **Trigger:** Run end (success or honest-stop).
- **Inputs:** `task_history.jsonl`, gate outcomes, retry logs.
- **Outputs:** `artifacts/evidence/retro.md` — failure-mode analysis, and proposed **harness edits** (NLAH module tweaks, adapter fixes) captured as candidate skill/AGENTS.md diffs for human ratification.
- **Stage structure:** replay ledger → classify failures → propose harness deltas → (autonomous: stage them; do not silently self-modify safety/permission logic).
- **Gates:** self-modifications to permission/safety/parsing logic are NEVER auto-applied (kept in code, human-ratified).
- **Observability:** failure-mode histogram, proposed-vs-accepted harness edits, trajectory-analysis findings (“agents that analyze their own traces to fix harness-level failure modes” — an open LangChain research direction).
- **Systems note:** this is NLAH’s strongest module (self-evolution: +5.8 SWE, +8.4 OSWorld). *Cost of inaction*: repeating the same failure every run.

-----

## 3. Scenario B — Human-in-the-Loop Interactive SDLC Skill Catalog

Scenario B **decomposes the same skills** into human-invoked units. The human sits in the middle, invoking one skill per decision point, gaining deep understanding of both process and code. Deltas from Scenario A (not repetition) are highlighted; each skill retains its full spec via inheritance from §2 plus the additions below.

**Universal B-deltas applied to every skill:**

- **Teaching output:** every skill emits, alongside its artifact, an `EXPLAIN.md` — plain-language “what I did, why, what I assumed, what alternatives I rejected, and what you should check.” (Anthropic’s evaluator-agent lesson: turn subjective judgment into concrete, gradable criteria the human can read.)
- **Decision checkpoint + approval gate:** the skill pauses via an `interrupt()`-style mechanism (durable, resumable state persisted to `STATE_ROOT`; LangGraph checkpointing / OpenAI Agents SDK RunState serialization), presenting a one-screen decision interface: inputs, output, reasoning, what changes, how to undo. Three-tier gating — auto-approve (safe/reversible reads), notify (recoverable), block (irreversible/high-stakes).
- **Clarifying questions are ON:** instead of resolving ambiguity by assumption, the skill asks the human targeted questions first.
- **No forward progress without human sign-off** on block-tier actions; each decision is logged with reviewer, timestamp, and exact arguments.

### B1. `interactive-requirements-clarification` (delta from A1)

- **Delta:** Does NOT auto-resolve ambiguities. Produces a structured question set and a draft goal statement; **blocks** until the human confirms goal, scope, and tooling/framework expectations. Emits `EXPLAIN.md` teaching *why* each question matters. Approval gate: human ratifies the confirmed goal before research proceeds.
- **Checkpoint:** “Is this the right problem?” — the highest-leverage human decision.

### B2. `guided-research` (delta from A1 research portion)

- **Delta:** Runs independent researcher children (context-pollution control preserved), but surfaces a **decision-ready research brief** with sources ranked by relevance and an explicit “what I did NOT investigate.” Human selects which threads to deepen. Checkpoint: approve the knowledge base before design.

### B3. `interactive-architecture-adr` (delta from A2)

- **Delta:** Presents 2–3 architecture options **side by side** with trade-offs, then requests a human decision; the chosen option becomes the ADR with the human recorded as decision-maker. Teaching output explains each trade-off in depth. This is where the user “gains deep understanding” — ADRs become a shared reasoning surface between human and agent.
- **Checkpoint (block-tier):** architecture decisions are irreversible-expensive; always human-approved.

### B4. `interactive-planning` (delta from A3)

- **Delta:** Proposes the decomposition; human edits/re-prioritizes the task tree before any implementation. Emits an estimated blast-radius per task so the human can decide which tasks to supervise closely vs let run.

### B5. `pair-implementation` (delta from A4)

- **Delta:** Implements one task at a time; after each, emits a diff walkthrough (`EXPLAIN.md`) narrating the change and its rationale so the human learns the code. **Notify-tier** for normal edits (human can undo), **block-tier** for schema/migration/dependency changes. Human approves each diff before commit.

### B6. `test-coaching` (delta from A5)

- **Delta:** Shows the human the derived test cases and the **test-of-tests** result explicitly (“here’s proof your tests actually fail on broken code”), teaching test design. Human can add cases before acceptance. Checkpoint: approve the test suite as the acceptance oracle.

### B7. `review-companion` (delta from A6)

- **Delta:** The fresh-context verifier runs as in A6, but its report is written **for the human** — severity-ranked, with plain-language explanations of each finding and suggested fixes the human chooses among. The human is the final approver of the verdict; the agent never self-certifies to merge. Supports the explicit human-driven loop: “review in fresh context, fix, re-test, repeat.”

### B8. `security-quality-explainer` (delta from A7)

- **Delta:** Presents findings with severity, exploitability, and remediation options; human decides accept/fix/waive (waivers logged with justification). Teaching output explains each vulnerability class.

### B9. `doc-and-knowledge-transfer` (delta from A8)

- **Delta:** Generates docs AND a “reading guide” onboarding the human to the changed code; flags where human tacit knowledge should be captured into AGENTS.md/ADRs.

### B10. `readiness-review` (delta from A9)

- **Delta:** Presents the readiness checklist as a go/no-go decision board; **block-tier** human sign-off required before any deploy action. Human owns the deploy decision.

### B11. `guided-retrospective` (delta from A10)

- **Delta:** Facilitates a joint retro: surfaces failure modes and *proposes* harness/skill improvements, but the human ratifies every change to the harness. Teaching output: “here’s what our process got wrong and how we’d tighten the acceptance loop.” This directly serves the user’s goal of understanding the *process*, not just the code.

**Shared skills used identically in both catalogs:** the deterministic adapter bindings (§1.3), the failure taxonomy (§1.4), and the file-backed state model (§1.2) are scenario-invariant. Only the orchestration topology (one harness vs stage-by-stage invocation) and the human-facing teaching/approval layer differ.

-----

## 4. Decision Framework: Full Autonomous Harness vs Individual Human-Invoked Skills

Use this rubric per task (or per stage). Score each dimension; a preponderance toward the right column pushes toward Scenario B (human-in-the-loop, decomposed skills).

|Dimension                     |→ Full autonomous harness (A)                              |→ Human-invoked skills (B)                                |
|------------------------------|-----------------------------------------------------------|----------------------------------------------------------|
|**Task risk**                 |Low; errors cheap                                          |High; errors costly/regulated                             |
|**Reversibility**             |Easily reversible (feature flag, revert)                   |Irreversible (data migration, prod deploy, external comms)|
|**Novelty**                   |Routine, well-trodden pattern                              |Novel/ambiguous; no established pattern                   |
|**Need for learning**         |None — throughput is the goal                              |High — human wants to understand process + code           |
|**Verification confidence**   |Strong deterministic verifier exists (test-of-tests passes)|Weak/subjective acceptance; rubric needs human judgment   |
|**Blast radius**              |Contained to one module/branch                             |Cross-cutting; many consumers                             |
|**Cost of action vs inaction**|Cost of delay > cost of error                              |Cost of error > cost of delay                             |
|**Spec clarity**              |Goal well-defined, acceptance testable                     |Goal fuzzy; requirements likely to shift                  |

**Decision rule (BLUF):** Default to the autonomous harness ONLY when a strong, spec-aligned deterministic verifier exists AND the action is reversible AND blast radius is contained. Absent any one of those, decompose into human-invoked skills with approval gates. This aligns with NLAH’s core finding — modules (and by extension full harnesses) help only when intermediate behavior is tightly aligned with the final acceptance condition;  where that alignment is weak or unverifiable, a human must supply the acceptance judgment. It also matches the industry pattern (OpenAI Codex agent-first: humans steer via PRs and CI; Anthropic: “separating the agent doing the work from the agent judging it proves to be a strong lever”).

**Threshold triggers that flip A→B mid-run:** verifier confidence drops (test-of-tests fails to discriminate); a block-tier action is reached; the self-evolution loop hits its retry cap without passing; novelty detected (agent low-confidence / conflicting evidence → escalate to clarification mode).

-----

## 5. Systems-Thinking Analysis

### 5.1 Inflows / outflows per skill family

- **Context family (A1/B1–B2):** In = raw internal+external knowledge; Out = distilled cited context. Bottleneck: retrieval coverage and distillation fidelity. NLAH’s weakest measured link was *information handoff recall* (0.32 SWE / 0.55 OSWorld under parent-child execution) — surfaced context can lose task-critical detail, so require children to write evidence to paths rather than rely on summarized handoff.
- **Design family (A2/B3):** In = context + constraints; Out = ADRs + design. Hidden assumption: recorded rationale is real, not fabricated.
- **Build/test family (A4–A5/B5–B6):** In = tasks + acceptance conditions; Out = code + discriminating tests. Hidden assumption: the test suite is a faithful proxy for the spec (guarded by test-of-tests).
- **Verify/gate family (A6–A7/B7–B8):** In = diffs; Out = fail-closed verdicts + evidence. Hidden assumption: the verifier’s spec equals the true spec.
- **Ship/learn family (A9–A10/B10–B11):** In = artifacts + ledger; Out = readiness decisions + harness improvements.

### 5.2 Hidden assumptions (system-wide)

1. Adapters are correctly bound per project (a mis-bound test-runner silently invalidates every gate).
1. File-backed state is authoritative — but handoff loss is real; compaction must preserve acceptance criteria, error signatures, and replay commands (NLAH: aggressive context compression *hurt* both benchmarks; never compress away action-critical detail).
1. The skill library stays below the semantic-confusability threshold (Li, arXiv:2601.04748): past a critical size, skill-selection accuracy collapses.  Keep each catalog small and role-scoped; use hierarchical routing (orchestrator → family → skill) rather than a flat pool.

### 5.3 Cost of action vs inaction

- **Autonomous over-reach:** acting without a valid verifier ships broken/insecure code at machine speed — the dominant risk of agent-first development. Mitigation: fail-closed gates, test-of-tests, baseline-relative regression.
- **Human-in-loop over-gating:** too many checkpoints → the human abandons the agent and throughput collapses; batch approvals, use the three-tier model, and only gate irreversible/high-stakes steps.

### 5.4 Alternatives: single-agent-with-skills vs multi-agent orchestration

- **Single-agent + skill library** (compile a multi-agent system into one agent selecting skills): ~54% fewer tokens and ~50% lower latency at comparable accuracy on GSM8K/HumanEval/HotpotQA (Li, arXiv:2601.04748) — cheaper, simpler, fewer handoff losses. Prefer this for routine, low-parallelism SDLC work and to avoid NLAH’s handoff-recall penalty.
- **Multi-agent orchestration** is warranted only when you need (a) **genuine parallelism** (independent branches), (b) **private state** (a child must not see parent context), or (c) **adversarial role structure** (fresh-context verifier must be independent of the solver). The fresh-context verifier is the one place multi-agent structure is *non-negotiable* in both scenarios. Note the cost: Anthropic reports single agents use ~4× the tokens of chat and multi-agent systems ~15× the tokens of chat — reserve multi-agent for where independence/parallelism genuinely pays.
- **Guardrail:** as the skill count grows, semantic confusability degrades selection; this is an argument *for* multi-agent decomposition at scale (role-based routing) and *against* an unbounded single-agent skill pool — the two alternatives converge at scale via hierarchy.

-----

## Recommendations

**Stage 1 — Build the charter first (before any skill).** Stand up `STATE_ROOT` conventions, AGENTS.md adapter bindings, the failure taxonomy, and OpenTelemetry-based observability emission. This is the durable, model-independent layer; NLAH’s evidence is that policy/state discipline outlives model swaps. *Benchmark to advance:* a child can be launched, write `RESPONSE.md`, and be reopened by path with zero context loss on required artifacts.

**Stage 2 — Ship the verifier and test-of-tests next (weeks 2–3).** Without a trustworthy, spec-aligned verifier, autonomy is unsafe and B-mode teaching is ungrounded. Co-design the verifier with the acceptance rubric (NLAH: verifier value tracks alignment with the true gate). *Benchmark to advance:* test-of-tests reliably fails on seeded faults; the fresh-context verifier catches deliberately injected bugs the builder missed.

**Stage 3 — Wire acceptance-gated self-evolution (week 4).** This was NLAH’s single strongest module. *Benchmark:* repair loops measurably raise first-pass acceptance without exceeding retry cap 5.

**Stage 4 — Implement A1–A10 as SKILL.md bundles (weeks 5–8), then derive B-deltas** (teaching + gates) from the same bundles. Keep each skill to 2–3 focused modules (SkillsBench: focused beats exhaustive).

**Stage 5 — Compose the harness and encode the A-vs-B decision rule as a runtime check (weeks 9–10).**

**How to evaluate the skills (test/rubric-driven, per SkillsBench).** Adopt **paired evaluation** as the foundation: run each task under matched **no-skill vs curated-skill** conditions with **deterministic verifiers**, measuring the delta.

- **Per-skill eval bundle** (mirroring Anthropic’s `skill-creator`): an `evals.json` with `skill_name` and eval cases, each with `prompt`, `expected_output`, `files`, and an **`expectations`** list of natural-language assertions (“the output includes X”, “the skill used script Y”). A grader child scores outputs against expectations; a comparator does blind A/B between skill versions.
- **Metrics** (`metrics.json`/benchmark.json style): `pass_rate`, tool-call counts by type (Read/Write/Bash), `total_steps`, `errors_encountered`, `time_seconds`, `tokens`;  run ≥3 times per configuration.
- **Trigger reliability:** split eval prompts 60/40 train/test, run each query 3× to measure trigger rate; select descriptions by held-out test score to avoid overfitting (Claude tends to *under*-trigger — write “pushy” descriptions).
- **Efficacy targets:** expect domain-dependent gains (SkillsBench: +16.2 pp average, +4.5 pp software engineering to +51.9 pp healthcare); treat any skill showing a negative delta (16 of 84 SkillsBench tasks did) as a removal candidate.
- **Organization efficacy:** validate that hierarchical routing beats a flat pool via LLM-based pairwise evaluation with Bradley-Terry aggregation (AgentSkillOS, arXiv:2603.02176, showed capability-tree retrieval + DAG orchestration substantially outperform flat invocation on the identical skill set across 200–200K-skill ecosystems).
- **Confusability guard:** periodically measure skill-selection accuracy as the library grows; split into role-routed sub-libraries when near-duplicates degrade selection.

**Observability to emit (both scenarios).** Instrument with vendor-neutral OpenTelemetry GenAI conventions so telemetry joins whole-stack APM. Capture **intent visibility, not just execution visibility** — log the reasoning/decision at each fork to distinguish “agent chose wrong” from “agent given bad inputs.” Core signals: per-stage LLM/tool calls, tokens (prompt/completion/cached), wall-clock, gate pass/fail, retry counts, verifier verdicts, failure-mode histogram, handoff-recall, % work delegated to children, and — for B — approval latency and reviewer decisions. Run three evaluation layers: unit evals on discrete steps, LLM-as-judge regression suites on subjective outputs, and continuous production-trace sampling for drift. 

-----

## Caveats

- **NLAH is a v1 preprint (March 2026) with a prototype runtime.** Its own limitations note natural-language imprecision and a real handoff/orchestration bottleneck (Information Handoff Recall dropped to 0.32/0.55 under parent-child execution); its module numbers come from specific benchmarks (SWE-bench Verified, OSWorld, Terminal-Bench 2.0) under one model setting (gpt-5.4-mini, Codex CLI) and should be read as directional for SDLC design, not guarantees. The vocabulary (roles/contracts/gates vs planner/generator/evaluator) is not yet settled across the field.
- **SkillsBench figures differ by version.** The +16.2 pp / 86 tasks / 11 domains / 7,308 trajectories figures are from v1 (Feb 2026); a later version reports 87 tasks / 8 domains and a 33.9%→50.5% (+16.6 pp) framing. Cite the version you rely on.
- **The single-agent efficiency numbers (~54% tokens, ~50% latency) are described by their authors as preliminary,** on reasoning benchmarks (GSM8K/HumanEval/HotpotQA), not full SDLC work; the “7–63% accuracy drop from competitor skills” comes from a secondary summary and should be re-confirmed against the paper’s tables before load-bearing use.
- **Several ecosystem sources are vendor blogs and practitioner posts** (LangChain, OpenAI, Anthropic engineering notes, Medium/Substack write-ups). They are consistent with each other and with the peer-review-track arXiv papers, but represent reported practice, not independent evaluation. The Anthropic three-agent (planner/generator/evaluator) and OpenAI Codex “~1M lines / ~1,500 PRs” results are self-reported case studies.
- **This proposal specifies skill *contracts*, not runnable code.** Each SKILL.md bundle must be bound to concrete per-project adapters and validated with its own `evals.json` before being trusted in an autonomous harness. Safety, permission, and parsing logic must remain in code and be human-ratified — never auto-evolved.
