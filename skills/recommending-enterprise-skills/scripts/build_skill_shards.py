#!/usr/bin/env python3
"""Build deterministic, bounded shards for a directory of SKILL.md files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
DEFAULT_MAX_FILES = 20
DEFAULT_MAX_BYTES = 100 * 1024
ALLOWED_STATUSES = {"recommended", "needs_clarification", "no_match", "error"}
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
BLOCK_SCALAR_PATTERN = re.compile(r"^[>|][+-]?\d*$")


def is_within(path: Path, root: Path) -> bool:
    """Return whether a resolved path is root or one of its descendants."""
    return path == root or root in path.parents


def scalar_value(raw: str) -> str:
    """Decode the small YAML scalar subset used by skill metadata."""
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid quoted scalar: {exc.msg}") from exc
        if not isinstance(decoded, str):
            raise ValueError("quoted scalar must decode to text")
        return decoded
    return value


def parse_frontmatter_fields(lines: list[str]) -> dict[str, str]:
    """Parse top-level name and description fields from bounded frontmatter."""
    fields: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line[0].isspace() or ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if key not in {"name", "description"}:
            index += 1
            continue

        if BLOCK_SCALAR_PATTERN.fullmatch(raw_value):
            block_lines: list[str] = []
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[0].isspace():
                    break
                block_lines.append(candidate)
                index += 1
            dedented = textwrap.dedent("\n".join(block_lines)).strip()
            if raw_value.startswith(">"):
                fields[key] = " ".join(
                    part.strip() for part in dedented.splitlines() if part.strip()
                )
            else:
                fields[key] = dedented
            continue

        fields[key] = scalar_value(raw_value)
        index += 1
    return fields


def extract_frontmatter(text: str) -> tuple[str | None, dict[str, str] | None, str | None]:
    """Extract only the opening fenced frontmatter, never YAML-like body text."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None, "missing_frontmatter"

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        return None, None, "unterminated_frontmatter"

    frontmatter_lines = lines[1:closing_index]
    frontmatter = "\n".join(frontmatter_lines)
    try:
        fields = parse_frontmatter_fields(frontmatter_lines)
    except ValueError:
        return frontmatter, None, "malformed_frontmatter"

    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if (
        not name
        or not NAME_PATTERN.fullmatch(name)
        or "--" in name
        or not description
    ):
        return frontmatter, None, "malformed_frontmatter"
    return frontmatter, {"name": name, "description": description}, None


