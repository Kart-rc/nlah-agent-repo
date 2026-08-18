---
id: verify-fixes
summary: "Independently verify every issue's acceptance criteria inside its own worktree and report per-issue verdicts with verbatim evidence."
producer: builder
inputs:
  - name: fix_manifest
    description: "Per-issue fix results with worktree paths and branches (from fix-issues)."
    format: json
    required: true
  - name: issue_manifest
    description: "The authoritative per-issue acceptance criteria (from issue-intake)."
    format: json
    required: true
  - name: target_repo
    description: "Path to the repo whose primary tree must remain untouched and whose worktrees are exercised."
    format: path
    required: true
outputs:
  - name: fix_verification_report
    file: fix_verification_report.md
    format: markdown
    description: "Per-issue, per-criterion verdicts (met / not met / not verifiable) with fenced command and output evidence gathered inside each issue's worktree, plus a rollup table."
acceptance_criteria:
  - "For every issue with status fixed in fix_manifest.json, every acceptance criterion from issue_manifest.json has a verdict (met / not met / not verifiable) backed by verbatim command output produced inside that issue's worktree - verification runs against the criteria issue-intake wrote, not against what fix-issues says it did."
  - "For every fixed issue, the worktree's test-suite result is recorded, and at least one negative or boundary case is exercised with its output shown."
  - "Every issue with status blocked is listed with its stated blocker checked - reproduced or refuted with evidence; a refuted blocker is recorded as refuted, not silently accepted."
  - "The report contains a rollup table: issue id, criteria met/total, verdict verified | not-verified | blocked."
  - "The report is honest: no verdict claims evidence the fenced output does not actually show, and any not-met or not-verifiable verdict states exactly what is missing and how a human could check it."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "test adequacy per issue - criteria verified only by unit tests, missing negative cases, evidence gathered in the wrong worktree, blocked verdicts taken on faith"
knowledge_slots: []
skill_refs:
  - skillpacks/addyosmani/debugging-and-error-recovery
permissions:
  writes: [own_artifact_dir]
---

# Verify Fixes

## Purpose

Independent evidence, per issue, that the batch actually meets its criteria.
The builder here never saw the fixing stage's reasoning: it takes the
acceptance criteria issue-intake wrote and exercises each issue's worktree
against them, so an unfixed issue cannot hide behind a confident summary.

## Procedure

1. Read the fix manifest and the issue manifest. The issue manifest's
   acceptance criteria are the contract; the fix manifest only says where to
   look.
2. Per fixed issue: change into its `worktree_path`, confirm the checked-out
   branch matches the fix manifest, then per acceptance criterion design the
   smallest end-to-end exercise that would prove or refute it, run it, and
   record the command plus its verbatim output.
3. Run that worktree's test suite and record the result; exercise at least
   one negative or boundary case per issue and show its output.
4. Per blocked issue: attempt to reproduce the stated blocker. Record it as
   reproduced (with evidence) or refuted (with evidence) — a refuted blocker
   means the issue was fixable.
5. Build the rollup table and give every issue an overall verdict:
   verified, not-verified, or blocked.

## Output format constraints

`fix_verification_report.md` sections in order:
`# Fix Verification Report`, `## Environment` (tools and versions used),
`## Rollup` (table: issue id, criteria met/total, verdict), `## Issues` (one
`### ISS-<n>` subsection per fixed issue: per-criterion `Verdict:` and
`Evidence:` fenced blocks, `Negative case:`, `Test suite:`),
`## Blocked issues` (per blocked issue: stated blocker, reproduced/refuted,
evidence; "none" if none), `## Gaps` (anything not verifiable and how a
human could check it; "none" if none), `## Knowledge gaps`.

## Knowledge consumption

No knowledge slots: verification uses only the run artifacts and the
worktrees, so its evidence is reproducible from the repo alone.

## Boundaries

- Do NOT fix the code. A failed criterion is a `not met` verdict — the gate
  and loopback handle it; the defect lives on that issue's branch.
- Do NOT commit anywhere, on any branch.
- Do NOT modify any worktree or the primary tree except ephemeral test
  scaffolding you remove before finishing.
- Do NOT re-interpret or weaken acceptance criteria to make them pass.

## Self-check before submitting

For every verdict, confirm the fenced output actually shows what the verdict
claims. Confirm every fixed issue covers every one of its criteria, every
blocked issue's blocker was checked, and the rollup counts match the
per-issue sections.

## Summary requirement

Write `summary.md` (≤200 words): issues verified / not-verified / blocked,
criteria met out of total, and the most significant gap or refuted blocker.
