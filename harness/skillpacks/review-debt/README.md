# Skill Pack: review-debt (first-party)

First-party practice skills for finding and reducing hidden human review
burden in code changes. This pack is original content authored for this
harness; it is not vendored from another skill repository.

- **Contents:** 1 skill, `review-debt-code-review`
- **Harness reference:** `skillpacks/review-debt/review-debt-code-review`
- **Format:** `<skill-name>/SKILL.md`, with optional supporting references

## Source and adaptation

The pack adapts the public framework presented by Sachin Gupta in
[“Your Coding Agent Is Creating Review Debt”](https://www.youtube.com/watch?v=TJPInBjhE4Q)
and the transcript of that talk supplied for this implementation.

The talk describes a scanner with ten deterministic checks and a 0–100 score,
but the public talk and supplied transcript do not disclose enough detail to
reproduce the checks, weights, or thresholds faithfully. This pack therefore
adapts the public review-debt concepts into an evidence-backed review practice;
it does not reproduce or claim compatibility with the undisclosed scanner.

## Using the skill in the harness

Reference the skill from a workflow manifest when review-debt analysis is
appropriate:

```yaml
skills:
  - uses: skillpacks/review-debt/review-debt-code-review
```

This pack does not attach itself to any workflow by default. The orchestrator
passes attached skill paths to the producer subagent, which reads the skill
before starting its work.
