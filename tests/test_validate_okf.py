"""Regression checks for the OKF bundle conformance validator."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / ".claude"
    / "skills"
    / "okf-second-brain"
    / "scripts"
    / "validate_okf.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_okf", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(bundle: Path, rel: str, content: str) -> Path:
    path = bundle / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def make_conformant_bundle(bundle: Path) -> None:
    write(
        bundle,
        "index.md",
        '---\nokf_version: "0.1"\n---\n\n# Test Brain\n\n'
        "* [References](references/) - distilled external sources\n",
    )
    write(
        bundle,
        "log.md",
        "# Log\n\n## 2026-07-17\n\n"
        "* **Creation**: Added [Caching](/references/caching.md).\n"
        "* **Update**: Linked [Caching](/references/caching.md)\n"
        "  to the latency playbook.\n",
    )
    write(
        bundle,
        "references/index.md",
        "# References\n\n* [Caching](/references/caching.md) - when caching pays off\n",
    )
    write(
        bundle,
        "references/caching.md",
        "---\ntype: Reference\ntitle: Caching\n"
        "description: When caching pays off.\n"
        "resource: https://example.com/caching\n"
        "tags: [performance, caching]\n"
        "timestamp: 2026-07-17T12:00:00Z\n---\n\n"
        "# Caching\n\nDistilled content.\n\n"
        "## Citations\n\n1. [Source](https://example.com/caching)\n",
    )


class ValidateOkfTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.bundle = Path(self._tmp.name)
        make_conformant_bundle(self.bundle)

    def findings(self):
        findings, warnings = self.validator.validate(self.bundle)
        return findings, warnings

    def assert_finding(self, fragment):
        findings, _ = self.findings()
        self.assertTrue(
            any(fragment in msg for _, msg in findings),
            f"expected a finding containing {fragment!r}, got: {findings}",
        )

    def test_conformant_bundle_passes(self):
        findings, warnings = self.findings()
        self.assertEqual(findings, [])
        self.assertEqual(warnings, [])

    def test_missing_type_fails(self):
        write(
            self.bundle,
            "references/no-type.md",
            "---\ntitle: No Type\n---\n\nBody.\n",
        )
        self.assert_finding("`type` is missing or empty")

    def test_missing_frontmatter_fails(self):
        write(self.bundle, "notes/bare.md", "# Bare\n\nNo frontmatter.\n")
        self.assert_finding("missing YAML frontmatter")

    def test_unterminated_frontmatter_fails(self):
        write(self.bundle, "notes/broken.md", "---\ntype: Note\n\nBody.\n")
        self.assert_finding("does not parse")

    def test_frontmatter_on_non_root_index_fails(self):
        write(
            self.bundle,
            "references/index.md",
            "---\nkind: index\n---\n\n# References\n\n"
            "* [Caching](/references/caching.md) - when caching pays off\n",
        )
        self.assert_finding("only the bundle root may")

    def test_root_index_frontmatter_restricted_to_okf_version(self):
        write(
            self.bundle,
            "index.md",
            '---\nokf_version: "0.1"\nextra: nope\n---\n\n# Test Brain\n',
        )
        self.assert_finding("only `okf_version`")

    def test_malformed_index_bullet_fails(self):
        write(
            self.bundle,
            "references/index.md",
            "# References\n\n* Caching - a bare bullet with no link\n",
        )
        self.assert_finding("index bullet must be")

    def test_dangling_index_link_warns_not_fails(self):
        write(
            self.bundle,
            "references/index.md",
            "# References\n\n"
            "* [Caching](/references/caching.md) - when caching pays off\n"
            "* [Ghost](/references/ghost.md) - points nowhere\n",
        )
        findings, warnings = self.findings()
        self.assertEqual(findings, [])
        self.assertTrue(any("missing file" in msg for _, msg in warnings))

    def test_bad_log_date_heading_fails(self):
        write(
            self.bundle,
            "log.md",
            "# Log\n\n## July 17, 2026\n\n* **Creation**: Something.\n",
        )
        self.assert_finding("ISO date")

    def test_non_bullet_log_entry_fails(self):
        write(
            self.bundle,
            "log.md",
            "# Log\n\n## 2026-07-17\n\nAdded something without a bullet.\n",
        )
        self.assert_finding("must be bullets")

    def test_missing_root_index_fails(self):
        (self.bundle / "index.md").unlink()
        self.assert_finding("no index.md")


if __name__ == "__main__":
    unittest.main()
