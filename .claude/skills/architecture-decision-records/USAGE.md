# Using `architecture-decision-records`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

Drives a significant technical decision to clarity — drivers first, real
alternatives, door classification — calibrated against enterprise context
discovered from connected MCP servers and supplied by you (Phase 0, never
skipped), then captures it as a numbered, cited ADR in the project's ADR log.

## When to invoke

- The activation cues in SKILL.md → When to Activate: "ADR this", "help me
  decide between X and Y", "we decided to...", or "why did we choose X?"
  (which reads existing ADRs rather than creating one).
- After a `tech-decision` workflow run completes, to transcribe its gated
  `decision.md` into the project ADR log (SKILL.md → Harness integration).
- Not for trivial decisions — naming or formatting choices don't need ADRs
  (SKILL.md → What Makes a Good ADR).
- Contested, High/Critical-risk, or one-way-door decisions with material
  blast radius are not settled in chat: the skill escalates them through
  `agentic-delivery-router` to the `tech-decision` workflow and captures the
  result afterward. It never orchestrates workflows itself.

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it whenever a significant technical choice is being
made, compared, questioned, or needs recording.

## How to invoke

### In conversation

Explicit invocation:

```text
/architecture-decision-records Record our choice of Postgres over DynamoDB
for the orders service.
```

Natural-language requests that trigger it via the frontmatter description:

```text
Help me decide between REST and GraphQL for the partner API.
```

```text
Why did we choose Next.js for the dashboard?
```

### Requirements

Run it in the target repository (it locates or, with your consent, creates
the ADR directory — `docs/adr/`, `docs/decisions/`, or `adr/`). Connected
enterprise MCP servers (internal docs/wiki search, ticket trackers, code
search, service catalogs) make Phase 0a far stronger; without them the skill
degrades honestly, recording unanswered questions under `## Knowledge gaps`
instead of guessing. Its MCP discipline follows
`harness/knowledge/enterprise-mcp/adapter.md`.

## What to expect

- A right-sized Phase 0 sweep (prior art, standards, platform inventory,
  policy, in-flight work) plus one batched round of questions covering only
  what discovery did not answer.
- The decision framed in one sentence with 3–6 drivers stated *before*
  options, each alternative judged for enterprise fit, and a one-way/two-way
  door classification with confidence.
- A draft ADR in the format from SKILL.md → ADR Format, presented for your
  review — nothing is written until you explicitly approve, and existing ADR
  conventions in the repo are followed, never replaced.
- On approval: `docs/adr/NNNN-decision-title.md` plus an index row in
  `docs/adr/README.md`, with every organizational claim cited
  `[source: enterprise-mcp/<tool-or-doc>]` or `[source: user]`.
- Warning signs it is misapplied: an empty `## Enterprise context` on a
  non-trivial decision (Phase 0 was skipped), or files created without your
  confirmation.

## Worked example

You say: "Help me decide between Kafka and SQS for order events." The skill
searches connected MCP sources and finds an approved-technology entry
mandating SQS for new internal queues plus a platform team operating it; you
add that this is an internal tool owned by a two-person team. It frames
drivers (ordering guarantees, ops burden, standards compliance), judges both
options, classifies a two-way door, recommends SQS, and presents ADR-0007
for review. On approval it writes `docs/adr/0007-sqs-for-order-events.md`
and updates the index.
