# Using `bootstrap-claude-context`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Installs a layered, self-improving Claude context scaffold into a target
repository — root `CLAUDE.md`, a `.claude/context/` codebase map and
learnings directory, session start/end hooks, and the `start-codebase`,
`finish-session`, and `review-learnings` project skills — using the
deterministic installer at `scripts/install.py`. Every instruction it writes
is evidence-backed, and no existing guidance is ever replaced silently.

## When to invoke

- A repository has no Claude Code onboarding and needs project instructions.
- You want layered instructions: lean universal root guidance, scoped detail
  in the narrowest `.claude/rules/` file or nested `CLAUDE.md`.
- You want the self-improving loop — session hooks plus review-gated
  learning admission — installed and wired up.
- Existing guidance needs improving: the skill treats every existing
  instruction as user-authored and reconciles only via an approved diff.
- Note: asking to *inspect* or *assess* a repo's guidance is not approval to
  mutate it — the skill will preview and stop for explicit approval.

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it when a repository needs Claude Code onboarding,
layered project instructions, or the context scaffold.

## How to invoke

### In conversation

Explicit invocation:

```text
/bootstrap-claude-context Set up ~/projects/billing-service.
```

Natural-language requests that trigger it via the frontmatter description:

```text
This repo has no CLAUDE.md — onboard it for Claude Code.
```

```text
Install the self-improving context scaffold into the target repo.
```

### Requirements

Name the target repository explicitly — the skill will not guess. It needs
read/write access to that repo and `python3` to run the bundled installer
(`scripts/install.py`, with `--dry-run`, `--apply`, and `--validate` modes).
The scaffold's stable files live under `assets/project/`, and
`references/layering.md` and `references/learning-admission.md` are read as
part of the workflow to govern layer placement and what the learning loop
may admit.

## What to expect

- A full read of the target's existing `CLAUDE.md`, `AGENTS.md`,
  `.claude/rules/`, settings, CI, and docs first, with a supporting path
  recorded for every repository claim and inferences labeled as such.
- A dry-run preview: an exact map of every create/merge/preserve action and
  every project-specific instruction diff, each rule traced to its evidence
  and narrowest layer.
- A hard stop for your explicit approval of those exact writes; any plan
  change means a revised diff and a fresh ask.
- After `--apply`: existing files preserved, only approved evidence-cited
  content written, then a `--validate` pass, a final diff inspection for
  scope and secrets, and a reminder to restart Claude Code (hooks load at
  session startup).
- Warning signs it is misapplied: any "helpful" edit landing before
  approval, or a repository-specific rule without identifiable evidence
  (SKILL.md → Common mistakes and Acceptance checks).

## Worked example

You say: "Onboard ~/projects/billing-service for Claude Code." The skill
reads the repo's existing `CLAUDE.md` stub, CI config, and test layout,
then runs the installer with `--dry-run` and shows the plan: create the
codebase map, hooks, and three project skills; merge one settings fragment;
preserve the handwritten `CLAUDE.md` with a two-line proposed addition citing
`Makefile:test`. You approve exactly that. It applies, validates, reports
preserved files and one unverified claim, and tells you to restart Claude
Code so the session hooks load.
