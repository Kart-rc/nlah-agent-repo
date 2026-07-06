---
id: design
summary: "Produce a technical design for a change, grounded in the target codebase, with traceable decisions and rollback thinking."
producer: planner
inputs:
  - name: requirements
    description: "Approved requirements with acceptance criteria (from intake)."
    format: markdown
    required: true
  - name: target_repo
    description: "Path to the codebase to change."
    format: path
    required: true
outputs:
  - name: design_doc
    file: design.md
    format: markdown
    description: "Architecture of the change, key decisions with rejected alternatives, failure modes, rollback strategy."
  - name: decisions
    file: decisions.json
    format: json
    description: "Machine-readable ADR list: [{id, decision, rationale, alternatives}]."
acceptance_criteria:
  - "Every requirement in requirements.md maps to at least one design element (traceability table or inline references)."
  - "Each key decision lists at least one rejected alternative with a concrete reason."
  - "The design is grounded in the actual codebase: it names real files/modules it will touch, verified to exist."
  - "Failure modes and a rollback strategy are addressed."
  - "No implementation code - design only."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
knowledge_slots: [org-context, prior-art]
skill_refs:
  - skillpacks/addyosmani/spec-driven-development
  - skillpacks/addyosmani/api-and-interface-design
permissions:
  writes: [own_artifact_dir]
---

# Design

## Purpose

Decide HOW before anyone writes code. The design makes decisions explicit and
attackable while they are still cheap to change, and gives the implement stage
an unambiguous target grounded in the real codebase.

## Procedure

1. Read the requirements artifact fully; extract the list of requirement ids.
2. Explore the target repo: locate the modules, patterns, and conventions the
   change must fit into. Prefer extending existing patterns over inventing new
   ones; note the pattern you are following.
3. Draft the architecture of the change: components touched, data flow,
   interface changes. Reference real paths in the target repo.
4. For each key decision, record the decision, rationale, and at least one
   rejected alternative with the reason for rejection.
5. Enumerate failure modes of the changed system and how each is detected and
   handled; define the rollback strategy.
6. Build the traceability mapping: requirement id → design element(s).
7. Consult attached knowledge sources for prior art and org constraints.

## Output format constraints

`design.md` sections in order: `# Design`, `## Overview`, `## Architecture`
(with real file/module references), `## Key decisions` (one subsection per
decision, each with `Rejected alternative(s):`), `## Failure modes and
rollback`, `## Traceability` (requirement id → design element table),
`## Knowledge gaps`. `decisions.json` is a JSON array of
`{"id", "decision", "rationale", "alternatives"}` mirroring Key decisions.

## Knowledge consumption

- `prior-art`: query attached sources for existing solutions to this problem
  inside the org or the requester's notes; cite what shaped the design.
- `org-context`: constraints (approved technologies, compliance) that bound
  the decision space.
- No adapter attached → proceed; record unanswered questions under
  `## Knowledge gaps`.

## Boundaries

- Do NOT write or modify code, tests, or configs — the implement stage owns
  that. Illustrative interface signatures are allowed; function bodies are not.
- Do NOT re-open requirements. If a requirement is undesignable as written,
  say so in the summary and stop rather than redefining it.

## Self-check before submitting

Verify every referenced path exists in the target repo. Re-read each key
decision asking "did I honestly consider the alternative, or is it a straw
man?" Check the traceability table covers every requirement id.

## Summary requirement

Write `summary.md` (≤200 words): the shape of the change, the 2-3 most
contested decisions and why they went this way, and any requirement that
proved hard to design for.
