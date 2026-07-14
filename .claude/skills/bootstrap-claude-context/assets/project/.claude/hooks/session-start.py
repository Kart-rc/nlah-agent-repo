#!/usr/bin/env python3
"""Emit concise project startup context without modifying the repository."""

import json
import os
import sys
from pathlib import Path


def parse_input() -> None:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, OSError, RuntimeError, TypeError, ValueError):
        pass


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def count_files(directory: Path, project: Path) -> int:
    try:
        if directory.is_symlink():
            return 0
        resolved_directory = directory.resolve(strict=False)
        if not is_within(resolved_directory, project):
            return 0
        return sum(
            1
            for path in resolved_directory.iterdir()
            if not path.is_symlink() and path.is_file()
        )
    except (OSError, RuntimeError, ValueError):
        return 0


def startup_context() -> str:
    receipt_count = 0
    pending_count = 0
    project_value = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_value:
        try:
            project = Path(project_value).resolve()
            learnings = (
                project / ".claude" / "context" / "learnings"
            )
            receipt_count = count_files(learnings / "receipts", project)
            pending_count = count_files(learnings / "pending", project)
        except (OSError, RuntimeError, ValueError):
            pass
    return (
        f"Claude context: {receipt_count} session receipt(s); "
        f"{pending_count} pending learning proposal(s). "
        "Run /start-codebase for the developer briefing and review pending "
        "proposals before changing project instructions."
    )


def main() -> int:
    parse_input()
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": startup_context(),
        }
    }
    try:
        print(json.dumps(output, sort_keys=True))
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
