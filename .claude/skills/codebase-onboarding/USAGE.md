# Using `codebase-onboarding`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Explores a target codebase with five parallel read-only subagents (stack and
commands; architecture and data flow; conventions; domain glossary and
config; git history and gotchas), then generates a persistent onboarding
package that makes the codebase approachable to a developer new to it:

- `docs/onboarding/` in the target repo — seven markdown docs: orientation
  tour, architecture with diagrams, getting started with tier-tagged
  commands, conventions, glossary, a first-change walkthrough, and gotchas.
- A draft `CLAUDE.md` at the target repo root — created when none exists;
  when one exists it is treated as user-authored and only changed via an
  explicitly approved diff.
- `onboarding.html` — a single self-contained file (inline CSS/JS, inline
  SVG diagrams, no network dependencies) that renders the whole guide from
  `file://`, suitable for sharing with someone who never opens the repo.

Every claim in the package cites a file path; inferences and unknowns are
labeled rather than papered over.

How it differs from its neighbors: `bootstrap-claude-context` installs the
layered Claude Code context *scaffold and learning loop* into a repo — it
generates no onboarding content. The `start-codebase` skill that bootstrap
installs produces an ephemeral session *briefing*, not persisted docs. This
skill produces the persistent, human-facing content; run bootstrap on top of
it if you also want the scaffold.

## When to invoke

- "Onboard me to this codebase" / "make this repo approachable".
- "Create onboarding docs for new developers" / "document this repo for a
  new hire".
- "What does a new engineer need to know to be productive here?" — when the
  answer should be persisted, not just chatted.
- **Not** for installing the Claude Code context scaffold or learning loop —
  that is `bootstrap-claude-context`.
- **Not** for delivery work (features, fixes, refactors, decisions) — that
  routes through `agentic-delivery-router`.
- **Not** inside a live harness run — during runs, producers write only
  inside `runs/<run-id>/` per `CLAUDE.md`; this skill writes to a target
  repo, standalone only.

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it on onboarding and make-this-approachable phrasing.

## How to invoke

Name the target repo — the skill asks rather than assumes:

```text
Onboard me to ~/code/my-service. Put the docs in docs/onboarding/.
```

or, with the defaults spelled out:

```text
Use the codebase-onboarding skill.
target_repo: /home/me/code/my-service
output_dir:  docs/onboarding/        (default)
audience:    junior developer        (default: experienced developer)
```

Requirements: the target repo must be readable; git history is optional (the
hotspot analysis degrades gracefully without it); a user should be available
to approve the CLAUDE.md diff when one already exists, and to approve any
command execution.

## What to expect

1. Input confirmation and a read-only preflight (existing `output_dir`
   content and any existing `CLAUDE.md` are surfaced before anything is
   written).
2. Five subagents launched in a single message; nothing is answered from
   memory.
3. Docs generated with every command tagged `documented`, `corroborated`
   (cited in CI or scripts), or — only if you approve execution —
   `executed`. The skill never installs dependencies or mutates state.
4. A stop for your approval if a `CLAUDE.md` already exists (declined or
   unattended, the proposal lands at `docs/onboarding/claude-md-draft.md`
   instead).
5. A final report listing every path written, the command-tier counts, the
   unknowns the team should answer, and a one-line pointer to
   `bootstrap-claude-context` as an optional follow-up.

## Worked example

"Onboard me to `~/code/billing-service`, audience: junior developer."

The skill confirms the target and defaults, finds `docs/onboarding/` absent
and a `CLAUDE.md` present, and says so. Five subagents fan out; Subagent A
returns `make test` as `corroborated` (cited from `.github/workflows/ci.yml`),
Subagent E flags `billing/ledger.py` as the churn hotspot. The seven docs are
written to `~/code/billing-service/docs/onboarding/`, with `first-change.md`
walking a realistic invoice-field addition through `billing/models.py` and
its named exemplar test. Because `CLAUDE.md` exists, the skill presents a
three-line diff (adding the corroborated test command and a pointer to the
onboarding docs) and stops; on approval it applies exactly that diff. It
renders `onboarding.html` with an inline-SVG architecture diagram, runs its
self-check, and reports nine written paths, two unknowns ("who owns the
payment-gateway sandbox credentials?"), and the optional bootstrap follow-up.
