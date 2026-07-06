# Skill Pack: addyosmani/agent-skills (vendored)

Practice skills vendored from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills),
MIT-licensed (see [LICENSE](LICENSE) in this directory).

- **Upstream commit:** `8c6530305396f341b5da7201cf1f7e390fdb863f`
- **Vendored:** 2026-07-06 (the `skills/` directory + LICENSE, verbatim)
- **Contents:** 24 skills (23 lifecycle + 1 meta), each a `<skill-name>/SKILL.md`

## What this pack is for

These are **practice skills**: engineering discipline documents that a stage's
producer subagent reads before doing its work. They are attached to workflow
stages via the manifest:

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/test-driven-development
```

Attaching, detaching, or swapping a practice skill is a one-line manifest edit.
The orchestrator passes attached skill *paths* to the producer subagent with an
instruction to read them before starting (see `HARNESS.md` → Prompt Templates).

Stage documents suggest defaults in their `skill_refs` frontmatter; the
workflow-composer materializes those into new manifests, where you can freely
override them.

## How to refresh this pack

```bash
git clone --depth 1 https://github.com/addyosmani/agent-skills.git /tmp/agent-skills
cp -r /tmp/agent-skills/skills/. harness/skillpacks/addyosmani/
cp /tmp/agent-skills/LICENSE harness/skillpacks/addyosmani/LICENSE
# then update the upstream commit hash above:
git -C /tmp/agent-skills rev-parse HEAD
```

After refreshing, run `python3 scripts/harness_lint.py` — manifests referencing
removed/renamed skills will fail the lint.

## Adding another pack

Create `harness/skillpacks/<pack-name>/<skill-name>/SKILL.md` and reference it
from manifests as `skillpacks/<pack-name>/<skill-name>`. Include a LICENSE and
an attribution README like this one.
