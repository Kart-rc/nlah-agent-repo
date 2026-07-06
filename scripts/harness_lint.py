#!/usr/bin/env python3
"""Harness lint: validates every contract in the repo.

Checks (schema layer):
  - workflow manifests against workflow-manifest.schema.json
  - stage/validator/adapter frontmatter against their schemas

Checks (cross-reference layer, what JSON Schema can't express):
  - every `uses` ref (stages/, validators/, knowledge/, skillpacks/) exists on disk
  - producer and validator agent personas exist in .claude/agents/
  - a stage's producer persona never appears among its validators' agents
  - completeness-check is the FIRST validator on every manifest stage
  - `needs` graph is acyclic; stage ids unique; needs refer to declared stages
  - input bindings reference `workflow:` inputs that exist, or `<stage>:<output>`
    where <stage> is in the transitive needs and <output> is declared by it
  - manifest outputs bind to declared stage outputs
  - stage.md bodies contain all required section headings
  - risk-policy.yaml refs (validators, gate checklists, stage selectors) exist

Exit code 0 = clean; 1 = findings (printed as file: message).

Dependencies: pyyaml, jsonschema  (pip install pyyaml jsonschema)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover
    print("ERROR: jsonschema not installed. Run: pip install pyyaml jsonschema")
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
HARNESS = REPO / "harness"
AGENTS_DIR = REPO / ".claude" / "agents"

REQUIRED_STAGE_SECTIONS = [
    "Purpose",
    "Procedure",
    "Output format constraints",
    "Knowledge consumption",
    "Boundaries",
    "Self-check before submitting",
    "Summary requirement",
]
REQUIRED_VALIDATOR_SECTIONS = ["Mission", "Method", "Verdict format", "Independence rules"]
REQUIRED_ADAPTER_SECTIONS = [
    "What this source knows",
    "How to query",
    "When to consult",
    "Citation rule",
    "On failure",
]

errors: list[str] = []


def err(path: Path | str, msg: str) -> None:
    rel = Path(path).relative_to(REPO) if str(path).startswith(str(REPO)) else path
    errors.append(f"{rel}: {msg}")


def load_schema(name: str) -> dict:
    return json.loads((HARNESS / "schema" / name).read_text())


def split_frontmatter(path: Path) -> tuple[dict | None, str]:
    """Return (frontmatter dict, body) for a `---` fenced markdown doc."""
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        err(path, "missing YAML frontmatter (--- fenced)")
        return None, text
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        err(path, f"frontmatter is not valid YAML: {e}")
        return None, m.group(2)
    return fm, m.group(2)


def validate_against(schema: dict, instance: dict, path: Path, label: str) -> bool:
    validator = jsonschema.Draft202012Validator(schema)
    ok = True
    for e in validator.iter_errors(instance):
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        err(path, f"{label} schema violation at {loc}: {e.message}")
        ok = False
    return ok


def check_sections(body: str, required: list[str], path: Path) -> None:
    headings = {h.strip() for h in re.findall(r"^#{1,3}\s+(.+)$", body, re.MULTILINE)}
    for section in required:
        if section not in headings:
            err(path, f"missing required section heading: '{section}'")


def check_uses_exists(uses: str, source: Path) -> None:
    """A `uses` ref resolves relative to harness/. Skillpack refs point at a dir containing SKILL.md."""
    target = HARNESS / uses
    if uses.startswith("skillpacks/"):
        if not (target / "SKILL.md").is_file():
            err(source, f"uses '{uses}' → missing {target.relative_to(REPO)}/SKILL.md")
    elif uses.startswith("stages/"):
        if not (target / "stage.md").is_file():
            err(source, f"uses '{uses}' → missing {target.relative_to(REPO)}/stage.md")
    elif uses.startswith("validators/"):
        if not (target / "validator.md").is_file():
            err(source, f"uses '{uses}' → missing {target.relative_to(REPO)}/validator.md")
    elif uses.startswith("knowledge/"):
        if not (target / "adapter.md").is_file():
            err(source, f"uses '{uses}' → missing {target.relative_to(REPO)}/adapter.md")
    else:
        err(source, f"uses '{uses}' has unknown prefix")


def agent_exists(name: str) -> bool:
    return (AGENTS_DIR / f"{name}.md").is_file()


# ---------------------------------------------------------------- libraries

def lint_stages() -> dict[str, dict]:
    """Return stage-id → frontmatter for every stage in the library."""
    schema = load_schema("stage-contract.schema.json")
    stages: dict[str, dict] = {}
    for doc in sorted(HARNESS.glob("stages/*/stage.md")):
        fm, body = split_frontmatter(doc)
        if fm is None:
            continue
        if not validate_against(schema, fm, doc, "stage-contract"):
            continue
        if fm["id"] != doc.parent.name:
            err(doc, f"frontmatter id '{fm['id']}' != directory name '{doc.parent.name}'")
        if not agent_exists(fm["producer"]):
            err(doc, f"producer persona '{fm['producer']}' not found in .claude/agents/")
        for v in fm.get("default_validators", []):
            check_uses_exists(v["uses"], doc)
        for s in fm.get("skill_refs", []):
            check_uses_exists(s, doc)
        check_sections(body, REQUIRED_STAGE_SECTIONS, doc)
        stages[fm["id"]] = fm
    return stages


def lint_validators() -> dict[str, dict]:
    schema = load_schema("validator-contract.schema.json")
    validators: dict[str, dict] = {}
    for doc in sorted(HARNESS.glob("validators/*/validator.md")):
        fm, body = split_frontmatter(doc)
        if fm is None:
            continue
        if not validate_against(schema, fm, doc, "validator-contract"):
            continue
        if fm["id"] != doc.parent.name:
            err(doc, f"frontmatter id '{fm['id']}' != directory name '{doc.parent.name}'")
        if not agent_exists(fm["agent"]):
            err(doc, f"validator persona '{fm['agent']}' not found in .claude/agents/")
        check_sections(body, REQUIRED_VALIDATOR_SECTIONS, doc)
        validators[fm["id"]] = fm
    return validators


def lint_adapters() -> dict[str, dict]:
    schema = load_schema("adapter-contract.schema.json")
    adapters: dict[str, dict] = {}
    for doc in sorted(HARNESS.glob("knowledge/*/adapter.md")):
        fm, body = split_frontmatter(doc)
        if fm is None:
            continue
        if not validate_against(schema, fm, doc, "adapter-contract"):
            continue
        if fm["id"] != doc.parent.name:
            err(doc, f"frontmatter id '{fm['id']}' != directory name '{doc.parent.name}'")
        check_sections(body, REQUIRED_ADAPTER_SECTIONS, doc)
        adapters[fm["id"]] = fm
    return adapters


# ---------------------------------------------------------------- manifests

def transitive_needs(stage_id: str, by_id: dict[str, dict]) -> set[str]:
    seen: set[str] = set()
    frontier = list(by_id[stage_id].get("needs", []))
    while frontier:
        n = frontier.pop()
        if n in seen or n not in by_id:
            continue
        seen.add(n)
        frontier.extend(by_id[n].get("needs", []))
    return seen


def lint_manifest(path: Path, stages: dict[str, dict], validators: dict[str, dict]) -> None:
    schema = load_schema("workflow-manifest.schema.json")
    try:
        manifest = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        err(path, f"not valid YAML: {e}")
        return
    if not validate_against(schema, manifest, path, "workflow-manifest"):
        return

    workflow_inputs = {i["name"] for i in manifest.get("inputs", [])}
    by_id = {s["id"]: s for s in manifest["stages"]}
    if len(by_id) != len(manifest["stages"]):
        err(path, "duplicate stage ids")
        return

    # acyclicity via DFS
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {sid: WHITE for sid in by_id}

    def dfs(sid: str) -> bool:
        color[sid] = GRAY
        for n in by_id[sid].get("needs", []):
            if n not in by_id:
                err(path, f"stage '{sid}' needs unknown stage '{n}'")
                continue
            if color[n] == GRAY:
                err(path, f"needs cycle involving '{sid}' → '{n}'")
                return False
            if color[n] == WHITE and not dfs(n):
                return False
        color[sid] = BLACK
        return True

    for sid in by_id:
        if color[sid] == WHITE and not dfs(sid):
            return

    for entry in manifest.get("knowledge", []):
        check_uses_exists(entry["uses"], path)

    for s in manifest["stages"]:
        sid = s["id"]
        check_uses_exists(s["uses"], path)
        stage_lib_id = s["uses"].split("/", 1)[1]
        contract = stages.get(stage_lib_id)

        # validator attachments
        vlist = s["validators"]
        first = vlist[0]["uses"].split("/", 1)[1] if vlist else None
        if first != "completeness-check":
            err(path, f"stage '{sid}': first validator must be validators/completeness-check (found '{vlist[0]['uses']}')")
        vagents = set()
        for v in vlist:
            check_uses_exists(v["uses"], path)
            vc = validators.get(v["uses"].split("/", 1)[1])
            if vc:
                vagents.add(vc["agent"])
        if contract and contract["producer"] in vagents:
            err(path, f"stage '{sid}': producer persona '{contract['producer']}' also validates its own output")

        for entry in s.get("knowledge", []):
            check_uses_exists(entry["uses"], path)
        for entry in s.get("skills", []):
            check_uses_exists(entry["uses"], path)

        # bindings
        allowed_sources = transitive_needs(sid, by_id)
        declared_inputs = {i["name"] for i in contract["inputs"]} if contract else None
        required_inputs = {i["name"] for i in contract["inputs"] if i["required"]} if contract else set()
        for name, binding in s.get("inputs", {}).items():
            if declared_inputs is not None and name not in declared_inputs:
                err(path, f"stage '{sid}': binds input '{name}' not declared by {s['uses']}")
            src, out = binding.split(":", 1)
            if src == "workflow":
                if out not in workflow_inputs:
                    err(path, f"stage '{sid}': input '{name}' binds unknown workflow input '{out}'")
            else:
                if src not in allowed_sources:
                    err(path, f"stage '{sid}': input '{name}' binds stage '{src}' which is not in its transitive needs")
                elif src in by_id:
                    src_contract = stages.get(by_id[src]["uses"].split("/", 1)[1])
                    if src_contract and out not in {o["name"] for o in src_contract["outputs"]}:
                        err(path, f"stage '{sid}': input '{name}' binds '{src}:{out}' but '{src}' declares no output '{out}'")
            required_inputs.discard(name)
        for missing in sorted(required_inputs):
            err(path, f"stage '{sid}': required input '{missing}' of {s['uses']} is not bound")

    for out in manifest["outputs"]:
        src, name = out["from"].split(":", 1)
        if src == "workflow":
            err(path, f"output '{out['name']}' cannot bind workflow inputs")
        elif src not in by_id:
            err(path, f"output '{out['name']}' binds unknown stage '{src}'")
        else:
            src_contract = stages.get(by_id[src]["uses"].split("/", 1)[1])
            if src_contract and name not in {o["name"] for o in src_contract["outputs"]}:
                err(path, f"output '{out['name']}' binds '{src}:{name}' but '{src}' declares no output '{name}'")


# ---------------------------------------------------------------- policies

def lint_risk_policy(stages_in_manifests: set[str]) -> None:
    path = HARNESS / "policies" / "risk-policy.yaml"
    if not path.is_file():
        err(path, "missing risk-policy.yaml")
        return
    try:
        policy = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        err(path, f"not valid YAML: {e}")
        return
    levels = policy.get("risk_levels", {})
    for expected in ("low", "medium", "high", "critical"):
        if expected not in levels:
            err(path, f"missing risk level '{expected}'")
    for level, spec in levels.items():
        if not isinstance(spec, dict):
            err(path, f"risk level '{level}' must be a mapping")
            continue
        for v in spec.get("additional_validators", []) or []:
            check_uses_exists(v["uses"], path)
            checklist = (v.get("with") or {}).get("checklist")
            if checklist and not (HARNESS / checklist).is_file():
                err(path, f"risk level '{level}': checklist '{checklist}' not found under harness/")
            at = v.get("at_stage")
            if at and at != "*" and at not in stages_in_manifests:
                err(path, f"risk level '{level}': at_stage '{at}' matches no stage id in any manifest")
        for cp in spec.get("approval_checkpoints", []) or []:
            before = cp.get("before")
            if before and before != "*" and before not in stages_in_manifests:
                err(path, f"risk level '{level}': approval checkpoint before '{before}' matches no stage id in any manifest")


def main() -> int:
    stages = lint_stages()
    validators = lint_validators()
    lint_adapters()

    manifest_stage_ids: set[str] = set()
    manifests = sorted(HARNESS.glob("workflows/*/workflow.yaml"))
    if not manifests:
        err(HARNESS / "workflows", "no workflow manifests found")
    for m in manifests:
        lint_manifest(m, stages, validators)
        try:
            data = yaml.safe_load(m.read_text())
            manifest_stage_ids.update(s["id"] for s in data.get("stages", []))
        except Exception:
            pass

    lint_risk_policy(manifest_stage_ids)

    if errors:
        print(f"harness lint: {len(errors)} finding(s)\n")
        for e in errors:
            print(f"  {e}")
        return 1
    print(f"harness lint: clean ({len(stages)} stages, {len(validators)} validators, {len(manifests)} workflows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
