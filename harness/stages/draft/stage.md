---
id: draft
summary: "Write the full proposal from validated research: recommendation, alternatives, costs, risks, and an actionable ask."
producer: analyst
inputs:
  - name: requirements
    description: "What the proposal must decide or argue for (from intake)."
    format: markdown
    required: true
  - name: research_digest
    description: "Sourced findings and options (from research)."
    format: markdown
    required: true
  - name: audience
    description: "Who will read and judge the proposal."
    format: text
    required: true
outputs:
  - name: proposal_draft
    file: proposal.md
    format: markdown
    description: "Complete proposal: executive summary, recommendation, alternatives, costs, risks, implementation sketch, ask."
acceptance_criteria:
  - "The executive summary states the recommendation, its cost, and its primary risk in under 200 words."
  - "Every factual claim traces to the research digest (or is marked as an assumption) - no new facts are invented at draft time."
  - "At least one alternative (including do-nothing) is presented fairly with the reason it loses."
  - "Costs and risks are quantified where research allows, with explicit uncertainty where it does not."
  - "The proposal ends with a concrete, decidable ask (approve X by Y, fund Z)."
  - "Knowledge gaps inherited from research remain visible where they weaken the argument."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
  - uses: validators/persona-reviewer
    with:
      persona: "Skeptical CFO evaluating cost, risk, and ROI"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/documentation-and-adrs
permissions:
  writes: [own_artifact_dir]
---

# Draft

## Purpose

Turn evidence into an argument a decision-maker can act on. The draft is
validated by the harshest gate in the proposal workflow — adversarial review
plus a skeptical-CFO persona — so it is written to survive attack, not to
sound good.

## Procedure

1. Read requirements (the decision needed), research digest (the evidence),
   and the audience input.
2. Choose the recommendation the evidence supports; if the evidence is
   genuinely balanced, recommend with explicit conditions rather than false
   confidence.
3. Write the executive summary last-decision-first: recommendation, cost,
   primary risk, the ask.
4. Build the body: context, recommendation with reasoning traced to research,
   fair treatment of alternatives (including do-nothing), quantified costs and
   risks with uncertainty ranges, implementation sketch, success measures.
5. End with the ask: exactly what decision, by whom, by when.
6. Carry research gaps forward where they matter — a CFO finds hidden gaps.

## Output format constraints

`proposal.md` sections in order: `# Proposal: <title>`, `## Executive
summary`, `## Context`, `## Recommendation`, `## Alternatives considered`,
`## Costs`, `## Risks and mitigations`, `## Implementation sketch`,
`## Success measures`, `## The ask`, `## Knowledge gaps`.

## Knowledge consumption

- `org-context`: templates/precedents for proposals in this org if attached;
  otherwise use the format above and note it under `## Knowledge gaps`.

## Boundaries

- Do NOT introduce facts absent from the research digest; new claims are
  assumptions and must be labeled as such.
- Do NOT re-run research; if the evidence cannot support any recommendation,
  say so in the summary and stop (the gate will escalate).
- Do NOT bury the weaknesses — the validators will find them anyway.

## Self-check before submitting

Read the executive summary alone: is the decision, cost, and risk clear in
under 200 words? Spot-check five claims back to the research digest. Confirm
the do-nothing alternative is treated fairly. Confirm the ask is decidable.

## Summary requirement

Write `summary.md` (≤200 words): the recommendation, the strongest supporting
evidence, the weakest point of the argument, and what the CFO gate will most
likely attack.
