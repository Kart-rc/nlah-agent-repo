# Direct Review-Learnings Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_review_final`
- Context: fresh child agent with `fork_turns:none`; explicit approval was sent as a second turn in the same context
- Evaluation root: `/private/tmp/claude-context-forward-review-final.I22Mwd`
- Target: disposable preinstalled fixture with a valid pending proposal and a preexisting same-name accepted sentinel
- Skill: installed `.claude/skills/review-learnings/SKILL.md`
- Isolation: no source-repository tests, plans, design, baselines, rubric, prior output, or expected answer

## Deterministic fixture construction

```sh
ROOT=/private/tmp/claude-context-forward-review-final.I22Mwd
mkdir -p "$ROOT/project/.claude/skills/review-learnings" \
  "$ROOT/project/.claude/context/learnings/pending" \
  "$ROOT/project/.claude/context/learnings/accepted" \
  "$ROOT/project/services/payments/test/helpers" \
  "$ROOT/controller"
cp .claude/skills/bootstrap-claude-context/assets/project/.claude/skills/review-learnings/SKILL.md \
  "$ROOT/project/.claude/skills/review-learnings/SKILL.md"
```

The remaining initial fixture files had these exact contents:

`CLAUDE.md`:

```markdown
# Project Instructions

Run tests before completing work.
```

`services/payments/README.md`:

```markdown
# Payments testing

Payment retry tests must use `withFrozenClock()` from `test/helpers/time.ts`; real timers make retry assertions flaky in CI.
```

`services/payments/test/helpers/time.ts`:

```ts
export function withFrozenClock<T>(run: () => T): T {
  const originalNow = Date.now;
  Date.now = () => 0;
  try {
    return run();
  } finally {
    Date.now = originalNow;
  }
}
```

`services/payments/test/retry-policy.test.ts`:

```ts
import { withFrozenClock } from "./helpers/time";

export const retryPolicyUsesFrozenClock = withFrozenClock(() => Date.now() === 0);
```

`services/payments/test/settlement-retry.test.ts`:

```ts
import { withFrozenClock } from "./helpers/time";

export const settlementRetryUsesFrozenClock = withFrozenClock(() => Date.now() === 0);
```

`.claude/context/learnings/accepted/2026-07-14-payment-retry-frozen-clock.md`:

```markdown
# Existing accepted artifact

This sentinel proves collision-safe archival preserves an existing artifact.
```

`.claude/context/learnings/pending/2026-07-14-payment-retry-frozen-clock.md`:

````markdown
# Payment retry tests must use the frozen clock

Status: pending
Target: `.claude/rules/payments-retry-tests.md`
Scope: `services/payments/test/**/*retry*.test.ts`
Expected benefit: prevent flaky payment retry timing assertions caused by real timers and route contributors to the established helper.

## Evidence

- `services/payments/README.md` requires payment retry tests to use `withFrozenClock()` because real timers are flaky in CI.
- `services/payments/test/helpers/time.ts` freezes and restores `Date.now` around a callback.
- `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` use the helper and observe the frozen time.

## Admission check

- Durable beyond this session: the documented requirement and helper behavior are repository-owned.
- Duplicate/conflict search: `CLAUDE.md` contains only universal test guidance; no rule files exist.
- Excluded material: no temporary state or credentials.
- Unknowns: none.

## Exact proposed diff

```diff
diff --git a/.claude/rules/payments-retry-tests.md b/.claude/rules/payments-retry-tests.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/payments-retry-tests.md
@@ -0,0 +1,8 @@
+---
+paths:
+  - "services/payments/test/**/*retry*.test.ts"
+---
+
+# Payment retry tests
+
+Use `withFrozenClock()` from `services/payments/test/helpers/time.ts` in payment retry tests. Do not use real timers; they are flaky in CI. Follow `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` as examples.
```

## Validation

- Confirm the README requirement, helper behavior, and both examples.
- Confirm the rule is retry-test-scoped and root remains unchanged.

## Decision

Pending explicit developer approval. Do not apply from this proposal alone.
````

The controller then ran:

```sh
cp -R "$ROOT/project" "$ROOT/controller/project.before"
```

## Turn 1 exact wrapper and prompt

> Work only inside `/private/tmp/claude-context-forward-review-final.I22Mwd`; do not inspect or reference any other repository or conversation. Treat `/private/tmp/claude-context-forward-review-final.I22Mwd/project` as the target repository. Use the installed review-learnings skill at `/private/tmp/claude-context-forward-review-final.I22Mwd/project/.claude/skills/review-learnings/SKILL.md` and follow it faithfully for this user request:
>
> Please review the pending payment retry frozen-clock learning proposal. Validate its evidence and scope, show me the exact diff and expected benefit, and ask for the proposal-specific decision required by the workflow. Do not infer my decision.
>
> Return your full user-facing response at the required decision checkpoint.

