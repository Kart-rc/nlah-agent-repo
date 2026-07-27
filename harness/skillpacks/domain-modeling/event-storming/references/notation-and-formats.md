# Event storming: notation, session formats, and facilitation

Optional deep-dive for `SKILL.md`. Read it when running (or reconstructing)
a live session, when you need the canonical sticky grammar, or when deciding
how deep to storm. The discipline itself is in `SKILL.md`; nothing here
overrides it.

## The sticky grammar

Event storming's colours are a type system. In a text artifact the colour is
gone, so the *label* has to carry the type — which is why `event-storm.md`
names command, actor, policy, external system, and read model explicitly per
event.

| Colour | Element | Reads as | Text form in `event-storm.md` |
|---|---|---|---|
| Orange | Domain event | "X happened" (past tense) | Timeline entry |
| Blue | Command | "do X" (imperative) | `Command:` on the event |
| Yellow (small) | Actor / role | The person or role issuing the command | `Actor:` on the event |
| Lilac / purple | Policy | "whenever X, then Y" — automatic reaction | `Policy:` on the event |
| Pink | External system | Third party or system outside our control | `External:` on the event |
| Green | Read model | What the actor looked at to decide | `Read model:` on the event |
| Red | Hotspot | Disagreement, unknown rule, "it depends" | `## Hotspots` entry |
| Yellow (large) | Aggregate | The thing that accepts the command | **Design level only — not at `intake`** |

The aggregate sticky is listed for completeness. It belongs to design-level
storming and to `domain-modeling/domain-driven-design`; introducing it at
`intake` is the scope drift the skill's Boundaries forbid.

## The three session levels

Pick the shallowest level that answers the question. Depth is not virtue.

### 1. Big picture

Whole business line, many stakeholders, chaotic exploration. Events only, then
rough ordering, then hotspots. No commands, no read models.

- Answers: what does this business actually do, and where does it hurt?
- Use when the request touches a process nobody in the room owns end to end.
- Output at this level: `## Timeline` (sparse) + a dense `## Hotspots`.

### 2. Process level

One process, narrower group. Adds commands, actors, policies, external
systems, and read models — the full grammar in `SKILL.md`.

- Answers: how does this process really run, including the unhappy paths?
- **This is the default level for a harness `intake` stage.**
- Output: all four `event-storm.md` sections.

### 3. Design level

One aggregate's behaviour, engineers only. Adds aggregates, invariants, and
consistency boundaries.

- Answers: what enforces the rules, and inside which transaction?
- **Do not run this at `intake`.** It is the `design` stage's work, and the
  discipline for it is `domain-modeling/domain-driven-design`.

## Facilitating a live session

Rough timeboxes for a process-level session with 5–8 people, 2.5–3 hours:

| Phase | Time | What happens |
|---|---|---|
| Chaotic exploration | 20–30 min | Everyone writes events in silence. Duplicates are fine and informative. |
| Timeline enforcement | 30–40 min | Order them together. Argue. Every argument becomes a hotspot or a split event. |
| Pain points | 15 min | Mark hotspots explicitly; size them where anyone knows the numbers. |
| Commands and actors | 30 min | Walk the timeline backwards asking "what caused this, and who did it?" |
| Policies and read models | 30 min | "What happens automatically after this?" and "what were they looking at?" |
| Walkthrough | 20 min | Narrate the timeline start to finish out loud. The narration exposes gaps nothing else does. |

Facilitation rules worth keeping:

- **Silent writing first.** Discussion first means the loudest person's model
  wins before anyone else has written theirs down.
- **No arrows early.** Arrows encode causality you have not established yet;
  order on the wall is enough.
- **Duplicates are data.** Three people writing the same event with three
  different names is the vocabulary finding of the session.
- **The narration test.** If nobody can narrate the timeline aloud without
  stopping to explain, it is not finished.
- **Timebox the arguments.** An argument that runs past three minutes is a
  hotspot, not a discussion.

## Remote and async adaptation

- A shared board works, but the artifact of record is still `event-storm.md` —
  transcribe before the board rots.
- Async: circulate a provisional timeline derived from evidence and ask
  reviewers to add, reorder, and mark disagreement. Disagreements become
  hotspots; silence is not agreement, and unconfirmed events stay marked
  provisional.
- Record **who** contributed each contested item. "Someone said" cannot be
  followed up; a named source can.

## Reconstructing a storm from a codebase

When there is no session at all, mine evidence in roughly this order — the
earlier sources describe the business, the later ones describe the software:

1. **State machines and status enums** — each transition is a candidate event.
2. **Outbound notifications** (email/SMS/webhook templates) — the business
   announces things it considers real events.
3. **Audit logs and event tables** — already past tense, often already named
   in domain language.
4. **Scheduled jobs and cron entries** — these are policies with a clock as
   the trigger.
5. **Support macros, runbooks, and manual-fix scripts** — the strongest
   hotspot source in any codebase: every manual fix is an unmodelled rule.
6. **Ticket and incident history** — where the process broke is where the
   process is under-specified.

Mark everything derived this way as provisional with its source. Code tells
you what the software does; only a person can confirm what the business
means. Where code and runbook contradict each other, that contradiction is a
hotspot — do not reconcile it yourself.
