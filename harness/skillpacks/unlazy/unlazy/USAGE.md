# Using `unlazy`

> Companion guide for [SKILL.md](SKILL.md). Read the skill itself before doing
> substantial work; this guide explains where it fits in NLAH.

## What it adds

`unlazy` externalizes completion criteria into `GATES.md` or `gates/*.md` and
uses `scripts/gate-check.mjs` to execute checks, match expected output, check
passing boxes, and record the deciding evidence. Its Depth Tree adds per-leaf
and integration ledgers when a task is too large for one focused context.

## When to invoke

- A substantial standalone task repeatedly returns half done.
- An agent is likely to narrow scope silently or report completion early.
- The user asks for exhaustive work, `tree N`, gates, or persistence until all
  outcomes are evidenced.
- A long task needs completion state to survive context pressure without the
  overhead of a full NLAH workflow.

Do not use it for conversational answers, trivial edits, or factual lookups.
Use a full NLAH workflow instead when the work needs risk classification,
approval checkpoints, independent validators, repair/escalation policy, or
resumable multi-stage state.

## Prerequisite and invocation

The markdown discipline works in any Agent Skills reader. The bundled checker
and optional hook require Node.js 16 or newer.

Standalone prompt:

```text
Read harness/skillpacks/unlazy/unlazy/SKILL.md fully and apply it to
<substantial task>. Keep the gate ledger in <working directory>, run its CHECK
commands, and do not report completion while any gate lacks evidence.
```

For a focused task, copy `templates/gates-leaf.md` to `GATES.md`, replace the
placeholders with observable outcomes, then run:

```bash
node harness/skillpacks/unlazy/unlazy/scripts/gate-check.mjs GATES.md
node harness/skillpacks/unlazy/unlazy/scripts/gate-check.mjs --status GATES.md
```

For tree depth 4+ or work clearly beyond one sitting, also read
`references/method.md` and `references/orchestration.md`; start from
`templates/PLAN.md`, `templates/gates-leaf.md`, and
`templates/gates-node.md`.

## Evidence and exit semantics

- A checked box with `EVIDENCE: pending` remains unmet.
- Re-measure every number used in the final report.
- `ABANDON: <gate> <reason>` is a visible statement of incomplete scope. It is
  an honest handoff, not proof that the promised outcome succeeded.
- `CHECK` values are shell commands. Review them with the same permission and
  destructive-action care as any other command before executing the checker.
- A complete report includes the ledger status, all abandoned gates, and
  evidence-backed counts.

## Full harness boundary

No shipped workflow attaches this skill. During a full NLAH run, `HARNESS.md`
remains the sole orchestration contract: producers write to their stage paths,
validators independently judge artifacts, failures repair or escalate, and
only the locked manifest defines topology. Do not create an overlapping
root-level `PLAN.md` or treat upstream `ABANDON` as a passed NLAH gate.

## Optional Stop hook

The upstream Stop hook can block Claude Code from ending a turn while local
gate files remain unmet. It changes project or global settings, writes
`.unlazy-hook-state.json`, and scans the process working directory. Never
install it implicitly. Offer it only when explicitly useful, explain its scope,
and obtain the user's permission before running `scripts/install-hooks.mjs`.

## Worked example

Request: “Refactor all twelve import adapters; do not stop at a sample.”

Create one gate per adapter outcome plus build, regression, and exact-count
gates. Run the checker after each slice. If only eleven adapters pass, report
`11 met, 1 unmet` and continue; never turn the missing adapter into an
unmentioned follow-up or state `12/12` from memory.
