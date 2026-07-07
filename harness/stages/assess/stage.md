---
id: assess
summary: "Assess an existing or proposed architecture and deliver a decisive verdict - approve, approve-with-conditions, or reject - with evidence cited from the subject itself."
producer: planner
inputs:
  - name: requirements
    description: "What the review must judge: scope, quality bar, decision drivers (from intake)."
    format: markdown
    required: true
  - name: subject
    description: "Path to the architecture under review: a design doc, RFC, or codebase root."
    format: path
    required: true
  - name: research_digest
    description: "Prior art, org constraints, and comparables (from research)."
    format: markdown
    required: false
outputs:
  - name: assessment_report
    file: assessment.md
    format: markdown
    description: "Verdict with justification, severity-ranked evidence-cited findings, decidable conditions, alternatives weighed, and failure-mode notes."
acceptance_criteria:
  - "The verdict is exactly one of approve / approve-with-conditions / reject, stated in the first section with a one-paragraph justification."
  - "Every finding cites concrete evidence from the subject: a file, section, or diagram reference verified to exist."
  - "Findings are severity-ranked (blocker/major/minor) and every blocker maps to a condition or to the reject rationale."
  - "Conditions are decidable: each names what must change, how it will be verified, and by when - a vague condition is a hidden reject."
  - "At least one simpler or more boring alternative is weighed, with an explicit statement of why the subject's approach is or is not justified against it."
  - "Failure modes and operational impact are assessed - who runs it, how failure is detected, what rollback looks like - not just structure."
default_validators:
  - uses: validators/completeness-check
    with:
      checklist: policies/gates/architecture.md
  - uses: validators/adversarial-reviewer
    with:
      focus: "verdict hedging, conditions that are actually rejections, findings without evidence in the subject, failure modes asserted but not traced"
  - uses: validators/persona-reviewer
    with:
      persona: "Staff engineer who owns this system and must live with every condition in this verdict"
knowledge_slots: [org-context, prior-art]
skill_refs:
  - skillpacks/tech-director/architectural-judgement
  - skillpacks/addyosmani/documentation-and-adrs
permissions:
  writes: [own_artifact_dir]
---

# Assess

## Purpose

Judge an architecture that already exists on paper or in code, and end the
review with a verdict someone can act on. This stage is judgment, not design:
its value is a decisive, evidence-cited call that survives the pushback of
the people who must live with it.

## Procedure

1. Read the requirements to fix the quality bar: what must this architecture
   satisfy, and what is explicitly out of scope for the review?
2. Explore the subject at the given path - design doc, RFC, or codebase.
   Inventory its key decisions and classify each decision's reversibility
   (one-way vs two-way door) first; scrutiny follows reversibility.
3. Judge against the bar: fitness for requirements, total cost of ownership
   and operational load, novel-technology spend against boring alternatives,
   failure modes and rollback, evolutionary headroom.
4. Record findings as located evidence: each names the file/section/diagram
   it comes from, its severity (blocker/major/minor), and its consequence.
5. Weigh at least one simpler or more boring alternative from the research
   digest or prior art; state explicitly why the subject's approach is or is
   not justified against it.
6. Deliver the verdict: approve / approve-with-conditions / reject. Attach
   decidable conditions only - what changes, verified how, by when. If the
   honest conditions amount to a redesign, the verdict is reject.
7. Consult attached knowledge for org constraints (approved technologies,
   compliance) and prior reviews of this or similar systems.

## Output format constraints

`assessment.md` sections in order: `# Architecture Assessment`, `## Verdict`
(one of approve / approve-with-conditions / reject; one-paragraph
justification), `## Findings` (severity-tagged, each with a subject
citation), `## Conditions` ("None" unless verdict is
approve-with-conditions; each condition: change / verification / deadline),
`## Alternatives weighed`, `## Failure modes and operations`, `## Knowledge
gaps`.

## Knowledge consumption

- `org-context` (e.g. enterprise-mcp): approved-technology lists, compliance
  and operational standards the subject must meet. Cite as
  `[source: enterprise-mcp/<what>]`.
- `prior-art`: earlier ADRs, reviews, or incidents involving this system or
  pattern; a verdict that contradicts a prior accepted decision must say so.
- No adapter attached → proceed; record unverifiable constraints under
  `## Knowledge gaps`.

## Boundaries

- Do NOT redesign the subject - findings and conditions, not a
  counter-design. Sketching your preferred architecture is scope drift (F4).
- Do NOT modify the subject; the path is read-only for this stage. You write
  only to your artifact directory.
- Do NOT soften a reject into a pile of conditions, and do NOT hedge the
  verdict; exactly one of the three outcomes, defended.

## Self-check before submitting

Verify every finding's citation exists in the subject (open the file or
section named). Read each condition asking "could someone verify this is
met, yes or no, by the stated date?" Check the verdict line contains exactly
one of the three allowed outcomes. Confirm the boring alternative got a real
paragraph, not a dismissal.

## Summary requirement

Write `summary.md` (≤200 words): the verdict and its one-paragraph
justification compressed to two sentences, the count of blockers/majors, the
single most consequential finding, and any condition with the nearest
deadline.
