# Using `review-debt-code-review`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Adds a review-debt lens to ordinary code review: traceable evidence across
five signal families (diff size/coupling, test evidence gap, owner spread,
AI-authorship indicators, rationale gaps), a human held accountable for
understanding and risk, and a qualitative burden and verdict — supplementing,
never replacing, engineering findings.

## When to invoke

SKILL.md has no "When to Use" section, so route on these cues:

- Reviewing a pull request or diff that is large, touches many directories or
  owners, or arrived faster than a human could plausibly have understood it.
- Changes with suspected AI-assisted volume, thin commit rationale, or tests
  that mirror the implementation rather than prove intended behavior.
- A team wants review findings framed around hidden human review burden —
  e.g. deciding where reviewer attention should go on a big change.
- Not for routine small diffs where an ordinary review suffices, and not as a
  scoring tool: the skill forbids inventing a 0-100 score or check weights.

**Default attachments:** none — ad hoc (the pack README states the pack does
not attach itself to any workflow). Attach it explicitly on a review-shaped
stage, most naturally `verify` in the `sdlc` workflow when the thing being
verified is a code change's reviewability.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: verify
    uses: stages/verify
    skills:
      - uses: skillpacks/review-debt/review-debt-code-review
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/review-debt/review-debt-code-review/SKILL.md fully,
including its required reference references/review-debt-framework.md, then
apply its workflow to review the pull request diff at <path or PR number>.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer must also read `references/review-debt-framework.md` —
  SKILL.md marks it required; it defines the signal evidence, burden
  calibration, and required output. A review without it is incomplete.
- Tests are inspected before implementation: intended behavior, whether they
  failed before the change, and assertion quality.
- Prioritized findings come first, each citing a file/line/diff fact with
  impact and a concrete remedy; then a report in stable sections: review-debt
  evidence, reviewer focus, author next actions, missing/unverified evidence,
  qualitative burden, verdict.
- AI-authorship indicators are informational only, never penalized; missing
  rationale or evidence is listed as unverified, never guessed; there is no
  numeric score and no empty `LGTM`.
- Misapplication signs (from Guardrails): a 0-100 score or invented
  thresholds in the output, or reviewer-focus items mixed into author actions.
- The folder also ships `agents/openai.yaml`, an agent definition for running
  the skill outside this harness; harness runs ignore it.

## Worked example

Request: "Review PR #482 — 3,800 added lines across 9 directories, opened
four hours after the ticket was filed."

Since the skill has no default attachment, attach it to the `sdlc` `verify`
stage via `workflow-composer`, or run the standalone prompt above against the
PR diff. Expected output shape: prioritized findings first (e.g. "assertions
in `tests/billing_test.py` restate the implementation's rounding logic — no
failure-before-fix evidence supplied"), then the six stable report sections,
with AI-authorship indicators noted as informational, unverified items listed
rather than guessed, a qualitative burden judgment, and a verdict stating
what evidence supports it and what remains unverified.
