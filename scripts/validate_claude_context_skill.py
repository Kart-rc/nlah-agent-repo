#!/usr/bin/env python3
"""Validate the distributable Claude context skill using only the stdlib."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY / ".claude/skills/bootstrap-claude-context"
PROJECT_ASSETS = SKILL_ROOT / "assets/project"
SKILLS = (
    SKILL_ROOT / "SKILL.md",
    PROJECT_ASSETS / ".claude/skills/start-codebase/SKILL.md",
    PROJECT_ASSETS / ".claude/skills/finish-session/SKILL.md",
    PROJECT_ASSETS / ".claude/skills/review-learnings/SKILL.md",
)
ROOT_TEMPLATE = PROJECT_ASSETS / "CLAUDE.md"
SETTINGS_FRAGMENT = PROJECT_ASSETS / ".claude/settings.fragment.json"
HOOKS = {
    "SessionStart": PROJECT_ASSETS / ".claude/hooks/session-start.py",
    "SessionEnd": PROJECT_ASSETS / ".claude/hooks/session-end.py",
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".yaml", ".yml"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_MACHINE_ABSOLUTE_PATH = re.compile(
    r"(?:/root(?:/|$)|/tmp(?:/|$)|/private/tmp(?:/|$)|/opt(?:/|$)|"
    r"/Volumes(?:/|$)|/Users/[^/\s]+/|/home/[^/\s]+/|"
    r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+[\\/])"
)
PLACEHOLDER_MARKER = re.compile(
    r"(?i)(?:^\s*(?:[-*+]\s+)?(?:TODO|FIXME|TBD)\s*:|"
    r"\bINSERT[_ -]+HERE\b|\bREPLACE[_ -]+ME\b|placeholder text)"
)


def relative(path: Path) -> str:
    try:
        return path.relative_to(REPOSITORY).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, violations: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        violations.append(f"{relative(path)}: required file is missing")
    except (OSError, UnicodeError) as error:
        violations.append(f"{relative(path)}: cannot read file: {error}")
    return None


def parse_frontmatter(path: Path, violations: list[str]) -> dict[str, str] | None:
    text = read_text(path, violations)
    if text is None:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        violations.append(f"{relative(path)}: missing opening frontmatter delimiter")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        violations.append(f"{relative(path)}: missing closing frontmatter delimiter")
        return None

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if ":" not in line:
            violations.append(
                f"{relative(path)}:{line_number}: invalid frontmatter field"
            )
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not key or key in fields:
            violations.append(
                f"{relative(path)}:{line_number}: empty or duplicate frontmatter key"
            )
            continue
        fields[key] = value.strip().strip('"\'')
    return fields


def validate_skills(violations: list[str]) -> None:
    seen_names: set[str] = set()
    for path in SKILLS:
        fields = parse_frontmatter(path, violations)
        if fields is None:
            continue
        keys = set(fields)
        if keys != {"name", "description"}:
            violations.append(
                f"{relative(path)}: frontmatter must contain name and description only; "
                f"found {', '.join(sorted(keys)) or 'no fields'}"
            )
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not NAME_PATTERN.fullmatch(name):
            violations.append(
                f"{relative(path)}: name must be lower-case kebab-case, got {name!r}"
            )
        elif name in seen_names:
            violations.append(f"{relative(path)}: duplicate skill name {name!r}")
        seen_names.add(name)
        if not description:
            violations.append(f"{relative(path)}: description must not be empty")


def validate_root_template(violations: list[str]) -> None:
    text = read_text(ROOT_TEMPLATE, violations)
    if text is not None and len(text.splitlines()) >= 200:
        violations.append(
            f"{relative(ROOT_TEMPLATE)}: root template must be under 200 lines; "
            f"found {len(text.splitlines())}"
        )


def validate_settings(violations: list[str]) -> None:
    text = read_text(SETTINGS_FRAGMENT, violations)
    if text is None:
        return
    try:
        settings = json.loads(text)
    except json.JSONDecodeError as error:
        violations.append(f"{relative(SETTINGS_FRAGMENT)}: invalid JSON: {error}")
        return
    if not isinstance(settings, dict) or set(settings) != {"hooks"}:
        violations.append(
            f"{relative(SETTINGS_FRAGMENT)}: fragment must contain only a hooks object"
        )
        return
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        violations.append(f"{relative(SETTINGS_FRAGMENT)}: hooks must be an object")
        return
    expected_events = set(HOOKS)
    if set(hooks) != expected_events:
        violations.append(
            f"{relative(SETTINGS_FRAGMENT)}: hooks must contain exactly "
            f"{', '.join(sorted(expected_events))}"
        )
    for event, hook_path in HOOKS.items():
        entries = hooks.get(event)
        if not isinstance(entries, list) or not entries:
            violations.append(
                f"{relative(SETTINGS_FRAGMENT)}: missing non-empty {event} lifecycle entries"
            )
            continue
        expected_command = (
            f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{hook_path.name}"'
        )
        for entry_index, entry in enumerate(entries):
            location = f"{event}[{entry_index}]"
            if not isinstance(entry, dict):
                violations.append(
                    f"{relative(SETTINGS_FRAGMENT)}: {location} must be an object"
                )
                continue
            allowed_entry_keys = {"matcher", "hooks"}
            if not set(entry).issubset(allowed_entry_keys):
                violations.append(
                    f"{relative(SETTINGS_FRAGMENT)}: {location} has invalid keys"
                )
            if "matcher" in entry and not isinstance(entry["matcher"], str):
                violations.append(
                    f"{relative(SETTINGS_FRAGMENT)}: {location}.matcher must be a string"
                )
            inner_hooks = entry.get("hooks")
            if not isinstance(inner_hooks, list) or not inner_hooks:
                violations.append(
                    f"{relative(SETTINGS_FRAGMENT)}: {location}.hooks must be a non-empty list"
                )
                continue
            for hook_index, hook in enumerate(inner_hooks):
                hook_location = f"{location}.hooks[{hook_index}]"
                if not isinstance(hook, dict):
                    violations.append(
                        f"{relative(SETTINGS_FRAGMENT)}: {hook_location} must be an object"
                    )
                    continue
                if set(hook) != {"type", "command"}:
                    violations.append(
                        f"{relative(SETTINGS_FRAGMENT)}: {hook_location} must contain "
                        "type and command only"
                    )
                    continue
                if hook.get("type") != "command":
                    violations.append(
                        f"{relative(SETTINGS_FRAGMENT)}: {hook_location}.type must be command"
                    )
                if hook.get("command") != expected_command:
                    violations.append(
                        f"{relative(SETTINGS_FRAGMENT)}: {hook_location}.command must be "
                        f"{expected_command!r}"
                    )


def validate_hooks(violations: list[str]) -> None:
    for event, path in HOOKS.items():
        text = read_text(path, violations)
        if text is None:
            continue
        try:
            compile(text, str(path), "exec")
        except SyntaxError as error:
            violations.append(
                f"{relative(path)}:{error.lineno or 0}: invalid Python syntax: {error.msg}"
            )


def require_language(
    path: Path,
    requirements: dict[str, tuple[str, ...]],
    violations: list[str],
) -> None:
    text = read_text(path, violations)
    if text is None:
        return
    folded = " ".join(text.casefold().split())
    for label, alternatives in requirements.items():
        if not any(
            " ".join(alternative.casefold().split()) in folded
            for alternative in alternatives
        ):
            violations.append(f"{relative(path)}: missing required {label} language")


def validate_workflow_language(violations: list[str]) -> None:
    learning = SKILL_ROOT / "references/learning-admission.md"
    start = SKILLS[1]
    finish = SKILLS[2]
    review = SKILLS[3]

    require_language(
        learning,
        {
            "evidence": ("## Evidence",),
            "expected-benefit": ("Expected benefit:",),
            "approval": ("explicit developer approval",),
            "collision-safe artifact": (
                "change `short-name` on collision",
                "choose an unused",
            ),
            "atomic artifact": ("atomically rename", "atomic rename"),
            "non-overwrite": ("never replace an existing artifact", "never overwrite"),
        },
        violations,
    )
    require_language(
        finish,
        {
            "direct-edit prohibition": ("never edit `claude.md`",),
            "pending proposal lifecycle": ("learnings/pending", "pending/"),
            "evidence": ("evidence citations", "observable evidence"),
            "expected-benefit": ("expected benefit",),
            "explicit approval": ("explicit developer approval",),
            "collision-safe artifact": ("if the name exists", "unused"),
            "atomic artifact": ("atomic rename",),
            "non-overwrite": ("never overwrite",),
        },
        violations,
    )
    require_language(
        start,
        {
            "receipt lifecycle": ("receipts/processing",),
            "processed receipt lifecycle": ("receipts/processed",),
            "discarded receipt lifecycle": ("receipts/discarded",),
            "trusted transcript root": ("trusted root",),
            "independently established transcript root": (
                "establish the transcript root independently",
                "transcript root independently",
            ),
            "collision-safe artifact": ("choose an unused",),
            "atomic artifact": ("atomic rename", "temporary file plus atomic"),
            "non-overwrite": ("never overwrite",),
        },
        violations,
    )
    require_language(
        review,
        {
            "approval gate": ("only `apply` authorizes",),
            "expected-benefit": ("expected benefit",),
            "accepted lifecycle": ("learnings/accepted",),
            "rejected lifecycle": ("learnings/rejected",),
            "deferred lifecycle": ("learnings/deferred",),
            "collision-safe artifact": ("choose an unused",),
            "atomic artifact": ("atomic rename",),
            "non-overwrite": ("never overwrite",),
        },
        violations,
    )


def contains_source_machine_absolute_path(text: str) -> bool:
    return SOURCE_MACHINE_ABSOLUTE_PATH.search(text) is not None


def contains_placeholder_marker(text: str) -> bool:
    return PLACEHOLDER_MARKER.search(text) is not None


def validate_no_source_debris(violations: list[str]) -> int:
    files = sorted(
        path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and path.suffix.casefold() in TEXT_SUFFIXES
    )
    for path in files:
        text = read_text(path, violations)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if contains_placeholder_marker(line):
                violations.append(
                    f"{relative(path)}:{line_number}: placeholder marker is not allowed"
                )
            if contains_source_machine_absolute_path(line):
                violations.append(
                    f"{relative(path)}:{line_number}: source-machine absolute path is not allowed"
                )
    return len(files)


def main() -> int:
    violations: list[str] = []
    validate_skills(violations)
    validate_root_template(violations)
    validate_settings(violations)
    validate_hooks(violations)
    validate_workflow_language(violations)
    artifact_count = validate_no_source_debris(violations)

    if violations:
        for violation in violations:
            print(f"VIOLATION: {violation}")
        print(f"Validation failed with {len(violations)} violation(s).")
        return 1

    print(f"Validated {artifact_count} Claude context artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
