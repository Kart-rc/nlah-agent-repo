---
name: okf-second-brain
description: Create and incrementally grow a personal "second brain" knowledge base as an Open Knowledge Format (OKF) v0.1 bundle. Use when the user wants to start a second brain or knowledge base, save or ingest a document, note, URL, or insight into their notes, port or link another existing OKF bundle, or maintain an OKF knowledge bundle.
metadata:
  spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md (OKF v0.1)
---

# OKF Second Brain

## What this skill maintains

A second brain: the user's personal knowledge base of distilled concepts —
notes, references, decisions, playbooks, people, projects — stored as an
**OKF v0.1 bundle**. A bundle is a plain directory tree of markdown files:
every concept document carries YAML frontmatter with a required `type`
field, and two reserved files structure the bundle — `index.md` (directory
listing) and `log.md` (chronological change history). No database, no
registry; everything is greppable text. The full grammar is condensed in
"OKF quick reference" below — never fetch the spec at runtime.

This skill has four operations:

- **Init** — scaffold a new, empty, conformant bundle.
- **Baseline** — seed a fresh bundle from an existing corpus (a folder of
  notes, exports, or documents) by running every file through the ingest
  pipeline.
- **Ingest** — incrementally add knowledge: distill a document, URL, or
  pasted text into concept documents, deduplicate against what already
  exists, cross-link, and update the indexes and log.
- **Port** — merge another already-existing OKF second brain (at any
  other location) into this bundle, preserving its typed concepts; or
  merely *link* it as an external bundle to consult without copying.

## Mode detection and target path

Resolve the bundle root before doing anything, in this order:

