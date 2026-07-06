---
id: verify
summary: "Independently exercise the implemented change against the original requirements and produce a verification report with evidence."
producer: builder
inputs:
  - name: change_summary
    description: "The implement stage's change record."
    format: markdown
    required: true
  - name: requirements
    description: "Original requirements with acceptance criteria (from intake)."
    format: markdown
    required: true
  - name: target_repo
    description: "Path to the changed codebase."
    format: path
    required: true
outputs:
  - name: verification_report
    file: verification_report.md
    format: markdown
    description: "Per-requirement verdict with the evidence (commands + verbatim output) that demonstrates it."
acceptance_criteria:
  - "Every acceptance criterion from requirements.md has a verdict (met / not met / not verifiable) backed by verbatim command output or an explicit reason."
  - "Verification exercises the changed behavior end-to-end, not only unit tests - the report shows the feature actually running."
  - "At least one negative case is exercised (invalid input, error path, or boundary), with its output recorded."
  - "Any 'not met' or 'not verifiable' verdict states exactly what is missing and how a human could verify it."
  - "The report is honest: no verdict claims evidence the fenced output does not actually show."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "test adequacy - what is untested, what evidence is missing, where the report overstates its output"
knowledge_slots: []
skill_refs:
  - skillpacks/addyosmani/debugging-and-error-recovery
permissions:
  writes: [own_artifact_dir]
---

# Verify

## Purpose

Produce the evidence. Implementation reported what it did; this stage
independently demonstrates the requirements are met by running the changed
system — the verification report is a deliverable the requester can audit.

## Procedure

1. Read the requirements and extract every acceptance criterion.
2. Read the change summary to learn what changed and how to exercise it — but
   verify against REQUIREMENTS, not against what implement says it did.
3. For each criterion: design the smallest end-to-end exercise that
   demonstrates it (run the CLI, call the API, execute the scenario). Run it.
   Record the command and verbatim output.
4. Exercise at least one negative/boundary case.
5. Run the target repo's full test suite; record the result.
6. Issue per-criterion verdicts: met / not met / not verifiable (with what's
   missing and how a human could check).

## Output format constraints

`verification_report.md` sections in order: `# Verification Report`,
`## Environment` (how/where things were run), `## Criteria` (one subsection
per acceptance criterion: `Verdict:`, `Evidence:` fenced command+output),
`## Negative cases`, `## Test suite` (fenced output), `## Gaps` (anything not
verifiable and why), `## Knowledge gaps`.

## Knowledge consumption

This stage declares no knowledge slots: verification uses only the repo and
the run artifacts. (Still record environment limitations under
`## Knowledge gaps` — e.g. services unreachable from this environment.)

## Boundaries

- Do NOT fix the code. A failed criterion is recorded as `not met` — the gate
  and repair loop handle what happens next.
- Do NOT modify the target repo except ephemeral test scaffolding you remove
  before finishing.
- Do NOT re-interpret requirements; verify what intake wrote.

## Self-check before submitting

Re-read each `Evidence:` block and confirm the output actually shows what the
verdict claims. Confirm a negative case exists. Confirm the test-suite output
is current (re-run if you changed anything since).

## Summary requirement

Write `summary.md` (≤200 words): criteria met vs not met vs not verifiable,
the strongest single piece of evidence, and any gap a human should close.
