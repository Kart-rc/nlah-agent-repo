#!/usr/bin/env python3
"""Install or validate the stable Claude context project scaffold."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = SKILL_ROOT / "assets" / "project"
SETTINGS_FRAGMENT = ASSET_ROOT / ".claude" / "settings.fragment.json"
SETTINGS_PATH = Path(".claude/settings.json")
STABLE_ASSETS = (
    Path("CLAUDE.md"),
    Path(".claude/context/codebase-map.md"),
    Path(".claude/context/learnings/.gitignore"),
    Path(".claude/hooks/session-start.py"),
    Path(".claude/hooks/session-end.py"),
    Path(".claude/skills/start-codebase/SKILL.md"),
    Path(".claude/skills/finish-session/SKILL.md"),
    Path(".claude/skills/review-learnings/SKILL.md"),
)
MANAGED_HOOK_ASSETS = (
    Path(".claude/hooks/session-start.py"),
    Path(".claude/hooks/session-end.py"),
)


def new_summary() -> dict[str, list[str]]:
    return {"create": [], "merge": [], "preserve": [], "warning": []}


def relative_name(path: Path) -> str:
    return path.as_posix()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_target(raw_target: Path, summary: dict[str, list[str]]) -> Path | None:
    if not raw_target.exists():
        summary["warning"].append(f"target does not exist: {raw_target}")
        return None
    if raw_target.is_symlink():
        summary["warning"].append(f"target must not be a symbolic link: {raw_target}")
        return None
    if not raw_target.is_dir():
        summary["warning"].append(f"target is not a directory: {raw_target}")
        return None

    target = raw_target.resolve()
    if target == Path(target.anchor):
        summary["warning"].append(f"refusing unsafe filesystem root target: {target}")
        return None

    for relative_path in (*STABLE_ASSETS, SETTINGS_PATH):
        destination = target / relative_path
        if destination.is_symlink():
            summary["warning"].append(
                f"destination must not be a symbolic link: {relative_name(relative_path)}"
            )
            continue
        if not is_within(destination.resolve(strict=False), target):
            summary["warning"].append(
                f"destination escapes target through a symbolic link: {relative_name(relative_path)}"
            )
    if summary["warning"]:
        return None
    return target


def preflight_destinations(
    target: Path, summary: dict[str, list[str]]
) -> bool:
    for relative_path in (*STABLE_ASSETS, SETTINGS_PATH):
        destination = target / relative_path
        name = relative_name(relative_path)

        current_parent = target
        for part in relative_path.parts[:-1]:
            current_parent /= part
            if current_parent.is_symlink():
                summary["warning"].append(
                    f"destination parent must not be a symbolic link: {name}"
                )
                break
            if current_parent.exists() and not current_parent.is_dir():
                summary["warning"].append(
                    f"destination parent is not a directory: {name}"
                )
                break

        if destination.is_symlink():
            summary["warning"].append(
                f"destination must not be a symbolic link: {name}"
            )
        elif destination.exists() and not destination.is_file():
            summary["warning"].append(
                f"destination is not a regular file: {name}"
            )
    return not summary["warning"]


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as input_file:
        return json.load(input_file)


def load_settings(
    settings_path: Path, summary: dict[str, list[str]]
) -> dict[str, Any] | None:
    if not settings_path.exists():
        return {}
    if not settings_path.is_file():
        summary["warning"].append(
            f"settings path is not a file: {relative_name(SETTINGS_PATH)}"
        )
        return None
    try:
        settings = read_json(settings_path)
    except (OSError, json.JSONDecodeError) as error:
        summary["warning"].append(f"cannot read existing settings: {error}")
        return None
    if not isinstance(settings, dict):
        summary["warning"].append("existing settings must contain a JSON object")
        return None
    return settings


def desired_hooks() -> dict[str, list[dict[str, Any]]]:
    fragment = read_json(SETTINGS_FRAGMENT)
    hooks = fragment.get("hooks") if isinstance(fragment, dict) else None
    if not isinstance(hooks, dict):
        raise ValueError("settings fragment must contain a hooks object")
    return hooks


def differing_managed_hooks(target: Path) -> set[Path]:
    differing: set[Path] = set()
    for relative_path in MANAGED_HOOK_ASSETS:
        destination = target / relative_path
        if (
            destination.exists()
            and destination.read_bytes() != (ASSET_ROOT / relative_path).read_bytes()
        ):
            differing.add(relative_path)
    return differing


def merge_settings(
    settings: dict[str, Any], hooks_to_add: dict[str, list[dict[str, Any]]]
) -> tuple[dict[str, Any] | None, bool, str | None]:
    merged = dict(settings)
    existing_hooks = merged.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        return None, False, "existing settings hooks must contain a JSON object"
    existing_hooks = dict(existing_hooks)

    changed = "hooks" not in merged
    for event, entries in hooks_to_add.items():
        current_entries = existing_hooks.get(event, [])
        if not isinstance(current_entries, list):
            return None, False, f"existing {event} hooks must contain a JSON array"
        current_entries = list(current_entries)
        for entry in entries:
            if entry not in current_entries:
                current_entries.append(entry)
                changed = True
        existing_hooks[event] = current_entries
    merged["hooks"] = existing_hooks
    return merged, changed, None


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, delete=False
        ) as temporary_file:
            temporary_name = temporary_file.name
            with source.open("rb") as source_file:
                shutil.copyfileobj(source_file, temporary_file)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        shutil.copymode(source, temporary_name)
        Path(temporary_name).replace(destination)
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def atomic_write_json(destination: Path, value: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination_mode = (
        stat.S_IMODE(destination.stat().st_mode) if destination.exists() else 0o644
    )
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent, delete=False
        ) as temporary_file:
            temporary_name = temporary_file.name
            json.dump(value, temporary_file, indent=2)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.chmod(temporary_name, destination_mode)
        Path(temporary_name).replace(destination)
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def plan_assets(target: Path, summary: dict[str, list[str]], apply: bool) -> None:
    for relative_path in STABLE_ASSETS:
        source = ASSET_ROOT / relative_path
        destination = target / relative_path
        name = relative_name(relative_path)
        if destination.exists() or destination.is_symlink():
            summary["preserve"].append(name)
            continue
        summary["create"].append(name)
        if apply:
            atomic_copy(source, destination)


def install(target: Path, apply: bool, summary: dict[str, list[str]]) -> bool:
    differing_hooks = differing_managed_hooks(target)
    if differing_hooks:
        for relative_path in sorted(differing_hooks):
            summary["warning"].append(
                "different existing managed hook requires explicit reconciliation: "
                f"{relative_name(relative_path)}"
            )
        return False

    settings_path = target / SETTINGS_PATH
    settings_existed = settings_path.exists()
    settings = load_settings(settings_path, summary)
    if settings is None:
        return False

    try:
        hooks_to_add = desired_hooks()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        summary["warning"].append(f"cannot read settings fragment: {error}")
        return False
    merged, changed, merge_error = merge_settings(settings, hooks_to_add)
    if merge_error:
        summary["warning"].append(merge_error)
        return False

    plan_assets(target, summary, apply)
    settings_name = relative_name(SETTINGS_PATH)
    if not settings_existed:
        summary["create"].append(settings_name)
    elif changed:
        summary["merge"].append(settings_name)
    else:
        summary["preserve"].append(settings_name)

    if apply and (not settings_existed or changed):
        atomic_write_json(settings_path, merged or {})
    return True


def validate_installation(target: Path, summary: dict[str, list[str]]) -> bool:
    valid = True
    differing_hooks = differing_managed_hooks(target)
    for relative_path in STABLE_ASSETS:
        destination = target / relative_path
        name = relative_name(relative_path)
        if relative_path in differing_hooks:
            summary["warning"].append(
                f"installed managed hook differs from managed asset: {name}"
            )
            valid = False
        elif destination.is_file():
            summary["preserve"].append(name)
        else:
            summary["warning"].append(f"missing installed file: {name}")
            valid = False

    settings_path = target / SETTINGS_PATH
    settings = load_settings(settings_path, summary)
    if settings is None or not settings_path.exists():
        if not settings_path.exists():
            summary["warning"].append(
                f"missing installed file: {relative_name(SETTINGS_PATH)}"
            )
        return False

    try:
        hooks_to_add = desired_hooks()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        summary["warning"].append(f"cannot read settings fragment: {error}")
        return False
    merged, changed, merge_error = merge_settings(settings, hooks_to_add)
    if merge_error:
        summary["warning"].append(merge_error)
        return False
    if changed or merged != settings:
        summary["warning"].append("settings are missing required lifecycle hooks")
        valid = False
    else:
        summary["preserve"].append(relative_name(SETTINGS_PATH))
    return valid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or validate the Claude context project scaffold."
    )
    parser.add_argument("--target", required=True, type=Path)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--validate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = new_summary()
    target = validate_target(args.target, summary)
    if target is None:
        print(json.dumps(summary, sort_keys=True))
        return 1
    if not preflight_destinations(target, summary):
        print(json.dumps(summary, sort_keys=True))
        return 1

    try:
        if args.validate:
            success = validate_installation(target, summary)
        else:
            success = install(target, args.apply, summary)
    except OSError as error:
        summary["warning"].append(str(error))
        success = False

    print(json.dumps(summary, sort_keys=True))
    return 0 if success and not summary["warning"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
