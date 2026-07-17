# Using `okf-second-brain`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Creates and incrementally grows a personal "second brain" as an
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
knowledge bundle: a plain directory of markdown files where every concept
document carries typed YAML frontmatter, an `index.md` per directory lists
what's inside, and an append-only `log.md` records every change by date.
On each ingest it distills the source into concept documents (not raw
copies), deduplicates against what the bundle already holds, cross-links
related concepts, updates the affected indexes and the log, and validates
the whole bundle for OKF conformance with a bundled script.

## When to invoke

- Starting a personal knowledge base: "set up a second brain", "create a
  knowledge base in OKF format".
- Adding to it: "save this to my second brain", "ingest this article/URL/
  file", "remember this decision", "add my notes from today's meeting".
- Health-checking an existing bundle: "validate my second brain".
- **Not** for architectural decisions that belong beside code — those go
  through the `architecture-decision-records` skill into the project's ADR
  log. A `Decision` concept in the second brain records the *user's*
  personal choice and rationale, not a project ADR.
- **Not** for harness run artifacts — during workflow runs, producers
  write only inside `runs/<run-id>/` per `CLAUDE.md`.

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it on second-brain, knowledge-base, and
save/ingest-this phrasing.

## How to invoke

### Step 1 — Initial baseline (one-time setup)

Create the bundle, optionally seeded from material you already have:

1. **Create the bundle.** Name a path, or accept the `./second-brain/`
   default:

   ```text
   /okf-second-brain create my second brain at ~/knowledge/second-brain
   ```

   Answer the one batched question round (bundle title, path
   confirmation, optional focus domains). You get a root `index.md` and a
   `log.md` — a valid, empty bundle.

2. **Seed it from an existing corpus** (optional but recommended). Point
   the skill at a folder of notes, exports, or documents — it enumerates
   readable files, tells you the count, and runs each through the full
   ingest pipeline (distill → dedup → file by type → cross-link → index →
   log), validating after every batch of ~10:

   ```text
   /okf-second-brain seed the baseline from ~/notes and ~/Downloads/exports
   ```

   Your source files are read-only — nothing is moved or modified. The
   run ends with a report: concepts created by type, files skipped, dedup
   merges, and a `Baseline complete` log entry.

3. **Check the result.** Skim the root `index.md` for the sections that
   appeared and `log.md` for what was created. The conformance validator
   has already passed (exit 0) or the skill isn't done.

### Step 2 — Continuous updates (ongoing routine)

Invoke the skill whenever new knowledge shows up; it finds the existing
bundle automatically (via the `okf_version` marker) so you don't repeat
the path:

- **A document or file**:
  `Save the key takeaways from meeting-notes/2026-07-17.md to my second brain.`
- **A URL**:
  `/okf-second-brain ingest https://simonwillison.net/2026/some-article/`
- **A conversational insight or decision**:
  `Remember this: we're standardizing on uv for Python tooling because ...`
- **A changed source you saved before**: just ingest it again — the
  `resource:` URI matches the existing concept, which is merged and
  refreshed with an **Update** log entry, never duplicated. This makes
  "re-run over everything new" safe.
- **Batch catch-up**: point it at a drop folder periodically
  (`ingest everything new in ~/inbox into my second brain`) — the dedup
  gate skips what's already captured, so only genuinely new material
  lands.
- **Health check**: `validate my second brain` runs the conformance
  validator and reports findings without changing anything.

Habits that keep the bundle current: ingest meeting notes the day they're
written, ingest articles as you finish reading them, and do a weekly
batch catch-up on your inbox/downloads folder. `log.md` shows exactly
what changed and when, so gaps are easy to spot.

### Requirements

- `python3` on PATH — the conformance validator
  (`scripts/validate_okf.py`, stdlib-only) runs after every operation.
- Web access (WebFetch) only when ingesting URLs.
- If no path is given, the skill auto-discovers an existing bundle (any
  `index.md` whose frontmatter declares `okf_version`) or defaults to
  `./second-brain/`. It never converts a non-empty, non-OKF directory
  without asking.

## What to expect

- **Init**: one batched question round (title, path, optional focus
  domains), then exactly two files — a root `index.md` declaring
  `okf_version: "0.1"` and a `log.md` opened with a **Creation** entry.
  Type directories (`notes/`, `references/`, `decisions/`, ...) appear
  lazily on first use.
- **Baseline seeding**: an existing corpus is enumerated (with a count
  shown before large runs), each readable file is ingested through the
  normal pipeline in validated batches of ~10, sources stay untouched,
  and the run ends with a by-type summary plus a `Baseline complete` log
  entry.
- **Ingest**: one concept document per source by default (split only when
  a source holds several independently linkable concepts), filed by its
  frontmatter `type`, cross-linked under `## Related` with
  bundle-absolute paths, cited under `## Citations`, indexed, and logged.
- **Idempotency**: re-ingesting the same document (matched by `resource:`
  URI first) updates the existing concept and logs an **Update** — it
  never creates a duplicate.
- **Your edits survive**: indexes are edited surgically (one bullet per
  touched file), never regenerated; `log.md` only ever grows.
- **Validation**: every operation ends with `validate_okf.py` exiting 0;
  dangling index links are warnings (the spec tolerates them), everything
  else is fixed before the skill finishes.
- **Harness compatibility**: the bundle is a valid vault for
  `harness/knowledge/second-brain/adapter.md` — set the run's
  `second_brain_path` to the bundle root and workflow producers can cite
  it as `[source: second-brain/<note-name>]`.
- Warning signs it is misapplied: raw source dumps instead of distilled
  concepts, duplicate documents for the same source, or index/log entries
  missing after an ingest.

## Worked example

You say: "Set up a second brain in ./second-brain and save this article on
prompt caching: `https://example.com/prompt-caching`." The skill asks for a
bundle title, scaffolds `second-brain/index.md` (with `okf_version: "0.1"`)
and `second-brain/log.md`, fetches the article, and writes
`second-brain/references/prompt-caching-guide.md` with `type: Reference`,
`resource:` set to the URL, a distilled body, and a citation. It creates
`references/index.md` with one bullet, adds a `References` bullet to the
root index, logs a **Creation** entry under today's date, and runs the
validator (exit 0). A week later you re-ingest the same URL after the
article was updated: the skill matches the `resource:` URI, merges the new
material into the existing document, refreshes its `timestamp`, and logs an
**Update** — no second file appears.
