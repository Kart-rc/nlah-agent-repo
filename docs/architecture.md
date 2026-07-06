# Architecture

This harness is a working implementation of the Natural-Language Agent Harness
(NLAH) model: **all control logic is text**, interpreted by Claude Code acting
as the paper's "Intelligent Harness Runtime" (IHR). Natural language carries
policy; the runtime carries mechanism (tool execution, subagent launching,
file I/O).

Primary source: "Natural-Language Agent Harnesses",
[arXiv 2603.25723](https://arxiv.org/abs/2603.25723). (This repo's design was
reconstructed from the paper's abstract and public summaries —
[Emergent Mind](https://www.emergentmind.com/papers/2603.25723),
[aiquinta](https://aiquinta.ai/blog/natural-language-agent-harnesses-nlahs/),
[Alibaba Cloud](https://www.alibabacloud.com/blog/code-harness-or-natural-language-harnesses_603240) —
as the full text was unreachable from the build environment.)

## NLAH paper concept → repo component

| Paper concept | What the paper requires | Where it lives here |
|---|---|---|
| **Runtime charter** | Policy/semantics the runtime enforces, separate from harness logic | `HARNESS.md` (principles, protocol, state semantics, prompt templates) |
| **Contracts** | Required inputs/outputs, format constraints, validation gates, permission boundaries, stop/retry rules | `harness/schema/*.json` + document frontmatter (stages, validators, adapters) + manifest gate policies |
| **Roles** | Distinct personas with non-overlapping responsibilities | `.claude/agents/` — 3 producers (planner, builder, analyst), 4 validators; producer ∉ validators enforced by lint |
| **Stage structure** | Explicit topology (plan → execute → verify → repair) | `workflow.yaml` manifests: `stages` + `needs` DAG; repair loop in HARNESS.md §3.1 |
| **State semantics** | State externalized to path-addressable artifacts, survives context resets | `runs/<id>/` layout: `task_state.json` resume anchor, per-stage artifacts, `events.jsonl` |
| **Failure taxonomy** | Named error modes triggering specific recovery | `docs/failure-taxonomy.md` (F1–F7) |
| **Adapters** | Thin translation layers to tools/knowledge | `harness/knowledge/*/adapter.md` (enterprise-mcp, second-brain) |
| **Validation gates** | Acceptance criteria checked before progression | Stage `acceptance_criteria` + validator library + blocking gate protocol (HARNESS.md §3.1.5–6) |
| **Artifact contracts** | Declared outputs with formats | Stage frontmatter `outputs` + completeness-check as first gate |

## agentic-delivery-router skill → harness component

The router skill's discipline (from the addyosmani/agent-skills ecosystem)
was merged harness-natively:

| Router skill element | Where it lives here |
|---|---|
| Work-type taxonomy (13+1 types) | Router SKILL.md Step 2; manifests declare `intent.work_types` |
| Risk rubric (Low/Medium/High/Critical) | Router SKILL.md Step 3 (prose) + `harness/policies/risk-policy.yaml` (data) |
| Skill paths (spec-driven → TDD → …) | Stage sequences in manifests; the named practice skills attach to stages via `skills:` (vendored pack) |
| Mandatory gates (Requirements/Architecture/Security/Data/Observability/Release) | `harness/policies/gates/*.md` checklists, consumed by any validator via `with.checklist` |
| REQUEST CLASSIFICATION block | Router Step 1–3 output, recorded in `task_state.json.classification` |
| Approval rules | Router Step 6 + risk-policy `approval_checkpoints` (`awaiting_approval` run status) |
| SUMMARY block | HARNESS.md §7.5, delivered at run completion and embedded in the deliver stage |

## The magnetic property

Four module libraries snap into manifests; every composition change is a
manifest edit validated by `scripts/harness_lint.py`:

```yaml
stages:
  - id: implement
    uses: stages/implement            # ← swap the stage
    validators:
      - uses: validators/completeness-check
      - uses: validators/red-team     # ← attach/detach a validator
        with: { checklist: policies/gates/security.md }   # ← parameterize
    knowledge:
      - uses: knowledge/enterprise-mcp   # ← attach org knowledge
    skills:
      - uses: skillpacks/addyosmani/test-driven-development  # ← attach a practice
```

Two mechanisms keep this safe:

1. **Materialized defaults.** Stage docs *suggest* validators/skills
   (`default_validators`, `skill_refs`); the composer copies them into the
   manifest at scaffold time. At runtime there is no inheritance — what you
   read in the manifest is exactly what runs.
2. **Lock files.** Each run freezes its manifest (+ risk overlay) into
   `workflow.lock.yaml`; library edits never corrupt in-flight runs.

## Subagents and context management

The orchestrator (main context) holds only `task_state.json` and ≤200-word
stage summaries. Every producer attempt and every validator runs in a fresh
subagent whose prompt is composed from the HARNESS.md §7 templates:

- producers get the stage doc + input *paths* + skill *paths* + adapter bodies;
- validators get the validator doc + criteria + artifact paths — **never the
  producer's reasoning or summary** (independence by prompt construction);
- repair attempts get prior artifacts + failure verdicts — never the prior
  producer's conversation (feedback via files, not context accumulation).

## Deliberate design decisions

- **Review is a gate, not a stage.** Adversarial/persona review attaches to
  stages as validators. SDLC's `verify` is a stage because running tests
  *produces* evidence — producer work, not judgment.
- **`design` is not reused by the proposal workflow.** A stage generic enough
  to serve both software design and proposal argumentation would need
  acceptance criteria too weak to gate either. Reuse is proven where contracts
  genuinely coincide: `intake` is shared verbatim, and the entire validator /
  adapter / persona / skill-pack libraries are shared.
- **`needs` is a DAG field, execution is sequential (v1).** The manifest
  contract supports parallel stages; the Claude Code runtime executes in
  needs-order. An SDK runtime can parallelize without a manifest change.
- **Independence is policy-enforced, not sandbox-enforced (v1).** Validator
  prompts never contain producer reasoning, validator docs forbid seeking it,
  and artifacts/summaries live at separate paths — but a validator *could*
  disobey and read `summary.md`. An SDK runtime can enforce this with
  filesystem scoping; accepted residual risk for the docs-first runtime.
- **Red-team may execute but never persist.** Its persona has Bash for
  probing; its hard rules forbid state mutation. Same SDK-sandbox note applies.

## SDK-readiness

Everything a programmatic runtime needs is machine-readable:

- `workflow.yaml` + lock files validate against
  `harness/schema/workflow-manifest.schema.json`;
- stage/validator/adapter frontmatter validate against their schemas;
- run state validates against `task-state.schema.json` (incl. `gate.json` and
  `verdict.json` shapes);
- the orchestration semantics an SDK must implement are exactly HARNESS.md §3.

A Claude Agent SDK harness would: parse the manifest → spawn producers/
validators as SDK subagents with the §7 prompt templates → enforce permission
boundaries via sandboxing → keep the identical on-disk state layout, so runs
stay resumable across both runtimes.
