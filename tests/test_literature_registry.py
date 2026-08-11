from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_parent / "src"))
        sys.path.insert(0, str(_parent / "tools" / "literature"))
        break

from krenn_gu.bootstrap import bootstrap  # noqa: E402
from source_registry import (  # noqa: E402
    inventory_identifiers,
    load_registry,
    normalize_arxiv,
    normalize_doi,
    validate_registry,
)

REPO_ROOT, HERE = bootstrap(__file__)


def source_record(path: str = "usage.md") -> dict:
    return {
        "citekey": "example-2026-source",
        "title": "A Verified Source",
        "authors": ["A. Author"],
        "year": 2026,
        "identifiers": {"doi": "10.1234/Example.1"},
        "authoritative_url": "https://doi.org/10.1234/example.1",
        "identity_verification": {
            "source_url": "https://doi.org/10.1234/example.1",
            "date": "2026-08-11",
        },
        "inspection_level": "identity_verified",
        "search_trail": [],
        "relevance": "Validator fixture.",
        "limitations": [],
        "repository_usages": [{"path": path, "role": "background"}],
    }


class LiteratureRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "usage.md").write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "usage.md"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def registry(self, *sources: dict) -> dict:
        return {"schema_version": 1, "sources": list(sources)}

    def test_committed_registry_is_valid(self) -> None:
        data = load_registry(REPO_ROOT / "catalog" / "literature" / "sources.json")
        self.assertEqual(validate_registry(data, REPO_ROOT), [])

    def test_malformed_and_incomplete_records_fail(self) -> None:
        self.assertIn("top level must be an object", validate_registry([])[0])
        errors = validate_registry(self.registry({}), self.root)
        self.assertTrue(any("missing required field" in error for error in errors))
        self.assertTrue(any("citekey" in error for error in errors))

    def test_duplicate_citekey_fails(self) -> None:
        first = source_record()
        second = deepcopy(first)
        second["identifiers"] = {"doi": "10.1234/example.2"}
        errors = validate_registry(self.registry(first, second), self.root)
        self.assertTrue(any("duplicate citekey" in error for error in errors))

    def test_duplicate_and_conflicting_source_identities_fail(self) -> None:
        first = source_record()
        duplicate = deepcopy(first)
        duplicate["citekey"] = "example-2026-duplicate"
        duplicate_errors = validate_registry(self.registry(first, duplicate), self.root)
        self.assertTrue(any("duplicate persistent identifier" in error for error in duplicate_errors))

        conflict = deepcopy(duplicate)
        conflict["title"] = "A Different Source"
        conflict_errors = validate_registry(self.registry(first, conflict), self.root)
        self.assertTrue(any("conflicting source identity" in error for error in conflict_errors))

    def test_missing_usage_path_fails(self) -> None:
        record = source_record("missing.md")
        errors = validate_registry(self.registry(record), self.root)
        self.assertTrue(any("not an index-visible" in error for error in errors))

    def test_untracked_file_and_directory_usage_paths_fail(self) -> None:
        (self.root / "untracked.md").write_text("not staged\n", encoding="utf-8")
        (self.root / "usage-directory").mkdir()
        for path in ("untracked.md", "usage-directory"):
            with self.subTest(path=path):
                record = source_record(path)
                errors = validate_registry(self.registry(record), self.root)
                self.assertTrue(any("not an index-visible" in error for error in errors))

    def test_git_symlink_mode_usage_path_fails(self) -> None:
        blob = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.root,
            input=b"target",
            capture_output=True,
            check=True,
        ).stdout.decode("ascii").strip()
        subprocess.run(
            ["git", "update-index", "--add", "--cacheinfo", f"120000,{blob},usage.md"],
            cwd=self.root,
            check=True,
        )
        errors = validate_registry(self.registry(source_record()), self.root)
        self.assertTrue(any("index entry is not a regular file" in error for error in errors))

    def test_malformed_persistent_identifier_fails(self) -> None:
        record = source_record()
        record["identifiers"] = {"doi": "remembered-doi"}
        errors = validate_registry(self.registry(record), self.root)
        self.assertTrue(any("malformed doi identifier" in error for error in errors))

    def test_verified_source_requires_authoritative_verification(self) -> None:
        record = source_record()
        record["authoritative_url"] = None
        record["identity_verification"] = None
        errors = validate_registry(self.registry(record), self.root)
        self.assertTrue(any("authoritative HTTPS URL" in error for error in errors))
        self.assertTrue(any("requires identity_verification" in error for error in errors))

    def test_verified_source_rejects_empty_or_credentialed_https_urls(self) -> None:
        for bad_url in (
            "https://",
            "https:// user.example",
            "https://user:pass@example.org",
            "https://example.org:bad",
            "https://.",
            "https://[bad",
        ):
            with self.subTest(url=bad_url):
                record = source_record()
                record["authoritative_url"] = bad_url
                record["identity_verification"]["source_url"] = bad_url
                errors = validate_registry(self.registry(record), self.root)
                self.assertTrue(any("authoritative HTTPS URL" in error for error in errors))
                self.assertTrue(any("source_url must be HTTPS" in error for error in errors))

    def test_verification_date_is_exact_and_not_in_the_future(self) -> None:
        for bad_date, expected in (
            ("20260811", "ISO YYYY-MM-DD"),
            (20260811, "ISO YYYY-MM-DD"),
            ("2999-01-01", "cannot be in the future"),
        ):
            with self.subTest(date=bad_date):
                record = source_record()
                record["identity_verification"]["date"] = bad_date
                errors = validate_registry(self.registry(record), self.root)
                self.assertTrue(any(expected in error for error in errors))

    def test_imported_result_without_full_text_fails_closed(self) -> None:
        record = source_record()
        record["repository_usages"] = [
            {
                "path": "usage.md",
                "role": "imported_result",
                "source_locator": None,
                "assumptions_scope": "Recorded scope.",
                "correspondence_note": "Recorded correspondence.",
                "unresolved_obligations": [],
            }
        ]
        errors = validate_registry(self.registry(record), self.root)
        self.assertTrue(any("missing source_locator" in error for error in errors))
        self.assertTrue(any("not inspected in full" in error for error in errors))

    def test_unverified_lead_is_valid_offline_with_trail_and_limit(self) -> None:
        lead = source_record()
        lead.update(
            {
                "authors": [],
                "year": None,
                "identifiers": {},
                "authoritative_url": None,
                "identity_verification": None,
                "inspection_level": "lead_unverified",
                "search_trail": ["query: exact graph matching terminology"],
                "limitations": ["Bibliographic identity and year are unverified."],
                "repository_usages": [],
            }
        )
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("network used")):
            self.assertEqual(validate_registry(self.registry(lead), self.root), [])

    def test_verified_record_cannot_hide_unknown_authors(self) -> None:
        record = source_record()
        record["authors"] = []
        errors = validate_registry(self.registry(record), self.root)
        self.assertTrue(any("authors must be a nonempty" in error for error in errors))

    def test_risk_based_background_and_novelty_requirements(self) -> None:
        lead = source_record()
        lead.update(
            {
                "authors": [],
                "year": None,
                "identifiers": {},
                "authoritative_url": None,
                "identity_verification": None,
                "inspection_level": "lead_unverified",
                "search_trail": ["query: candidate source"],
                "limitations": ["Identity is unresolved."],
            }
        )
        errors = validate_registry(self.registry(lead), self.root)
        self.assertTrue(any("background citation requires" in error for error in errors))

        novelty = source_record()
        novelty["repository_usages"] = [
            {"path": "usage.md", "role": "novelty_assessment"}
        ]
        errors = validate_registry(self.registry(novelty), self.root)
        self.assertTrue(any("novelty assessment requires a search trail" in error for error in errors))
        self.assertTrue(any("novelty assessment requires explicit search limits" in error for error in errors))

    def test_identifier_normalization_and_line_deduplication(self) -> None:
        self.assertEqual(normalize_arxiv("https://arxiv.org/abs/2407.00303v2"), "2407.00303")
        self.assertEqual(normalize_doi("https://doi.org/10.1234/EXAMPLE.1."), "10.1234/example.1")
        self.assertEqual(
            normalize_doi("10.1016/0095-8956(89)90063-4)"),
            "10.1016/0095-8956(89)90063-4",
        )
        text = self.root / "identifiers.md"
        text.write_text(
            "arXiv:2407.00303 and https://arxiv.org/abs/2407.00303v2\n"
            "DOI 10.1234/EXAMPLE.1; https://doi.org/10.1234/example.1\n",
            encoding="utf-8",
        )
        inventory = inventory_identifiers([text], self.root)
        self.assertEqual(inventory["arxiv"]["line_mentions"], 1)
        self.assertEqual(inventory["arxiv"]["unique"], 1)
        self.assertEqual(inventory["doi"]["line_mentions"], 1)
        self.assertEqual(inventory["doi"]["unique"], 1)

    def test_json_registry_round_trip(self) -> None:
        path = self.root / "registry.json"
        payload = self.registry(source_record())
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(load_registry(path), payload)


if __name__ == "__main__":
    unittest.main()
