---
id: readiness
summary: "Deployment-readiness verdict: rollback procedure, health signals, and a go/no-go decision backed by evidence."
producer: builder
inputs:
  - name: change_summary
    description: "The implement stage's change record."
    format: markdown
    required: true
  - name: verification_report
    description: "The verify stage's evidence report."
    format: markdown
    required: true
  - name: target_repo
    description: "Path to the changed codebase."
    format: path
    required: true
outputs:
  - name: readiness_report
    file: readiness.md
    format: markdown
    description: "Release-readiness report: rollback procedure, health signals, per-concern go/no-go verdicts, and one overall verdict."
acceptance_criteria:
  - "A concrete rollback procedure exists: exact commands or steps, expected duration, and the state it restores. A missing or vague rollback is a blocking failure."
  - "Health signals for the changed behavior are identified: what to watch, where to watch it, and the threshold that triggers rollback."
  - "Every release concern examined (tests, build, migrations, monitoring, rollout shape) carries a go/no-go verdict with evidence quoted from the verification report or from commands actually run."
  - "The report ends with exactly one overall verdict - go / no-go / go-with-conditions - and any conditions are specific enough that a human can decide when they are met."
  - "The report never contradicts the verification report; unresolved verification gaps appear as conditions or no-go reasons, never silently dropped."
default_validators:
  - uses: validators/completeness-check
    with:
      checklist: policies/gates/release.md
  - uses: validators/persona-reviewer
    with:
      persona: "Site Reliability Engineer on call for this service the night it ships"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/shipping-and-launch
  - skillpacks/addyosmani/observability-and-instrumentation
  - skillpacks/distinguished-engineer/failure-domain-thinking
permissions:
  writes: [own_artifact_dir]
---

# Readiness

## Purpose

Decide whether this change can ship — and prove the decision. The dangerous
failure this stage guards against is the silent one: a change that deploys
green and misbehaves with no one watching and no way back. No rollback path,
no go.

## Procedure

1. Read the change summary and verification report; list every release
   concern this change raises (tests, build reproducibility, migrations,
   configuration, monitoring, rollout shape).
2. Write the rollback procedure: the exact commands or steps, how long they
   take, and what state they restore. If data or schema changes make rollback
   partial, say precisely what cannot be undone.
3. Identify health signals: what metric/log/behavior shows this change is
   healthy, where it is observed, and the threshold at which rollback is
   triggered.
4. For each concern, issue a go/no-go verdict with evidence — quoted from the
   verification report, or from commands you run in the target repo (build,
   test suite, packaging). Record commands and verbatim output.
5. Issue the overall verdict: go / no-go / go-with-conditions, conditions
   decidable by a human.

## Output format constraints

`readiness.md` sections in order: `# Readiness Report`, `## Rollback`
(procedure, duration, restored state), `## Health signals` (signal → where →
threshold), `## Concerns` (one subsection per concern: `Verdict:`,
`Evidence:`), `## Verdict` (exactly one of go / no-go / go-with-conditions,
plus conditions), `## Knowledge gaps`.

## Knowledge consumption

- `org-context`: deployment topology, release calendar, and change-management
  rules if attached; otherwise assess against the repo's own release
  mechanics and note the gap under `## Knowledge gaps`.

## Boundaries

- Do NOT modify the target repo; run read-only checks (build, tests,
  packaging) only, and remove any ephemeral scaffolding before finishing.
- Do NOT deploy, tag, or release anything — the report informs the human who
  does.
- Do NOT soften a no-go: if rollback is missing or a blocker stands, the
  verdict is no-go regardless of delivery pressure.

## Self-check before submitting

Walk the rollback procedure step by step against the actual repo state —
would each command run as written? Confirm every concern has evidence, the
overall verdict matches the per-concern verdicts, and no verification gap
vanished on the way here.

## Summary requirement

Write `summary.md` (≤200 words): the overall verdict, the rollback headline
(exists / partial / missing), and the single riskiest concern.
