---
id: deliver
summary: "Assemble the validated change into a delivery package a stakeholder can act on: what changed, why, evidence, and follow-ups."
producer: analyst
inputs:
  - name: change_summary
    description: "The implement stage's change record."
    format: markdown
    required: true
  - name: verification_report
    description: "The verify stage's evidence report."
    format: markdown
    required: true
  - name: requirements
    description: "Original requirements (from intake)."
    format: markdown
    required: true
outputs:
  - name: delivery_package
    file: delivery.md
    format: markdown
    description: "Stakeholder-facing delivery document: SUMMARY block, evidence digest, risks, follow-ups, how to release/rollback."
acceptance_criteria:
  - "The package opens with the HARNESS.md SUMMARY block (what changed / why / files / verification / risks) filled in from real artifacts."
  - "A non-technical reader can understand what changed and why from the opening section alone."
  - "Every claim in the package is traceable to the change summary or verification report - no new claims appear here."
  - "Unmet or unverifiable criteria from the verification report are carried forward visibly, never dropped."
  - "The package states how to release the change and how to roll it back."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/persona-reviewer
    with:
      persona: "Non-technical stakeholder who must understand what changed, why, and what risk remains"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/shipping-and-launch
  - skillpacks/addyosmani/documentation-and-adrs
permissions:
  writes: [own_artifact_dir]
---

# Deliver

## Purpose

The last mile: package the validated work so a human can accept, release, and
operate it. This stage adds no new engineering — it makes the completed work
legible and actionable.

## Procedure

1. Read the change summary, verification report, and requirements.
2. Fill in the SUMMARY block (HARNESS.md §7.5) from those artifacts only.
3. Write the plain-language narrative: the problem, what changed, what the
   evidence shows, for a reader who will not open the diff.
4. Digest the evidence: per requirement, met/not-met with a pointer into the
   verification report. Carry forward every gap visibly.
5. Write release guidance (how to ship: merge/deploy/flag) and the rollback
   procedure (from the design's rollback strategy, updated by reality).
6. List follow-ups: deferred plan items, verification gaps, risks accepted.

## Output format constraints

`delivery.md` sections in order: `# Delivery`, `## Summary` (the SUMMARY
block), `## What changed and why` (plain language), `## Evidence`
(requirement → verdict → report pointer), `## Release and rollback`,
`## Risks and follow-ups`, `## Knowledge gaps`.

## Knowledge consumption

- `org-context`: release conventions (change management, announcement
  channels) if attached; otherwise give generic release guidance and note the
  gap under `## Knowledge gaps`.

## Boundaries

- Do NOT modify code or re-run verification; report what exists.
- Do NOT soften or omit unmet criteria, deviations, or risks — visibility here
  is the point of the stage.
- Do NOT commit, push, or deploy; the package tells the human how.

## Self-check before submitting

Read only your `## Summary` and `## What changed and why` sections as if you
were the requester's manager: do you know what you got and what risk remains?
Cross-check every evidence pointer resolves to a real section of the
verification report.

## Summary requirement

Write `summary.md` (≤200 words): one-line description of the delivery, the
headline evidence, and the top remaining risk or follow-up.
