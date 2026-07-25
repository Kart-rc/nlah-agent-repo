---
id: retrospect
summary: "Replay the run's own ledger, classify every failure against the taxonomy, and propose harness improvements as candidate diffs for human ratification."
producer: analyst
inputs:
  - name: run_dir
    description: "Path to this run's directory (runs/<run-id>), resolved by the orchestrator at initialization - never requested from the user."
    format: path
    required: true
outputs:
  - name: retrospective
    file: retrospective.md
    format: markdown
    description: "Evidence-backed replay of the run: failure classification, run metrics, and context-usage statistics."
  - name: harness_proposals
    file: harness_proposals.md
    format: markdown
    description: "Candidate harness edits as concrete diffs, each marked NOT APPLIED and awaiting human ratification."
acceptance_criteria:
  - "Every non-pass gate attempt, repair, and escalation found in events.jsonl and the per-stage gate.json files is classified against docs/failure-taxonomy.md (F1-F7) with evidence paths into the run directory."
  - "Run metrics are reported: attempts per stage, verdict outcomes per validator, and repair success rate."
  - "When a context register exists in the run, context-usage statistics are reported: register entries cited vs never cited across downstream stage artifacts (citation marker `[context: CR-n]`), never-cited entries listed as wasted retrieval, and load-bearing claims lacking citations flagged as fabrication risk."
  - "Every improvement proposal is a candidate diff naming the exact harness file and the exact text to change, explicitly marked NOT APPLIED, and requiring human ratification."
  - "Any proposal touching HARNESS.md, .claude/agents/, permissions, the risk policy, or approval logic is prominently flagged as safety-critical."
  - "A run with no failures yields a retrospective that states what evidence is therefore missing, rather than inventing findings."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "failure misclassification, proposals that would weaken gates or permissions, evidence-free claims"
knowledge_slots: []
skill_refs:
  - skillpacks/addyosmani/debugging-and-error-recovery
  - skillpacks/distinguished-engineer/problem-framing
permissions:
  writes: [own_artifact_dir]
---

# Retrospect

## Purpose

Make the harness learn from its own run. Every repair loop, escalation, and
surviving weakness in this run is evidence about the harness itself; left
unexamined, the same failure repeats next run. This stage turns the run's
ledger into classified findings and ratifiable improvement proposals — it
never applies them.

## Procedure

1. Read `task_state.json`, `events.jsonl`, and every stage's `gate.json` and
   verdict files under the given run directory.
2. Classify each non-pass event against `docs/failure-taxonomy.md` (F1-F7),
   citing the evidence path for every classification.
3. Compute run metrics: attempts per stage, verdicts per validator, repair
   success rate (repairs that led to a pass / repairs attempted).
4. If a context register exists (`context-register.md` in a stage's
   artifacts): scan downstream stage artifacts for `[context: CR-n]`
   citations; report cited vs never-cited entries, and flag load-bearing
   claims that carry no citation.
5. Derive improvement proposals from the classified failures: for each, the
   harness file, the exact candidate diff, the failure it prevents, and its
   risk. Mark every proposal NOT APPLIED.
6. If the run had no failures, say so — and state what the absence of
   failures leaves unknown about the harness.

## Output format constraints

`retrospective.md` sections in order: `# Retrospective`, `## Run metrics`,
`## Failure classification` (one subsection per failure: class, stage,
evidence path), `## Context usage` (or a one-line note that no register
exists), `## Knowledge gaps`. `harness_proposals.md` sections: `# Harness
Proposals (NOT APPLIED)`, then one `## Proposal N` per item with `File:`,
`Diff:` (fenced), `Prevents:`, `Risk:`, and a `SAFETY-CRITICAL` marker line
where it applies.

## Knowledge consumption

This stage declares no knowledge slots: it reads only within the given run
directory plus the harness documents it cites (`docs/failure-taxonomy.md`).
Its own stage's records are in-flight while it runs and are excluded from
analysis.

## Boundaries

- Do NOT modify anything under `harness/`, `.claude/`, `scripts/`, or
  `HARNESS.md` — proposals are text inside your artifacts, nothing more.
- Do NOT re-litigate the delivered change; judge the process, not the
  product.
- Do NOT propose loosening a gate, permission, or approval as a convenience;
  such a proposal needs the failure evidence that justifies it.

## Self-check before submitting

Every classification cites a real path inside the run directory. Every
proposal's diff names a file that exists and text that is actually there.
Every safety-critical proposal carries its marker. Nothing in your artifacts
modified anything outside your artifact directory.

## Summary requirement

Write `summary.md` (≤200 words): failure count by class, the single most
valuable proposal, and whether any safety-critical proposals await
ratification.
