# Using `harness-navigator`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Picks an entry point for you when a shipped workflow is not what you want. It
discovers this repository's actual skills, workflows, and stages through read-only
subagents, assesses the work with the router's own taxonomy and risk rubric,
interviews you about what you actually need, and returns the reasoning followed by
one concrete command — either a standalone practice-skill sequence you drive
yourself, or a pre-filled handoff to `workflow-composer` for a new workflow.

It advises only. It never runs a workflow, writes a manifest, or creates run state.

## When to invoke

- You want to know what is available: *"which skills should I use"*, *"what
  workflows and skills are in this repo"*.
- You have work in hand but do not want a full harness run: *"I don't want a
  workflow for this"*, *"can I just use the practice skills directly"*, *"no harness
  for this one"*.
- The work recurs and you suspect it deserves its own workflow, but you are not sure
  whether one already covers it.
- Not for a delivery request. *"Add rate limiting to the API client"*, *"fix this
  bug"*, *"should we use Postgres or DynamoDB"* all go to `agentic-delivery-router`,
  which classifies risk and orchestrates gates.
- Not for a stage-by-stage walkthrough of a change. That is what the router's
  interactive execution mode exists for, and it keeps the gates and teaching
  artifacts a standalone path cannot provide.
- Not while a run is live and unfinished. The skill checks for this and will say so
  before it proposes anything.

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it on meta-questions about this repository and on explicit
requests to skip the harness or build a new workflow. Its description deliberately
excludes delivery phrasing so it does not compete with `agentic-delivery-router`.

## How to invoke

### In conversation

Explicit invocation:

```text
/harness-navigator I need to add structured logging across our three services.
```

Or phrasings that trigger it through the frontmatter description:

```text
What skills are available in this repo, and which apply to a data migration?
```

```text
I don't want a full workflow run for this — can I just use the practice skills?
```

### Requirements

Run it with this repository as the working directory: it globs
`harness/skillpacks/`, `harness/workflows/`, `harness/stages/`, `.claude/skills/`,
and `runs/`, and reads `docs/skillpack-catalog.md`,
`docs/using-skills-standalone.md`, and `docs/future-workflows.md`.

The interview step needs a live, responsive user. In a non-interactive context
(CI, a scheduled run, an autonomous loop) it will flag an underspecified ask as a
blocker instead of guessing at a sequence.

## What to expect

- Two read-only subagents launch first and report back the current inventory,
  including a drift report if `docs/skillpack-catalog.md` disagrees with what is
  actually on disk.
- A short work assessment: work type, risk level, reversibility, and whether the
  work is a one-off or a repeating process.
- One line naming an existing workflow if one covers the work — a mention, not an
  argument. You already said you did not want it.
- For a standalone path, an interview before any recommendation: a stated hypothesis
  with a confidence number, then one question at a time, each with a guess attached,
  until an explicit yes on the restated intent.
- Reasoning first, then exactly one command, then who takes over next. When the
  recommendation is a standalone path, the specific guarantees you are giving up are
  named — not implied.
- Warning signs it is misapplied: a sequence appears before any question was asked;
  several questions arrive at once; a matching workflow is argued for rather than
  mentioned; a path is refused because the risk is High; a manual review is described
  as a validation gate; the handoff to the composer already contains validators or
  skills (SKILL.md → Anti-patterns).

## Worked example

You say: *"We keep doing these one-off data backfills and every one is slightly
different. I don't want the whole workflow ceremony every time — what should I be
using?"*

The skill checks that no run is live, then fans out two subagents to inventory the
skill packs and the workflow and stage libraries. It classifies the work as
`data-change` at Medium risk and notes it is explicitly *repeating*, not a one-off.
The fit check reports that no shipped workflow's intent claims `data-change` — one
line, with the mapping doc cited.

Because you described a recurring process rather than a single task, it recommends
composing a workflow rather than a standalone sequence, and says why: the ceremony
you object to is the part that would stop being ad hoc. It prints the reasoning, the
runner-up path and what ruled it out, and a `workflow-composer` handoff carrying your
own phrasings as the intent triggers, the fit-check result so the composer does not
repeat it, and an explicit note that validators and skills are the composer's to
choose. The command is yours to run — or not.
