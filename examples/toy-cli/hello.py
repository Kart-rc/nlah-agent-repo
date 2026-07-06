#!/usr/bin/env python3
"""Toy CLI: greet a person by name.

Usage (from the repository root):
    python3 examples/toy-cli/hello.py <name>

Prints "Hello, <name>!" to stdout and exits 0. A missing or surplus
argument yields argparse's usage/error text on stderr and exit status 2.
Stdlib only; the name is an opaque string (no validation or transformation).
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hello.py",
        description="Greet a person by name.",
    )
    parser.add_argument("name", help="name of the person to greet")
    args = parser.parse_args(argv)
    print(f"Hello, {args.name}!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
