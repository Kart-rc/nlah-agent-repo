# Skill Pack Catalog

One-page index of every skill in this repository: the harness's runtime
skills in `.claude/skills/` and every practice skill in
`harness/skillpacks/`. Each skill folder contains:

- `SKILL.md` — the discipline document a stage's producer subagent reads in
  full before working (see `HARNESS.md` → Prompt Templates).
- `USAGE.md` — a companion guide for humans and orchestrators: when to
  invoke the skill, how to attach it (manifest snippet) or use it standalone,
  and what output to expect. USAGE.md is never included in producer prompts.

Attach a skill to a stage with a one-line manifest edit (use the
`workflow-composer` skill, then run `python3 scripts/harness_lint.py`).
For direct use without a harness run, see `docs/using-skills-standalone.md`.

"Default attachment" below means: suggested by a stage's `skill_refs`
frontmatter (materialized into new manifests by workflow-composer) and/or
attached in a shipped workflow manifest. "ad hoc" = no default; attach it
explicitly where its USAGE.md suggests.

## `.claude/skills` — Claude Code runtime skills (4 skills)

These are a different category from the practice skills below: Claude Code
discovers them automatically and triggers them from their frontmatter
`description`, or you invoke them by name in conversation. They are not
attached to workflow stages. The router and composer are the harness's
operating controls (see `CLAUDE.md`).

| Skill | What it does | How it runs |
|---|---|---|
| [agentic-delivery-router](../.claude/skills/agentic-delivery-router/USAGE.md) | Entry point for any delivery request: classifies work type + risk, applies gates, orchestrates the workflow per HARNESS.md; resumes runs | Triggered by any non-trivial delivery request, or invoked by name |
| [workflow-composer](../.claude/skills/workflow-composer/USAGE.md) | Creates/modifies workflow manifests from existing stages, validators, adapters, skill packs; lints and dry-runs | Invoked when you ask for a new/changed workflow |
| [architecture-decision-records](../.claude/skills/architecture-decision-records/USAGE.md) | Drives and records architectural decisions as ADRs calibrated to enterprise context | Triggered when a significant technical choice is made or questioned |
| [bootstrap-claude-context](../.claude/skills/bootstrap-claude-context/USAGE.md) | Installs a layered, self-improving Claude Code context scaffold into a repository | Invoked when onboarding a repo to Claude Code |

## `addyosmani` — engineering lifecycle (24 skills, vendored)

| Skill | What it does | Default attachment |
|---|---|---|
| [api-and-interface-design](../harness/skillpacks/addyosmani/api-and-interface-design/USAGE.md) | Stable API, module-boundary, and contract design | `design` (sdlc) |
| [browser-testing-with-devtools](../harness/skillpacks/addyosmani/browser-testing-with-devtools/USAGE.md) | Real-browser verification via Chrome DevTools MCP | ad hoc |
| [ci-cd-and-automation](../harness/skillpacks/addyosmani/ci-cd-and-automation/USAGE.md) | Pipeline setup, quality gates, deployment strategies | ad hoc |
| [code-review-and-quality](../harness/skillpacks/addyosmani/code-review-and-quality/USAGE.md) | Five-axis review before any merge | ad hoc |
| [code-simplification](../harness/skillpacks/addyosmani/code-simplification/USAGE.md) | Behavior-preserving refactors for clarity | ad hoc |
| [context-engineering](../harness/skillpacks/addyosmani/context-engineering/USAGE.md) | Agent context/rules-file setup and hygiene | ad hoc |
| [debugging-and-error-recovery](../harness/skillpacks/addyosmani/debugging-and-error-recovery/USAGE.md) | Systematic root-cause debugging | `verify` (sdlc) |
| [deprecation-and-migration](../harness/skillpacks/addyosmani/deprecation-and-migration/USAGE.md) | Sunsetting systems and migrating users safely | ad hoc |
| [documentation-and-adrs](../harness/skillpacks/addyosmani/documentation-and-adrs/USAGE.md) | Decision records and durable documentation | `assess`, `decide`, `deliver`, `draft` stages |
| [doubt-driven-development](../harness/skillpacks/addyosmani/doubt-driven-development/USAGE.md) | Fresh-context adversarial review of confident output | ad hoc |
| [frontend-ui-engineering](../harness/skillpacks/addyosmani/frontend-ui-engineering/USAGE.md) | Production-quality user interfaces | ad hoc |
| [git-workflow-and-versioning](../harness/skillpacks/addyosmani/git-workflow-and-versioning/USAGE.md) | Commits, branching, releases, semantic versioning | ad hoc |
| [idea-refine](../harness/skillpacks/addyosmani/idea-refine/USAGE.md) | Divergent/convergent refinement of raw ideas | `research`, `options` stages |
| [incremental-implementation](../harness/skillpacks/addyosmani/incremental-implementation/USAGE.md) | Small, verifiable implementation steps | `implement` (sdlc) |
| [interview-me](../harness/skillpacks/addyosmani/interview-me/USAGE.md) | One-question-at-a-time intent extraction | `intake` (all workflows) |
| [observability-and-instrumentation](../harness/skillpacks/addyosmani/observability-and-instrumentation/USAGE.md) | Logging, metrics, tracing, alerting | ad hoc |
| [performance-optimization](../harness/skillpacks/addyosmani/performance-optimization/USAGE.md) | Profiling-driven performance work | ad hoc |
| [planning-and-task-breakdown](../harness/skillpacks/addyosmani/planning-and-task-breakdown/USAGE.md) | Ordered, implementable task decomposition | `plan` (sdlc) |
| [security-and-hardening](../harness/skillpacks/addyosmani/security-and-hardening/USAGE.md) | Hardening against untrusted input and vulnerabilities | ad hoc |
| [shipping-and-launch](../harness/skillpacks/addyosmani/shipping-and-launch/USAGE.md) | Launch checklists, staged rollout, rollback | `deliver` (sdlc) |
| [source-driven-development](../harness/skillpacks/addyosmani/source-driven-development/USAGE.md) | Official-documentation-grounded implementation | ad hoc |
| [spec-driven-development](../harness/skillpacks/addyosmani/spec-driven-development/USAGE.md) | Specs before code | `intake`, `design` (sdlc) |
| [test-driven-development](../harness/skillpacks/addyosmani/test-driven-development/USAGE.md) | Failing test first; tests as proof | `implement` (sdlc) |
| [using-agent-skills](../harness/skillpacks/addyosmani/using-agent-skills/USAGE.md) | Meta-skill: discover and route to other skills | standalone router only |

