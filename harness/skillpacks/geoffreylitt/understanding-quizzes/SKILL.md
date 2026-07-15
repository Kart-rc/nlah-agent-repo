---
name: understanding-quizzes
description: Write a short comprehension quiz for an AI-written change and enforce the rule that code is not sent for review until the responsible human can pass it. Use at the end of every code explainer, before requesting human review of agent-written code, or whenever a human claims to have read and understood a change.
---

# Understanding Quizzes

## Overview

Reading is easy to fake to yourself. "Books don't work" (Andy Matuschak):
it is entirely possible to read an explainer end to end, feel informed, and
be unable to answer the most basic question about the change. A quiz is the
cheap, honest check — and, more importantly, a **speed regulator**. Every
incentive in agentic development pushes toward faster; the quiz is the
mechanism that keeps the team moving at the speed of understanding, not
just the speed of correctness.

## When to Use

- Closing out a code explainer (`code-explainers` ends with a quiz)
- Before a human sends agent-written code to teammates for review
- After any large agent-produced change lands, to check the owner is still
  genuinely in the loop
- Periodically on long-running projects, to detect accumulating cognitive
  debt before it compounds

**When NOT to use:** As a gate on trivial changes, or as a test of the
*agent's* understanding — the quiz exists to measure and protect the
human's understanding, nobody else's.

## The Speed-Regulator Rule

**Code is not sent for human review until the responsible human can pass
the quiz about it.**

- Failing the quiz is a signal, not a shame: re-read the explainer, ask the
  agent questions, or explore a micro-world — then retake it.
- The rule is only worth having if it actually blocks. Skipping it "just
  this once" converts it from a regulator into decoration.
- In a harness run, record the outcome (passed / retaken / waived-with-
  reason) alongside the stage artifacts so the waiver is visible, not
  silent.

## Writing the Quiz

Default shape: **five questions, medium difficulty**, answerable by anyone
who genuinely understood the change — and by nobody who merely skimmed it.

- Target the *decisions and behavior* of the change, not trivia. Filenames,
  function names, and line counts measure memory of the text, not
  understanding of the system.
- Keep answers out of the question view (collapsed section, second page, or
  answer key at the end) so the reader must commit before checking.
- Calibrate difficulty: if the questions can be answered from the section
  headings alone, they are too easy; if they require memorizing incidental
  detail, too hard.

Three question types carry most of the weight:

- **Prediction:** "What happens if X?" — given an input, state, or edge
  case, what does the changed system do?
- **Rationale:** "Why was Y chosen over Z?" — can the reader reproduce the
  reasoning, not just the result?
- **Boundary:** "Where would this break?" — what assumption, load, or input
  would invalidate the approach?

## Anti-Patterns

- **Softball self-grading:** questions written to be passable, graded by
  the same person hoping to pass. Write questions adversarially — aim them
  at what the reader is *most likely* to have glossed over.
- **Prose trivia:** quizzing the wording of the explainer ("what metaphor
  did the background section use?") instead of the behavior of the system.
- **Recall theater:** questions answerable by scrolling up and pattern-
  matching. Prefer questions whose answers require combining two facts.
- **Quiz inflation:** twenty questions nobody will take. Five good ones
  beat twenty mediocre ones.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I read the whole explainer carefully" | So had the engineer who then couldn't answer their reviewer's most basic question. Reading feels like understanding; the quiz tells them apart. |
| "A quiz is childish for senior engineers" | The failure mode it catches — fluent self-deception — gets *more* likely with seniority and speed, not less. |
| "It slows us down" | That is its job. It trades minutes now for not shipping code nobody on the team understands. |
| "The agent verified correctness already" | Correctness and human understanding are different assets. The quiz protects the second one. |

## Red Flags

- Questions answerable without having understood the change (names, counts,
  headings)
- Answers visible next to the questions
- A failed quiz followed by sending the code for review anyway, with no
  recorded waiver
- Quizzes that are always passed on the first try, forever (they are too
  easy — recalibrate)
- No prediction, rationale, or boundary question among the five

## Verification

- [ ] Five questions (or a deliberate, stated different count), medium difficulty
- [ ] Questions target decisions and behavior, not text trivia
- [ ] At least one prediction, one rationale, and one boundary question
- [ ] Answers hidden from the question view
- [ ] Speed-regulator rule stated with the quiz (no review request before a pass)
- [ ] Outcome recorded (passed / retaken / waived-with-reason) where the change's artifacts live
