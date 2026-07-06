---
id: research
summary: "Gather and digest the evidence a proposal or decision needs: options, prior art, costs, constraints - with sources."
producer: planner
inputs:
  - name: requirements
    description: "What the proposal must decide or argue for (from intake)."
    format: markdown
    required: true
outputs:
  - name: research_digest
    file: research.md
    format: markdown
    description: "Sourced findings organized by the questions the requirements pose: options, prior art, costs, risks, constraints."
acceptance_criteria:
  - "Every open question and requirement from the requirements artifact has a corresponding findings section (or an explicit entry in Knowledge gaps)."
  - "Every factual claim carries a source: a cited document, a knowledge-adapter query result, or a web source."
  - "At least two options/approaches are surfaced for the central question, with observed (not invented) pros and cons."
  - "Findings are separated from interpretation: what sources say vs what the researcher concludes."
  - "Gaps are honest: what could not be learned, and what it would take to learn it."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "unsourced claims, cherry-picked evidence, options dismissed without evidence"
knowledge_slots: [org-context, prior-art, personal-notes]
skill_refs:
  - skillpacks/addyosmani/idea-refine
permissions:
  writes: [own_artifact_dir]
---

# Research

## Purpose

Give the draft stage something true to argue from. This stage is
knowledge-adapter-heavy by design: enterprise context and second-brain notes
change proposals more than eloquence does.

## Procedure

1. Extract the questions: from the requirements' acceptance criteria and open
   questions, list what the proposal must know to be credible.
2. Query every attached knowledge adapter per its adapter doc (see Knowledge
   consumption); then fill remaining gaps with web research where permitted.
3. For the central question, gather at least two options with evidence-based
   pros, cons, and costs. Record where the evidence is thin.
4. Separate findings (sourced) from interpretation (yours, marked as such).
5. Compile the digest organized by question, and an explicit gaps list.

## Output format constraints

`research.md` sections in order: `# Research Digest`, `## Questions
investigated` (list), `## Findings` (one subsection per question; every claim
with a `[source: ...]` marker), `## Options compared` (table or subsections
with pros/cons/costs), `## Interpretation` (clearly separated), `## Knowledge
gaps` (question → what's missing → how to obtain).

## Knowledge consumption

- `org-context` (enterprise-mcp): systems, budgets, policies, and prior
  initiatives relevant to the proposal. Cite as `[source: enterprise-mcp/<what>]`.
- `prior-art`: earlier internal proposals/decisions on this topic.
- `personal-notes` (second-brain): the requester's own notes, preferences,
  past conclusions. Cite as `[source: second-brain/<note>]`.
- Missing adapters degrade gracefully: proceed, and record each unanswered
  question under `## Knowledge gaps` (failure class F6 handling per adapter).

## Boundaries

- Do NOT draft the proposal or make the recommendation — the draft stage owns
  argument; you own evidence. (A "Recommendation" section here is scope drift.)
- Do NOT present interpretation as finding; keep the sections separate.
- Do NOT fabricate sources; an unsourced claim belongs in Interpretation or
  Knowledge gaps.

## Self-check before submitting

Scan every paragraph of `## Findings` for a `[source: ...]` marker. Check each
requirements question has either findings or a gap entry. Verify the options
section has ≥2 genuinely explored options.

## Summary requirement

Write `summary.md` (≤200 words): the questions investigated, the most
decision-relevant finding, the biggest gap, and which option the evidence
currently favors (marked as interpretation).
