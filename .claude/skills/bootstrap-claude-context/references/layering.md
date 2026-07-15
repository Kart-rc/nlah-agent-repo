# Layer Selection

Choose the narrowest layer that reliably reaches the affected work. A broader
layer requires broader evidence; convenience is not evidence.

## Selection order

| Layer | Put here | Do not put here |
| --- | --- | --- |
| Root `CLAUDE.md` | Repository purpose, universal invariants, essential root commands, and routing | One service's conventions, static inventories, session state, or guesses |
| Unscoped `.claude/rules/*.md` | A cross-cutting rule proven to apply throughout the repository | Language, module, or path-specific behavior |
| Path-scoped `.claude/rules/*.md` | Rules for explicit globs such as `services/payments/**` or `**/*.py` | Unrelated paths or claims inferred from one example |
| Nested `CLAUDE.md` | A genuine subsystem's architecture and local commands when that directory is a durable ownership boundary | A rule affecting only a smaller path or a duplicate of a broader rule |
| Skill or context file | On-demand procedures, walkthroughs, detailed maps, and volatile orientation | Mandatory invariants that must load for affected work |

Prefer a path-scoped rule over a nested `CLAUDE.md` when a precise glob can
express the scope. Use a nested file only when the directory is independently
owned or operated and several local instructions belong together.
When durable facts inside one subsystem have different narrow scopes, create
separate path-scoped rules for each scope; never widen them to a common parent
only for file-count or organizational convenience.

Express path scope in rule frontmatter, for example:

```markdown
---
paths:
  - "services/payments/**"
---
```

## Rule admission

For each proposed rule:

1. State the behavior in one testable sentence.
2. Cite the exact source with complete repository-relative paths: repository
   file, command/config entry, maintainer correction, or repeatable failure.
   Cite all confirming files, not shortened names that cannot be located. Never
   put an absolute home or transcript path in tracked guidance or context.
3. Separate observed facts from inference. Do not promote an inference until
   repository evidence confirms it.
4. Search root guidance, all applicable rule files, and parent/nested
   instructions for duplication or contradiction.
5. Select the smallest path set supported by the evidence. Do not create rules
   for adjacent or unrelated areas.

## Evidence and conflict examples

- A sparse `apps/web/src/index.ts` proves an entry point exists; it does not
  prove browser behavior, framework choice, or who consumes a shared type.
- `.nvmrc` and CI agreeing on Node 22 can outweigh an outdated subsystem README;
  state only the globally supported Node 22 fact in root guidance. Preserve the
  stale subtree README conflict and its sources in that subtree's scoped rule;
  do not move a path-specific conflict into the root.
- An observed overwritten file supports a rule for that file or confirmed
  generated directory only. Verify and cite the generator input and command;
  otherwise mark them unknown instead of inventing them.

## Root budget

Keep root `CLAUDE.md` below 200 lines and preferably below 60 nonblank lines.
Route readers to scoped files rather than copying their contents. Remove
duplicates before adding a new layer.

## Layer map format

Before writing, show:

```text
PATH
Scope: <paths or repository-wide>
Evidence: <complete repository-relative sources or sanitized session receipt ID>
Action: create | minimally edit | preserve
Exact diff: <unified diff>
Conflicts/unknowns: <none or explicit list>
```

Approval applies only to this map and diff. Re-propose material changes.