## Turn 1 full response

The proposal is valid and appropriately scoped. Its claims are supported, with no instruction conflicts or unsupported citations.

Evidence:

- `services/payments/README.md` explicitly requires `withFrozenClock()` for payment retry tests and says real timers make retry assertions flaky in CI.
- `services/payments/test/helpers/time.ts` freezes `Date.now` to `0` and reliably restores it in `finally`.
- `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` both use the helper and assert against the frozen time.
- The scoped pattern covers both current retry test files.
- `CLAUDE.md` contains only the universal instruction to run tests. No existing `.claude/rules` guidance duplicates or contradicts this proposal.

Expected benefit: contributors editing payment retry tests receive the established helper and examples in-context, reducing CI-flaky timing assertions. The flakiness claim is directly documented; improved contributor routing is a reasonable inference from the path-scoped rule.

Scope: `services/payments/test/**/*retry*.test.ts` is suitably narrow. Payment-specific guidance stays out of the three-line root `CLAUDE.md`, which remains well below the 200-line limit.

Exact minimal diff:

```diff
diff --git a/.claude/rules/payments-retry-tests.md b/.claude/rules/payments-retry-tests.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/payments-retry-tests.md
@@ -0,0 +1,8 @@
+---
+paths:
+  - "services/payments/test/**/*retry*.test.ts"
+---
+
+# Payment retry tests
+
+Use `withFrozenClock()` from `services/payments/test/helpers/time.ts` in payment retry tests. Do not use real timers; they are flaky in CI. Follow `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` as examples.
```

Validation after an explicit apply would confirm the displayed diff is unchanged, recheck the referenced paths and scoped frontmatter, verify root guidance remains untouched, and repeat the duplicate/contradiction search. No project context validator is present. The preferred accepted-archive filename is already occupied by a sentinel artifact, so archival must use an unused filename without overwriting it.

Choose **apply, revise, defer, or reject** for this exact diff to `.claude/rules/payments-retry-tests.md`. Only **apply** authorizes the instruction edit.

## Intermediate manifest and diff

Controller commands:

```sh
cp -R "$ROOT/project" "$ROOT/controller/project.intermediate"
find "$ROOT/controller/project.before" -type f -exec shasum -a 256 {} + | sort
find "$ROOT/controller/project.intermediate" -type f -exec shasum -a 256 {} + | sort
diff -ruN "$ROOT/controller/project.before" "$ROOT/controller/project.intermediate"
```

The complete intermediate manifest matched the before manifest byte-for-byte. `diff -ruN` exited 0, proving the review turn did not mutate instructions, the proposal, or the sentinel.

```text
354bf85a69caaf441ab5050bb6d7e2bbde267d7f5d293040e22c9f7ff65c8774  services/payments/test/settlement-retry.test.ts
6d5b2308405cea0498df43ab562ad9958e073b8f8dcd3ac476c8f38921b2bac6  services/payments/test/retry-policy.test.ts
73b41a4ed7713f65a3e90148b9c51c73663fb1742427089277a7ddf8018e2318  .claude/context/learnings/pending/2026-07-14-payment-retry-frozen-clock.md
7bc2c3a3ae973ac74376334e051b0eee8c9a6ad826aaf57fb944473267a3c505  CLAUDE.md
96ce1bf7639e74936851b35cbb122d6a406e274c835edc27b1bb5f9a08a3e4c6  .claude/context/learnings/accepted/2026-07-14-payment-retry-frozen-clock.md
b7b4ce62c9ab51d274a73628092fba909a62b82cea78a982d2a2228902b79f25  services/payments/test/helpers/time.ts
dff9c3671d3b43866dc57ecb853942474e838463e00dae45c6dee040c10e5ed1  services/payments/README.md
efc9e77a1e6e23a514d59896917a12c7bda978a2dd08e26c00b6d87c717f6116  .claude/skills/review-learnings/SKILL.md
```

## Turn 2 exact user approval

> Apply this exact diff.

## Turn 2 full response

Applied the approved exact diff to `.claude/rules/payments-retry-tests.md`.

Fresh validation passed:

- Rule content matches the approved eight-line diff exactly.
- All cited evidence paths exist.
- Scope covers both current payment retry tests.
- Root `CLAUDE.md` remains unchanged at three lines.
- The existing accepted sentinel was preserved.
- The disposition, approver, date, applied diff, and validation result were recorded in `2026-07-14-payment-retry-frozen-clock-applied.md`.
- The pending proposal was removed only after successful collision-safe archival.
- No project context validator was available.

## After manifest

Controller commands:

