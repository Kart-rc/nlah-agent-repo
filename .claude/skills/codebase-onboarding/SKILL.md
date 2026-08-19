---
name: codebase-onboarding
description: Explore a target codebase with parallel read-only subagents and generate a persistent onboarding package that makes it approachable to a developer new to it - a docs/onboarding/ guide set (tour, architecture, getting started, conventions, glossary, first change, gotchas), a draft CLAUDE.md at the repo root, and a single self-contained onboarding.html. Use for "onboard me to this codebase", "make this repo approachable", "create onboarding docs", "document this repo for new developers", "what does a new engineer need to know here". Do NOT use for installing the layered Claude Code context scaffold or learning loop - that is bootstrap-claude-context; not for an ephemeral session briefing; and not for delivery work (features, fixes, refactors), which goes to agentic-delivery-router.
---

# Codebase Onboarding

## Overview

This skill turns an unfamiliar repository into an onboarding package a new
developer can actually use: it explains a codebase to humans. It generates
persistent artifacts; it does not install machinery into the target repo —
that is `bootstrap-claude-context`'s job, and the two are deliberately
complementary (see Step 4).

```text
0. Confirm inputs: target repo, output dir, audience; preflight collisions
1. Fan out five read-only Explore subagents in a single message
2. Synthesize: reconcile findings, resolve conflicts, label unknowns
3. Generate the onboarding docs (templates in references/)
4. Draft CLAUDE.md - approval-gated when one already exists
5. Render onboarding.html from the docs (skeleton in assets/, zero network deps)
6. Self-check evidence, commands, and self-containment; report and hand off
```

Standing rules, in force for every step:

- **Every repository claim carries a file path.** Inferences and unknowns are
  labeled as such; a claim with no evidence path is an inference by
  definition.
- **Exploration is read-only.** No installs, no network mutations, no fixes,
  no formatting. Executing a non-mutating command (a version check, the test
  suite) is allowed only behind an explicit user approval in Step 3 — never
  by default.
- **Writes to the target repo happen with user awareness.** Like
  `bootstrap-claude-context` and `okf-second-brain`, this skill writes real
  files into a working tree; it lists every path it writes and never commits.
- **Never invoke this skill inside a live harness run.** During a run,
  producers write only inside `runs/<run-id>/` (see `CLAUDE.md`); this skill
  writes to a target repo, so it operates standalone only.

## Step 0: Inputs and preflight

Resolve the inputs before any exploration. `target_repo` is never assumed —
if the request does not name one and the working directory is this harness
repo, ask.

```text
ONBOARDING REQUEST
- target_repo:  <absolute path; REQUIRED - ask if unstated, never assume>
- output_dir:   <default: <target_repo>/docs/onboarding/>
- audience:     <default: experienced developer new to this codebase;
                 alternatives: junior developer, non-engineer stakeholder>
- exclusions:   <optional paths or topics to skip>
```

Preflight, all read-only:

1. `target_repo` exists and is readable. If it is not a git repository,
   degrade gracefully: Subagent E's history charter is skipped and
   `gotchas.md` says so.
2. If `output_dir` already exists with content, list what is there and ask
   before writing anything — existing onboarding docs are someone's work.
3. Record whether `<target_repo>/CLAUDE.md` exists. This decides Step 4's
   mode; check it now, not later.
4. Estimate repo scale (file count, top-level layout) to calibrate how
   tightly each subagent's charter must scope.

## Step 1: Parallel exploration

Never answer about the codebase from memory — everything the docs will claim
comes from this session's subagent returns. **Launch all five subagents in a
single message so they run concurrently.** Use a read-only search subagent
(`Explore`, or `general-purpose` if unavailable). These subagents are context
management for this skill; they are **not harness stages**: no artifacts, no
gates, no run state, no `HARNESS.md` §3 protocol.

Every charter ends with the same three instructions: cite a file path for
every claim; return `UNKNOWN: <question>` rather than guessing; cap your
return at the stated budget so five returns fit in the synthesizing context.

