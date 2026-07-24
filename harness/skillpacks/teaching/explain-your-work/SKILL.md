---
name: explain-your-work
description: Write an EXPLAIN.md teaching artifact alongside every declared output — what you did, why, assumptions, rejected alternatives, what the human should check, and questions for them. Use whenever a human will review, approve, or learn from the stage's work rather than just receive it.
---

# Explain Your Work

## Overview

Your artifacts satisfy a contract; they do not teach. The human at the next
checkpoint has not seen your reasoning — subagent work is invisible by
design — and a pile of correct files does not tell them what to trust, what
to question, or what you silently assumed. This skill adds one artifact that
does: `EXPLAIN.md`, written for a human who wants to *understand* the work,
not grade it.

## When to Use

- The workflow pauses at human checkpoints (notify or block tier) after your
  stage — your EXPLAIN.md is the evidence presented there.
- The requester wants to learn the system or the process, not only receive
  the deliverable.
- Skip nothing by seniority: experts skim the sections they trust and read
  the ones they don't.

## The EXPLAIN.md contract

Write `EXPLAIN.md` into your artifact directory, alongside (never instead
of) your declared outputs, with exactly these six sections:

1. **What I did** — concrete and specific, referencing your artifact files
   by name. Where a context register exists in this run, cite the entries
   that shaped the work as `[context: CR-n]`.
2. **Why** — tie each significant choice to a requirement, criterion, or
   design decision. Cite `[context: CR-n]` for externally-sourced rationale.
3. **What I assumed** — every assumption, ranked by risk: the ones that
   would change the work if wrong come first.
4. **What alternatives I rejected** — real alternatives with the reason each
   lost. "None considered" is an honest entry when true.
5. **What you should check** — actionable: commands to run, files to open,
   the one place a mistake would hide. Not "review the code".
6. **Questions for you** — blocking or shaping questions for the human. The
   harness surfaces these at the next checkpoint; prefer asking here over
   resolving ambiguity by silent assumption. Write "None" when you truly
   have none.

## Voice

The audience is a human learning the system, not a reviewer grading it.
Plain language; define terms on first use; short sections over exhaustive
ones. If a section would exceed a screen, you are documenting, not teaching
— cut to what changes the reader's decisions.

## Red flags

- EXPLAIN.md restates the artifact instead of explaining it.
- Assumptions listed without risk ranking, or an empty assumptions section
  on non-trivial work.
- "What you should check" that no one could act on.
- A question buried in prose instead of the Questions section — it will not
  be surfaced.

## Verification

Before finishing: all six sections present and in order; every `[context:
CR-n]` citation resolves to a register entry; the Questions section exists
even when its content is "None".
