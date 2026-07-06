---
id: enterprise-mcp
summary: "Organizational knowledge via the enterprise's MCP servers: systems, policies, prior initiatives, people, budgets."
kind: mcp
capabilities: [org-context, prior-art]
tools_required:
  - "mcp__*"
failure_mode: degrade
---

# Enterprise MCP Adapter

## What this source knows

Whatever the organization has exposed through its MCP servers — typically:
internal documentation and wikis, project/ticket trackers, prior proposals and
ADRs, org structure, budget and procurement constraints, approved technology
lists. This adapter is deliberately generic: it describes HOW a stage consumes
enterprise MCP knowledge, and the session's connected MCP servers determine
WHAT is actually reachable.

## How to query

1. Discover: use ToolSearch (or the tool listing) to find connected MCP tools
   matching the question domain (search/docs/tickets/people). Do not assume a
   specific server name.
2. Query narrowly: one focused question per call (e.g. "prior proposals about
   API rate limiting"), preferring search-style tools before fetch-style tools.
3. Extract only what answers the stage's question; never paste large dumps
   into artifacts — summarize and cite.

## When to consult

- `org-context` slot: before finalizing requirements, designs, or proposals —
  constraints, precedents, and conventions the requester assumes you know.
- `prior-art` slot: before comparing options — has the org already tried,
  bought, or rejected one of them?

## Citation rule

Every claim sourced here is marked inline as
`[source: enterprise-mcp/<tool-or-doc>]` so validators can audit the trail.

## On failure

`failure_mode: degrade` — if no matching MCP tools are connected, a query
errors, or results are empty: proceed with the stage, and record each
unanswered question under the artifact's `## Knowledge gaps` section (failure
class F6). Do not guess at organizational facts; a visible gap beats a
fabricated one. If the manifest attached this adapter with `required: true`,
report the failure in your summary so the orchestrator escalates instead.
