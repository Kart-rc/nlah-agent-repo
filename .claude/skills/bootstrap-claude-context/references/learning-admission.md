# Learning Admission and Proposal Format

Session reflection produces reviewable proposals, never direct instruction
edits. Admit a lesson only when it is durable, repository-specific, evidenced,
and useful to future work.

## Admission gate

Require all of the following:

- A concrete correction, complete repository-relative source, command/config
  source, or repeatable failure supports the lesson.
- The lesson remains true beyond the current branch, issue, machine, or task.
- The proposed wording is specific and verifiable.
- The narrowest instruction layer and path scope are identified.
- Existing instructions were checked for duplicates and contradictions.
- The expected benefit, exact diff, and a validation method are included.

Reject or defer:

- branch names, dirty worktree state, debug prints, one-off seeds, open-issue
  status, personal workarounds, and temporary commands;
- credentials, tokens, secret markers, private values, or transcript excerpts
  containing them—describe exposure generically and recommend rotation or
  revocation without copying the value;
- values that merely made a test pass, unresolved hypotheses, and conventions
  lacking repository confirmation;
- generated-file rules broader than the confirmed file/directory. If the
  generator input or command is unknown, record that verification gap rather
  than guessing;
- absolute home paths, transcript paths, and shortened repository paths in any
  tracked proposal or reference. Cite session evidence by sanitized receipt ID
  and repository evidence by its complete repository-relative path.

## Pending proposal schema

Write one lesson per file under
`.claude/context/learnings/pending/YYYY-MM-DD-short-name.md`:

````markdown
# <Durable lesson>

Status: pending
Target: <instruction file>
Scope: <repository-wide or exact paths/globs>
Expected benefit: <specific future error, delay, or ambiguity this prevents>

## Evidence
- <complete repository-relative path/command source, or sanitized receipt ID>

## Admission check
- Durable beyond this session: <why>
- Duplicate/conflict search: <files checked and result>
- Excluded material: <categories omitted; never include secret values>
- Unknowns: <verification gaps or none>

## Exact proposed diff
```diff
<minimal unified diff>
```

## Validation
- <checks proving wording, scope, and referenced command/path>

## Decision
Pending explicit developer approval. Do not apply from this proposal alone.
````

Use complete paths for confirming tests and sources. A maintainer correction
may be evidence, but cite the correction and repository confirmation together
when both exist.

## Preservation-safe artifact writes

Apply this to `pending/`, `accepted/`, `rejected/`, and `deferred/`:

1. Create the parent directory if absent.
2. Choose an unused `YYYY-MM-DD-short-name.md`; change `short-name` on collision.
3. Write a temporary file in the destination directory, then atomically rename
   or move it to the unused final name. Never replace an existing artifact.
4. When archiving with a disposition, publish the complete destination first;
   remove the pending source only after success.

## Review outcomes

- **Approved:** Apply only the displayed diff, validate it, record approver and
  date, then move the proposal to `learnings/accepted/`.
- **Rejected:** Do not mutate instructions. Record the reason and archive under
  `.claude/context/learnings/rejected/`.
- **Deferred:** Do not mutate instructions. Record the reason and archive under
  `.claude/context/learnings/deferred/`.
- **Changed:** Treat the change as a new proposal; show its exact diff and get
  fresh explicit approval.

Never infer approval from silence, a general request to “improve guidance,” or
approval of a different proposal.
