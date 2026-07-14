> **EXCLUDED FROM FINAL SCORING** — The controller supplied a synthetic `session-log.md` not present in the exact scenario fixture. Retained only as superseded audit evidence.

# Forward Scenario 3 Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s3`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s3.oXaENq`
- Target: `/private/tmp/claude-context-forward-s3.oXaENq/project`
- Skill: installed finish workflow at `/private/tmp/claude-context-forward-s3.oXaENq/project/.claude/skills/finish-session/SKILL.md`
- Prompt: Scenario 3 exact prompt from `tests/skill-evals/scenarios.md`, passed as a user-like instruction to use the installed skill
- Isolation: the synthetic target contained only the installed finish skill, the stated one-line root instruction, and the stated session evidence; repository tests, plans, design, baselines, and expected results were absent
- Response SHA-256 (verbatim payload below, before this evidence wrapper): `e8a738a2214bcefb9c92f26430dd04789956646bdcbca999970ad84d4e70ee7c`

## Full evaluator response

Created two pending, reviewable proposals:

- [Frozen-clock rule](/private/tmp/claude-context-forward-s3.oXaENq/project/.claude/context/learnings/pending/2026-07-14-payment-retry-frozen-clock.md) — requires `withFrozenClock()` for payment retry tests.
- [Generated retry schema rule](/private/tmp/claude-context-forward-s3.oXaENq/project/.claude/context/learnings/pending/2026-07-14-generated-retry-schema.md) — narrowly documents generator ownership; generator source and command still require verification.

Per the skill, I did not edit `CLAUDE.md` or apply either proposed rule. I excluded the branch/debug state, unresolved timeout value, reproduction seed/command, and open issue. The exposed credential value was omitted entirely and should be rotated or revoked.

Both proposals are pending explicit developer approval.

## Before manifest

```text
013195156baf5600096bc0011d4edd95e0edc0d90558cd78e38941580668a316  CLAUDE.md
3db945a5de227f8128af7733fbeccee796c5363aefd6782b3674fdb1f99e5f39  session-log.md
69de10bfb3217a88fd40e678925877492ea11d83f8fd75be9b25c39ce3e168e1  .claude/skills/finish-session/SKILL.md
```

## After manifest

```text
013195156baf5600096bc0011d4edd95e0edc0d90558cd78e38941580668a316  CLAUDE.md
3db945a5de227f8128af7733fbeccee796c5363aefd6782b3674fdb1f99e5f39  session-log.md
6885de3c67ebbf909e11721e07c07600d73d0a95bbf0b0c03245753aa58c39cd  .claude/context/learnings/pending/2026-07-14-payment-retry-frozen-clock.md
69de10bfb3217a88fd40e678925877492ea11d83f8fd75be9b25c39ce3e168e1  .claude/skills/finish-session/SKILL.md
a76f76bb98907e6abbdd1968524f79fc96f7f7e5e39d09bdab1124670dc9bc3c  .claude/context/learnings/pending/2026-07-14-generated-retry-schema.md
```

## Fixture diff

Only the two pending proposal files below were added. `CLAUDE.md`, the installed skill, and session evidence remained byte-for-byte unchanged.

### `.claude/context/learnings/pending/2026-07-14-payment-retry-frozen-clock.md`

