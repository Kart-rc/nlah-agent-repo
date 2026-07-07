---
id: options
summary: "Build a decision-grade option matrix: viable options scored against weighted decision drivers, with trade-offs, costs, and reversibility - no recommendation."
producer: planner
inputs:
  - name: requirements
    description: "The decision to be made, its constraints and acceptance criteria (from intake)."
    format: markdown
    required: true
  - name: research_digest
    description: "Sourced evidence about the options (from research)."
    format: markdown
    required: true
outputs:
  - name: option_matrix
    file: options.md
    format: markdown
    description: "Weighted decision drivers, scored options with justifications, costs, reversibility classes, dominant risks, and a sensitivity note."
acceptance_criteria:
  - "At least three options are analyzed, including do-nothing/status-quo, each given full-strength advocacy before scoring."
  - "Decision drivers are explicit and weighted, and every weight traces to the requirements; no driver appears mid-matrix unannounced."
  - "Every option is scored against every driver with a one-line justification that traces to the research digest or is labeled as an assumption."
  - "Each option states its total cost (build, run, opportunity), its reversibility class (one-way vs two-way door) with reasoning, and its dominant risk."
  - "A sensitivity note states which single weight or assumption change would alter the ranking."
  - "No recommendation is made - the matrix ranks; the decide stage chooses."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/adversarial-reviewer
    with:
      focus: "straw-man options, missing do-nothing option, weights reverse-engineered to force a winner, unpriced costs, reversibility misclassified"
knowledge_slots: [org-context, prior-art]
skill_refs:
  - skillpacks/tech-director/options-and-tradeoffs
  - skillpacks/addyosmani/idea-refine
permissions:
  writes: [own_artifact_dir]
---

# Options

## Purpose

Give the decide stage an option space it can trust. The matrix is built and
independently attacked *before* any winner exists, so weights cannot be
reverse-engineered to crown a favorite and losing options get their fair
hearing while it is still cheap to take them seriously.

## Procedure

1. Read the requirements fully; derive the decision drivers - the dimensions
   that matter - and weight them, tracing every weight to a requirement or
   stated constraint.
2. Enumerate the viable options from the research digest, always including
   do-nothing/status-quo. Write each option's strongest honest case before
   scoring anything.
3. Score every option against every driver with a one-line justification per
   cell, citing the research digest; label unsupported cells as assumptions.
4. Price each option as total cost of ownership (build, run, opportunity),
   classify its reversibility (one-way vs two-way door) with reasoning, and
   name its dominant risk.
5. Run the sensitivity check: which single weight or assumption change flips
   the ranking? Record it.
6. Consult attached knowledge sources for org constraints and prior art that
   bound or reorder the option space.

## Output format constraints

`options.md` sections in order: `# Option Matrix`, `## Decision drivers`
(table: driver | weight | source requirement), `## Options` (one subsection
per option: description, strongest case, total cost, reversibility class with
reasoning, dominant risk), `## Scoring matrix` (options x drivers table, each
cell scored and justified inline or footnoted), `## Sensitivity`,
`## Knowledge gaps`.

## Knowledge consumption

- `org-context` (e.g. enterprise-mcp): approved technologies, budget
  ceilings, compliance constraints that eliminate or bound options. Cite as
  `[source: enterprise-mcp/<what>]`.
- `prior-art`: earlier internal decisions on the same question - an option
  the org already tried and abandoned changes its score.
- No adapter attached → proceed; record unanswered constraint questions
  under `## Knowledge gaps`.

## Boundaries

- Do NOT recommend or choose - the decide stage owns the call. A
  "Recommendation" section here is scope drift (F4).
- Do NOT introduce facts absent from the research digest; new claims are
  labeled assumptions or go to Knowledge gaps.
- Do NOT drop an option to "simplify" without recording it and the reason
  under the Options section.

## Self-check before submitting

Verify every driver weight traces to a requirement. Re-read each option's
strongest case asking "would its advocate endorse this phrasing?" Check
do-nothing is present and scored. Confirm every scoring cell has a
justification or an assumption label, and the sensitivity note names a
concrete flip condition.

## Summary requirement

Write `summary.md` (≤200 words): the drivers and their weights, the options
compared, which option currently ranks first and by how much margin, and the
single sensitivity that most threatens that ranking.