def read_skill(
    path: Path, root: Path
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Read and validate one candidate without interpreting its body."""
    try:
        canonical = path.resolve(strict=True)
    except OSError as exc:
        return None, {"path": str(path), "reason": "unreadable", "detail": str(exc)}

    if not is_within(canonical, root):
        return None, {
            "path": str(path),
            "reason": "symlink_escape",
            "detail": str(canonical),
        }

    try:
        text = path.read_text(encoding="utf-8")
        size = canonical.stat().st_size
    except (OSError, UnicodeError) as exc:
        return None, {"path": str(path), "reason": "unreadable", "detail": str(exc)}

    frontmatter, fields, reason = extract_frontmatter(text)
    if reason is not None or fields is None or frontmatter is None:
        return None, {"path": str(path), "reason": reason or "malformed_frontmatter"}

    return (
        {
            "name": fields["name"],
            "description": fields["description"],
            "path": str(canonical),
            "relative_path": canonical.relative_to(root).as_posix(),
            "bytes": size,
            "frontmatter": frontmatter,
        },
        None,
    )


def discover_paths(root: Path) -> tuple[list[Path], list[dict[str, str]]]:
    """Discover exact filenames without following directory symlinks."""
    candidates: list[Path] = []
    warnings: list[dict[str, str]] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for current, directory_names, filenames in os.walk(
        root, followlinks=False, onerror=raise_walk_error
    ):
        current_path = Path(current)
        retained: list[str] = []
        for directory_name in sorted(directory_names):
            directory = current_path / directory_name
            if not directory.is_symlink():
                retained.append(directory_name)
                continue
            try:
                target = directory.resolve(strict=True)
                reason = (
                    "symlink_directory_not_followed"
                    if is_within(target, root)
                    else "symlink_escape"
                )
            except OSError:
                reason = "unreadable"
            warnings.append({"path": str(directory), "reason": reason})
        directory_names[:] = retained

        if "SKILL.md" in filenames:
            candidates.append(current_path / "SKILL.md")

    candidates.sort(
        key=lambda path: (
            path.is_symlink(),
            path.relative_to(root).as_posix(),
        )
    )
    return candidates, warnings


def scan_catalog(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Return valid entries and compact reports for every skipped candidate."""
    candidates, skipped = discover_paths(root)
    entries: list[dict[str, Any]] = []
    seen: set[Path] = set()

    for candidate in candidates:
        try:
            canonical = candidate.resolve(strict=True)
        except OSError as exc:
            skipped.append(
                {"path": str(candidate), "reason": "unreadable", "detail": str(exc)}
            )
            continue
        if canonical in seen:
            skipped.append(
                {"path": str(candidate), "reason": "duplicate_canonical_path"}
            )
            continue

        entry, error = read_skill(candidate, root)
        if error is not None:
            skipped.append(error)
            continue
        assert entry is not None
        seen.add(canonical)
        entries.append(entry)

    entries.sort(key=lambda entry: entry["relative_path"])
    skipped.sort(key=lambda item: (item["path"], item["reason"]))
    return entries, skipped


def make_shards(
    entries: list[dict[str, Any]], max_files: int, max_bytes: int
) -> list[dict[str, Any]]:
    """Partition entries deterministically while respecting both caps."""
    if max_files < 1 or max_bytes < 1:
        raise ValueError("max_files and max_bytes must be positive")

    groups: list[tuple[list[dict[str, Any]], bool]] = []
    current: list[dict[str, Any]] = []
    current_bytes = 0

    def flush() -> None:
        nonlocal current, current_bytes
        if current:
            groups.append((current, False))
            current = []
            current_bytes = 0

    for entry in entries:
        entry_bytes = int(entry["bytes"])
        if entry_bytes > max_bytes:
            flush()
            groups.append(([entry], True))
            continue
        if current and (
            len(current) >= max_files or current_bytes + entry_bytes > max_bytes
        ):
            flush()
        current.append(entry)
        current_bytes += entry_bytes
    flush()

    shards: list[dict[str, Any]] = []
    for index, (group, oversized) in enumerate(groups, start=1):
        shards.append(
            {
                "schema_version": SCHEMA_VERSION,
                "shard_id": f"shard-{index:04d}",
                "entry_count": len(group),
                "total_bytes": sum(int(entry["bytes"]) for entry in group),
                "oversized_singleton": oversized,
                "entries": group,
            }
        )
    return shards


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find_name_collisions(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Report duplicate metadata names while preserving every path/version."""
    paths_by_name: dict[str, list[str]] = {}
    for entry in entries:
        paths_by_name.setdefault(entry["name"], []).append(entry["path"])
    return [
        {"name": name, "paths": sorted(paths)}
        for name, paths in sorted(paths_by_name.items())
        if len(paths) > 1
    ]


def prepare_output(output: Path, root: Path) -> Path:
    resolved = output.resolve(strict=False)
    if is_within(resolved, root):
        raise ValueError("output directory must be outside the skills directory")
    if output.exists():
        if not output.is_dir():
            raise ValueError("output path exists and is not a directory")
        if any(output.iterdir()):
            raise ValueError("output directory must be new or empty")
    else:
        output.mkdir(parents=True)
    return resolved


def build_catalog(
    skills_directory: Path | str,
    output_directory: Path | str,
    *,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> dict[str, Any]:
    """Scan a catalog, write inventory and shard JSON, and return the inventory."""
    root = Path(skills_directory).expanduser().resolve(strict=True)
    if not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
        raise ValueError("skills directory must be a readable directory")
    output = Path(output_directory).expanduser()
    resolved_output = prepare_output(output, root)

    entries, skipped = scan_catalog(root)
    name_collisions = find_name_collisions(entries)
    shards = make_shards(entries, max_files, max_bytes)
    shard_directory = resolved_output / "shards"
    shard_directory.mkdir()
    for shard in shards:
        shard_path = shard_directory / f"{shard['shard_id']}.json"
        shard["shard_path"] = str(shard_path)
        write_json(shard_path, shard)

    inventory = {
        "schema_version": SCHEMA_VERSION,
        "catalog_root": str(root),
        "discovered_count": len(entries) + len(skipped),
        "included_count": len(entries),
        "skipped_count": len(skipped),
        "entries": entries,
        "skipped": skipped,
        "name_collisions": name_collisions,
        "max_files": max_files,
        "max_bytes": max_bytes,
        "shards": shards,
    }
    write_json(resolved_output / "inventory.json", inventory)
    return inventory


def validate_result(
    skills_directory: Path | str, result_path: Path | str
) -> dict[str, Any]:
    """Validate the final status/collection contract and every returned path."""
    root = Path(skills_directory).expanduser().resolve(strict=True)
    payload = json.loads(Path(result_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("result must be a JSON object")

    errors: list[dict[str, str]] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append({"path": "schema_version", "reason": "invalid_schema_version"})

    status = payload.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append({"path": "status", "reason": "invalid_status"})

    catalog = payload.get("catalog")
    supplied_root = catalog.get("root") if isinstance(catalog, dict) else None
    if supplied_root != str(root):
        errors.append({"path": "catalog.root", "reason": "catalog_root_mismatch"})

    checked = 0
    seen: set[Path] = set()
    collection_specs = {
        "recommendations": "required",
        "conditional_skills": "conditional",
        "rejected_alternatives": "excluded",
    }
    collection_sizes: dict[str, int] = {}
    for collection, expected_classification in collection_specs.items():
        items = payload.get(collection, [])
        if not isinstance(items, list):
            errors.append({"path": collection, "reason": "not_a_list"})
            collection_sizes[collection] = 0
            continue
        collection_sizes[collection] = len(items)
        for item in items:
            checked += 1
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                errors.append({"path": collection, "reason": "missing_path"})
                continue
            if item.get("classification") != expected_classification:
                errors.append(
                    {
                        "path": item["path"],
                        "reason": "invalid_classification",
                    }
                )
            raw_path = item["path"]
            try:
                canonical = Path(raw_path).expanduser().resolve(strict=True)
            except OSError:
                errors.append({"path": raw_path, "reason": "path_missing"})
                continue
            if not is_within(canonical, root):
                errors.append({"path": raw_path, "reason": "path_outside_catalog"})
                continue
            if not canonical.is_file() or canonical.name != "SKILL.md":
                errors.append({"path": raw_path, "reason": "not_a_skill_file"})
                continue
            if raw_path != str(canonical):
                errors.append({"path": raw_path, "reason": "path_not_canonical"})
                continue
            if canonical in seen:
                errors.append({"path": raw_path, "reason": "duplicate_recommendation"})
                continue
            seen.add(canonical)

    recommendation_count = collection_sizes.get("recommendations", 0)
    conditional_count = collection_sizes.get("conditional_skills", 0)
    if status == "recommended" and recommendation_count == 0:
        errors.append({"path": "status", "reason": "status_collection_mismatch"})
    if status in {"needs_clarification", "no_match", "error"} and (
        recommendation_count or conditional_count
    ):
        errors.append({"path": "status", "reason": "status_collection_mismatch"})

    clarifying_question = payload.get("clarifying_question")
    if status == "needs_clarification" and (
        not isinstance(clarifying_question, str) or not clarifying_question.strip()
    ):
        errors.append({"path": "clarifying_question", "reason": "missing_question"})

    return {
        "valid": not errors,
        "catalog_root": str(root),
        "checked_count": checked,
        "errors": errors,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build bounded SKILL.md shards or validate recommendation paths."
    )
    parser.add_argument("skills_directory", help="Directory containing enterprise skills")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", help="New or empty output directory outside the catalog")
    action.add_argument(
        "--validate-result", help="Recommendation JSON whose skill paths must be checked"
    )
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.validate_result:
            result = validate_result(args.skills_directory, args.validate_result)
            print(json.dumps(result, sort_keys=True))
            return 0 if result["valid"] else 1

        inventory = build_catalog(
            args.skills_directory,
            args.output,
            max_files=args.max_files,
            max_bytes=args.max_bytes,
        )
        summary = {
            "status": "ok",
            "catalog_root": inventory["catalog_root"],
            "inventory_path": str(Path(args.output).expanduser().resolve() / "inventory.json"),
            "discovered_count": inventory["discovered_count"],
            "included_count": inventory["included_count"],
            "skipped_count": inventory["skipped_count"],
            "shard_count": len(inventory["shards"]),
        }
        print(json.dumps(summary, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