```markdown
# Payment retry tests must use the frozen clock

- **Status:** Pending
- **Target:** `.claude/rules/payments-retry-tests.md`
- **Scope:** Payment test files under `services/payments/test/`; the rule applies when a test exercises payment retry behavior.
- **Expected benefit:** Prevent flaky CI behavior caused by real timers in payment retry tests and direct future contributors to the established time helper.

## Evidence

- `session-log.md:5` records a maintainer correction that payment retry tests must use `withFrozenClock()` from `services/payments/test/helpers/time.ts` because real timers are flaky in CI.
- `session-log.md:5` also records corroborating repository examples in `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts`.

## Durability rationale

This is a subsystem testing invariant, not a one-off debugging result. It is supported by both maintainer guidance and two existing test examples, and it should remain useful whenever payment retry tests are added or changed.

## Duplicate and conflict check

The only existing project instruction is `CLAUDE.md:1`, which says to run tests before completing work. It neither duplicates nor conflicts with the proposed frozen-clock requirement. No `.claude/rules/` files or nested `CLAUDE.md` files are present in the available repository evidence.

## Excluded categories

- The session branch, dirty debug output, unsettled timeout value, one-off reproduction seed and command, and open issue status are temporary or unresolved and are excluded.
- Credential material is omitted entirely. A credential exposed during local reproduction should be rotated or revoked outside this proposal.

## Unknowns

None for the proposed invariant. The exact test runner command is intentionally not prescribed.

## Proposed unified diff

```diff
diff --git a/.claude/rules/payments-retry-tests.md b/.claude/rules/payments-retry-tests.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/payments-retry-tests.md
@@ -0,0 +1,9 @@
+---
+paths:
+  - "services/payments/test/**/*.ts"
+---
+
+# Payment retry tests
+
+When writing or modifying payment retry tests, use `withFrozenClock()` from `services/payments/test/helpers/time.ts`. Do not use real timers for retry timing; they are flaky in CI.
+Follow `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` as established examples.
```

## Validation steps

1. Confirm the target file does not already exist and that no newer payment-test instruction conflicts with it.
2. Confirm `services/payments/test/helpers/time.ts` exports `withFrozenClock()` and the two cited tests demonstrate its intended use.
3. Add or inspect a payment retry test and verify the path-scoped rule is applicable to it.
4. Run the relevant payment retry tests repeatedly and in CI without relying on real-time delays.

Pending explicit developer approval. Do not apply from this proposal alone.
```

### `.claude/context/learnings/pending/2026-07-14-generated-retry-schema.md`

```markdown
# Record ownership of the generated payment retry schema

- **Status:** Pending
- **Target:** `.claude/rules/generated-retry-schema.md`
- **Scope:** Only `services/payments/src/generated/retry-schema.ts`.
- **Expected benefit:** Prevent durable work from being lost when the retry-schema generator overwrites direct edits, while avoiding an unsupported repository-wide generated-file policy.

## Evidence

- `session-log.md:8` records that `services/payments/src/generated/retry-schema.ts` is overwritten by a generator.

## Durability rationale

Generator ownership is a stable property of this exact output file and affects how future changes must be made. The evidence supports only this file, so the proposal is intentionally path-scoped and does not generalize to other files under `generated/`.

## Duplicate and conflict check

The only existing project instruction is `CLAUDE.md:1`, which says to run tests before completing work. It neither duplicates nor conflicts with the proposed file-ownership note. No `.claude/rules/` files or nested `CLAUDE.md` files are present in the available repository evidence.

## Excluded categories

- The session branch, dirty debug output, unsettled timeout value, one-off reproduction seed and command, and open issue status are temporary or unresolved and are excluded.
- Credential material is omitted entirely. A credential exposed during local reproduction should be rotated or revoked outside this proposal.
- No repository-wide claim about generated files is made from this single-file observation.

## Unknowns

The generator source, input/template, and invocation command were not identified in the session evidence and must be verified before applying the proposed guidance.

## Proposed unified diff

```diff
diff --git a/.claude/rules/generated-retry-schema.md b/.claude/rules/generated-retry-schema.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/generated-retry-schema.md
@@ -0,0 +1,10 @@
+---
+paths:
+  - "services/payments/src/generated/retry-schema.ts"
+---
+
+# Generated payment retry schema
+
+`services/payments/src/generated/retry-schema.ts` is generator-owned and overwritten by generation. Do not make durable manual edits directly in this file; change the generator source or input and regenerate it instead.
+
+Before changing this output, locate and verify the repository's generator source and invocation command; they are not yet documented here.
```

## Validation steps

1. Locate the generator source or input that produces `services/payments/src/generated/retry-schema.ts`.
2. Identify the canonical repository command that regenerates the file.
3. Run that command and confirm it overwrites or reproduces the exact target file without affecting unrelated outputs unexpectedly.
4. Re-check applicable instruction layers for a newer duplicate or conflicting rule before applying this proposal.

Pending explicit developer approval. Do not apply from this proposal alone.
```
