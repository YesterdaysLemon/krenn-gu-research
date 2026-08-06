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

import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]
                       / "tools" / "migration"))

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


if __name__ == "__main__":
    unittest.main()
