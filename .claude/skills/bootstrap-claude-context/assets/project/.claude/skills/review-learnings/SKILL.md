---
name: review-learnings
description: Use when pending Claude Code learning proposals need approval, rejection, revision, or application to project instructions.
---

# Review Learnings

Review one pending proposal at a time. Approval is proposal-specific; never
infer it from silence or a general request to improve instructions.

## Review workflow

1. Read the proposal, target instruction, all applicable broader/narrower
   layers, and every cited repository source. Reject unsupported claims and
   incomplete citations. Validate that its expected benefit is specific and
   supported; require complete repository-relative evidence paths and reject
   absolute home/transcript paths in tracked artifacts. Label inferences and
   verification gaps.
2. Recheck durability, duplicates, contradictions, and scope. Keep service or
   generated-path knowledge out of root guidance. Reject secrets, temporary
   state, and unsettled hypotheses; if exposure is reported, recommend
   rotation/revocation without reproducing the value.
3. For a valid proposal, recompute and show the minimal exact diff, expected
   benefit, evidence, scope, conflicts, and validation plan. Ask the developer
   to choose **apply, revise, defer, or reject**. For an invalid proposal, show
   findings and ask for **revise, defer, or reject**; do not offer apply.
4. A bare “no,” cancellation, silence, or ambiguous response leaves the pending
   proposal unchanged. Archive only an explicit apply/defer/reject disposition.
   Revise remains pending, and its new exact diff requires a new choice.
5. After explicit apply, apply only the displayed diff. Preserve unrelated and
   handwritten content; stop and re-propose if the target changed materially.
6. Validate referenced paths/commands, rule frontmatter and scope, root size,
   duplicate/contradictory guidance, and the final diff. Enforce root
   `CLAUDE.md` below 200 lines. Run a project context validator when available.
7. Record disposition, approver, date, applied diff, and validation result.
   Archive apply under `.claude/context/learnings/accepted/`, reject under
   `.claude/context/learnings/rejected/`, and defer under
   `.claude/context/learnings/deferred/`. Create the parent, choose an unused
   `YYYY-MM-DD-short-name.md`, and use a destination temporary file plus atomic
   rename/move; never overwrite. Remove pending only after archive success.

## Layer selection

- Root `CLAUDE.md`: universal guidance only; fewer than 200 lines.
- Unscoped rule: proven repository-wide cross-cutting guidance.
- Path-scoped rule: guidance for one file or subtree.
- Nested `CLAUDE.md`: several instructions for a real subsystem boundary.
- Skill/context: procedures, walkthroughs, and detailed reference.

## Approval checkpoint

Use a direct question such as: “Choose apply, revise, defer, or reject for this
exact diff to `<path>`.” Only `apply` authorizes the instruction edit.

## Common mistakes

- Approving several proposals as a batch without showing each diff.
- Applying a cleaned-up diff that differs from the approved one.
- Moving payment-only or generated-file knowledge into root guidance.
- Deleting rejected evidence instead of recording its disposition.
