---
id: second-brain
summary: "The requester's personal knowledge base (notes, decisions, preferences) - filesystem or MCP-backed."
kind: filesystem
capabilities: [personal-notes, prior-art]
tools_required: []
failure_mode: degrade
---

# Second Brain Adapter

## What this source knows

The requester's accumulated personal knowledge: meeting notes, decision logs,
reading highlights, preferences, half-formed plans. Typically an Obsidian/
Logseq-style vault of markdown files, or a notes app exposed via MCP. It knows
*why the requester thinks what they think* — context no enterprise system has.

## How to query

1. Locate the vault: the run's `inputs.json` may carry a `second_brain_path`;
   otherwise check the manifest attachment's `with.path` parameter; otherwise
   look for an MCP notes tool (via ToolSearch). If none of these exist, treat
   as failure (see On failure).
2. Search by topic keywords with Grep/Glob across the vault (or the MCP
   search tool): the request's nouns, project names, people.
3. Read only matching notes; extract decisions, preferences, and constraints
   relevant to the stage's question. Respect the personal nature of the
   source: quote the minimum needed, never copy private content into
   artifacts beyond what the question requires.

## When to consult

- `personal-notes` slot: at intake and research time — what has the requester
  already decided, tried, or ruled out?
- `prior-art` slot: the requester's notes on similar past efforts.

## Citation rule

Claims sourced here are marked inline as `[source: second-brain/<note-name>]`.

## On failure

`failure_mode: degrade` — if no vault path or notes tool is available, or a
search returns nothing: proceed, and record what you would have looked up
under the artifact's `## Knowledge gaps` (failure class F6). Never infer the
requester's private opinions without a note to cite.