## `tech-director` — technical judgment and leadership (7 skills)

| Skill | What it does | Default attachment |
|---|---|---|
| [architectural-judgement](../harness/skillpacks/tech-director/architectural-judgement/USAGE.md) | Judging designs and rendering defensible verdicts | `assess` (architecture-review) |
| [executive-communication](../harness/skillpacks/tech-director/executive-communication/USAGE.md) | BLUF briefs, calibrated uncertainty, altitude | `decide`; `finalize` (tech-decision, architecture-review, proposal) |
| [influence-without-authority](../harness/skillpacks/tech-director/influence-without-authority/USAGE.md) | Stakeholder maps and coalition-building | `draft` (proposal) |
| [options-and-tradeoffs](../harness/skillpacks/tech-director/options-and-tradeoffs/USAGE.md) | Decision-grade option matrices with TCO and reversibility | `options` (tech-decision) |
| [people-leadership](../harness/skillpacks/tech-director/people-leadership/USAGE.md) | Delegation, feedback, coaching, team health | ad hoc |
| [risk-mitigation](../harness/skillpacks/tech-director/risk-mitigation/USAGE.md) | Actionable risk registers and pre-mortems | ad hoc |
| [timeboxed-decision-making](../harness/skillpacks/tech-director/timeboxed-decision-making/USAGE.md) | Calls at stated confidence within a deadline | `decide` (tech-decision) |

## `geoffreylitt` — understanding AI-written code (3 skills)

| Skill | What it does | Default attachment |
|---|---|---|
| [code-explainers](../harness/skillpacks/geoffreylitt/code-explainers/USAGE.md) | Literate explainer documents instead of raw diffs | ad hoc (natural home: `implement`/`verify`) |
| [understanding-quizzes](../harness/skillpacks/geoffreylitt/understanding-quizzes/USAGE.md) | Comprehension quiz gating human review | ad hoc (natural home: `implement`/`verify`) |
| [micro-worlds](../harness/skillpacks/geoffreylitt/micro-worlds/USAGE.md) | Ephemeral interactive artifacts for runtime intuition | ad hoc (natural home: `implement`/`verify`) |

## `review-debt` — hidden review burden (1 skill)

| Skill | What it does | Default attachment |
|---|---|---|
| [review-debt-code-review](../harness/skillpacks/review-debt/review-debt-code-review/USAGE.md) | Evidence-backed review of reviewability and review debt | ad hoc |
