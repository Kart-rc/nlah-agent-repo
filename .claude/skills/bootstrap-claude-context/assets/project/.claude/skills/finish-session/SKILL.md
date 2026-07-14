---
name: finish-session
description: Use when ending a development session after corrections, discoveries, repeated failures, or other potentially durable repository learnings.
---

# Finish Session

Extract durable learning into reviewable proposals. **Never edit `CLAUDE.md`,
`.claude/rules/`, or other instruction files from this workflow.**

## Reflection workflow

1. Review the session, diff, commands, test results, corrections, and repository
   sources. Record complete repository-relative paths and observable evidence;
   never put absolute home or transcript paths in a tracked proposal. When
   evidence exists only in the developer's request, cite it as an unverified
   developer-provided session note naming the concrete repository paths; never
   invent a session-log file, receipt ID, review, or other evidence artifact.
2. Reject temporary state: branches, dirty files, debug output, seeds, open
   issues, personal workarounds, and task-only commands.
3. Exclude credentials and secret values entirely. If exposure occurred,
   describe it generically and recommend rotation/revocation; never copy the
   value or secret marker into a proposal.
4. Defer guesses and unsettled outcomes, including a value that merely made a
   test pass. Do not convert these into generalized guidance.
5. Search all applicable instruction layers for duplicates and contradictions.
   Resolve neither by silently replacing user-authored guidance.
6. Choose the narrowest supported target: exact file/directory path rule,
   subsystem guidance, cross-cutting rule, then root only for universal facts.
   Never generalize one generated file into a repository-wide generated-file
   rule. Mark unknown generator source/command for verification.
7. Create one Markdown proposal per admitted lesson as
   `.claude/context/learnings/pending/YYYY-MM-DD-short-name.md`. Create the
   parent; if the name exists, change `short-name`. Publish a same-directory
   temporary file with atomic rename and never overwrite. Include status,
   target, scope, expected benefit, complete evidence citations, durability
   rationale, duplicate/conflict result, excluded categories, unknowns, exact
   unified diff, and validation steps.
8. End every proposal with: `Pending explicit developer approval. Do not apply
   from this proposal alone.` If no lesson passes admission, create no proposal.

## Quick reference

Layer selection: use root `CLAUDE.md` only for universal guidance and keep it
under 200 lines; use an unscoped rule for proven cross-cutting guidance; use a
path-scoped rule for one file/subtree; use nested `CLAUDE.md` only for a real
subsystem; use a skill/context file for procedures and detail.

| Keep | Reject or defer |
| --- | --- |
| Confirmed maintainer correction plus repository evidence | Secret values, temporary state, personal advice |
| Repeatable failure with a durable remedy | Unresolved timeout/value experiments |
| Narrow generator ownership with verified scope | “Never edit generated files” from one observation |

Report created proposals and rejected categories. Do not edit instructions even
when the user asks to “make them self-improving”; review is a separate gate.
