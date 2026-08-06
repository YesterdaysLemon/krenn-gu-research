"""Tests for the migration machinery (PR review item 5).

Covers, at minimum:
  - moved source + moved target;
  - moved source + unmoved target;
  - unmoved source + moved target;
  - ../ and ./ paths;
  - URL fragments;
  - reference-style markdown links;
  - image links;
  - duplicate replay-command basenames;
  - fenced commands with arguments;
  - nonexistent targets;
  - final-destination collisions;
  - ledger path and hash updates.

The rewriter functions take an explicit root, so every case runs
against a synthetic fixture tree in a temp directory — no repository
state is touched.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]
                       / "tools" / "migration"))
# check_hygiene.py lives at the repository root.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from rewrite_links import (  # noqa: E402
    _remap_target,
    load_move_map,
    normalize_rel,
    relative_to,
    rewrite_markdown,
    update_ledger,
)
from build_manifest import (  # noqa: E402
    normalize,
    pilot_destination,
    validate_records,
)


def make_fixture(tmp: pathlib.Path, moves: dict[str, str]) -> dict:
    """Create catalog/moved-paths.json + placeholder files."""
    (tmp / "catalog").mkdir(parents=True, exist_ok=True)
    manifest = {
        "moves": [
            {"old_path": o, "new_path": n, "status": "moved",
             "reason": "test"}
            for o, n in moves.items()
        ]
    }
    (tmp / "catalog" / "moved-paths.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    # Post-move tree: files exist only at their NEW locations; the
    # old locations are gone, exactly as after execute_moves.py.
    for n in moves.values():
        f = tmp / n
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("moved\n", encoding="utf-8")
    return load_move_map(tmp)


def write_md(tmp: pathlib.Path, rel: str, content: str) -> None:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def read_md(tmp: pathlib.Path, rel: str) -> str:
    return (tmp / rel).read_text(encoding="utf-8")


class NormalizeTests(unittest.TestCase):
    def test_normalize_rel_dot_and_dotdot(self):
        self.assertEqual(normalize_rel("claims/p5", "./x.md"),
                         "claims/p5/x.md")
        self.assertEqual(normalize_rel("claims/p5/h22", "../h31/x.md"),
                         "claims/p5/h31/x.md")
        self.assertEqual(normalize_rel("", "README.md"), "README.md")
        self.assertEqual(normalize_rel("docs", "../README.md"),
                         "README.md")

    def test_normalize_rel_escape_is_none(self):
        self.assertIsNone(normalize_rel("", "../escape.md"))
        self.assertIsNone(normalize_rel("claims", "../../escape.md"))

    def test_relative_to(self):
        self.assertEqual(
            relative_to("claims/p5/h22/pkg",
                        "claims/p5/h22/pkg/alternate/t.md"),
            "alternate/t.md")
        self.assertEqual(
            relative_to("claims/p5/h22/pkg", "P4_DOC.md"),
            "../../../../P4_DOC.md")
        self.assertEqual(relative_to("", "docs/index.md"),
                         "docs/index.md")

    def test_manifest_normalize(self):
        self.assertEqual(normalize("a/./b//c"), "a/b/c")
        with self.assertRaises(ValueError):
            normalize("a/../escape")


class RemapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.moves = {
            "DOC_A.md": "claims/p5/h22/pkg/DOC_A.md",
            "verify_a.py": "claims/p5/h22/pkg/verify_a.py",
            "claims/p5/h22/pkg/DOC_B.md":
                "claims/p5/h22/pkg/boundaries/DOC_B.md",
        }
        self.m = make_fixture(self.tmp, self.moves)

    def remap(self, target, written_from, now_from, moved):
        counter = {"n": 0}
        return _remap_target(target, self.m, written_from, now_from,
                             moved, counter, self.tmp)

    def test_moved_source_moved_target(self):
        # DOC_B (itself moved) links to DOC_A (moved).
        out = self.remap("DOC_A.md", "claims/p5/h22/pkg",
                         "claims/p5/h22/pkg/boundaries", True)
        self.assertEqual(out, "../DOC_A.md")

    def test_moved_source_unmoved_target(self):
        # doc moved root -> package; its links were WRITTEN relative
        # to the root, so written_from is "".  The still-root target
        # must re-anchor upward from the new location.
        write_md(self.tmp, "P4_STILL_ROOT.md", "unmoved\n")
        out = self.remap("P4_STILL_ROOT.md", "",
                         "claims/p5/h22/pkg", True)
        self.assertEqual(out, "../../../../P4_STILL_ROOT.md")

    def test_unmoved_source_moved_target(self):
        out = self.remap("DOC_A.md", "", "", False)
        self.assertEqual(out, "claims/p5/h22/pkg/DOC_A.md")

    def test_unmoved_source_unmoved_target_untouched(self):
        self.assertIsNone(
            self.remap("OTHER.md", "", "", False))

    def test_dotdot_resolution(self):
        # source stays at the package root; the link uses ../../ to
        # reach a sibling h31 doc that is tracked but NOT moved.  The
        # link already resolves from the source's current location, so
        # the idempotency guard leaves it untouched (remap returns
        # None and the text keeps its identical expression).
        write_md(self.tmp, "claims/p5/h31/DOC_H31.md", "tracked\n")
        out = self.remap("../../h31/DOC_H31.md", "claims/p5/h22/pkg",
                         "claims/p5/h22/pkg", True)
        self.assertIsNone(out)

    def test_dotdot_onto_moved_target(self):
        # ../../ from the package dir reaches a target that DID move;
        # the new expression points at the destination.
        self.m["claims/p5/h31/DOC_H31.md"] = (
            "claims/p5/h31/fam/DOC_H31.md")
        out = self.remap("../../h31/DOC_H31.md", "claims/p5/h22/pkg",
                         "claims/p5/h22/pkg", False)
        self.assertEqual(out, "../../h31/fam/DOC_H31.md")

    def test_url_fragment_preserved(self):
        # unmoved root source linking to a moved doc with a fragment:
        # the fragment must survive the rewrite.
        out = self.remap("DOC_A.md#section-2", "", "", False)
        self.assertEqual(out, "claims/p5/h22/pkg/DOC_A.md#section-2")

    def test_already_correct_link_untouched(self):
        # from inside the package, DOC_A.md already resolves; the
        # guard must not rewrite it.
        out = self.remap("DOC_A.md", "claims/p5/h22/pkg",
                         "claims/p5/h22/pkg", True)
        self.assertIsNone(out)

    def test_external_url_untouched(self):
        self.assertIsNone(
            self.remap("https://example.com/x.md", "", "", True))

    def test_nonexistent_target_unmoved_source(self):
        # unmoved source, target not moved -> untouched (returns None)
        self.assertIsNone(self.remap("NO_SUCH.md", "", "", False))


class RewriteMarkdownTests(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.moves = {
            "DOC_A.md": "claims/p5/h22/pkg/DOC_A.md",
            "verify_a.py": "claims/p5/h22/pkg/verify_a.py",
            "dup_name.py": "claims/x/dup_name.py",
            "other/dup_name.py": "claims/y/dup_name.py",
        }
        self.m = make_fixture(self.tmp, self.moves)

    def test_inline_link_from_unmoved_source(self):
        write_md(self.tmp, "README.md",
                 "See [theorem](DOC_A.md).\n")
        stats = rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertEqual(stats["links_rewritten"], 1)
        self.assertIn("](claims/p5/h22/pkg/DOC_A.md)",
                      read_md(self.tmp, "README.md"))

    def test_reference_style_link(self):
        write_md(self.tmp, "README.md",
                 "See [theorem][ref].\n\n[ref]: DOC_A.md\n")
        rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertIn("[ref]: claims/p5/h22/pkg/DOC_A.md",
                      read_md(self.tmp, "README.md"))

    def test_image_link(self):
        # image links use the same ](  ) syntax
        write_md(self.tmp, "README.md",
                 "![diagram](DOC_A.md)\n")
        rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertIn("](claims/p5/h22/pkg/DOC_A.md)",
                      read_md(self.tmp, "README.md"))

    def test_replay_command_with_args(self):
        write_md(self.tmp, "README.md",
                 "```text\npython verify_a.py --limit 10\n```\n")
        stats = rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertEqual(stats["replay_rewritten"], 1)
        self.assertIn("python claims/p5/h22/pkg/verify_a.py --limit 10",
                      read_md(self.tmp, "README.md"))

    def test_duplicate_replay_basename_ambiguous(self):
        write_md(self.tmp, "README.md",
                 "```text\npython dup_name.py\n```\n")
        stats = rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertEqual(stats["replay_rewritten"], 0)
        self.assertEqual(len(stats["ambiguous"]), 1)
        # content untouched
        self.assertIn("python dup_name.py", read_md(self.tmp, "README.md"))

    def test_outside_fence_untouched(self):
        write_md(self.tmp, "README.md",
                 "    python verify_a.py\n")
        stats = rewrite_markdown(self.m, ["README.md"], self.tmp)
        self.assertEqual(stats["replay_rewritten"], 0)


class CollisionTests(unittest.TestCase):
    def test_final_destination_collisions(self):
        records = [
            {"old_path": "A.md", "new_path": "claims/x/A.md"},
            {"old_path": "B.md", "new_path": "claims/x/A.md"},
        ]
        collisions, doubles, cycles = validate_records(records)
        self.assertEqual(len(collisions), 1)
        self.assertEqual(doubles, [])
        self.assertEqual(cycles, [])

    def test_double_move_detection(self):
        records = [
            {"old_path": "A.md", "new_path": "claims/x/A.md"},
            {"old_path": "A.md", "new_path": "claims/y/A.md"},
        ]
        collisions, doubles, cycles = validate_records(records)
        self.assertEqual(doubles, ["A.md"])

    def test_overlap_cycle_detection(self):
        records = [
            {"old_path": "A.md", "new_path": "B.md"},
            {"old_path": "B.md", "new_path": "claims/x/B.md"},
        ]
        collisions, doubles, cycles = validate_records(records)
        self.assertEqual(len(cycles), 1)

    def test_clean_records_pass(self):
        records = [
            {"old_path": "A.md", "new_path": "claims/x/A.md"},
            {"old_path": "B.md", "new_path": "claims/x/B.md"},
        ]
        collisions, doubles, cycles = validate_records(records)
        self.assertEqual((collisions, doubles, cycles), ([], [], []))

    def test_pilot_destination_layout(self):
        base = "claims/p5/h22/pkg"
        alt = pilot_destination("X_ALTERNATE.md", base)
        self.assertEqual(alt, "claims/p5/h22/pkg/alternate/X_ALTERNATE.md")
        bnd = pilot_destination(
            "X_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md", base)
        self.assertTrue(bnd.startswith(
            "claims/p5/h22/pkg/boundaries/"))


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        (self.tmp / "catalog").mkdir(parents=True)
        self.ledger = {
            "entries": [{
                "name": "doc a",
                "document": "DOC_A.md",
                "document_sha256_16": "0000000000000000",
                "status": "verified",
                "primary_verifier": "verify_a.py",
                "independent_audit": None,
            }]
        }
        (self.tmp / "catalog" / "theorem-ledger.json").write_text(
            json.dumps(self.ledger), encoding="utf-8")
        self.moves = {
            "DOC_A.md": "claims/p5/h22/pkg/DOC_A.md",
            "verify_a.py": "claims/p5/h22/pkg/verify_a.py",
        }

    def test_paths_updated_and_fields_added(self):
        update_ledger(self.moves, self.tmp, rehash=False)
        d = json.loads((self.tmp / "catalog" / "theorem-ledger.json")
                       .read_text(encoding="utf-8"))
        e = d["entries"][0]
        self.assertEqual(e["document"], "claims/p5/h22/pkg/DOC_A.md")
        self.assertEqual(e["primary_verifier"],
                         "claims/p5/h22/pkg/verify_a.py")
        self.assertEqual(e["claim_package"], "claims/p5/h22/pkg")
        self.assertIn("DOC_A.md", e["legacy_paths"])
        self.assertIn("verify_a.py", e["legacy_paths"])

    def test_status_not_changed(self):
        update_ledger(self.moves, self.tmp, rehash=False)
        d = json.loads((self.tmp / "catalog" / "theorem-ledger.json")
                       .read_text(encoding="utf-8"))
        self.assertEqual(d["entries"][0]["status"], "verified")




from check_hygiene import find_stale_bare_refs  # noqa: E402




from rewrite_links import blob_sha16  # noqa: E402


def _git(tmp, *args):
    return subprocess.run(["git", *args], cwd=tmp, capture_output=True,
                          text=True, check=True)


class LedgerHashTests(unittest.TestCase):
    """Actually exercise update_ledger's hash-update path against a
    real temporary git repository (review item 4)."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        _git(self.tmp, "init", "-q")
        _git(self.tmp, "config", "user.email", "test@example.com")
        _git(self.tmp, "config", "user.name", "test")
        (self.tmp / "catalog").mkdir()
        (self.tmp / "DOC_A.md").write_text("theorem v1\n",
                                           encoding="utf-8")
        (self.tmp / "verify_a.py").write_text("# verifier\n",
                                              encoding="utf-8")
        self.ledger = {
            "entries": [{
                "name": "doc a",
                "document": "DOC_A.md",
                "document_sha256_16": "0000000000000000",
                "status": "verified",
                "primary_verifier": "verify_a.py",
                "independent_audit": None,
            }]
        }
        (self.tmp / "catalog" / "theorem-ledger.json").write_text(
            json.dumps(self.ledger), encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-q", "-m", "base")
        # execute the move in git history, like execute_moves.py would
        (self.tmp / "claims" / "p5" / "h22" / "pkg").mkdir(
            parents=True)
        _git(self.tmp, "mv", "DOC_A.md",
             "claims/p5/h22/pkg/DOC_A.md")
        _git(self.tmp, "mv", "verify_a.py",
             "claims/p5/h22/pkg/verify_a.py")
        _git(self.tmp, "commit", "-q", "-m", "move")
        self.moves = {
            "DOC_A.md": "claims/p5/h22/pkg/DOC_A.md",
            "verify_a.py": "claims/p5/h22/pkg/verify_a.py",
        }

    def test_hash_matches_moved_committed_blob(self):
        # default hash_func = blob_sha16 over the temp repo's index
        update_ledger(self.moves, self.tmp)
        d = json.loads((self.tmp / "catalog" / "theorem-ledger.json")
                       .read_text(encoding="utf-8"))
        e = d["entries"][0]
        expected = hashlib.sha256(
            subprocess.run(
                ["git", "show", ":claims/p5/h22/pkg/DOC_A.md"],
                cwd=self.tmp, capture_output=True,
                check=True).stdout).hexdigest()[:16]
        self.assertEqual(e["document_sha256_16"], expected)
        self.assertEqual(e["document"], "claims/p5/h22/pkg/DOC_A.md")
        self.assertEqual(e["status"], "verified")

    def test_blob_sha16_is_lf_normalized(self):
        # the committed blob is LF-normalized content
        h = blob_sha16(self.tmp, "claims/p5/h22/pkg/DOC_A.md")
        manual = hashlib.sha256(b"theorem v1\n").hexdigest()[:16]
        self.assertEqual(h, manual)

    def test_runs_from_foreign_working_directory(self):
        # run update_ledger with cwd far away from the repo root
        elsewhere = pathlib.Path(tempfile.mkdtemp())
        old_cwd = os.getcwd()
        try:
            os.chdir(elsewhere)
            update_ledger(self.moves, self.tmp)
        finally:
            os.chdir(old_cwd)
        d = json.loads((self.tmp / "catalog" / "theorem-ledger.json")
                       .read_text(encoding="utf-8"))
        expected = hashlib.sha256(
            subprocess.run(
                ["git", "show", ":claims/p5/h22/pkg/DOC_A.md"],
                cwd=self.tmp, capture_output=True,
                check=True).stdout).hexdigest()[:16]
        self.assertEqual(d["entries"][0]["document_sha256_16"],
                         expected)


class LedgerInjectableHashTests(unittest.TestCase):
    """update_ledger must honor an injected hash function, so hash
    behavior is testable without git at all."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        (self.tmp / "catalog").mkdir()
        # Post-move state: the document already sits at its NEW path
        # (as it would after execute_moves.py), so the exists() guard
        # passes and the injected hash is invoked.
        (self.tmp / "pkg").mkdir()
        (self.tmp / "pkg" / "DOC_A.md").write_text("x",
                                                   encoding="utf-8")
        ledger = {"entries": [{
            "name": "doc a", "document": "DOC_A.md",
            "document_sha256_16": "0000000000000000",
            "status": "verified"}]}
        (self.tmp / "catalog" / "theorem-ledger.json").write_text(
            json.dumps(ledger), encoding="utf-8")

    def test_injected_hash_used(self):
        calls = []

        def fake_hash(root, rel):
            calls.append(rel)
            return "deadbeefcafe0000"

        update_ledger({"DOC_A.md": "pkg/DOC_A.md"}, self.tmp,
                      hash_func=fake_hash)
        d = json.loads((self.tmp / "catalog" / "theorem-ledger.json")
                       .read_text(encoding="utf-8"))
        self.assertEqual(d["entries"][0]["document_sha256_16"],
                         "deadbeefcafe0000")
        self.assertEqual(calls, ["pkg/DOC_A.md"])


class StaleReferenceTests(unittest.TestCase):
    """A stale root-level pilot reference must fail; the rewritten
    destination (or a valid in-package sibling reference) must pass."""

    MOVED = {
        "verify_p5_h22_disjoint_mixed_star_component_generic_"
        "obstruction.py":
            "claims/p5/h22/disjoint-mixed-star/"
            "verify_p5_h22_disjoint_mixed_star_component_generic_"
            "obstruction.py",
    }
    BASE = ("verify_p5_h22_disjoint_mixed_star_component_generic_"
            "obstruction.py")

    def test_stale_root_replay_command_fails(self):
        text = ("Run:\n\n```text\npython " + self.BASE
                + "\n```\n")
        hits = find_stale_bare_refs(text, "README.md", self.MOVED)
        self.assertTrue(any(ctx == "fenced replay command"
                            for ctx, b in hits), hits)

    def test_rewritten_command_in_doc_is_valid(self):
        text = ("```text\npython claims/p5/h22/disjoint-mixed-star/"
                + self.BASE + "\n```\n")
        hits = find_stale_bare_refs(text, "README.md", self.MOVED)
        self.assertEqual(hits, [])

    def test_sibling_reference_inside_package_valid(self):
        # inside the destination package the basename is a sibling.
        text = "```text\npython " + self.BASE + "\n```\n"
        hits = find_stale_bare_refs(
            text, "claims/p5/h22/disjoint-mixed-star/README.md",
            self.MOVED)
        self.assertEqual(hits, [])

    def test_stale_root_markdown_link_fails(self):
        text = "See [theorem](" + self.BASE.replace(".py", ".md") + ").\n"
        moved = {self.BASE.replace(".py", ".md"):
                 "claims/p5/h22/disjoint-mixed-star/"
                 + self.BASE.replace(".py", ".md")}
        hits = find_stale_bare_refs(text, "README.md", moved)
        self.assertTrue(any(ctx == "markdown link"
                            for ctx, b in hits), hits)

    def test_reference_style_link_stale_fails(self):
        text = "[ref]: " + self.BASE + "\n"
        hits = find_stale_bare_refs(text, "SOME_DOC.md", self.MOVED)
        self.assertTrue(any(ctx == "reference-style link"
                            for ctx, b in hits), hits)

    def test_python_subprocess_string_outside_package_fails(self):
        text = ('subprocess.run([sys.executable, "' + self.BASE
                + '"])\n')
        hits = find_stale_bare_refs(text, "some_script.py", self.MOVED)
        self.assertTrue(any(ctx == "python command string"
                            for ctx, b in hits), hits)

    def test_python_subprocess_string_inside_package_valid(self):
        text = ('subprocess.run([sys.executable, "' + self.BASE
                + '"])\n')
        hits = find_stale_bare_refs(
            text,
            "claims/p5/h22/disjoint-mixed-star/boundaries/tool.py",
            self.MOVED)
        self.assertEqual(hits, [])

    def test_yaml_command_reference_fails(self):
        text = "run: python " + self.BASE + "\n"
        hits = find_stale_bare_refs(text, ".github/x.yml", self.MOVED)
        self.assertTrue(any(ctx == "command reference"
                            for ctx, b in hits), hits)


if __name__ == "__main__":
    unittest.main()
