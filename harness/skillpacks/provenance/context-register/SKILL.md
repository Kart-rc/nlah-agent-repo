---
name: context-register
description: Make gathered context visible and auditable — gathering stages write a context-register.md of every source consulted; consuming stages cite [context: CR-n] on load-bearing decisions. Use whenever downstream work must be traceable to the context that shaped it.
---

# Context Register

## Overview

Context gathering is invisible by default: a stage reads widely, distills,
and hands a summary forward — and nobody downstream can tell which sources
actually shaped the work, which were retrieved and wasted, or which claims
rest on nothing at all. Summarized handoff is the harness's weakest link
(the NLAH paper measured information-handoff recall as low as 0.32 under
parent-child execution). This skill makes context flow auditable: gathered
context gets a register; used context gets a citation; the retrospect stage
computes the difference.

## Two roles

Read the stage contract in your prompt to know which role applies — a stage
that both gathers and consumes plays both.

### Gathering (intake, research)

Write `context-register.md` into your artifact directory, alongside your
declared outputs. One table row per source consulted:

```markdown
# Context Register

| id | source | provenance | relevance | key claim it supports |
|----|--------|------------|-----------|-----------------------|
| CR-1 | docs/architecture.md | repo file, read in full | high | the harness executes manifests, not code |
| CR-2 | user's request | verbatim input | high | the deliverable is a CLI flag, not an API |
```

- `id` is `CR-<n>`, dense from CR-1, never reused or renumbered.
- `provenance` says how you obtained it (file read, adapter query, user
  statement) — enough for a human to re-derive it.
- List sources you consulted and *discarded* too, with relevance `none` and
  the reason; a register of only winners hides the search.

### Consuming (design, plan, implement)

- Cite the register on every load-bearing decision: `[context: CR-n]`
  inline, at the point in your artifact where the decision is stated.
- A load-bearing decision with no register entry behind it gets an explicit
  marker instead: state that no external context informed it. Unmarked,
  uncited claims read as fabrication risk downstream.
- Never edit the register — it lives in the gathering stage's artifacts and
  is not yours to write. Usage is derived from your citations at
  retrospect time, not from mutating the register.

## Red flags

- A register with three winner rows and no discards — the search is hidden.
- Citations sprinkled on trivia while the architecture-shaping decision
  stands uncited.
- `provenance` entries a human could not act on ("web", "docs").
- A consuming stage that copies or rewrites the register instead of citing
  it.

## Verification

Gathering: every source you actually consulted has a row; ids are dense and
unique. Consuming: every load-bearing decision carries a citation or the
explicit no-external-context marker, and every cited `CR-n` exists in the
register.
