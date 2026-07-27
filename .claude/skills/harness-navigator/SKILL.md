---
name: harness-navigator
description: Advises which entry point of this harness fits, when the user is NOT asking to execute delivery work. Use for meta-questions about this repository itself - "which skills should I use", "what workflows and skills are available here", "I don't want a full workflow for this", "can I just use the practice skills directly", "no harness for this one", "help me build a new workflow". Interviews the user before recommending a standalone path, and always answers with the reasoning plus one concrete command. Do NOT use for an actual delivery request - adding a feature, fixing a bug, refactoring, making a technical decision, reviewing an architecture, or a stage-by-stage walkthrough of a change; those go to agentic-delivery-router.
---

# Harness Navigator

## Overview

This skill is the starting point for someone who does **not** want to run one of
the shipped workflows — either because the work is a one-off they would rather do
themselves with practice skills, or because it recurs often enough to deserve a
new workflow of its own.

It answers with **reasoning first, then exactly one command**:

```text
0. Check this is actually your job (and that no live run is being abandoned)
1. Discover what exists - delegated to read-only subagents
2. Assess the work using the router's taxonomy and risk rubric
3. Fit check, then a provisional path
4. Interview the user (Path B only) - one question at a time
5. Emit the reasoning, then the command
```

**You advise; you never execute.** You do not run a workflow, write a
`workflow.yaml`, create anything under `runs/`, or touch the target repo. Your
deliverable is a command a human chooses to run. That keystroke between advice and
action is the point — keep it there.

Two skills own the work you route to, and this skill never duplicates them:
`agentic-delivery-router` classifies and orchestrates delivery;
`workflow-composer` authors manifests. See `CLAUDE.md`.

## Step 0: Am I the right skill?

1. **Is there a delivery object?** A feature to add, a bug to fix, a repo to
   change, a decision to make, an architecture to judge. If yes — even phrased as
   "keep it light" or "walk me through it" — STOP. Say: *"That is a delivery
   request; `agentic-delivery-router` owns it, and it has an interactive mode for
   stage-by-stage walkthroughs."* Hand off without inventorying anything.
2. **Is a run already live?** Glob `runs/*/task_state.json`. If any run has status
   `running`, `awaiting_approval`, or `escalated`, name it and say what walking away
   would discard before proposing anything else. Runs are resumable by design
   (`HARNESS.md` §3.2); "let me just do this by hand" is exactly the moment that
   state gets orphaned.
3. Otherwise, continue.

## Step 1: Discover what exists

Never answer from memory, and never carry the whole library in your own context.
**Launch both subagents in a single message so they run concurrently.** Use a
read-only search subagent (`Explore`, or `general-purpose` if unavailable). Neither
writes anything.

**Subagent A — skill inventory.** Glob `harness/skillpacks/*/*/SKILL.md` and
`.claude/skills/*/SKILL.md`; read frontmatter `name` and `description` only. Read
`docs/skillpack-catalog.md` as the pre-built index. Return a compact
name → one-line table grouped by pack, **plus a drift report**: counts from the glob
versus the catalog, naming anything present in one and absent from the other. On
disagreement, trust the glob and report the catalog as stale.

**Subagent B — harness inventory.** Read the `workflow.intent` block of every
`harness/workflows/*/workflow.yaml`; the frontmatter of every
`harness/stages/*/stage.md`; and the work-type mapping table in
`docs/future-workflows.md`. Return which workflow intents match the work (and why),
a candidate stage order for a new composition, and any needed capability no existing
stage covers.

These subagents are context management for an advisory skill. They are **not
harness stages**: no artifacts, no gates, no run state, no `HARNESS.md` §3 protocol.

## Step 2: Assess the work

Read `.claude/skills/agentic-delivery-router/SKILL.md` Steps 2 and 3 and apply its
work-type table and risk rubric. Reference them; never restate them here
(`HARNESS.md` Principle 1). Then record:

```text
WORK ASSESSMENT
- Goal:
- Work type (router taxonomy):
- Risk level (router rubric):
- Reversibility / blast radius:
- Evidence available (tests, spec, docs):
- Repeatable? (one-off, or a process worth encoding):
```

**Risk is stated, never blocking.** At High or Critical, name the specific rubric
trigger and the guarantees a standalone path cannot provide — no approval
checkpoint, no blocking gate, no persisted verdict — and then proceed with what the
user asked for. You never refuse a path, and you never record or imply an approval:
approvals live in run state and belong to the human (`HARNESS.md` §3.1.1).

## Step 3: Fit check, then a provisional path

**Fit check — always runs, never argues.** If an existing workflow's intent covers
this work, say so in **one line** and move on: *"the `<id>` workflow also covers
this, if you change your mind."* Do not recommend it over the paths below; the user
already declined that. The check earns its place by feeding evidence into Path C, so
a new workflow is never built to shadow an existing intent.

- **Path B — standalone practice-skill sequence.** The default. A one-off, a single
  discipline, or work the user wants to drive themselves.
- **Path C — compose a new workflow.** The work recurs and deserves enforced gates,
  or no intent block matches at all (failure class F7, `docs/failure-taxonomy.md`).