```sh
find "$ROOT/project" -type f -exec shasum -a 256 {} + | sort
diff -ruN "$ROOT/controller/project.intermediate" "$ROOT/project"
```

```text
354bf85a69caaf441ab5050bb6d7e2bbde267d7f5d293040e22c9f7ff65c8774  services/payments/test/settlement-retry.test.ts
6d5b2308405cea0498df43ab562ad9958e073b8f8dcd3ac476c8f38921b2bac6  services/payments/test/retry-policy.test.ts
7bc2c3a3ae973ac74376334e051b0eee8c9a6ad826aaf57fb944473267a3c505  CLAUDE.md
96ce1bf7639e74936851b35cbb122d6a406e274c835edc27b1bb5f9a08a3e4c6  .claude/context/learnings/accepted/2026-07-14-payment-retry-frozen-clock.md
b7b4ce62c9ab51d274a73628092fba909a62b82cea78a982d2a2228902b79f25  services/payments/test/helpers/time.ts
d5c9daad3e4c7208795fbc086d736c03713f69b60a6f85fd970596ffb3a05c5c  .claude/context/learnings/accepted/2026-07-14-payment-retry-frozen-clock-applied.md
dff9c3671d3b43866dc57ecb853942474e838463e00dae45c6dee040c10e5ed1  services/payments/README.md
e62dc2a005fa323361fd9dabe1837056a03ae83f1085190ba679aeacbbb856bf  .claude/rules/payments-retry-tests.md
efc9e77a1e6e23a514d59896917a12c7bda978a2dd08e26c00b6d87c717f6116  .claude/skills/review-learnings/SKILL.md
```

## Intermediate-to-after diff

The applied instruction file was exactly the approved eight-line diff:

```diff
--- /dev/null
+++ b/.claude/rules/payments-retry-tests.md
@@ -0,0 +1,8 @@
+---
+paths:
+  - "services/payments/test/**/*retry*.test.ts"
+---
+
+# Payment retry tests
+
+Use `withFrozenClock()` from `services/payments/test/helpers/time.ts` in payment retry tests. Do not use real timers; they are flaky in CI. Follow `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` as examples.
```

The final state contains the unused collision-safe archive name `2026-07-14-payment-retry-frozen-clock-applied.md`, the complete proposal evidence, applied diff, disposition, approver, date, and validation result. The existing `2026-07-14-payment-retry-frozen-clock.md` sentinel retained SHA-256 `96ce1bf7639e74936851b35cbb122d6a406e274c835edc27b1bb5f9a08a3e4c6`, and pending is absent. The evaluator reported archive-before-removal ordering; the controller manifests prove only these intermediate/final states, not filesystem operation order.

The complete added accepted artifact was:

```markdown
# Payment retry tests must use the frozen clock

Status: accepted
Target: `.claude/rules/payments-retry-tests.md`
Scope: `services/payments/test/**/*retry*.test.ts`
Expected benefit: prevent flaky payment retry timing assertions caused by real timers and route contributors to the established helper.

## Evidence

- `services/payments/README.md` requires payment retry tests to use `withFrozenClock()` because real timers are flaky in CI.
- `services/payments/test/helpers/time.ts` freezes and restores `Date.now` around a callback.
- `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` use the helper and observe the frozen time.

## Admission check

- Durable beyond this session: the documented requirement and helper behavior are repository-owned.
- Duplicate/conflict search: `CLAUDE.md` contains only universal test guidance; no prior rule files existed.
- Excluded material: no temporary state or credentials.
- Unknowns: none.

## Applied diff

```diff
diff --git a/.claude/rules/payments-retry-tests.md b/.claude/rules/payments-retry-tests.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/payments-retry-tests.md
@@ -0,0 +1,8 @@
+---
+paths:
+  - "services/payments/test/**/*retry*.test.ts"
+---
+
+# Payment retry tests
+
+Use `withFrozenClock()` from `services/payments/test/helpers/time.ts` in payment retry tests. Do not use real timers; they are flaky in CI. Follow `services/payments/test/retry-policy.test.ts` and `services/payments/test/settlement-retry.test.ts` as examples.
```

## Disposition

- Disposition: apply
- Approver: developer
- Date: 2026-07-14
- Validation result: passed. The applied rule matched the approved exact diff; all referenced repository paths exist; the scope matches both current payment retry tests; the root `CLAUDE.md` remained unchanged at three lines; no conflicting guidance was found; no project context validator was available.
```

The removed pending artifact was the original 46-line proposal whose SHA-256 was `73b41a4ed7713f65a3e90148b9c51c73663fb1742427089277a7ddf8018e2318`; its evidence, exact diff, and decision text are reproduced by the accepted artifact above, with status/disposition and validation updated only after successful application.
