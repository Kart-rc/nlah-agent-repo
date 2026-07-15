---
name: architecture-decision-records
description: Drive and capture architectural decisions as structured ADRs. Calibrates every decision against enterprise context — discovered from connected MCP servers and supplied by the user — so the recorded decision fits the actual organization, project, and scope. Use when a significant technical choice is being made, compared, questioned, or needs recording.
metadata:
  origin: ECC (refined for the NLAH harness)
---

# Architecture Decision Records

This skill has two jobs, in order:

1. **Drive the decision to clarity.** Surface the decision drivers, the real
   alternatives, and — critically — the enterprise context that makes one
   option fit and another a liability, *before* anything is committed.
2. **Capture it as an ADR** that lives alongside the code, so future
   developers and agents understand why the codebase is shaped the way it is.

An ADR drafted from general knowledge alone is a textbook answer: correct in
the abstract, wrong for the org. "Use PostgreSQL" is a different decision in
a company with a managed Postgres platform team than in one standardized on
DynamoDB with no relational operations experience. **Context calibration
(Phase 0) is therefore never skipped**, only right-sized to the decision.

## When to Activate

- User explicitly says "record this decision", "ADR this", or "help me decide
  between X and Y"
- User chooses between significant alternatives (framework, library, pattern,
  database, API design) or says "we decided to..." / "the reason we're doing
  X instead of Y is..."
- User asks "why did we choose X?" (read existing ADRs — see Reading below)
- A `tech-decision` workflow run completes and its decision record should
  enter the project's ADR log (see Harness integration)
- During planning phases when architectural trade-offs are discussed
  (suggest recording — do not auto-create without user confirmation)

## Phase 0 — Calibrate enterprise context

Run this before drafting anything. Scale the effort to the decision: a
two-way-door library choice needs one or two checks; a one-way-door platform
choice needs the full sweep.

### 0a. Discover what the enterprise already has (MCP)

Follow the discipline defined in `harness/knowledge/enterprise-mcp/adapter.md`
(it is the authoritative contract for consuming enterprise MCP knowledge):

1. **Discover**: use ToolSearch (or the tool listing) to find connected MCP
   tools matching the question domain — internal docs/wiki search, ticket
   trackers, code search, architecture repositories, service catalogs. Never
   assume a specific server name; work with what this session actually has.
2. **Query narrowly** — one focused question per call, search-style tools
   before fetch-style tools. For an architectural decision, sweep in this
   order of value:
   - **Prior art**: existing ADRs or decision records on this question or a
     neighboring one — does this decision affirm, supersede, or contradict one?
   - **Standards**: approved-technology list, tech radar, golden paths,
     mandated stacks for this domain
   - **Platform inventory**: services the org already runs or pays for that
     solve part of the problem (auth, messaging, data stores, CI/CD,
     observability)
   - **Policy**: security, compliance, and procurement policies that bind
     this decision
   - **In-flight work**: initiatives or teams already working on or near
     this problem
3. **Cite everything**: every organizational claim in the ADR is marked
   inline as `[source: enterprise-mcp/<tool-or-doc>]` so it can be audited.
4. **Degrade honestly**: if no matching MCP tools are connected, a query
   errors, or results are empty — proceed, and record each unanswered
   question under the ADR's `## Knowledge gaps` section. Never guess at
   organizational facts; a visible gap beats a fabricated one.

### 0b. Ask the user for local context

MCP discovery shows what is *available*; the user knows what *applies* to
this project and scope. Ask only what discovery did not already answer, in
one batched round (use AskUserQuestion where available), smallest set
possible:

| Dimension | What to ask |
|---|---|
| **Scope & lifetime** | Prototype, internal tool, or product? Expected lifetime and scale? |
| **Standards** | Is there a tech radar, approved list, or golden path this must follow — or deviate from with justification? |
| **Platform** | Which existing platform services (auth, data stores, queues, CI/CD, hosting) are already procured and expected to be used? |
| **Compliance** | Which regimes bind this system (SOC 2, HIPAA, GDPR, PCI, data-residency, internal security tiers)? |
| **Team** | What are the skills of the team that will own this? Who maintains it in two years? |
| **Money & procurement** | Budget ceilings, licensing constraints, vendor-approval requirements? |
| **Authority & deadline** | Who has decision authority, who must be consulted, and by when must the call be made? |