1. **Explicit path** — if the user names a directory, use it.
2. **Auto-discovery** — Glob for `**/index.md` under the working directory
   (skip `node_modules`, `.git`, and this repo's `runs/`). A file whose
   frontmatter contains `okf_version` marks a bundle root. Exactly one
   found → use it. Several found → ask the user which one.
3. **Default** — `./second-brain/`.

Then pick the mode from what is at that path:

- Root `index.md` with `okf_version` frontmatter → **update mode** (ingest).
- Path absent or empty directory → **init mode**.
- Path exists with content but no OKF marker → **stop and ask**. Never
  silently convert a non-OKF directory into a bundle.

The bundle root's `okf_version` marker is the only state this skill relies
on — no sidecar config files. If the user wants the location remembered,
offer to note it in the project's `CLAUDE.md`; never write there unprompted.

## Init: creating a bundle

Ask one batched round of questions (skip any already answered):

1. Bundle title (e.g. "Priya's Second Brain").
2. Confirm the target path.
3. Optional: focus domains (used as suggested `tags` vocabulary, **not** as
   directory structure).

Then scaffold exactly two files. Root `index.md`:

```markdown
---
okf_version: "0.1"
---

# <Bundle Title>

Personal knowledge base in OKF format. Sections appear as content is added.
```

And `log.md`:

```markdown
# Log

## <today, YYYY-MM-DD>

* **Creation**: Initialized second brain bundle.
```

Create no other files or directories — type directories appear lazily on
first ingest, so every index entry always points at a real file. Finish
with the conformance check.

## Baseline: seeding from an existing corpus

When the user points at existing material (a notes folder, doc exports, a
list of files or URLs) to establish the initial baseline:

1. **Init first** if no bundle exists at the target path (bundle root and
   source corpus must be different directories — never init inside the
   corpus).
2. **Enumerate the corpus**: Glob for readable text formats (`.md`,
   `.txt`, and similar); list anything skipped (binaries, unreadable
   formats) so the user knows the baseline's coverage. Show the user the
   file count and ask before proceeding if it is large (>25 files).
3. **Ingest each file through the normal pipeline below** — distill,
   dedup, place, cross-link, index, log. The dedup gate matters even
   here: corpora often contain near-duplicates, and the `resource:` URI
   (the source file's path) makes each baseline doc re-ingestable later.
4. **Work in batches** of roughly 10 files: after each batch, run the
   conformance check, then continue. Cross-linking improves as the bundle
   grows, so revisit obvious missed links in a final pass.
5. **Log** one bullet per document under today's date heading, then close
   the baseline with a summary bullet, e.g.
   `* **Update**: Baseline complete — seeded 34 concepts from ~/notes (3 files skipped: binary).`
6. Finish with the conformance check and report: concepts created by
   type, files skipped, and any dedup merges.

The source corpus is read-only throughout — the skill never modifies or
moves the user's original files.

## Port: merging or linking other second brains

When the user points at another OKF bundle — a second brain already
created elsewhere — first verify it *is* one: its root `index.md` must
carry the `okf_version` frontmatter marker. If the marker is absent, the
directory is not an OKF bundle; offer to treat it as a **Baseline** corpus
instead (which re-distills) rather than porting blindly.

Then ask which of the two modes the user wants:

### Port (copy and merge)

Source concepts are already distilled and typed, so porting preserves
them instead of re-distilling:

1. **Enumerate** the source's non-reserved `.md` files. Its `index.md`
   and `log.md` files are *not* copied — indexes are rebuilt here
   surgically, and the source's history stays with the source.
2. **Per document, run the dedup gate** against this bundle (resource
   URI → slug → semantic). A genuine match merges into the existing
   concept (logged as **Update**); otherwise the document is copied
   verbatim — frontmatter (`type`, `title`, `tags`, `timestamp`,
   `resource`) intact — with one addition: a custom
   `ported_from: <source-bundle-root>/<relative-path>` key recording
   provenance. Keep the original `timestamp`; porting is relocation, not
   modification.
3. **Place by type**: file each document into this bundle's type
   directory for its `type`. Source types not yet used here are new
   producer-defined types — confirm them with the user once, then apply
   consistently. On slug collision with a *different* concept, qualify
   the incoming slug (e.g. `-ported`), never overwrite.
4. **Rewrite cross-links after all documents are placed**: source
   bundle-absolute links (`/foo/bar.md`) point into the *source* root.
   Build an old-path → new-path map from step 3 and rewrite each ported
   document's links to the targets' new locations. Links to source
   documents that were *merged* during dedup point at the merge target.
   Unresolvable links may remain (the spec tolerates broken links) —
   list them in the port report.
5. **Index and log**: one surgical index bullet per ported document; one
   log bullet per document under today's date, closed by a summary, e.g.
   `* **Update**: Ported 28 concepts from ~/old-brain (4 merged into existing concepts, 2 unresolved links).`
6. Work in validated batches of ~10 (as for Baseline). The source bundle
   is read-only throughout — porting never mutates or deletes it; the
   user decides separately whether to retire it.

### Link (refer without copying)

When the user wants to *refer* to another bundle but keep it where it is
(e.g. a shared team brain), register it instead of copying:

- Add a bullet under a `# Linked Bundles` section in this bundle's root
  `index.md`:
  `* [Team Platform Brain](../team-brain/) - shared platform knowledge; consult before creating platform concepts`
  (a path outside the bundle is acceptable — consumers tolerate links
  they cannot resolve).
- From then on, during ingest, extend the **semantic dedup check and
  cross-link grep** across linked bundle roots too: if a concept already
  lives in a linked bundle, prefer linking to it from the new document's
  `## Related` section over duplicating it locally.
- Linked bundles are never written to — they have their own owners,
  indexes, and logs.

## Ingest: adding knowledge

### Acquire the source

- File path → Read it.
- URL → WebFetch it.
- Pasted text or conversational insight → use as given.

Always capture provenance: set `resource:` to the canonical URI (absolute
file path or URL; omit for pure conversation) and add a numbered
`## Citations` section at the document bottom.

### Distill into concept documents

Pick a `type` from the bundle's existing taxonomy. Starter taxonomy:

| Type | Directory | One-line definition |
|---|---|---|
| `Note` | `notes/` | A free-form thought, insight, or observation |
| `Reference` | `references/` | Distilled knowledge from an external source (article, doc, video) |
| `Decision` | `decisions/` | A choice the user made, with rationale |
| `Playbook` | `playbooks/` | A repeatable procedure or how-to |
| `Person` | `people/` | Context about an individual |
| `Project` | `projects/` | An initiative and its state |
| `Meeting` | `meetings/` | What happened in a specific meeting |
| `Source` | `sources/` | Provenance record for a large ingested document |

Before inventing a new type, grep the bundle for types already in use
(`grep -rh "^type:" <bundle>`) and reuse one if it fits. A new
producer-defined type requires user confirmation, then gets its own lazy
directory and must be reused consistently.

**Split policy**: one concept document per ingest by default. Split only
when the source contains two or more *independently linkable* concepts —
e.g. a meeting that produced two decisions becomes one `Meeting` doc plus
two `Decision` docs, cross-linked. When splitting a long external source,
also create one `Source` doc holding the provenance, which the concept
docs cite.

Concept document template:

```markdown
---
type: Reference
title: <Human-readable display name>
description: <One sentence, one line>
resource: <canonical URI of the underlying asset>
tags: [<tag>, <tag>]
timestamp: <now, ISO 8601, e.g. 2026-07-17T14:30:00Z>
---

# <Title>

<Distilled content — the insight, not a raw copy. Conventional headings
like Schema and Examples where they fit the type.>

## Related

* [<Existing concept>](/<dir>/<slug>.md) - <why it relates>

## Citations

1. [<Source name>](<url-or-bundle-absolute-path>)
```

Distill, don't mirror: capture what the user will want back later, in their
context, at a fraction of the source's length. Quote the minimum needed.

### Deduplicate before creating

Run all three checks, in order, before writing any new file:

1. **Resource match** — grep frontmatter for the same `resource:` URI.
2. **Slug collision** — does the derived filename already exist?
3. **Semantic match** — Grep the new doc's title keywords and tags across
   existing titles and headings.

Any hit that is genuinely the same concept → **update** the existing
document: merge the new content in, refresh `timestamp`, append any new
citation, and log `* **Update**: ...`. No hit → **create** and log
`* **Creation**: ...`. This is the idempotency gate: re-ingesting the same
document must update, never duplicate. The resource check runs first
because a URI is stable even when titles drift.

### Name and place the document

- Filename: kebab-case ASCII slug of the title, ≤60 chars.
- Never `index.md` or `log.md` — these are reserved.
- Slug collision with a genuinely *different* concept → append a short
  qualifier (year or domain word, e.g. `retro-2026.md`), never overwrite.
- Place in the type's directory (table above), creating it on first use.

### Cross-link

Grep the bundle for the new document's key terms, people, and project
names. Link related concepts under `## Related` using bundle-absolute
paths (`/decisions/foo.md` — the spec-recommended form). Add a reciprocal
backlink into an existing document only when it materially improves that
document, and log a separate `**Update**` entry for each document touched.
Links must mean something — the surrounding prose says why.

### Update indexes and the log

Indexes are **surgically edited, never regenerated** — the bundle is the
user's artifact and hand-curation must survive every ingest.

- In the type directory's `index.md` (create it with the directory; no
  frontmatter), insert or replace the single bullet for the touched file,
  alphabetically:

  ```markdown
  # References

  * [Prompt Caching Guide](/references/prompt-caching-guide.md) - How and when Anthropic prompt caching pays off
  ```

- Touch the root `index.md` only when a directory first appears — add one
  bullet: `* [References](references/) - distilled external sources`.
- Append to `log.md` under today's `## YYYY-MM-DD` heading (create the
  heading at the top of the entries, newest first, if absent). One bullet
  per document created or updated:

  ```markdown
  ## 2026-07-17

  * **Creation**: Added [Prompt Caching Guide](/references/prompt-caching-guide.md).
  * **Update**: Linked [Latency Playbook](/playbooks/latency.md) to the new reference.
  ```

  `log.md` is append-only: never rewrite or delete history.

