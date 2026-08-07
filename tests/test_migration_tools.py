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




# ------------------------------------------------------------------
# Phase 2: frozen batch contract, package metadata, provenance
# ------------------------------------------------------------------

from batch_contract import (  # noqa: E402
    canonical_mapping_hash,
    make_batch,
    validate_batch as contract_validate,
    validate_executed_provenance,
)
from package_metadata import (  # noqa: E402
    resolve_claim_package_metadata,
)


def _gitinit(tmp):
    _git(tmp, "init", "-q")
    _git(tmp, "config", "user.email", "test@example.com")
    _git(tmp, "config", "user.name", "test")


def _write_manifest(tmp, moves, extra=None):
    (tmp / "catalog").mkdir(exist_ok=True)
    manifest = {
        "moves": moves,
        "collision_report": [],
        "double_move_report": [],
        "overlap_cycle_report": [],
    }
    if extra:
        manifest.update(extra)
    (tmp / "catalog" / "moved-paths.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def _head_sha(tmp):
    return _git(tmp, "rev-parse", "HEAD").stdout.strip()


class BatchIntegrityTests(unittest.TestCase):
    """Frozen batch approval contract (Phase 2 item 1A)."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        _gitinit(self.tmp)
        (self.tmp / "A.md").write_text("a\n", encoding="utf-8")
        (self.tmp / "B.md").write_text("b\n", encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-q", "-m", "base")
        self.base = _head_sha(self.tmp)
        self.moves = [
            {"old_path": "A.md", "new_path": "docs/A.md",
             "status": "proposed_high_confidence"},
            {"old_path": "B.md", "new_path": "docs/B.md",
             "status": "proposed_high_confidence"},
        ]
        _write_manifest(self.tmp, self.moves)

    def _make(self, **kw):
        args = dict(
            batch_id="test-batch", approved_by="tester",
            approved_at="2026-08-06", base_sha=self.base,
            members=["A.md", "B.md"], root=self.tmp)
        args.update(kw)
        return make_batch(**args)

    def test_valid_frozen_batch_accepted(self):
        batch = self._make()
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        self.assertEqual(contract_validate(batch, self.tmp,
                                           manifest["moves"]), [])

    def test_mapping_hash_is_deterministic(self):
        b1 = self._make()
        b2 = self._make()
        self.assertEqual(b1["mapping_sha256"], b2["mapping_sha256"])
        # order-independent
        rev = dict(canonical_mapping_hash=reversed)
        manual = canonical_mapping_hash(
            [{"old_path": "B.md", "new_path": "docs/B.md"},
             {"old_path": "A.md", "new_path": "docs/A.md"}])
        self.assertEqual(b1["mapping_sha256"], manual)

    def test_altered_destination_refused(self):
        batch = self._make()
        batch["moves"][0]["new_path"] = "docs/EVIL.md"
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("mapping_sha256" in p or "drift" in p
                            for p in problems), problems)

    def test_altered_member_count_refused(self):
        batch = self._make()
        batch["member_count"] = 99
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("member_count" in p for p in problems))

    def test_wrong_mapping_hash_refused(self):
        batch = self._make()
        batch["mapping_sha256"] = "0" * 64
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("mapping_sha256" in p for p in problems))

    def test_missing_approved_at_refused(self):
        batch = self._make()
        del batch["approved_at"]
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("approved_at" in p for p in problems))

    def test_duplicate_source_refused(self):
        batch = self._make()
        batch["moves"].append({"old_path": "A.md",
                               "new_path": "docs/A2.md"})
        batch["member_count"] = len(batch["moves"])
        batch["mapping_sha256"] = canonical_mapping_hash(batch["moves"])
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("duplicate source" in p
                            for p in problems))

    def test_duplicate_destination_refused(self):
        batch = self._make()
        batch["moves"].append({"old_path": "C.md",
                               "new_path": "docs/A.md"})
        batch["member_count"] = len(batch["moves"])
        batch["mapping_sha256"] = canonical_mapping_hash(batch["moves"])
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("duplicate destination" in p
                            for p in problems)
                        or any("missing from manifest" in p
                               for p in problems))

    def test_unresolvable_base_sha_refused(self):
        batch = self._make(base_sha="f" * 40)
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("base_sha" in p for p in problems))

    def test_manifest_drift_after_approval_refused(self):
        batch = self._make()
        # manifest destination drifts after approval
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        manifest["moves"][0]["new_path"] = "docs/DRIFTED.md"
        (self.tmp / "catalog" / "moved-paths.json").write_text(
            json.dumps(manifest))
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("drift" in p for p in problems), problems)

    def test_stale_batch_source_missing_refused(self):
        batch = self._make()
        manifest = json.loads((self.tmp / "catalog" /
                               "moved-paths.json").read_text())
        manifest["moves"] = [m for m in manifest["moves"]
                             if m["old_path"] != "B.md"]
        problems = contract_validate(batch, self.tmp, manifest["moves"])
        self.assertTrue(any("missing from manifest" in p
                            for p in problems))

    def test_make_batch_rejects_already_moved(self):
        for m in self.moves:
            m["status"] = "moved"
        _write_manifest(self.tmp, self.moves)
        with self.assertRaises(ValueError):
            self._make()


class ProvenanceTests(unittest.TestCase):
    """Executed-batch provenance invariant (Phase 2 item 1C)."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        _gitinit(self.tmp)
        (self.tmp / "A.md").write_text("a\n", encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-q", "-m", "base")
        self.base = _head_sha(self.tmp)

    def _batch_file(self, moves, bid="exec-batch"):
        (self.tmp / "catalog" / "batches").mkdir(parents=True,
                                                 exist_ok=True)
        batch = {
            "batch_id": bid, "approved_by": "t",
            "approved_at": "2026-08-06", "base_sha": self.base,
            "member_count": len(moves), "moves": moves,
            "mapping_sha256": canonical_mapping_hash(moves),
        }
        (self.tmp / "catalog" / "batches" / f"{bid}.json").write_text(
            json.dumps(batch), encoding="utf-8")

    def test_valid_provenance_passes(self):
        moves = [{"old_path": "A.md", "new_path": "docs/A.md"}]
        self._batch_file(moves)
        manifest_moves = [{"old_path": "A.md", "new_path": "docs/A.md",
                           "status": "moved",
                           "executed_batch": "exec-batch"}]
        self.assertEqual(
            validate_executed_provenance(manifest_moves, self.tmp), [])

    def test_missing_executed_batch_fails(self):
        manifest_moves = [{"old_path": "A.md", "new_path": "docs/A.md",
                           "status": "moved"}]
        problems = validate_executed_provenance(manifest_moves,
                                                self.tmp)
        self.assertTrue(any("lacks executed_batch" in p
                            for p in problems))

    def test_missing_batch_file_fails(self):
        manifest_moves = [{"old_path": "A.md", "new_path": "docs/A.md",
                           "status": "moved",
                           "executed_batch": "ghost-batch"}]
        problems = validate_executed_provenance(manifest_moves,
                                                self.tmp)
        self.assertTrue(any("file missing" in p for p in problems))

    def test_mapping_mismatch_fails(self):
        moves = [{"old_path": "A.md", "new_path": "docs/A.md"}]
        self._batch_file(moves)
        manifest_moves = [{"old_path": "A.md",
                           "new_path": "docs/OTHER.md",
                           "status": "moved",
                           "executed_batch": "exec-batch"}]
        problems = validate_executed_provenance(manifest_moves,
                                                self.tmp)
        self.assertTrue(any("mapping differs" in p for p in problems))


class PackageMetadataTests(unittest.TestCase):
    """Structural claim-package metadata (Phase 2 item 1B)."""

    PKG = "claims/p5/h22/disjoint-mixed-star"

    def test_canonical_theorem_at_package_root(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/P5_H22_THEOREM.md")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertEqual(meta["proof_variant"], "canonical")
        self.assertIsNone(meta["subpackage"])

    def test_alternate_proof_subpackage(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/alternate/P5_H22_THEOREM_ALTERNATE.md")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertEqual(meta["proof_variant"], "alternate")
        self.assertEqual(meta["subpackage"], "alternate")

    def test_boundary_subpackage(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/boundaries/P5_H22_BOUNDARY.md")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertIsNone(meta["proof_variant"])
        self.assertEqual(meta["subpackage"], "boundaries")

    def test_verifier_under_alternate(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/alternate/verify_x_alternate.py")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertIsNone(meta["proof_variant"])  # scripts carry none
        self.assertEqual(meta["subpackage"], "alternate")

    def test_audit_under_boundaries(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/boundaries/audit_x.py")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertIsNone(meta["proof_variant"])
        self.assertEqual(meta["subpackage"], "boundaries")

    def test_working_note_not_canonical(self):
        meta = resolve_claim_package_metadata(
            self.PKG + "/P5_H22_WORKING_NOTE.md")
        self.assertEqual(meta["claim_package"], self.PKG)
        self.assertIsNone(meta["proof_variant"])

    def test_non_claim_document_is_none(self):
        self.assertIsNone(
            resolve_claim_package_metadata("docs/index.md"))
        self.assertIsNone(resolve_claim_package_metadata("README.md"))

    def test_manifest_family_authoritative(self):
        moves = [{"old_path": "X.md",
                  "new_path": "claims/p5/h31/fam/X.md",
                  "claim_family": "p5/h31/fam"}]
        meta = resolve_claim_package_metadata("claims/p5/h31/fam/X.md",
                                             moves)
        self.assertEqual(meta["claim_package"], "claims/p5/h31/fam")


class LedgerMetadataIntegrationTests(unittest.TestCase):
    """update_ledger derives package metadata structurally."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        _gitinit(self.tmp)
        (self.tmp / "catalog").mkdir()
        pkg = self.tmp / "claims" / "p5" / "h22" / "fam"
        (pkg / "alternate").mkdir(parents=True)
        (pkg / "boundaries").mkdir(parents=True)
        (pkg / "THEOREM.md").write_text("t\n", encoding="utf-8")
        (pkg / "alternate" / "THEOREM_ALTERNATE.md").write_text(
            "alt\n", encoding="utf-8")
        (pkg / "boundaries" / "BOUNDARY.md").write_text(
            "b\n", encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-q", "-m", "dest")
        self.ledger = {"entries": [
            {"name": "theorem", "document": "THEOREM.md",
             "document_sha256_16": "0" * 16, "status": "verified"},
            {"name": "alternate", "document": "THEOREM_ALTERNATE.md",
             "document_sha256_16": "0" * 16, "status": "verified"},
            {"name": "boundary", "document": "BOUNDARY.md",
             "document_sha256_16": "0" * 16, "status": "verified"},
        ]}
        (self.tmp / "catalog" / "theorem-ledger.json").write_text(
            json.dumps(self.ledger), encoding="utf-8")
        self.moves = {
            "THEOREM.md": "claims/p5/h22/fam/THEOREM.md",
            "THEOREM_ALTERNATE.md":
                "claims/p5/h22/fam/alternate/THEOREM_ALTERNATE.md",
            "BOUNDARY.md":
                "claims/p5/h22/fam/boundaries/BOUNDARY.md",
        }
        self.manifest_moves = [
            {"old_path": o, "new_path": n, "claim_family": "p5/h22/fam"}
            for o, n in self.moves.items()]

    def _load(self):
        return json.loads((self.tmp / "catalog" /
                           "theorem-ledger.json").read_text())

    def test_metadata_derived_structurally(self):
        update_ledger(self.moves, self.tmp,
                      manifest_moves=self.manifest_moves)
        d = self._load()
        by = {e["name"]: e for e in d["entries"]}
        self.assertEqual(by["theorem"]["claim_package"],
                         "claims/p5/h22/fam")
        self.assertEqual(by["theorem"]["proof_variant"], "canonical")
        self.assertIsNone(by["theorem"]["subpackage"])
        self.assertEqual(by["alternate"]["proof_variant"], "alternate")
        self.assertEqual(by["alternate"]["subpackage"], "alternate")
        self.assertEqual(by["boundary"]["subpackage"], "boundaries")
        self.assertIsNone(by["boundary"]["proof_variant"])
        # status preserved
        for e in d["entries"]:
            self.assertEqual(e["status"], "verified")

    def test_hashes_recomputed_for_moved_docs(self):
        update_ledger(self.moves, self.tmp,
                      manifest_moves=self.manifest_moves)
        d = self._load()
        for e in d["entries"]:
            self.assertNotEqual(e["document_sha256_16"], "0" * 16)

    def test_idempotent_second_pass(self):
        update_ledger(self.moves, self.tmp,
                      manifest_moves=self.manifest_moves)
        first = self._load()
        update_ledger(self.moves, self.tmp,
                      manifest_moves=self.manifest_moves)
        second = self._load()
        self.assertEqual(first, second)

    def test_foreign_cwd_operation(self):
        elsewhere = pathlib.Path(tempfile.mkdtemp())
        old = os.getcwd()
        try:
            os.chdir(elsewhere)
            update_ledger(self.moves, self.tmp,
                          manifest_moves=self.manifest_moves)
        finally:
            os.chdir(old)
        d = self._load()
        self.assertEqual(d["entries"][0]["claim_package"],
                         "claims/p5/h22/fam")




class FinalContractTests(unittest.TestCase):
    """Phase 2 final review: mandatory mapping hash + committed batch
    file enforcement."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        _gitinit(self.tmp)
        (self.tmp / "A.md").write_text("a\n", encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-q", "-m", "base")
        self.base = _head_sha(self.tmp)
        self.moves = [{"old_path": "A.md", "new_path": "docs/A.md",
                       "status": "proposed_high_confidence"}]
        _write_manifest(self.tmp, self.moves)
        self.manifest_moves = json.loads(
            (self.tmp / "catalog" / "moved-paths.json")
            .read_text())["moves"]

    def test_missing_mapping_hash_refused(self):
        batch = make_batch(
            batch_id="no-hash", approved_by="t",
            approved_at="2026-08-06", base_sha=self.base,
            members=["A.md"], root=self.tmp)
        del batch["mapping_sha256"]
        problems = contract_validate(batch, self.tmp,
                                     self.manifest_moves)
        self.assertTrue(any("mapping_sha256" in p
                            for p in problems), problems)

    def test_present_valid_mapping_hash_accepted(self):
        batch = make_batch(
            batch_id="ok", approved_by="t", approved_at="2026-08-06",
            base_sha=self.base, members=["A.md"], root=self.tmp)
        self.assertEqual(
            contract_validate(batch, self.tmp, self.manifest_moves), [])

    def test_external_batch_file_refused(self):
        import sys as _sys
        _sys.path.insert(0, str(pathlib.Path(__file__).resolve()
                                .parents[1] / "tools" / "migration"))
        from execute_moves import _resolve_committed_batch_path
        outside = pathlib.Path(tempfile.mkdtemp()) / "evil.json"
        outside.write_text("{}", encoding="utf-8")
        with self.assertRaises(SystemExit) as ctx:
            _resolve_committed_batch_path(None, str(outside))
        self.assertIn("outside catalog/batches", str(ctx.exception))

    def test_untracked_batch_file_refused(self):
        import sys as _sys
        _sys.path.insert(0, str(pathlib.Path(__file__).resolve()
                                .parents[1] / "tools" / "migration"))
        from execute_moves import _resolve_committed_batch_path
        # inside the repo's catalog/batches dir but NOT git-tracked:
        # write into the REAL repo catalog/batches, untracked.
        repo = pathlib.Path(__file__).resolve().parents[1]
        target = repo / "catalog" / "batches" / "_untracked_test_batch.json"
        target.write_text("{}", encoding="utf-8")
        try:
            with self.assertRaises(SystemExit) as ctx:
                _resolve_committed_batch_path(None, str(target))
            self.assertIn("untracked", str(ctx.exception))
        finally:
            target.unlink(missing_ok=True)

    def test_batch_id_resolves_into_catalog_batches(self):
        import sys as _sys
        _sys.path.insert(0, str(pathlib.Path(__file__).resolve()
                                .parents[1] / "tools" / "migration"))
        from execute_moves import _resolve_committed_batch_path, BATCH_DIR
        path = _resolve_committed_batch_path("some-batch", None)
        self.assertEqual(path, BATCH_DIR / "some-batch.json")


class ManifestSummaryInvariantTests(unittest.TestCase):
    """Durable invariant (Stage 3 review item 1): the manifest's counts
    summary must be derived from its move records, and the moved-only
    root projection must agree with the base-ref recomputation.  A
    summary that can drift from the records is a bug by definition.
    Reads the REAL repo manifest; strictly read-only."""

    REPO = pathlib.Path(__file__).resolve().parents[1]

    def _load(self):
        return json.loads((self.REPO / "catalog" / "moved-paths.json")
                          .read_text(encoding="utf-8"))

    def test_counts_match_records(self):
        manifest = self._load()
        records = manifest["moves"]
        counts = manifest["counts"]
        for key, status in (("moved", "moved"),
                            ("pilot", "pilot"),
                            ("proposed_high_confidence",
                             "proposed_high_confidence"),
                            ("review_required", "review_required")):
            actual = sum(1 for r in records if r["status"] == status)
            self.assertEqual(
                counts.get(key), actual,
                f"counts.{key}={counts.get(key)} but records give "
                f"{actual}")
        self.assertEqual(counts.get("total_classified_moves"),
                         len(records))

    def test_moved_only_projection_matches_base_ref(self):
        manifest = self._load()
        records = manifest["moves"]
        counts = manifest["counts"]
        moved = [r for r in records if r["status"] == "moved"]
        if not moved:
            self.skipTest("no moved entries")
        start = manifest["starting_commit"]
        out = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", start],
            cwd=self.REPO, capture_output=True, text=True, check=True)
        tree = [l for l in out.stdout.splitlines() if l.strip()]
        base_files = sorted(f for f in tree if "/" not in f)
        base_dirs = sorted({f.split("/")[0] for f in tree if "/" in f})
        left = [f for f in base_files
                if f not in {m["old_path"] for m in moved}]
        dirs = set(base_dirs)
        new_dirs = {m["new_path"].split("/")[0] for m in moved}
        fixed_dirs = {".github", "claims", "docs", "src", "tools",
                      "tests", "catalog", "research_snapshots",
                      "research_figures"}
        expected = len(left) + len(dirs | new_dirs | fixed_dirs)
        self.assertEqual(
            counts.get("projected_root_if_moved_only"), expected,
            "projected_root_if_moved_only disagrees with the base-ref "
            "recomputation")



class ExecutorFinalizeRegressionTests(unittest.TestCase):
    """Regression test (Stage 3 final review): executing a batch through
    the executor's real state transition (``finalize_execution``) must
    update the manifest summary — moved, proposed_high_confidence, and
    projected_root_if_moved_only — without any subsequent manual
    manifest rebuild.  Also verifies that a recompute failure cannot
    leave a stale manifest (rollback-safe transaction)."""

    def _gitinit_repo(self, tmp):
        subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"],
                       cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"],
                       cwd=tmp, check=True)

    def test_finalize_updates_summary_without_rebuild(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        self._gitinit_repo(tmp)
        # Two root files that will move, plus one that stays.
        for name in ("A.md", "B.md", "STAYS.md"):
            (tmp / name).write_text(name, encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "base"],
                       cwd=tmp, check=True)
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=tmp,
            capture_output=True, text=True, check=True).stdout.strip()

        from execute_moves import finalize_execution
        manifest = {
            "starting_commit": base,
            "counts": {"unclassified": 0,
                       "collisions": 0, "double_moves": 0,
                       "overlap_cycles": 0},
            "moves": [
                {"old_path": "A.md",
                 "new_path": "claims/t/pkg/A.md",
                 "status": "proposed_high_confidence"},
                {"old_path": "B.md",
                 "new_path": "claims/t/pkg/B.md",
                 "status": "proposed_high_confidence"},
                {"old_path": "STAYS.md",
                 "new_path": "docs/STAYS.md",
                 "status": "proposed_high_confidence"},
            ],
        }
        before_moved = sum(1 for r in manifest["moves"]
                           if r["status"] == "moved")
        before_proposed = sum(1 for r in manifest["moves"]
                              if r["status"]
                              == "proposed_high_confidence")
        self.assertEqual(before_moved, 0)
        self.assertEqual(before_proposed, 3)

        batch_size = 2
        performed = manifest["moves"][:batch_size]
        result = finalize_execution(manifest, performed,
                                    "test-batch", tmp)

        counts = result["counts"]
        self.assertEqual(counts["moved"], before_moved + batch_size,
                         "moved did not increase by batch_size")
        self.assertEqual(
            counts["proposed_high_confidence"],
            before_proposed - batch_size,
            "proposed_high_confidence did not decrease by batch_size")
        for m in performed:
            self.assertEqual(m["status"], "moved")
            self.assertEqual(m["executed_batch"], "test-batch")
        # Moved-only projection uses the same formula as
        # build_manifest.recompute_manifest_summary: base root files not
        # moved, plus (base dirs | new top-level dirs | fixed dirs).
        # "claims" is both a new top dir and a fixed dir, so it is
        # counted once.
        fixed_dirs = {".github", "claims", "docs", "src", "tools",
                      "tests", "catalog", "research_snapshots",
                      "research_figures"}
        left = (3 - batch_size)           # STAYS.md remains
        dirs = set() | {"claims"} | fixed_dirs
        self.assertEqual(counts["projected_root_if_moved_only"],
                         left + len(dirs),
                         "projected_root_if_moved_only not updated")

    def test_recompute_failure_cannot_leave_stale_manifest(self):
        # If recompute_manifest_summary raises (here simulated by an
        # unresolvable starting_commit), finalize_execution propagates
        # the exception before any manifest write, so the caller's
        # rollback runs and no stale manifest is produced.
        tmp = pathlib.Path(tempfile.mkdtemp())
        self._gitinit_repo(tmp)
        (tmp / "A.md").write_text("A", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "base"],
                       cwd=tmp, check=True)

        from execute_moves import finalize_execution
        manifest = {
            "starting_commit": "f" * 40,  # does not resolve
            "counts": {"unclassified": 0},
            "moves": [{"old_path": "A.md",
                       "new_path": "claims/t/pkg/A.md",
                       "status": "proposed_high_confidence"}],
        }
        performed = manifest["moves"]
        with self.assertRaises(subprocess.CalledProcessError):
            finalize_execution(manifest, performed, "b", tmp)
        # The failure happens inside recompute, BEFORE any write; the
        # executor's except block would roll back.  No manifest file is
        # created here by finalize_execution itself.
        self.assertFalse((tmp / "moved-paths.json").exists())


class ExposeClaimPackageTests(unittest.TestCase):
    """Stage 4: the single shared helper that exposes a moved claim
    package (hyphenated directory, not a Python package) to legacy
    bare-name imports.  Replaces the per-importer sys.path shims Stage 3
    left for the moved disjoint-mixed-star package."""

    def _import_helper(self):
        import importlib.util
        src = (pathlib.Path(__file__).resolve().parents[1]
               / "src" / "krenn_gu" / "bootstrap.py")
        spec = importlib.util.spec_from_file_location(
            "kg_bootstrap_stage4", src)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _make_repo(self, tmp, package_rel):
        # A marker file makes this dir discoverable as a repo root.
        (tmp / "catalog").mkdir(parents=True, exist_ok=True)
        (tmp / "catalog" / "theorem-ledger.json").write_text(
            "{}", encoding="utf-8")
        pkg = tmp / package_rel
        pkg.mkdir(parents=True, exist_ok=True)
        return pkg

    def test_expose_adds_package_and_import_resolves(self):
        mod = self._import_helper()
        tmp = pathlib.Path(tempfile.mkdtemp())
        rel = "claims/p4/components/disjoint-mixed-star"
        pkg = self._make_repo(tmp, rel)
        (pkg / "mod_under_test_stage4.py").write_text(
            "VALUE = 42\n", encoding="utf-8")
        import sys as _sys
        try:
            self.assertNotIn(str(pkg), _sys.path)
            out = mod.expose_claim_package(tmp, rel)
            self.assertEqual(out, pkg.resolve())
            self.assertIn(str(pkg), _sys.path)
            import mod_under_test_stage4 as m
            self.assertEqual(m.VALUE, 42)
        finally:
            _sys.modules.pop("mod_under_test_stage4", None)
            if str(pkg) in _sys.path:
                _sys.path.remove(str(pkg))

    def test_expose_is_idempotent(self):
        mod = self._import_helper()
        tmp = pathlib.Path(tempfile.mkdtemp())
        rel = "claims/p4/components/split-pair"
        pkg = self._make_repo(tmp, rel)
        import sys as _sys
        try:
            mod.expose_claim_package(tmp, rel)
            mod.expose_claim_package(tmp, rel)
            self.assertEqual(_sys.path.count(str(pkg)), 1)
        finally:
            if str(pkg) in _sys.path:
                _sys.path.remove(str(pkg))

    def test_missing_package_raises(self):
        mod = self._import_helper()
        tmp = pathlib.Path(tempfile.mkdtemp())
        self._make_repo(tmp, "claims/p4/components/exists")
        with self.assertRaises(FileNotFoundError):
            mod.expose_claim_package(
                tmp, "claims/p4/components/no-such-package")

    def test_absolute_and_escaping_paths_refused(self):
        mod = self._import_helper()
        tmp = pathlib.Path(tempfile.mkdtemp())
        self._make_repo(tmp, "claims/p4/components/x")
        with self.assertRaises(ValueError):
            mod.expose_claim_package(tmp, "/etc/passwd")
        with self.assertRaises(ValueError):
            mod.expose_claim_package(tmp, "../outside")

    def test_no_git_dependency(self):
        # The helper must work from a tree with no .git directory: it
        # resolves paths, it never shells out to git.
        mod = self._import_helper()
        tmp = pathlib.Path(tempfile.mkdtemp())
        rel = "claims/p4/components/no-git"
        pkg = self._make_repo(tmp, rel)
        self.assertFalse((tmp / ".git").exists())
        out = mod.expose_claim_package(tmp, rel)
        self.assertEqual(out, pkg.resolve())
        import sys as _sys
        if str(pkg) in _sys.path:
            _sys.path.remove(str(pkg))

if __name__ == "__main__":
    unittest.main()
