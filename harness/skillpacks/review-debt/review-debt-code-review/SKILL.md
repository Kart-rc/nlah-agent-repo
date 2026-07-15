---
name: review-debt-code-review
description: Use when reviewing pull requests or code changes where reviewability, human understanding, AI-assisted volume, weak rationale, test evidence, cross-module coupling, or ownership spread may create hidden review burden.
---

# Review-Debt Code Review

## Core Principle

Review the complexity and evidence, not who or what wrote the code. Hold a human accountable for understanding the change, supplying evidence, and accepting its risk. Apply the same engineering standard to every change.

**Required:** Read [the review-debt framework](references/review-debt-framework.md) before applying this workflow. It defines the signal evidence, burden calibration, and required output.

## Workflow

1. Establish the change's intent, requirements, claimed behavior, available diff, ownership, and verification evidence. Mark anything unavailable as unverified; never guess.
2. Inspect tests before implementation. Determine the intended behavior they claim to prove, whether they failed before the change, and whether assertions test behavior instead of mirroring implementation.
3. Collect traceable evidence for all five signal families:
   - diff size and coupling;
   - test evidence gap;
   - directory and owner spread;
   - AI-authorship indicators;
   - evidence and rationale gaps.
4. Review the implementation for correctness, test intent, architecture, security, and performance. Preserve ordinary code-review rigor: review debt supplements engineering findings; it does not replace them.
5. Lead with prioritized, evidence-backed findings. For each finding, cite the affected file, line, diff fact, or supplied artifact; explain impact; and propose a concrete remedy.
6. Then report, in stable sections: review-debt evidence, reviewer focus, author next actions, missing or unverified evidence, qualitative burden, and verdict.

## Quick Reference

| Stage | Required result |
|---|---|
| Understand | Intent, requirements, claims, owners, available evidence |
| Test first | Intended behavior, failure-before-fix, assertion quality |
| Measure | Traceable evidence for all five signal families |
| Judge | Correctness, tests, architecture, security, performance |
| Report | Findings first, structured actions, burden, verdict |

## Guardrails and Red Flags

- Never penalize AI authorship automatically. Treat indicators as informational only and say so explicitly.
- Never invent a 0–100 score, undisclosed ten checks, weights, or thresholds. Use qualitative burden unless the team supplies historically calibrated criteria; cite those criteria when used.
- Never guess missing rationale, ownership, test results, or implementation details. List them as missing or unverified.
- Never return an empty `LGTM`; state what evidence supports approval and what remains unverified.
- Never lower correctness, security, architecture, evidence, or ownership standards under deadline pressure.
- Do not confuse test presence or test-to-production ratio with tests that prove intended behavior.
- Keep reviewer focus separate from author actions: one directs review attention; the other requests remediation.