**Subagent A — stack, build, run, test.** Read manifests and lockfiles
(`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, ...), Makefile or
task-runner files, repo scripts, CI workflows, Dockerfiles, and any docs that
claim commands. Return: a language/framework/tooling table; the canonical
setup → build → test → run command sequence, each command tagged with a
verification tier — `documented` (claimed in docs only) or `corroborated`
(appears in CI or scripts; cite the path); required env vars and
prerequisites, each with an evidence path. The `executed` tier is reserved
for Step 3's approval-gated runs.

**Subagent B — architecture and data flow.** Find entry points, the
module/package map with a one-line responsibility each, the key abstractions
and their relationships, the request/data lifecycle for the one or two
dominant flows, and external services or storage touched. Return: a component
list with paths; a structured diagram description (nodes plus labeled edges,
renderable by the synthesizer); the top 5 files a newcomer should read first,
in order, with one line on why each.

**Subagent C — conventions and quality.** Read lint/format configs, the test
layout and patterns (name a representative test file), error-handling and
logging idioms, naming and structure conventions inferred from at least three
concrete examples each, contribution docs, and commit-message style from the
log. Return: a convention → evidence-paths table, plus "how code review here
will judge you" bullets.

**Subagent D — domain glossary and configuration.** Extract domain nouns and
verbs from type/class/table names and docs; core entities and where each is
defined; the configuration surface (env vars, config files, feature flags —
names only, never values); external integrations and the credentials they
expect (names only). Return: glossary rows (term → definition →
defining path) and a config table.

**Subagent E — history, hotspots, gotchas.** Analyze `git log`: most-changed
files and directories, activity centers of the last 90 days, files that
change together, oldest untouched load-bearing code; plus long-lived
TODO/FIXME/HACK clusters and anything the docs claim that disk contradicts.
Return: a hotspot table with churn counts, and candidate gotchas each tagged
`observed` (evidence path) or `inferred`.

## Step 2: Synthesis

Merge the five returns in the invoking context, applying these rules:

- **Conflict resolution:** disk beats docs; CI beats README; newer beats
  older. Every conflict that survives resolution becomes an entry in
  `gotchas.md` — never a silent choice.
- **Coverage check:** walk the artifact spec in Step 3 against the merged
  findings. A gap becomes an explicit "Unknown — verify with the team" entry
  in the relevant doc, never filler prose.
- **Audience calibration:** decide, from the declared audience, what to
  explain and what to assume. A junior-developer audience gets the "what a
  service is" sentence; an experienced one does not.

## Step 3: Generate the onboarding docs

Read [references/artifact-templates.md](references/artifact-templates.md)
fully before writing — it carries the exact heading skeleton and per-section
guidance for each file. Write all docs into `output_dir`:

| File | Content |
|---|---|
| `README.md` | Orientation: what the system does, doc index with reading order, a "your first 30 minutes" tour (Subagent B's top-5 file walk) |
| `architecture.md` | Component map with responsibilities, Mermaid diagram(s) of structure and the dominant data flow, key abstractions, external dependencies |
| `getting-started.md` | Prereqs, setup → build → test → run sequence with a verification tier and evidence path per command, troubleshooting of likely first failures |
| `conventions.md` | Code style, test patterns with a named exemplar test, error handling, PR/commit conventions — every rule with at least one evidence path |
| `glossary.md` | Domain term table (term, meaning, defined-at path); config/env-var table |
| `first-change.md` | A walkthrough of one realistic small change grounded in a real module: where it goes, which tests cover it, how to verify, what review will check |
| `gotchas.md` | FAQ and hotspots: churn table, surviving doc-vs-disk conflicts, footguns, "things that look wrong but are intentional" — each tagged observed/inferred |

Command verification tiers resolve here. You may **offer** to execute
non-mutating checks (version checks, the test suite) to upgrade commands
from `documented`/`corroborated` to `executed` — only with explicit user
approval, and never an install or any state mutation. Whatever happens,
`getting-started.md` prints each command's tier honestly.

## Step 4: Draft CLAUDE.md

The rules depend on what preflight found:

- **No existing CLAUDE.md:** write a lean one at `<target_repo>/CLAUDE.md`:
  what the project is (2–3 lines), the corroborated build/test/run commands,
  the 3–5 highest-value conventions, and a pointer to the onboarding docs for
  depth. Every line is evidence-cited at generation time; detail lives in the
  onboarding docs, not the root file — the same layering philosophy as
  `bootstrap-claude-context`'s `references/layering.md` (reference it, don't
  restate it).
- **Existing CLAUDE.md:** treat it as user-authored — never rewrite silently.
  Present the exact proposed additions as a diff in conversation and **stop
  for explicit approval**: a request to onboard is not approval to mutate
  guidance. If declined, or if no user is available to approve, write the
  draft to `output_dir/claude-md-draft.md` instead and say so in the report.

The boundary with `bootstrap-claude-context`, stated plainly: this skill
writes onboarding *content*; bootstrap installs the layered *scaffold and
learning loop*. The CLAUDE.md generated here is deliberately compatible —
bootstrap's installer preserves existing files. The Step 6 report recommends
`bootstrap-claude-context` as an optional follow-up, in one line.

## Step 5: Render onboarding.html

Copy [assets/onboarding-template.html](assets/onboarding-template.html) and
fill it by hand — you are the renderer; there is no pandoc, npm, or build
step. Convert each onboarding doc into a `<section>`, then fill `{{TITLE}}`,
`{{GENERATED_DATE}}`, `{{NAV}}`, and `{{SECTIONS}}`. Write the result to
`output_dir/onboarding.html`.

Hard rules:

- **Zero external resources.** No `<script src>`, no `<link href>`, no remote
  images, no webfonts — system font stack only. Outbound anchor links (`<a
  href>` to external sites) are allowed; they degrade gracefully offline.
- The file must render from `file://` with no server.
- Diagrams: the markdown keeps its Mermaid fences (GitHub renders them
  natively); the HTML embeds the same diagrams as hand-authored inline SVG,
  with an ASCII `<pre>` fallback for any diagram too complex to draw well —
  never a Mermaid CDN.

## Step 6: Self-check and handoff

Before reporting, verify:

```text
SELF-CHECK
- [ ] Every doc has its template's required sections
- [ ] Spot-checked >= 3 claims per doc against real paths on disk
- [ ] Every command in getting-started.md carries a tier tag
- [ ] grep -E '(src|href)="http' onboarding.html matches only <a href> links
- [ ] CLAUDE.md gate honored (new file, approved diff, or draft written)
- [ ] Every unknown is an explicit entry, not filler prose
```

Then report:

```text
ONBOARDING PACKAGE
- Artifacts written:      <every path, including CLAUDE.md or the draft>
- Commands:               <executed / corroborated / documented counts>
- Unknowns for the team:  <the questions the docs could not answer>
- Optional follow-up:     bootstrap-claude-context installs the layered
                          Claude Code context scaffold on top of this.
```

## Anti-patterns

Avoid: answering about the codebase from memory instead of this session's
subagent returns; sequential subagent launches when one message suffices;
overwriting an existing CLAUDE.md or existing onboarding docs without an
approved exact diff; padding docs with generic engineering advice not
grounded in this repository; presenting a documented command as verified;
guessing where the synthesis has a gap instead of writing an explicit
unknown; external scripts, stylesheets, fonts, or images in onboarding.html;
installing dependencies, running mutating commands, or fixing bugs
mid-exploration; duplicating bootstrap-claude-context's scaffold or restating
its layering rules; invoking this skill inside a live harness run;
hardcoding any inventory of the target repo in this file.

## Final checklist

- [ ] Inputs confirmed; target_repo asked for, never assumed
- [ ] Preflight ran: output_dir collisions surfaced, CLAUDE.md presence recorded
- [ ] Five subagents launched in a single message, all read-only
- [ ] Conflicts resolved disk-beats-docs and surfaced in gotchas.md
- [ ] All seven docs match references/artifact-templates.md
- [ ] Commands tier-tagged; executed only behind explicit approval
- [ ] CLAUDE.md gate honored
- [ ] onboarding.html self-contained and file://-renderable
- [ ] Report emitted with every written path and every unknown named
