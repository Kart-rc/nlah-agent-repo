# Using `doubt-driven-development`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Subjects every non-trivial in-flight decision to a fresh-context adversarial
review before it stands: name the CLAIM, extract the smallest artifact plus
its contract, hand only those to a reviewer prompted to disprove, reconcile
findings yourself, and stop within three bounded cycles.

## When to invoke

- Correctness outweighs speed: production-affecting logic, security-sensitive
  code, data migrations, or other irreversible blast radii.
- A decision matches the skill's non-triviality tests — new branching logic,
  cross-boundary changes, or properties the compiler cannot verify (thread
  safety, idempotence, ordering).
- Work in unfamiliar code where confident output is cheaper to verify now
  than to debug later.
- See SKILL.md → When to Use / When NOT to use — it exempts mechanical edits,
  one-liners, and cases where the user asked for speed over verification.

**Default attachments:** none — and deliberately so. SKILL.md → Loading
Constraints states this skill is designed for the **main-session
orchestrator** and must NOT be added to a persona's skills: its DOUBT step
spawns a fresh-context reviewer, which a producer subagent cannot do
(personas do not invoke other personas).

## How to invoke

### In a harness workflow

Do not attach it to producer stages — that places it inside a subagent,
where SKILL.md permits only a degraded self-questioning fallback flagged as
such. The harness's validator stages already institutionalize the DOUBT step
(HARNESS.md §7.1); use this skill from the main session instead. If you
nevertheless attach it, expect degraded-mode output only:

```yaml
# Not recommended — see SKILL.md → Loading Constraints before doing this.
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/doubt-driven-development
```

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/doubt-driven-development/SKILL.md fully,
then apply its doubt cycle to <the pending decision or diff>: write the
CLAIM, extract ARTIFACT + CONTRACT, spawn an adversarial fresh-context
reviewer, reconcile findings, and stop per its bounds.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Each non-trivial decision produces a visible five-step doubt cycle
  (CLAIM → EXTRACT → DOUBT → RECONCILE → STOP) with the checklist filled in.
- The reviewer receives ARTIFACT + CONTRACT only — never the CLAIM or the
  author's reasoning — and is prompted to find issues, not to validate.
- In interactive sessions a cross-model second opinion is explicitly offered
  every cycle; in non-interactive contexts the skip is announced. External
  CLIs run only with per-invocation authorization, via stdin, read-only.
- Findings are classified by precedence (contract misread, actionable,
  trade-off, noise); the loop stops at trivial findings, three cycles — then
  escalate — or user override.
- Misapplication signs: doubt theater (cycles with substantive findings but
  zero classified actionable), or rubber-stamping the reviewer without
  re-reading the artifact (see SKILL.md → Red Flags).

## Worked example

Request (main session, no formal run): "Add per-user caching to the session
lookup — it's on the hot path and must be safe under concurrent refresh."

The orchestrator reads SKILL.md and writes the CLAIM ("the cache is safe
under concurrent token refresh") with why it matters. It extracts the
~40-line diff plus the contract (no stale session served after logout) and
spawns a fresh-context reviewer with the adversarial prompt, ARTIFACT +
CONTRACT only. The reviewer finds a check-then-act gap; the orchestrator
classifies it actionable, fixes the ordering, re-loops once (trivial
findings), offers a cross-model pass (user skips, acknowledged), and commits.
