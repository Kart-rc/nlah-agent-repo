---
name: code-explainers
description: Produce a literate explainer document for a nontrivial AI-written change instead of handing over a raw diff. Use when delivering implemented code to a human, when a reviewer must understand a change they did not write, or when a change touches a system the reader may not know.
---

# Code Explainers

## Overview

A raw diff is the material of a change, not an explanation of it. When an
agent writes code, the human who must stay in the loop deserves the best
possible explanation — the one a team would produce if sent away to build a
personalized curriculum for this single change. This skill is the discipline
for writing that explainer: background first, intuition before details, then
a literate walk through the code in teaching order. The goal is not
verification alone; it is understanding deep enough that the reader can
participate in the next idea.

## When to Use

- Delivering any nontrivial implemented change to a human owner or reviewer
- A change touches a subsystem the likely reader did not build or has not
  visited recently
- A migration, refactor, or behavioral change whose "why" is not obvious
  from its "what"
- The reader asked "walk me through what you did"

**When NOT to use:** Trivial mechanical changes (typo fixes, renames,
version bumps) where the diff *is* the explanation — an explainer for a
one-line change is ceremony, not teaching.

## Background Before the Change

Do not start with what happened. Start by teaching how the affected system
works today, as if the reader were joining the project at this file.

- Name the components involved, what each is responsible for, and how data
  flows between them — only the slice relevant to this change.
- Write it skippably: a reader who already knows the system should be able
  to skim headers and move on. Personalize to what the reader is likely to
  already know when you know your audience.
- If the change exists to fix a defect, describe the *correct* current
  behavior first, then where and why it goes wrong.

## Intuition Before Details

Before any code appears, state the essence of the change — what a deep,
well-written commit message would say.

- One or two sentences of goal ("make the garden feel three-dimensional
  using only 2D drawing tricks"), then the *approach* in plain language.
- Give concrete examples and before/after behavior so the reader has a feel
  for the change before reading a line of code. This is what good teachers
  do: essence first, mechanism second.
- Name the alternatives that were rejected and why, in a sentence each —
  rationale is the part of a change that a diff can never show.

## Literate Code Diff

Then, and only then, show the code — as prose-led teaching, never as a raw
file-order dump.

- Order the files by narrative, not alphabetically: start where the change
  conceptually begins (the data model, the entry point, the core algorithm)
  and let each section motivate the next.
- Before each file or hunk, write a short paragraph: what this piece does,
  why it changed, and what to notice in it.
- Quote the relevant hunks, trimmed to what teaches; link or reference the
  full diff for completeness rather than inlining every line.
- Accumulated properly, the document reads like a chapter about the PR —
  something a reader could take to a coffee shop and follow without an IDE.

## Interactive Figures, Used Tastefully

Where a static explanation cannot carry the intuition, embed something to
fiddle with — a draggable simulation, a scrubbable timeline, a live
coordinate readout.

- Interactivity must reveal something text and pictures cannot; as a
  default garnish it is a crutch and reads as slop.
- Prefer one figure that makes the core mechanism feelable over several
  decorative ones.
- If a full interactive micro-world is warranted, hand off to the
  `micro-worlds` skill rather than growing the explainer into an app.

## Output Contract

- Produce **both** a markdown artifact and a self-contained HTML artifact,
  written next to the change: in a harness run, under the stage's artifact
  directory inside `runs/<run-id>/`; standalone, alongside the deliverable
  or where the operator directs.
- Markdown is the canonical, diffable, comment-friendly version; HTML is the
  rendered reading version and the only carrier for interactive figures
  (keep it dependency-free and openable from disk).
- End the document with a short comprehension quiz per the
  `understanding-quizzes` skill — an explainer without a check is a book,
  and books don't work.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The diff is self-explanatory" | To its author. The reader lacks the context the author burned hours acquiring; the explainer transfers it in minutes. |
| "The commit message covers it" | A commit message states the what and a hint of why. It teaches no background and walks no code. |
| "Writing docs slows delivery" | Un-understood code is cognitive debt; it gets repaid later with interest, by a human who can no longer participate. |
| "I'll add an interactive demo to make it engaging" | Engagement is not the goal; understanding is. Interactivity that reveals nothing is slop. |

## Red Flags

- The explainer opens with a file list or the diff itself
- Background section missing, or unskippable (interleaved with the change)
- Code shown in alphabetical/file order with no prose between hunks
- Rejected alternatives and rationale nowhere in the document
- Interactive figures that demonstrate nothing a sentence couldn't
- Only one output format produced, or HTML that requires a build step to view
- No quiz at the end

## Verification

- [ ] Document opens with skippable background teaching the affected system
- [ ] Essence of the change stated in plain language before any code
- [ ] Code walked in narrative order with prose before each file/hunk
- [ ] Rejected alternatives and rationale recorded
- [ ] Any interactive figure justifies itself (reveals what static text cannot)
- [ ] Both markdown and self-contained HTML artifacts written to the correct location
- [ ] Document ends with a quiz per `understanding-quizzes`
