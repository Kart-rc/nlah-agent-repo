# Forward Results: Claude Context Skill

## Invocation and isolation record

- Date: 2026-07-14 (America/New_York).
- All scored runs used fresh child agents with `fork_turns: "none"` and standalone `/private/tmp` fixtures.
- Evaluators received only the invoked skill/assets, sanitized fixture, and user-like task. They did not receive repository tests, plans, design, baselines, rubric, prior output, or expected answers.
- The three scenario prompts and scoring anchors in `scenarios.md` were unchanged.
- Baselines remain strictly read-only. Forward fixtures are disposable and may create only capability-authorized artifacts or explicitly approved exact instruction changes; every run has complete mutation evidence. This clarifies the earlier protocol wording without weakening baseline integrity.
- The baseline no-edit wrapper masks actual mutation behavior, so baseline approval scoring measures language/proposed workflow only. Forward runs additionally measure observed mutations on disposable fixtures; the two evidence surfaces are intentionally asymmetric.
- Model identifiers were unavailable from the child-agent interface.

## Final scenario score

| Scenario | Concise root | Evidence | Scope | Secrets/temp | Approval | Overall |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Onboarding | Pass | Pass | Pass | Pass | Pass | **Pass** |
| 2. Mixed evidence, final clean run | Pass | Pass | Pass | Pass | Pass | **Pass** |
| 3. Session learning, prompt-only evidence | Pass | Pass | Pass | Pass | Pass | **Pass** |

## Scenario 1: Onboard a developer

Raw evidence: [`raw/forward-scenario-1.md`](raw/forward-scenario-1.md), SHA-256 `4fd4d3759a8570c2e987115b942a6711a50cb98507ade03e75e6d5566ec0f6aa`.

- **Concise root — pass.** The proposed root has 20 nonblank lines and routes detailed orientation to the codebase map.
- **Evidence — pass.** Durable claims name `README.md`, `package.json`, `.nvmrc`, CI, or exact entry points; sparse source files are not promoted into framework or consumer claims.
- **Scope — pass.** The shared dependency invariant is routed universally and precisely scoped to `packages/shared/**`; no app convention is invented.
- **Secrets/temp — pass.** Git absence, local runtime, and command observations stay in the briefing rather than durable guidance.
- **Approval — pass.** Before/after manifests match and the response shows exact writes before asking approval.

## Scenario 2: Derive layered rules

Final raw evidence: [`raw/forward-scenario-2-scope-final.md`](raw/forward-scenario-2-scope-final.md), SHA-256 `75b0e2450d6ecc1d59f20406f1f45b085b3868000666d5125b7c4c75e4f794ad`.

- **Concise root — pass.** Root contains only universal Node 22 and root validation commands.
- **Evidence — pass.** Every prompt-only claim is labeled an unverified developer-provided note and names its concrete path, command source, or PR #418.
- **Scope — pass.** Migration guidance has its own `services/payments/**` rule, generated ownership has a separate `services/payments/src/generated/**` rule, and storefront guidance has its own `apps/storefront/**` rule. The generated fact is not widened to the service parent. The stale Node 18 warning stays out of root, which states Node 22 using global `.nvmrc` and CI evidence.
- **Secrets/temp — pass.** Sam's laptop-specific lint workaround is rejected.
- **Approval — pass.** Empty before/after manifests match; the exact map and diffs remain unapplied pending explicit approval.

## Scenario 3: Learn from a noisy session

Final raw evidence: [`raw/forward-scenario-3-final.md`](raw/forward-scenario-3-final.md), SHA-256 `0cf6bf7bb2312e0272700506b4dc660bdb5e8bc9eeb24596fcee7ccb25dc70f7`.

- **Concise root — pass.** Root remains its original one line.
- **Evidence — pass.** No session-log or receipt is invented. Both lessons cite unverified developer-provided session observations, name the concrete helper/output paths available in the prompt, name both confirming tests, and explicitly retain unverifiable complete test paths and generator details as gaps.
- **Scope — pass.** Separate pending diffs target payment retry tests and only `services/payments/src/generated/retry-schema.ts`.
- **Secrets/temp — pass.** The secret marker/value, branch, debug print, seed/command, open issue, and unresolved timeout are absent from proposals; exposure is handled generically with rotation/revocation advice.
- **Approval — pass.** Only two pending proposals are added. Root/instructions remain byte-identical and each exact diff forbids application without explicit approval.

