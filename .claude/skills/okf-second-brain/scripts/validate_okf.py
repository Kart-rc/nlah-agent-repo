#!/usr/bin/env python3
"""Validate an OKF v0.1 bundle (stdlib only).

Usage: python3 validate_okf.py <bundle-path>

Exit 0: conformant (warnings allowed). Exit 1: findings. Exit 2: bad usage.

Checks (OKF v0.1, https://github.com/GoogleCloudPlatform/knowledge-catalog
/blob/main/okf/SPEC.md):
- every non-reserved .md has parseable YAML frontmatter with a non-empty
  `type`
- non-root index.md files carry no frontmatter; the root index.md may carry
  frontmatter containing only `okf_version`
- index.md bullets follow `* [Title](url) - description`; entries pointing
  at missing files are WARNINGS (the spec tolerates broken links)
- log.md `##` headings are valid ISO 8601 dates (YYYY-MM-DD) and entries
  are bullets
"""

import re
import sys
from pathlib import Path

RESERVED = {"index.md", "log.md"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

INDEX_BULLET_RE = re.compile(r"^[*-] \[[^\]]+\]\([^)]+\)\s+-\s+\S.*$")
LOG_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(lines):
    """Return (dict-or-None, error-or-None, body_start_index).

    A tolerant `key: value` parser — OKF frontmatter is flat enough that a
    PyYAML dependency isn't warranted. Nested/list values are kept as raw
    strings; only structural breakage is an error.
    """
    if not lines or lines[0].strip() != "---":
        return None, None, 0
    fm = {}
    for i in range(1, len(lines)):
        stripped = lines[i].strip()
        if stripped == "---":
            return fm, None, i + 1
        if not stripped or stripped.startswith("#"):
            continue
        if lines[i].startswith((" ", "\t")) or stripped.startswith("- "):
            continue  # continuation of a nested/list value
        if ":" not in stripped:
            return None, f"line {i + 1}: not `key: value`: {stripped!r}", 0
        key, _, value = stripped.partition(":")
        fm[key.strip()] = value.strip().strip("\"'")
    return None, "unterminated frontmatter block (no closing ---)", 0


def check_concept(path, lines, findings):
    fm, err, _ = parse_frontmatter(lines)
    if err:
        findings.append((path, f"frontmatter does not parse: {err}"))
        return
    if fm is None:
        findings.append((path, "missing YAML frontmatter (required `type` field)"))
        return
    if not fm.get("type"):
        findings.append((path, "frontmatter `type` is missing or empty"))


def check_index(path, lines, is_root, bundle, findings, warnings):
    fm, err, body_start = parse_frontmatter(lines)
    if err:
        findings.append((path, f"frontmatter does not parse: {err}"))
        return
    if fm is not None:
        if not is_root:
            findings.append((path, "index.md must not contain frontmatter (only the bundle root may)"))
        elif set(fm) != {"okf_version"}:
            findings.append((path, "root index.md frontmatter may contain only `okf_version`"))
    for n, line in enumerate(lines[body_start:], start=body_start + 1):
        stripped = line.strip()
        if not stripped.startswith(("* ", "- ")):
            continue
        if not INDEX_BULLET_RE.match(stripped):
            findings.append((path, f"line {n}: index bullet must be `* [Title](url) - description`"))
            continue
        target = LINK_RE.search(stripped).group(1)
        if "://" in target:
            continue
        resolved = (bundle / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
        if not resolved.exists():
            warnings.append((path, f"line {n}: entry points at missing file: {target}"))


def check_log(path, lines, findings):
    _, err, body_start = parse_frontmatter(lines)
    if err or body_start:
        findings.append((path, "log.md must not contain frontmatter"))
        return
    for n, line in enumerate(lines, start=1):
        if line[:1] in (" ", "\t"):
            continue  # wrapped continuation of a bullet
        stripped = line.strip()
        if stripped.startswith("## "):
            if not LOG_DATE_RE.match(stripped[3:].strip()):
                findings.append((path, f"line {n}: log heading must be an ISO date `## YYYY-MM-DD`"))
        elif stripped and not stripped.startswith(("#", "* ", "- ")):
            findings.append((path, f"line {n}: log entries must be bullets under a date heading"))


def validate(bundle):
    findings, warnings = [], []
    root_index = bundle / "index.md"
    if not root_index.is_file():
        findings.append((bundle, "bundle root has no index.md"))
    for path in sorted(bundle.rglob("*.md")):
        if SKIP_DIRS & set(p.name for p in path.parents):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if path.name == "index.md":
            check_index(path, lines, path == root_index, bundle, findings, warnings)
        elif path.name == "log.md":
            check_log(path, lines, findings)
        else:
            check_concept(path, lines, findings)
    return findings, warnings


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2])
        return 2
    bundle = Path(sys.argv[1])
    if not bundle.is_dir():
        print(f"not a directory: {bundle}")
        return 2
    findings, warnings = validate(bundle)
    for path, msg in warnings:
        print(f"WARN  {path}: {msg}")
    for path, msg in findings:
        print(f"FAIL  {path}: {msg}")
    if findings:
        print(f"\n{len(findings)} finding(s), {len(warnings)} warning(s) — bundle is NOT conformant")
        return 1
    print(f"OK — OKF v0.1 conformant ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
