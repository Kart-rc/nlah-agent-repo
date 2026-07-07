---
id: decide
summary: "Make the call, time-bound: a decision record with rationale traced to the option matrix, steelmanned dissent, reversibility, revisit triggers, and execution asks."
producer: planner
inputs:
  - name: requirements
    description: "The decision to be made and its constraints (from intake)."
    format: markdown
    required: true
  - name: option_matrix
    description: "The independently validated option matrix (from options)."
    format: markdown
    required: true
  - name: decision_deadline
    description: "When the call must be made or take effect; drives the confidence-vs-analysis trade."
    format: text
    required: false
outputs:
  - name: decision_record
    file: decision.md
    format: markdown
    description: "The call, rationale, dissent and responses, reversibility and confidence, revisit triggers, and execution asks."
acceptance_criteria:
  - "The decision is stated in one unambiguous sentence naming the chosen option, with an owner and a decision date."
  - "The rationale traces to the option matrix; if the call departs from the top-ranked option, the departure is justified explicitly."
  - "The strongest argument against the decision is steelmanned and answered - not omitted, not caricatured."
  - "Reversibility is classified (one-way vs two-way door) and confidence is stated; deciding a two-way door at partial information is acceptable and says so."
  - "Revisit triggers are concrete and observable: the measurable event or date that reopens this decision."
  - "The record ends with execution asks: who does what by when to make the decision real."
default_validators:
  - uses: validators/completeness-check
    with:
      checklist: policies/gates/decision.md
  - uses: validators/adversarial-reviewer
    with:
      focus: "rationale that does not follow from the matrix, dissent omitted or straw-manned, one-way doors treated as reversible, revisit triggers nobody can observe, deadline ignored"
  - uses: validators/persona-reviewer
    with:
      persona: "Principal engineer who championed the losing option and will re-litigate this decision in every forum unless the record answers them"
knowledge_slots: [prior-art, personal-notes]
skill_refs:
  - skillpacks/tech-director/timeboxed-decision-making
  - skillpacks/tech-director/executive-communication
  - skillpacks/addyosmani/documentation-and-adrs
permissions:
  writes: [own_artifact_dir]
---

# Decide

## Purpose

Convert a validated option space into a commitment the organization can act
on and will not quietly re-make. The deliverable is the call itself -
recorded so that a skeptic finds their objection already answered, and so
the decision reopens on observable triggers rather than on repetition of the
original arguments.

## Procedure

1. Read the requirements and the option matrix fully. Classify the door: is
   this decision one-way or two-way? Match the depth of deliberation to
   that class and to the deadline.
2. Make the call. Default to the matrix's top-ranked option; a departure is
   legitimate only with an explicit justification the matrix's authors could
   follow (e.g. a driver the matrix flagged as sensitive, an org constraint
   from attached knowledge).
3. State confidence honestly against the information available. If the
   deadline binds, decide at stated confidence rather than deferring; if the
   door is one-way and confidence is genuinely insufficient, the recorded
   decision is to buy specific information, with an owner and a date.
4. Steelman the strongest dissent - phrase it so its advocate would endorse
   the wording - and answer it with substance from the matrix or evidence.
5. Define revisit triggers: the observable metric threshold or dated event
   that reopens this decision. Nothing else reopens it.
6. Close with execution asks: who does what by when, and who must be
   informed before the decision takes effect.
7. Consult attached knowledge for prior decisions on this question and the
   requester's own recorded positions; a decision that contradicts either
   must say so.

## Output format constraints

`decision.md` sections in order: `# Decision Record`, `## The call` (one
sentence naming the chosen option; owner; decision date; confidence; door
class), `## Rationale` (traced to the matrix; any departure from its ranking
justified), `## Dissent and responses`, `## Reversibility and revisit
triggers`, `## Execution asks` (who / what / by when; inform-list),
`## Knowledge gaps`.

## Knowledge consumption

- `prior-art`: earlier internal decisions or ADRs on this question; cite
  what this record affirms, supersedes, or contradicts.
- `personal-notes` (e.g. second-brain): the requester's recorded
  preferences and past conclusions - a call that overrides them should
  acknowledge it. Cite as `[source: second-brain/<note>]`.
- No adapter attached → proceed; record what could not be checked under
  `## Knowledge gaps`.

## Boundaries

- Do NOT rebuild, re-score, or extend the option matrix - it passed its own
  gate. If it cannot support any call, say so in the summary and stop; the
  gate escalates rather than you repairing another stage's artifact.
- Do NOT defer without a date and a default; "decide later" is not a
  decision.
- Do NOT soften the call into a hedge ("we lean towards..."); one option is
  chosen, the others lose, on the record.

## Self-check before submitting

Read `## The call` alone: does it name one option, an owner, a date, and a
confidence? Check every rationale claim traces to the matrix or to cited
knowledge. Ask of the dissent section: "would the losing option's champion
say this is their actual argument?" Verify each revisit trigger is something
a person could observe firing.

## Summary requirement

Write `summary.md` (≤200 words): the call in one sentence, the deciding
rationale, the strongest dissent and its answer, the confidence and door
class, and the first execution ask.