## Conformance check

After **every** init or ingest, run the validator:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/validate_okf.py" <bundle-path>
```

It fails (exit 1) on: unparseable or missing frontmatter, empty/missing
`type`, frontmatter on a non-root `index.md`, root frontmatter with keys
other than `okf_version`, malformed index bullets, and invalid `log.md`
date headings. It warns (exit 0) on index entries pointing at missing
files, since the spec tolerates broken links — fix warnings you caused,
report pre-existing ones. Fix all failures before finishing.

Then verify the semantic layer the script cannot:

- [ ] The dedup gate actually ran (all three checks) before any create.
- [ ] `description` is a single sentence on a single line.
- [ ] Every `## Related` link is explained by its trailing prose.
- [ ] Every claim taken from a source is covered by a citation.
- [ ] One log bullet exists per document created or updated.

## Idempotency guarantees

State these as promises and keep them:

- Re-ingesting the same document **updates** the existing concept; it
  never creates a duplicate.
- Index edits are surgical; the user's hand-edits, custom sections, and
  ordering survive.
- `log.md` only ever grows.
- The skill never writes outside the bundle root (except an explicitly
  requested `CLAUDE.md` note).

## OKF quick reference

Condensed from OKF v0.1 — authoritative for this skill; do not fetch the
spec at runtime.

- **Bundle** = directory tree of markdown files; hierarchy is
  producer-defined. Reserved filenames: `index.md`, `log.md` only.
- **Concept frontmatter**: `type` (REQUIRED, short string), `title`
  (recommended), `description` (recommended, one line), `resource`
  (recommended canonical URI), `tags` (optional list), `timestamp`
  (optional ISO 8601), plus producer-defined keys.
- **index.md**: `# Section Heading` then `* [Title](relative-url) - short
  description` bullets; subdirectory entries like `* [Subdir](subdir/) -
  description`. No frontmatter — except the bundle-root `index.md`, which
  may carry a frontmatter block containing only `okf_version: "0.1"`.
- **log.md**: `## YYYY-MM-DD` headings (ISO 8601 date), bullets beginning
  `* **Creation**:` or `* **Update**:` with prose and links.
- **Links**: bundle-absolute starting with `/` (recommended) or relative.
  Broken links are tolerated by consumers.
- **Citations**: numbered list under a `Citations` heading at the bottom.
- **Conformance**: every non-reserved `.md` parses with a non-empty
  `type`; reserved files follow their structure; consumers tolerate
  missing optional fields, unknown types, broken links.

## Harness integration

An OKF bundle is directly consumable by this repo's
`harness/knowledge/second-brain/adapter.md`: point the run's
`second_brain_path` (in `inputs.json` or the manifest attachment's
`with.path`) at the bundle root and producers grep it like any vault. No
changes under `harness/` are needed to use this skill.
