# Self-Improving Claude Context Design

## Goal

Create a reusable Claude Code capability that bootstraps a target repository
with a developer-oriented start walkthrough, lean layered instructions, and a
review-gated learning loop at session end.

## Design principles

- Keep `CLAUDE.md` short, concrete, and limited to universal project guidance.
- Put topic-specific and path-specific instructions in `.claude/rules/`.
- Create nested `CLAUDE.md` files only at genuine subsystem boundaries.
- Load detailed context on demand through skills rather than at every launch.
- Treat session learning as a proposal, never as permission to mutate rules.
- Preserve user-authored files and make bootstrap operations repeatable.
- Make hooks fast, deterministic, non-blocking, and safe for untrusted input.

## Selected approach

Use a hybrid project capability: Claude Code skills perform repository analysis
and judgment, while Python standard-library helpers handle deterministic hook
and file operations. This keeps the capability portable and versionable without
the installation overhead of a full plugin or the weak repository understanding
of a standalone generator.

## Source capability

The reusable source lives in this repository as a skill with bundled scripts,
references, and templates. It installs the following structure into a target
repository:

```text
CLAUDE.md
.claude/
├── settings.json
├── hooks/
│   ├── session-start.py
│   └── session-end.py
├── rules/
│   ├── development-workflow.md
│   ├── testing.md
│   └── architecture/
├── skills/
│   ├── start-codebase/SKILL.md
│   ├── finish-session/SKILL.md
│   └── review-learnings/SKILL.md
└── context/
    ├── codebase-map.md
    └── learnings/
        ├── pending/
        └── accepted/
```

The bootstrap skill proposes project-specific content after examining repository
structure, build files, tests, documentation, and existing agent instructions.
It shows conflicts and planned writes before applying them. Re-running it is
idempotent and preserves handwritten content.

## Start workflow

The `start-codebase` skill prepares a developer to work by:

1. Checking repository status and recent changes.
2. Reading the lean instruction layers relevant to the requested work.
3. Identifying languages, build tools, tests, entry points, and subsystem
   boundaries.
4. Explaining the architecture and likely change points with file evidence.
5. Running safe, read-only baseline checks when available.
6. Surfacing pending learning proposals for review.

The `SessionStart` hook injects only a concise startup message. It points Claude
to the start skill, current codebase map, and pending proposals rather than
dumping a repository summary into every session.

## Layered instruction model

Use the narrowest scope that reliably reaches the work:

| Layer | Content | Loading behavior |
|---|---|---|
| Root `CLAUDE.md` | Universal invariants, essential commands, navigation | Every session |
| Unscoped `.claude/rules/*.md` | Cross-cutting testing and workflow rules | Every session |
| Path-scoped rules | Language, module, and file-pattern guardrails | When matching paths are used |
| Nested `CLAUDE.md` | Subsystem-only architecture and commands | When the subsystem is accessed |
| Skills and context files | Walkthroughs, procedures, and detailed maps | On demand |

The root file targets fewer than 200 lines. Rules must be specific, verifiable,
non-duplicative, and free of contradictions with broader layers.

## Session-end learning flow

Use `SessionEnd` rather than Claude Code's `Stop` event for the automatic
session boundary because `Stop` fires after every assistant response. Provide a
manual `finish-session` skill for immediate reflection before exiting.

At session end, the deterministic hook records a small receipt containing the
session identifier, transcript path, working directory, and repository state.
It does not edit instructions. At the next session start, Claude is told to
evaluate pending receipts. Durable lessons become proposal files; sessions with
no durable lesson produce no proposal.

The `review-learnings` skill checks each proposal, displays the exact instruction
diff, and applies only developer-approved changes. Applied proposals move to the
accepted directory with their evidence and disposition.

## Learning admission rules

A proposal must:

- cite repository paths, commands, corrections, or repeatable failures;
- describe durable project behavior rather than temporary task state;
- select the narrowest correct instruction layer and path scope;
- search all existing layers for duplication and contradiction;
- contain an exact proposed diff and expected benefit;
- exclude secrets, personal preferences, guesses, and generated-file details;
- preserve handwritten instructions and the root file's size budget; and
- remain pending until a developer explicitly approves it.

## Hook safety and failure behavior

- Parse hook JSON with the Python standard library.
- Treat every input field as untrusted and validate paths before access.
- Avoid shell interpolation and external dependencies such as `jq`.
- Write receipts atomically with unique session-derived names.
- Never block session startup or exit because reflection failed.
- Emit concise diagnostics without transcript content or secrets.
- Avoid global state and writes outside the target repository.

## Verification

1. Run fixture-repository tests for bootstrap generation and repeat execution.
2. Prove existing files and user edits survive re-runs.
3. Exercise `SessionStart` and `SessionEnd` helpers with representative JSON.
4. Cover malformed input, missing Git metadata, clean and dirty worktrees,
   unsafe paths, duplicate receipts, and unavailable context files.
5. Validate skill frontmatter, settings JSON, rule scopes, and line budgets.
6. Run baseline and forward scenarios to show that the skills change agent
   behavior without leaking the expected answer.
7. Perform a manual Claude Code restart test because hooks load at session
   startup.

## Non-goals

- Automatically editing committed instructions at session end.
- Replacing Claude Code auto memory.
- Building a cross-editor agent configuration standard.
- Requiring a remote service, database, or third-party runtime.
- Generating detailed rules for parts of a repository that were not inspected.
