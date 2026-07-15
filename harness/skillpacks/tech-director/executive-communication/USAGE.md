# Using `executive-communication`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer package technical judgment for readers who act on documents
under time pressure: answer-first (BLUF) structure, the five-section one-page
decision brief, calibrated uncertainty, and depth tuned to the audience's
altitude.

## When to invoke

- Any run whose final artifact lands on an executive or cross-functional desk —
  the router's decision-, review-, and proposal-shaped work all end here, which
  is why every shipped judgment workflow attaches it at `finalize`.
- A decision record is being written for leadership, or a recommendation will
  be presented in a decision meeting.
- A practitioner-grade document needs rewriting for a VP or cross-org audience.
- See SKILL.md → When to Use / When NOT to use; do not attach it to
  practitioner working stages (e.g. `implement`), where compression loses
  load-bearing detail.

**Default attachments:** suggested by `stages/decide` `skill_refs` (with
`timeboxed-decision-making` and `documentation-and-adrs`); attached to the
`decide` stage of the `tech-decision` workflow and to the `finalize` stage of
the `tech-decision`, `architecture-review`, and `proposal` workflows.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: finalize
    uses: stages/finalize
    skills:
      - uses: skillpacks/tech-director/executive-communication
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/executive-communication/SKILL.md fully,
then rewrite the assessment at <path> as a one-page decision brief for a VP
audience, keeping the full document as the appendix of record.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The artifact's first sentence contains the ask or the verdict; support
  follows in descending importance, never the journey of the analysis.
- A one-page brief with exactly five sections: the ask, recommendation, cost,
  primary risk, decision-needed-by date with the do-nothing default.
- The five standing executive questions (do nothing, alternatives, all-in
  cost, risk/reversibility, sign-offs) are answered inside the document.
- Every number carries a source or a label ("estimate", "measured", "vendor
  claim"); confidence is stated with its basis, neither hedged nor overclaimed.
- Done looks like SKILL.md → Verification: six checkboxes, all answerable from
  the brief itself.
- Misapplication signs (from Red Flags): the ask appearing on page two, or a
  brief that sprawls past one page with ten unowned risks and no primary one.

## Worked example

Request: "We've decided to adopt the managed Kafka offering — get the decision
in front of the platform VP for sign-off this week."

The router runs `tech-decision`; the shipped manifest already attaches this
skill at both `decide` and `finalize`, so no edit is needed. Expected output
shape: a one-page brief in `runs/<run-id>/` opening "We request approval to
migrate streaming to <vendor> managed Kafka, at $180-220k/yr all-in", followed
by the single strongest reason, sourced cost range, the primary risk with its
mitigation, and "decision needed by 2026-07-24; by default the self-managed
cluster renews for 12 months" — with the full option matrix linked as the
artifact of record, not summarized away.
