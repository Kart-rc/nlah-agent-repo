# Review-Debt Framework

Use this reference to apply the five signal families consistently, classify review burden, and produce the required review output.

## Contents

- [Definition and compounding loops](#definition-and-compounding-loops)
- [Evidence model](#evidence-model)
- [Test evidence: presence versus intent](#test-evidence-presence-versus-intent)
- [Qualitative burden classes](#qualitative-burden-classes)
- [Exact output template](#exact-output-template)
- [Worked example](#worked-example)
- [Scoring boundary](#scoring-boundary)

## Definition and Compounding Loops

Review debt is the accumulating gap between code produced and code that humans have actually reviewed, trusted, and understood. The debt consumes human attention and compounds through three loops:

1. **Generative grounding:** Agents learn from the codebase, so insufficiently reviewed code can ground future suggestions and pull requests.
2. **Attention contraction:** When reviewers perceive most code as generated, attention can narrow to syntax and obvious bugs while architectural decisions escape review.
3. **Capacity reset:** Increased throughput resets velocity expectations without proportional reviewer capacity, leaving no slack to repay the debt.

These loops explain why human accountability matters. They do not justify treating AI assistance as a defect.

## Evidence Model

Record concrete observations, their source, and what remains unavailable. A diff statistic, file path, CODEOWNERS mapping, test name, CI link, PR sentence, commit footer, or branch name is traceable evidence; an inference without a cited artifact is not.

| Signal family | Traceable evidence | Review question | Response |
|---|---|---|---|
| Diff size and coupling | Net lines changed; files and modules touched; shared interfaces modified; duplicated logic; change-shape mismatch with the stated goal | Is the change cohesive and locally understandable, or does coupling force reviewers to construct a broad mental model? | Request a split, shared abstraction, dependency map, or contract evidence when sprawl or coupling obscures safety. Do not equate raw size alone with a defect. |
| Test evidence gap | Test and production lines changed; tests added or removed; named behaviors and edge cases; failure-before-fix record; exact commands and results | Did relevant tests arrive, and do they demonstrate the intended behavior rather than encode the implementation? | Separate presence or ratio from quality. Request behavior-focused assertions, regression proof, or missing verification. Treat ratios as prompts for inspection, not quality scores. |
| Directory and owner spread | Directories and ownership territories touched; CODEOWNERS mappings; required approvals; operational or documentation owners | Does one reviewer hold the necessary context, and have all affected owners assessed the change? | Identify required reviewer contexts, request owner review, or suggest reshaping the change to reduce coordination. Owner count alone is not a correctness finding. |
| AI-authorship indicators | Co-author footers; generated-by markers; tool-pattern branch names; explicit author disclosure | Is AI assistance disclosed, and do the other evidence families show actual review burden? | State that the indicator is informational only. Never raise burden, block, or relax review solely because a tool may have helped author the change. |
| Evidence and rationale gaps | PR title and body; issue or requirement links; design decision; risk statement; benchmark, logs, reproduction, rollout and rollback evidence | Does the artifact explain why the change is needed, what should happen, and how the claim was verified? | Ask for the smallest missing evidence that makes the change reviewable. Mark unavailable evidence as missing or unverified; never fill gaps by assumption. |

After collecting the table, apply engineering judgment to correctness, test intent, architecture, security, and performance. A review-debt summary must not hide an actionable defect.

## Test Evidence: Presence Versus Intent

Evaluate test evidence in two separate layers:

1. **Presence and ratio:** Note whether tests changed and compare the shape of test changes with production changes. This can reveal an evidence gap, but it cannot prove quality.
2. **Intended-behavior quality:** Identify the requirement each test asserts, whether the regression test failed before the fix, whether boundary and failure cases are covered, and whether assertions would reject a plausible wrong implementation.

Implementation-shaped snapshots, copied control flow, and assertions derived only from current output may lock in bugs. Prefer tests tied to an independent requirement, contract, incident reproduction, or externally observable behavior.

If only a summary is available, say which test properties cannot be verified. Do not claim that green CI proves correctness.

## Qualitative Burden Classes

Classify the human effort required to reach a responsible decision, not the perceived quality of the author.

| Class | Meaning | Typical response |
|---|---|---|
| **Low** | Cohesive change with clear intent, strong behavior evidence, concentrated ownership, and manageable residual uncertainty | Complete normal review; approve when engineering findings are resolved. |
| **Moderate** | Reviewable change with one or more bounded evidence, coupling, or coordination gaps | Focus review on named risks; request targeted evidence or owner input. |
| **High** | Broad coupling, weak behavior evidence, multiple contexts, or missing rationale makes responsible review expensive or unreliable | Request changes, a split, stronger evidence, or coordinated specialist review before approval. |
| **Critical** | The artifact is not responsibly reviewable, or unresolved correctness/security risk combines with severe evidence and ownership gaps | Reject or require refactoring and re-submission with a reviewable scope and evidence package. |

Calibrate classes against the team's historical pull requests, review time, rework, incidents, and ownership model. Document the sample, definitions, and decision rules. If the team has historically calibrated numeric thresholds, apply and cite them explicitly. Otherwise, never assert numeric cutoffs or imply that these qualitative classes reproduce a scanner score.

AI-authorship indicators cannot determine or increase a class by themselves. Complexity, missing evidence, and required human coordination drive burden.

## Exact Output Template

Use these headings in this order. Write `None` only after checking the available evidence.

```markdown
## Prioritized findings

1. **[severity] Finding title** — `path:line` or artifact evidence
   - Impact: ...
   - Remedy: ...

## Review-debt evidence

| Signal family | Traceable evidence | Implication |
|---|---|---|
| Diff size and coupling | ... | ... |
| Test evidence gap | ... | ... |
| Directory and owner spread | ... | ... |
| AI-authorship indicators | ... | Informational only; no automatic penalty. |
| Evidence and rationale gaps | ... | ... |

## Reviewer focus

- ...

## Author next actions

- ...

## Missing/unverified evidence

- ...

## Burden

**Class:** Low | Moderate | High | Critical

**Rationale:** ...

**Calibration:** Qualitative and uncalibrated, or cite the team's historical criteria.

## Verdict

**Approve | Comment | Request changes | Reject/refactor:** ...
```

Prioritize real correctness, security, data-loss, or compatibility findings above review-debt observations. `Reviewer focus` names what reviewers should inspect or which expertise is needed. `Author next actions` names what the author must change or supply. Do not collapse them into a generic follow-up list.

## Worked Example

### Artifact

PR: "Consolidate retry handling." The summary reports +1,080/-170 lines across 18 files in `api/`, `billing/`, `worker/`, `shared/`, and `tests/`: four production ownership territories plus tests. Six call sites add the same predicate while a shared backoff helper changes. Four tests snapshot schedules produced by the new implementation. CI passes. No retry contract, test chronology, or failure-before-fix evidence is supplied. Four production CODEOWNERS teams are affected. Release approval is requested today.

### Review

## Prioritized findings

1. **High: Retry semantics have no reviewable contract** — PR summary identifies a changed shared helper and six consumers but supplies no before/after policy.
   - Impact: Reviewers cannot verify attempt limits, retryable failures, backoff bounds, or compatibility across services.
   - Remedy: Add a before/after retry-policy table and behavior tests for each shared invariant.
2. **Medium: The implementation duplicates the predicate it claims to consolidate** — PR summary reports the same predicate at six call sites.
   - Impact: Service behavior can drift and the architectural intent remains unfulfilled.
   - Remedy: Centralize the decision or justify distinct policies with explicit contracts.
3. **Medium: Snapshot tests mirror implementation output** — four tests snapshot returned schedules; whether they were written before or after implementation is unverified.
   - Impact: Green CI may preserve an incorrect schedule instead of validating intended behavior.
   - Remedy: Add requirement-derived assertions and show the regression test failing before the fix.

## Review-debt evidence

| Signal family | Traceable evidence | Implication |
|---|---|---|
| Diff size and coupling | +1,080/-170, 18 files, shared helper plus six consumers | Broad coupled change requires multiple service mental models. |
| Test evidence gap | Four tests for the change; snapshots of implementation output; chronology and failure-before-fix proof are not supplied | Test presence is visible, but intended-behavior quality is weak. |
| Directory and owner spread | Five directories: four production ownership territories plus `tests/`; four production CODEOWNERS teams | Coordinated specialist review is required. |
| AI-authorship indicators | None supplied | No inference; authorship is not a burden signal here. |
| Evidence and rationale gaps | No retry contract; deadline is given instead of behavioral rationale | Key claims cannot be verified from the artifact. |

## Reviewer focus

- Confirm shared retry invariants, service-specific exceptions, and compatibility with each owner team.
- Inspect whether one centralized policy can replace six predicates.

## Author next actions

- Supply the before/after policy and failure reproduction.
- Replace implementation-shaped snapshots with behavior assertions.
- Split the shared-helper change from consumer migrations if they cannot be reviewed cohesively.
- Obtain the four required owner reviews.

## Missing/unverified evidence

- Source diff, retry requirement, test chronology, failing-before-fix result, exact CI commands, and owner approvals.
- Security and performance effects of changed retry volume remain unverified.

## Burden

**Class:** High

**Rationale:** Broad coupling, four-owner coordination, weak behavioral evidence, and missing rationale make responsible review expensive.

**Calibration:** Qualitative and uncalibrated; no repository history was supplied.

## Verdict

**Request changes:** Provide a reviewable contract, behavior evidence, cohesive change shape, and owner coverage before approval. The deadline does not reduce the evidence standard.

## Scoring Boundary

The source talk mentions ten deterministic checks and a 0–100 score, but the public material does not permit faithful reproduction of the checks, weights, or thresholds. Do not reverse-engineer, invent, or present such a score as the talk's framework. Use the traceable qualitative method above unless a team supplies its own documented, historically calibrated model.
