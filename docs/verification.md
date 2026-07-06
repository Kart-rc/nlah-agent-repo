# Verification

How the harness was proven to work, and the repeatable checklist for
re-verifying after changes. All of this was executed for real on
2026-07-06; evidence pointers are given per test.

## 1. Static verification — `harness_lint.py`

```bash
pip install pyyaml jsonschema     # once
python3 scripts/harness_lint.py   # must exit 0
```

Validates: all manifests + frontmatter against the five schemas; every `uses`
ref exists on disk (stages, validators, knowledge, skillpacks); producer and
validator personas exist; every stage has ≥1 validator with completeness-check
first; a stage's producer never validates its own output; `needs` acyclic;
bindings resolve to declared outputs of transitive needs; required body
sections present; risk-policy refs valid.

**Result: clean — 9 stages, 4 validators, 2 workflows.**

## 2. End-to-end SDLC run (all six gates + repair loop + resume)

Toy request: *"Add a hello CLI script under examples/toy-cli/ that greets a
person by name"* (classified new-feature / low risk).

- All 6 stages ran as fresh subagents; every gate fired (13 validator
  verdicts); run reached `complete`; all state files validate against
  `task-state.schema.json`.
- **Natural repair loop (F1/F2):** the deliver stage FAILED attempt 1 — the
  completeness-check found the release-gate checklist item "Monitoring exists
  for the changed behavior" silently unaddressed. A fresh producer received
  the failure verdict + prior artifacts (never the prior producer's context),
  fixed it, and attempt 2 passed. Evidence:
  `docs/examples/sample-run/stages/deliver/`.
- **Resume test:** after stage 3 the orchestrator context was deliberately
  dropped; the next action (`implement`) was derived purely from
  `task_state.json`, with no passed stage re-executed. Evidence: the
  `orchestrator_reset` event in `docs/examples/sample-run/events.jsonl`.
- **Delivered change works:** `python3 examples/toy-cli/hello.py World` →
  `Hello, World!`; missing-name invocation exits with a usage error.
- Trimmed snapshot committed at `docs/examples/sample-run/`.

## 3. End-to-end Proposal run (generalization + F6 + CFO gate + repair loop)

Toy request: *"Propose adopting this NLAH magnetic harness for a 5-person
software team"* (classified proposal / low risk). 4 stages, 11 verdicts,
run `complete`.

- **Stage reuse proven:** `intake` ran verbatim from the shared library.
- **F6 knowledge degrade:** both attached adapters (enterprise-mcp,
  second-brain) had no reachable source; the research stage proceeded and
  recorded every unanswered question under `## Knowledge gaps`, visible to
  validators and carried into the final proposal.
- **Natural repair loop (F2):** the research stage FAILED attempt 1 — the
  adversarial reviewer spot-checked numeric claims against cited sources and
  caught a load-bearing error ("9 of 14 work types unrouted" vs the source's
  actual 6). The repaired digest passed attempt 2 with every number
  re-verified. This is the centerpiece behavior: an independent validator
  catching plausible-but-wrong content before it reaches a decision-maker.
- **Persona gates:** the "Skeptical CFO" validator interrogated and PASSED
  the draft ("I would approve this pilot — the proposal anticipates my
  skepticism instead of managing it"); the finalize gate re-read everything
  as the time-poor EM audience.
- **F3 environment failures handled:** this environment's runtime blocks
  subagent writes of summary-style files; producers returned summaries in
  their final message and the orchestrator persisted them verbatim (logged as
  `f3_recovered` events, repair budget untouched). This also motivated a
  protocol improvement: validators are now mechanically write-less — they
  RETURN verdict JSON and the orchestrator persists it (HARNESS.md §3.1.5).

## 4. Risk overlay dry-run (High risk → validators + approval pause)

Mock request: *"Change the auth token validation logic..."* → classified
security-sensitive-change / **high**. Programmatically applied
`harness/policies/risk-policy.yaml[high]` while locking the manifest:

- `implement` gained `validators/red-team` with
  `checklist: policies/gates/security.md`; `deliver` gained the release
  checklist — and the policy's `draft`-stage entry was correctly skipped
  (sdlc has no draft stage).
- Approval checkpoint `before: implement` recorded; run state set to
  `awaiting_approval`; state validates against the schema.

## 5. Magnetic attach/detach tests

On `harness/workflows/sdlc/workflow.yaml`:

- **Detach** `test-driven-development` from implement (delete one line) →
  lint clean. **Re-attach** → lint clean.
- **Swap** for `doubt-driven-development` → lint clean.
- **Negative:** attach `skillpacks/addyosmani/nonexistent-skill` → lint FAILS
  with the exact missing path. The manifest was restored byte-identical.

## 6. Schema conformance sweep

Every `task_state.json`, `gate.json`, and `verdict.json` across both completed
runs validates against `harness/schema/task-state.schema.json` (root, `$defs/gate`,
`$defs/verdict` respectively): 10 gate files, 26 verdict files, 3 state files.

## Re-verification checklist (after any harness change)

1. `python3 scripts/harness_lint.py` → exit 0.
2. If the orchestration protocol, stage contracts, or validators changed:
   re-run one toy SDLC run end-to-end and confirm a gate can fail → repair →
   pass (seed a deliberate omission if needed).
3. If risk policy changed: re-run the §4 dry-run and inspect the lock file.
4. If manifests changed: spot-run the §5 attach/detach + negative test.
5. Schema changes bump `manifest_version` and require re-validating the
   committed `docs/examples/sample-run/` snapshot.

## Known environment caveats

- Subagent personas load at session start; personas added mid-session are not
  yet registered as agent types (fall back to a general agent with the persona
  doc prepended, as the first SDLC run did).
- This environment's runtime blocks subagent report-file writes (see §3, F3);
  producer summaries are persisted by the orchestrator when that happens.
- arxiv.org and most fetch domains are blocked by the network policy here;
  the NLAH paper mapping in `docs/architecture.md` cites the accessible
  summaries used instead.
