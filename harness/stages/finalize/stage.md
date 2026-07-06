---
id: finalize
summary: "Polish the validated draft for its audience and package it with a decision brief - no new arguments."
producer: analyst
inputs:
  - name: proposal_draft
    description: "The validated proposal draft (from draft)."
    format: markdown
    required: true
  - name: audience
    description: "Who will read and judge the proposal."
    format: text
    required: true
outputs:
  - name: final_proposal
    file: final_proposal.md
    format: markdown
    description: "Audience-ready final proposal."
  - name: decision_brief
    file: decision_brief.md
    format: markdown
    description: "One-page brief: the ask, the recommendation, cost, risk, deadline - for the decision meeting."
acceptance_criteria:
  - "The final proposal preserves the draft's substance: recommendation, costs, risks, and knowledge gaps are unchanged in meaning."
  - "Language, framing, and level of detail fit the declared audience."
  - "The decision brief fits on one page and contains the ask, recommendation, cost, primary risk, and requested decision date."
  - "No new facts, numbers, or commitments appear that were absent from the draft."
  - "Formatting is consistent and links/references resolve."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/persona-reviewer
    with:
      persona: "The declared target audience, reading this cold with ten minutes before the decision meeting"
knowledge_slots: [org-context]
skill_refs: []
permissions:
  writes: [own_artifact_dir]
---

# Finalize

## Purpose

The draft won the argument gates; this stage makes it land with the human
audience. Finalize is deliberately substance-preserving: persuasion polish
without moving any number or claim.

## Procedure

1. Read the validated draft and the audience input.
2. Rewrite for the audience: vocabulary, depth, ordering — executives get
   decisions first, practitioners get mechanics. Substance stays identical.
3. Produce the one-page decision brief: ask, recommendation, cost, primary
   risk, requested decision date.
4. Copy-edit: consistency, resolving references, formatting.
5. Diff-check yourself against the draft for accidental meaning changes.

## Output format constraints

`final_proposal.md`: same section skeleton as the draft (title, executive
summary, context, recommendation, alternatives, costs, risks, implementation
sketch, success measures, ask, knowledge gaps), reworded for the audience.
`decision_brief.md`: `# Decision Brief`, `## The ask`, `## Recommendation`,
`## Cost`, `## Primary risk`, `## Decision needed by` — total under one page
(~400 words).

## Knowledge consumption

- `org-context`: house style or template if attached; otherwise keep the
  skeleton above and note it under a final `## Knowledge gaps` section.

## Boundaries

- Do NOT change any number, commitment, recommendation, or risk statement.
- Do NOT drop the knowledge-gaps section, however unflattering.
- Do NOT add promises the draft did not make.

## Self-check before submitting

Compare every number and named commitment against the draft — zero deltas.
Read the decision brief in under two minutes: can the audience decide from it?

## Summary requirement

Write `summary.md` (≤200 words): what changed in tone/structure for the
audience, confirmation that substance is unchanged, and where the final files
are.
