---
id: intake
summary: "Turn a raw request into precise, testable requirements with acceptance criteria, non-goals, and surfaced assumptions."
producer: planner
inputs:
  - name: request
    description: "The user's request, verbatim."
    format: markdown
    required: true
outputs:
  - name: requirements
    file: requirements.md
    format: markdown
    description: "Problem statement, success criteria, acceptance criteria, non-goals, assumptions, open questions."
acceptance_criteria:
  - "The problem statement says what is wrong or missing today, not just what to build."
  - "Every requirement has at least one testable acceptance criterion (a check someone could run and get yes/no)."
  - "Non-goals are stated explicitly - at least two things this work will NOT do."
  - "Every assumption that materially affects the outcome is surfaced in the Assumptions section, not embedded silently in requirements."
  - "Open questions are separated from requirements; nothing ambiguous is presented as decided."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "ambiguity, missing acceptance criteria, hidden assumptions"
knowledge_slots: [org-context, personal-notes]
skill_refs:
  - skillpacks/addyosmani/interview-me
  - skillpacks/addyosmani/spec-driven-development
permissions:
  writes: [own_artifact_dir]
---

# Intake

## Purpose

Every workflow starts here. This stage converts a raw, often ambiguous request
into a requirements artifact precise enough that downstream stages can be
validated against it. Ambiguity that survives intake poisons every later gate,
so this stage is deliberately strict about testability and assumptions.

## Procedure

1. Read the request verbatim. Identify what the requester is trying to
   accomplish (the outcome), not just what they asked for (the mechanism).
2. Draft the problem statement: what is wrong or missing today, for whom, and
   why it matters now.
3. Derive requirements. For each, write at least one acceptance criterion as a
   runnable yes/no check ("running X produces Y", "a reader can find Z").
4. State non-goals: adjacent things this work explicitly will not do.
5. Surface assumptions: everything you decided that the request did not say.
   If an assumption materially changes the outcome and you cannot resolve it
   from attached knowledge sources, list it under Open questions instead.
6. Consult attached knowledge sources (see Knowledge consumption) for
   organizational context before finalizing.

## Output format constraints

`requirements.md` must contain exactly these sections, in order:
`# Requirements`, `## Problem statement`, `## Requirements` (numbered list;
each item followed by its indented `Acceptance:` line(s)), `## Non-goals`
(bulleted, ≥2 items), `## Assumptions` (bulleted; may be empty only if Open
questions explains why), `## Open questions` (bulleted; "none" is acceptable),
`## Knowledge gaps` (what attached sources could not answer; "none" if none).

## Knowledge consumption

- `org-context` (e.g. enterprise-mcp): query for prior art, existing systems,
  and constraints the requester assumes you know. Cite what you use inline
  ("per <source>").
- `personal-notes` (e.g. second-brain): query for the requester's earlier
  decisions or preferences relevant to this request.
- If a slot has no adapter attached, proceed without it and record what you
  would have asked under `## Knowledge gaps`.

## Boundaries

- Do NOT design solutions, name technologies, or sketch implementations —
  requirements only. (Solution content in this artifact is scope drift, F4.)
- Do NOT silently resolve ambiguity in the requester's favor; surface it.
- Do NOT invent constraints the request or knowledge sources don't support.

## Self-check before submitting

Walk each acceptance criterion above against your draft. Specifically re-read
every requirement asking "could two reasonable people implement this
differently and both claim success?" — if yes, tighten the acceptance
criterion or move the point to Open questions.

## Summary requirement

Write `summary.md` (≤200 words) beside your artifacts directory: what the
request is, the 2-3 most consequential requirements, the assumptions most
likely to be challenged, and any open questions blocking downstream stages.