Record the answers in the ADR's `## Enterprise context` section, attributed
`[source: user]`. If neither MCP nor the user can answer a dimension that
materially affects the decision, it goes in `## Knowledge gaps` as a stated
risk — the ADR is explicit about what it was decided *without* knowing.

## Phase 1 — Drive the decision

1. **Frame it**: state the decision in one sentence, then list 3–6 decision
   drivers — the measurable or observable forces that should determine the
   winner (latency budget, team skill, compliance regime, cost ceiling,
   time-to-market). Drivers come before options, so options can't be
   reverse-engineered to crown a favorite.
2. **Enumerate real alternatives**: include do-nothing and buy-vs-build where
   relevant. Judge each against the drivers *and* against the enterprise
   context from Phase 0 — an option that fights the org's standards,
   platform, or skills carries that cost explicitly.
3. **Classify the door**: one-way (hard to reverse) or two-way (cheap to
   reverse), and state confidence. Deciding a two-way door at partial
   information is fine and the ADR says so; a one-way door at low confidence
   means the recorded decision may be "buy specific information first, owner
   and date named".
4. **Escalate when the decision outgrows a conversation.** If the decision is
   contested across teams, High/Critical risk (per the router's rubric), or a
   one-way door with material blast radius — do not settle it in chat. Route
   it through the `agentic-delivery-router` skill, which will select the
   `tech-decision` workflow: framing, evidence, an adversarially-validated
   option matrix, and an independently gated decision record. This skill then
   captures the result (Phase 2). This skill never orchestrates workflows
   itself.
5. Otherwise, state a recommendation with rationale traced to the drivers and
   the cited context, and move to capture.

## Phase 2 — Capture the ADR

1. **Locate the log**: detect an existing ADR directory first —
   `docs/adr/`, `docs/decisions/`, or `adr/` — and follow the incumbent
   convention (directory, numbering, template). Never introduce a second
   convention into a repo that already has one.
2. **Initialize (first time only)**: if no ADR directory exists, ask the user
   for confirmation before creating `docs/adr/` with a `README.md` seeded
   with the index table header (see ADR Index Format) and a `template.md`
   for manual use. Do not create files without explicit consent.
3. **Assign a number**: scan existing ADRs and increment.
4. **Draft** using the format below, with context, alternatives, and
   consequences filled from Phases 0–1 — sources cited, gaps declared.
5. **Confirm and write**: present the draft to the user for review. Only
   write `docs/adr/NNNN-decision-title.md` after explicit approval. If the
   user declines, discard the draft without writing any files.
6. **Update the index**: append the row to `docs/adr/README.md`.

## ADR Format

Lightweight Nygard-style ADR, extended with the sections that make a decision
auditable and fit-for-context:

```markdown
# ADR-NNNN: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: proposed | accepted | deprecated | superseded by ADR-NNNN
**Deciders**: [who was involved]
**Door**: one-way | two-way · **Confidence**: high | medium | low

## Context

What problem or force is motivating this decision? [2–5 sentences: the
situation, constraints, and what happens if no decision is made.]

## Decision drivers

- [driver 1 — measurable or observable]
- [driver 2]
- [driver 3]

## Enterprise context

What in this organization shapes the decision. Every line cited.

- [prior ADR / standard / platform service / policy] [source: enterprise-mcp/<tool-or-doc>]
- [scope, team, budget, compliance facts supplied by the requester] [source: user]

## Decision

[1–3 sentences stating the decision clearly, naming the chosen option.]

## Alternatives considered

### Alternative 1: [Name]
- **Pros**: [benefits]
- **Cons**: [drawbacks]
- **Enterprise fit**: [how it lands against the standards, platform, and skills above]
- **Why not**: [the specific reason this was rejected]

### Alternative 2: [Name]
- **Pros**: / **Cons**: / **Enterprise fit**: / **Why not**:

## Consequences

### Positive
- [what becomes easier]

### Negative
- [the trade-offs accepted]

### Risks
- [risk and mitigation]

## Revisit triggers

- [the observable metric threshold or dated event that reopens this
  decision — nothing else reopens it]

## Knowledge gaps

- [organizational questions that could not be answered from MCP sources or
  the user, and what risk deciding without them carries]
```

Omit `## Enterprise context` or `## Knowledge gaps` only when genuinely
empty — and an empty Enterprise context section on a non-trivial decision is
itself a signal that Phase 0 was skipped.

## Reading Existing ADRs

When a user asks "why did we choose X?":

1. Check if an ADR directory exists — if not, respond: "No ADRs found in
   this project. Would you like to start recording architectural decisions?"
2. If it exists, scan the `README.md` index for relevant entries; also check
   enterprise MCP sources for org-level decision records the repo doesn't
   hold.
3. Read matching ADR files and present the Context and Decision sections.
4. If no match is found, respond: "No ADR found for that decision. Would you
   like to record one now?"

### ADR Directory Structure

```
docs/
└── adr/
    ├── README.md              ← index of all ADRs
    ├── 0001-use-nextjs.md
    ├── 0002-postgres-over-mongo.md
    └── template.md            ← blank template for manual use
```

### ADR Index Format

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-use-nextjs.md) | Use Next.js as frontend framework | accepted | 2026-01-15 |
| [0002](0002-postgres-over-mongo.md) | PostgreSQL over MongoDB for primary datastore | accepted | 2026-01-20 |
```

## Decision Detection Signals

**Explicit** — act on these:
- "Let's go with X" / "We should use X instead of Y"
- "The trade-off is worth it because..."
- "Record this as an ADR"

**Implicit** — suggest recording; never auto-create without confirmation:
- Comparing frameworks/libraries and reaching a conclusion
- A schema or data-model choice with stated rationale
- Choosing between architectural patterns (monolith vs microservices,
  REST vs GraphQL), auth strategy, or deployment infrastructure

## What Makes a Good ADR

### Do
- **Be specific** — "Use Prisma ORM", not "use an ORM"
- **Record the why** — the rationale matters more than the what
- **Include rejected alternatives** — with their enterprise-fit assessment
- **Cite organizational facts** — `[source: enterprise-mcp/…]` or
  `[source: user]`; an uncited org claim is an assumption and belongs in
  Knowledge gaps
- **State consequences honestly** — every decision has trade-offs
- **Make revisit triggers observable** — a threshold someone can watch fire
- **Keep it short** — readable in 2 minutes; **use present tense**

### Don't
- Record trivial decisions — naming or formatting choices don't need ADRs
- Write essays — if Context exceeds 10 lines, it's too long
- Omit alternatives — "we just picked it" is not a rationale
- Launder assumptions as enterprise facts — cite it or gap it
- Backfill without marking it — note the original decision date
- Let ADRs go stale — superseded decisions link their replacement

## ADR Lifecycle

```
proposed → accepted → [deprecated | superseded by ADR-NNNN]
```

- **proposed**: under discussion, not yet committed
- **accepted**: in effect and being followed
- **deprecated**: no longer relevant (e.g., feature removed)
- **superseded**: replaced — always link the replacement; never delete the
  old record, it is historical context

## Categories of Decisions Worth Recording

| Category | Examples |
|----------|---------|
| **Technology choices** | Framework, language, database, cloud provider |
| **Architecture patterns** | Monolith vs microservices, event-driven, CQRS |
| **API design** | REST vs GraphQL, versioning strategy, auth mechanism |
| **Data modeling** | Schema design, normalization, caching strategy |
| **Infrastructure** | Deployment model, CI/CD pipeline, monitoring stack |
| **Security** | Auth strategy, encryption approach, secret management |
| **Testing** | Test framework, coverage targets, E2E vs integration balance |
| **Process** | Branching strategy, review process, release cadence |

## Harness integration

This skill is the interactive, user-facing side of decision capture in this
repository. It composes with the harness; it never replaces it.

- **`tech-decision` workflow**: for escalated decisions (Phase 1 step 4), the
  workflow's `decide` stage produces a gated `decision.md` (the call,
  rationale, steelmanned dissent, reversibility, revisit triggers). When such
  a run completes, offer to transcribe that record into the project's ADR log
  as a new numbered ADR — status `accepted`, linking the `runs/<run-id>/`
  artifacts as evidence. The workflow's record is authoritative; the ADR is
  its durable, discoverable index entry beside the code.
- **`harness/knowledge/enterprise-mcp/adapter.md`**: the contract this
  skill's Phase 0a follows — do not restate or diverge from its query,
  citation, and failure discipline.
- **`harness/skillpacks/addyosmani/documentation-and-adrs`**: the practice
  discipline producers read inside workflow runs. Keep ADR formats
  compatible; when working in a repo that already follows that skillpack's
  `docs/decisions/` convention, follow it (Phase 2 step 1).
- **Code review**: flag PRs that introduce architectural changes without a
  corresponding ADR, and offer to draft one from the PR's context.
