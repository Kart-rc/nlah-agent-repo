---
name: timeboxed-decision-making
description: Makes technical calls at stated confidence within a deadline. Use when a decision has a date attached, when analysis is dragging past its value, or when dissent must be resolved into commitment rather than re-litigated.
---

# Time-boxed Decision Making

## Overview

A director's job is not to be right with unlimited time; it is to be right
*enough, on time*, and to make the decision stick. This skill covers matching
decision process to decision weight, deciding at partial information without
pretending it is complete, and converting disagreement into commitment with
honest revisit conditions.

The failure mode this defeats is the un-decision: analysis that continues
past its value, deferral without a date, and decisions that get quietly
re-made in every subsequent meeting.

## When to Use

- A decision has a deadline, or the cost of delay now exceeds the value of
  more analysis
- Choosing how much process a decision deserves
- Recording a decision others disagreed with
- A previously "made" decision keeps getting reopened

**When NOT to use:** Genuine one-way doors where more information is cheaply
available before the deadline — go get it. Decisions that are not yours to
make — route them to the right owner instead of deciding faster.

## Doors: Match Process to Reversibility

Classify the decision first:

- **Two-way door** — reversal is cheap. Decide fast, with the smallest group
  that has the context. The risk of over-analyzing a two-way door is real:
  the delay costs more than a wrong pick would.
- **One-way door** — reversal is expensive or impossible. Slow down
  deliberately: full option matrix, dissent actively solicited, the decision
  socialized before it is announced.

Most decisions are two-way doors treated as one-way doors. The costly errors
are the reverse.

## The 70% Rule

Decide when you have roughly 70% of the information you wish you had. Waiting
for 90% means being late on almost everything; deciding at 40% is gambling.

- **State confidence honestly** in the record: "deciding at moderate
  confidence because the deadline binds and the door is two-way."
- Deciding a two-way door at partial information is not a compromise — it is
  the correct calibration, and the record should say so without apology.
- If confidence is genuinely below the bar for a one-way door, the decision
  is to *buy information*, with a date: what will be learned, by whom, by when.

## Deadline Mechanics

- Every open decision carries a **decide-by date** and a **default**: what
  happens if no decision is made by then. A missing default means the status
  quo is deciding for you, silently.
- When the timebox expires, one of three things happens — the call is made,
  the default takes effect, or the decision is **escalated** with a crisp
  framing (options, recommendation, what the escalation resolves). Escalation
  on criteria is a designed move, not a failure.
- Deferral is only a decision when it has a date and a reason. "Let's revisit
  later" without either is abdication.

## Disagree and Commit

Dissent is fuel before the decision and poison after it — unless it is
handled explicitly:

- **Steelman the dissent in the record.** The strongest opposing argument,
  stated so its advocate would endorse the phrasing, then answered with
  substance. Omitted or caricatured dissent guarantees re-litigation.
- Ask dissenters for explicit commitment, and give them the honest exit:
  concrete **revisit triggers** — the observable event or metric that reopens
  the decision. "We revisit if p99 latency exceeds 200ms in production" is a
  trigger; "we'll revisit if it doesn't work out" is not.
- Once recorded, the decision is re-opened by triggers, not by repetition of
  the original arguments.

## Decision Hygiene

- **Decide at the right level.** If a team can safely own the call, pushing
  it up adds latency and subtracts ownership. If it crosses team boundaries
  or is a one-way door, deciding it quietly below the line creates rework.
- **Inform deliberately.** List who must hear the decision before it takes
  effect, from the record, not from rumor.
- **Keep a decision journal.** Decisions with dates, confidence, and
  expected outcomes — reviewed later against reality — are the only reliable
  way to calibrate your own judgment.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We need more data" | Sometimes true. Then buying data *is* the decision — with an owner and a date, not an open-ended pause. |
| "Consensus will emerge" | Consensus at the deadline is luck. Alignment is built by deciding and honestly recording dissent. |
| "It's too early to commit" | If the door is two-way, it is almost never too early. Commit, instrument, revisit on triggers. |
| "Re-opening shows we listen" | Re-opening without a trigger teaches everyone that decisions are provisional and lobbying works. |

## Red Flags

- Decisions with no decide-by date and no default
- One-way doors decided in a hallway; two-way doors given month-long studies
- Records with no dissent section on a contested decision
- Revisit conditions no one could observe or measure
- The same decision appearing on three consecutive meeting agendas

## Verification

- [ ] Door type classified, with reasoning
- [ ] Decide-by date and default stated
- [ ] Confidence stated honestly against the information available
- [ ] Strongest dissent steelmanned and answered
- [ ] Revisit triggers observable and concrete
- [ ] Owner and inform-list named