## Step 4: Interview before proposing Path B

**Read `harness/skillpacks/addyosmani/interview-me/SKILL.md` fully and apply it
before writing a Path B recommendation.** A sequence built on guessed requirements
is worse than no sequence, and this is the cheapest moment to close that gap.

- **Conduct it in this conversation, never in a subagent** — that skill's *Loading
  Constraints* require a live, responsive user. In a non-interactive context, follow
  its instruction to flag the underspecification as a blocker rather than guessing.
- Honor its **When NOT to use**: skip the interview when the ask is unambiguous and
  self-contained, or when you are already at ~95% confidence.
- Open with `HYPOTHESIS` and a `CONFIDENCE` number. Ask **one** question at a time
  with a `GUESS` attached, and wait for the reaction before the next.
- Stop at its 95% test, restate intent in the user's own words, and loop until you
  get an **explicit yes**.

The restate's fields populate the standalone invocation contract directly: Outcome →
task goal, Constraint → constraints, Success → acceptance criteria, Out of scope →
prohibited changes. Collect input paths, expected output path, and verification
evidence in the same pass.

**Path C gets no interview here.** `workflow-composer` Create mode Step 1 *is* an
interview and owns it. Carry forward what this conversation already contains —
above all the user's verbatim phrasings — and let the composer fill the gaps.

## Step 5: Reasoning, then command

Reasoning comes first. If the command leads, it gets copied and the trade-off never
gets read.

```text
WHY THIS PATH
- <the assessment facts that select it>
- Existing workflow: <one line, or "none matches">
- Runner-up: <the next-best path, and the one fact that ruled it out>
- What a standalone path drops: <the specific guarantees>

COMMAND
<the exact thing to say or run>

WHAT HAPPENS NEXT
- <who takes over: you, the composer, or the router>
- <the next human checkpoint>
```

### Path B command

Fill the standalone invocation contract in `docs/using-skills-standalone.md` from
the interview restate, naming each selected skill by its full
`harness/skillpacks/<pack>/<skill>/SKILL.md` path. Include that document's existing
warning that standalone review is not a harness validation gate.

That document also carries hand-tuned sequences for the common task shapes. **If the
work matches one, cite it rather than inventing a sequence.** Synthesize only when
none fit — and say that you are synthesizing.

### Path C command

Hand off to `workflow-composer` with its Create-mode interview pre-filled:

```text
COMPOSER HANDOFF - pre-filled Create-mode interview (Step 1)
id / name / description:
goal + final deliverables:
intent.summary:              # one sentence the router can match on
intent.triggers:             # the user's VERBATIM phrasings from this conversation
intent.signals:
intent.work_types:           # copied from the router's Step 2 table, never invented
inputs:                      # name, description, format, required

FIT CHECK (already done - do not repeat)
  <workflow id>: rejected because <reason>   # one line per existing workflow

STAGE HINT (the composer owns the final composition - its Step 2)
  <candidate order, and any capability no stage covers>

NOT PRE-DECIDED (composer Steps 3-6): validators, `with` blocks, skills, input
bindings, gate defaults, loopback, knowledge attachments, outputs.
```

The forbidden list is not a formality. Stage `default_validators` and `skill_refs`
are consumed **exactly once**, at scaffold time (`workflow-composer` Create mode) —
a second materialization site is a second place for them to drift out of sync. The
composer also owns lint and the dry-run, which are the real gates on a new manifest.

## Anti-patterns

Avoid: recommending anything before Step 1's subagents return; proposing a Path B
sequence without the interview when the ask is underspecified; asking interview
questions in a batch instead of one at a time; treating a matching workflow as a
reason to argue rather than a one-line mention; refusing a path because the risk is
High; implying that a standalone review is a validation gate; materializing
validators or skills into the composer handoff; running a workflow, writing a
manifest, or creating run state yourself; restating the orchestration protocol
instead of referencing `HARNESS.md`.

**Never enumerate the inventory in this file.** A hardcoded skill list is what made
the previous meta-skill rot silently — nothing lints this file, so a renamed skill
stays green forever. Named dependencies (the router, the composer, `interview-me`)
are structural and belong here; the library is discovered every time.

## Harness integration

This skill sits beside the harness, not inside it. It executes no stage, produces no
artifact, and is bound by no gate — which is exactly why it must be honest about
what the paths it recommends do and do not guarantee.

The harness's guarantees (independent blocking validators, bounded repair, approval
checkpoints, resumable state) exist only inside a run. A standalone sequence has
none of them; the human is the gate. Say so plainly whenever you recommend one, and
let the user choose with that in view rather than by omission.

## Final checklist

- [ ] Step 0 ran: no delivery object, and no live run silently abandoned
- [ ] Inventory came from subagents this session, not memory or a hardcoded list
- [ ] Catalog drift reported if the glob and the catalog disagree
- [ ] Fit check stated in one line, even when the answer is "none matches"
- [ ] Risk named from the router's rubric; no path refused on account of it
- [ ] Interview conducted (or explicitly skipped per its own criteria) before Path B
- [ ] Reasoning printed before the command, with the dropped guarantees named
- [ ] Exactly one concrete command emitted