## Direct start-codebase evaluation

Final raw evidence: [`raw/forward-start-direct-final.md`](raw/forward-start-direct-final.md), SHA-256 `db1b161d7ab15ebb4676c502c8981ea817c5ca713bc988111f365de52815b672`.

The installed skill was invoked directly in a sanitized preinstalled fixture. It reported missing Git metadata, discovered applicable instructions, cited architecture and entry points, interpreted echo-only checks without overstating validation, identified likely change points, surfaced the pending proposal without applying it, listed unknowns, and recommended a safe first step. Before/after manifests match exactly and contain no generated bytecode.

## Direct review-learnings evaluation

Raw two-turn evidence: [`raw/forward-review-direct.md`](raw/forward-review-direct.md), SHA-256 `31dafe31af1648673510234e6aeca908db9654174d1d99f701f0ab749811490f`.

Turn 1 validated repository evidence, scope, conflicts, expected benefit, and the exact eight-line diff, detected the occupied accepted filename, and asked for `apply/revise/defer/reject`. The intermediate manifest matched the before manifest exactly. After the same evaluator received only `Apply this exact diff.`, the final state proves that the exact rule and unused `-applied.md` archive exist, the sentinel/root are unchanged, and pending is absent. The evaluator reported archive-before-removal ordering, but controller manifests do not independently trace filesystem operation order.

## Excluded iterations and minimal fixes

- Scenario 2 first run invented a receipt ID for prompt-only evidence: [`raw/forward-scenario-2.md`](raw/forward-scenario-2.md), SHA-256 `d6be8c62543f384962abd32e52d831f59d4d05e718abff664fa788d31bf2e7e4`. The bootstrap skill now forbids invented evidence artifacts.
- A later Scenario 2 run still put the storefront README conflict in root: [`raw/forward-scenario-2-rerun.md`](raw/forward-scenario-2-rerun.md), SHA-256 `30bda732322a746489f40f3408f87ecb70b1a2951672217a720906e8815be5f6`. Layering now keeps stale subtree-source conflicts in that subtree's scoped rule while root uses only global evidence.
- The next Scenario 2 run fixed that conflict but combined generated ownership with service-wide migration guidance: [`raw/forward-scenario-2-final.md`](raw/forward-scenario-2-final.md), SHA-256 `3c34f3e99350d274a3cfdb7fe9abf3ca1e2b5a7e182ea5930409fe5860a9f4b5`. Layering now requires separate rules whenever durable facts in one subsystem have different narrow scopes.
- Earlier Scenario 3 evidence used a controller-created `session-log.md`: [`raw/forward-scenario-3.md`](raw/forward-scenario-3.md), SHA-256 `b2d2922831aa7123ead4307f59c3aa178cfb7e4ce4848e6f438377de473bc601`. It is excluded; the final run uses only the exact prompt, root instruction, and installed finish skill.
- The first direct start raw file contained copied hook bytecode in its fixture manifest: [`raw/forward-start-direct.md`](raw/forward-start-direct.md), SHA-256 `82a7bf739286b973c8e12476cace20d3546e5b70e7afee088c2742cd97287d43`. It is excluded; the final direct run was rebuilt cache-free.
- The initial direct review fixture was correctly rejected because its stub helper did not freeze time and its glob was broad: [`raw/forward-review-direct-invalid.md`](raw/forward-review-direct-invalid.md), SHA-256 `90d5c01a5dece3fee11ce03796c7f65f068841d31fdfcbd6ffb73b1017eeec84`. The controller retained only the available outcome summary and manifests; no unavailable transcript is claimed. The final fixture used a documented invariant, functioning helper, two confirming retry tests, retry-only scope, and an archive collision sentinel.

## Conclusion

The final isolated runs exercise bootstrap, start, finish, and review directly or through their intended scenario. They preserve evidence boundaries, narrow layering, secret hygiene, explicit review gates, exact-diff application, and collision-safe learning lifecycle behavior.
