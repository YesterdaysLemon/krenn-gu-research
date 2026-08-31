from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
OWNER = BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_ALL_ZERO_COEFFICIENT_BRANCH_EXCLUSION_THEOREM.md"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"
HELPER = BASE / "_gld103_all_zero_exact.py"
CERTIFICATE = BASE / "certificates" / "GLD103_ALL_ZERO_COEFFICIENT_BRANCH_CERTIFICATE.json"
REPLAY = BASE / "certificates" / "GLD103_ALL_ZERO_COEFFICIENT_BRANCH_REPLAY_PROVENANCE.json"
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_ALL_ZERO_COEFFICIENT_BRANCH_EXCLUSION_"
    "REVIEW_2026-08-31.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
ROOT_README = ROOT / "README.md"
README = BASE / "README.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"

PRIMARY_SHA256 = "c87feeb983f6f14a8d6c3c9c3bf788d113d655a4efdce206b98994cf2395d916"
AUDIT_SHA256 = "7fa82c67b4322dcc75a59b17cb41d24851b417593962d15070a75130dc2fe79d"
HELPER_SHA256 = "06ca97b8b38136659b8a57279b66959a28130f1ef75ff0dd5bc367ce990f2f23"
CERTIFICATE_PAYLOAD_SHA256 = (
    "f85feebddb4601e107f1728e52261a60c3f5ebb65d121eb0f29376e3409efc97"
)
CERTIFICATE_FILE_SHA256 = "7bbcf82508673262f5e5a493ccc7aae8949cc155ea49f0e472fb0cc4baa93236"
REPLAY_CANDIDATE_COMMIT = "02ca1921c00deecbec1fd9c2b3dd378f381ce67e"
F40_FACTOR_SHA256 = "83f6ac7c7e4011a85960b57f145918d910c94fb9ef61b2f27741f91ef69efe2f"
F40_RELATION_SHA256 = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
Q6_SREPR_SHA256 = "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"

SOURCE_PINS = {
    "GLD70": (
        "claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py",
        "a53433329023223f1f24e960a8b23c7c57baf87b9767c4b2acabc819b982918e",
        "1a967f71bc4a08995a9187557eccd0ce39ab0f65544652f99c538049c49251f2",
    ),
    "GLD71": (
        "claims/arbitrary-order/verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py",
        "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d",
        "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    ),
    "GLD88": (
        "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py",
        "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752",
        "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    ),
    "GLD102": (
        "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py",
        "742aaccfb1e4b7cab194d8d20addd3d5e7b5448a367180d01b398be306317eea",
        "c78130ad8ed5a639ffc7683ef21ae2b578312d6c7475820689a996dbc13bbd8e",
    ),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path, *, lf: bool = False) -> str:
    value = path.read_bytes()
    if lf:
        value = value.replace(b"\r\n", b"\n")
    return sha256_bytes(value)


def staged_index_hash(path: Path) -> str:
    """Hash the staged owner blob, matching theorem-ledger's 16-byte pin."""
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return sha256_bytes(blob)[:16]


def commit_blob_hash(commit: str, path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return sha256_bytes(blob)


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"document has no {heading!r} section")
    return match.group(1)


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(read(path), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


class GLD103EvidenceStatusTests(unittest.TestCase):
    def test_repaired_same_commit_replay_provenance_is_complete(self) -> None:
        self.assertTrue(REPLAY.is_file(), f"missing GLD103 replay provenance: {REPLAY}")
        replay = json.loads(read(REPLAY))
        self.assertEqual(replay["schema_version"], 1)
        self.assertEqual(replay["claim_id"], "GLD103")
        self.assertEqual(replay["artifact_role"], "durable_exact_replay_provenance")
        self.assertEqual(replay["replay_candidate_commit"], REPLAY_CANDIDATE_COMMIT)
        self.assertEqual(replay["global_conjecture"], "UNRESOLVED")

        subprocess.run(
            ["git", "cat-file", "-e", f"{REPLAY_CANDIDATE_COMMIT}^{{commit}}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        source_records = {
            "primary": (PRIMARY, PRIMARY_SHA256),
            "independent_audit": (AUDIT, AUDIT_SHA256),
            "comparison_helper": (HELPER, HELPER_SHA256),
        }
        for name, (path, expected) in source_records.items():
            record = replay["sources"][name]
            with self.subTest(source=name):
                self.assertEqual(record["path"], path.relative_to(ROOT).as_posix())
                self.assertEqual(record["lf_sha256"], expected)
                self.assertEqual(commit_blob_hash(REPLAY_CANDIDATE_COMMIT, path), expected)

        tracked = replay["tracked_certificate"]
        self.assertEqual(tracked["path"], CERTIFICATE.relative_to(ROOT).as_posix())
        self.assertEqual(tracked["file_sha256"], CERTIFICATE_FILE_SHA256)
        self.assertEqual(sha256_file(CERTIFICATE), CERTIFICATE_FILE_SHA256)
        self.assertEqual(tracked["payload_sha256"], CERTIFICATE_PAYLOAD_SHA256)
        self.assertIs(tracked["replay_complete"], True)
        self.assertIs(tracked["embedded_comparison_is_acceptance_dependency"], False)

        repaired = replay["repaired_candidate_run"]["primary_v10"]
        self.assertEqual(repaired["run_id"], "gld103-primary-full-20260831-allhashfix-v10")
        self.assertEqual(repaired["status"], "succeeded")
        self.assertEqual(repaired["child_exit_code"], 0)
        self.assertEqual(repaired["runner_exit_code"], 0)
        self.assertEqual(repaired["certificate_file_sha256"], CERTIFICATE_FILE_SHA256)
        self.assertEqual(repaired["certificate_payload_sha256"], CERTIFICATE_PAYLOAD_SHA256)

        clean = replay["final_clean_checkout"]
        self.assertEqual(clean["commit"], REPLAY_CANDIDATE_COMMIT)
        expected_clean_runs = {
            "primary": (
                "gld103-allhash-clean-primary-20260831-v1",
                "8a37d0b0d5ba45481d8e446dd22d7bd55bb2131eefb1373afcc2085598ebc304",
                "2fcf7960192dc5302c8a6c5d725bf12c2e7ea01e8b490f6864c93dfb82dd3c42",
            ),
            "independent_audit": (
                "gld103-allhash-clean-audit-20260831-v1",
                "615fac6fdc6b4132c7078c1900d1ed095aeed26c864a1b0c7f1f016fc91035d1",
                "c620430f66bebf4429df46fb821d2a210fd60c94980be66677aa0fd36a795c44",
            ),
            "comparison": (
                "gld103-allhash-clean-compare-20260831-v1",
                "433d13986e8ca3eec1cf3d5588cd2c8e157c4f552530897f09e4b0bbc6d3fa39",
                "d647ef5a1964b6f8fd8f71d74f639990ec61bcc0e6c4a025eaf88eeeaf2b8a82",
            ),
        }
        for name, (run_id, run_json, run_log) in expected_clean_runs.items():
            record = clean[name]
            with self.subTest(clean_run=name):
                self.assertEqual(record["run_id"], run_id)
                self.assertEqual(record["status"], "succeeded")
                self.assertEqual(record["child_exit_code"], 0)
                self.assertEqual(record["runner_exit_code"], 0)
                self.assertEqual(record["run_json_sha256"], run_json)
                self.assertEqual(record["run_log_sha256"], run_log)

        self.assertNotEqual(
            clean["primary"]["canonical_source_sha256"],
            clean["primary"]["raw_source_sha256"],
        )
        self.assertEqual(clean["primary"]["canonical_source_sha256"], PRIMARY_SHA256)
        self.assertEqual(clean["independent_audit"]["canonical_source_sha256"], AUDIT_SHA256)
        self.assertEqual(clean["comparison"]["helper_lf_sha256"], HELPER_SHA256)
        self.assertEqual(
            clean["comparison"]["run_log_sha256"],
            replay["superseded_lineage"]["comparison_v5"]["run_log_sha256"],
        )
        self.assertIs(clean["comparison"]["used_for_primary_acceptance"], False)
        self.assertIn("not an independent graph-model", replay["sources"]["independent_audit"]["independence_boundary"])

        reconciliation = replay["clean_certificate_reconciliation"]
        self.assertEqual(
            reconciliation["changed_scalar_fields"],
            [
                "certificate_payload_sha256",
                "elapsed_seconds",
                "p0_p1_gld102.elapsed_seconds",
                "verifier_raw_sha256",
            ],
        )
        self.assertIs(reconciliation["mathematical_payload_fields_unchanged"], True)
        promotion = replay["promotion_adjudication"]
        for key in (
            "same_commit_clean_primary_full_replay_passed",
            "same_commit_clean_independent_full_audit_passed",
            "same_commit_clean_exact_comparison_passed",
            "one_way_scope_preserved",
            "scope_promotable_as_exact_scoped_theorem",
        ):
            self.assertIs(promotion[key], True)
        self.assertIs(promotion["global_status_change_authorized"], False)

        def assert_hash_fields(value: object) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    if key.endswith("sha256"):
                        self.assertIsInstance(item, str)
                        assert isinstance(item, str)
                        self.assertRegex(item, re.compile(r"^[0-9a-f]{64}$"))
                    assert_hash_fields(item)
            elif isinstance(value, list):
                for item in value:
                    assert_hash_fields(item)

        assert_hash_fields(replay)

    def test_owner_and_review_are_promoted_at_the_exact_scoped_status(self) -> None:
        owner = read(OWNER)
        status = section(owner, "Status and exact scope")
        self.assertRegex(
            status,
            re.compile(
                r"\*\*Proved exact scoped characteristic-zero theorem \(`?GLD103`?\)\.\*\*",
                re.IGNORECASE,
            ),
        )
        self.assertNotRegex(status, re.compile(r"\b(candidate|draft|pending|experimental)\b", re.I))
        self.assertIn("D(B*H2*Delta)", status)
        self.assertIn("symbolic", status.lower())
        self.assertRegex(
            status,
            re.compile(r"global\s+Krenn(?:--|–)Gu\s+conjecture\s+remains\s+\*\*UNRESOLVED\*\*", re.I),
        )

        self.assertTrue(REVIEW.is_file(), f"missing GLD103 review: {REVIEW}")
        review = read(REVIEW)
        verdict = section(review, "Verdict")
        first_line = next((line.strip() for line in verdict.splitlines() if line.strip()), "")
        self.assertIn("GLD103", first_line)
        self.assertRegex(first_line, re.compile(r"\bPASS\b", re.I))
        self.assertNotRegex(first_line, re.compile(r"\b(?:DRAFT|PENDING)\b|not\s+PASS", re.I))
        self.assertRegex(
            review,
            re.compile(r"global\s+Krenn(?:--|–)Gu\s+conjecture\s+remains\s+\*\*UNRESOLVED\*\*", re.I),
        )
        for fence in ("one-way", "E31", "Delta=0", "H2=0", "physical", "global"):
            with self.subTest(fence=fence):
                self.assertIn(fence, review)

    def test_full_certificate_replay_and_current_primary_hash_are_pinned(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["claim_id"], "GLD103")
        self.assertEqual(payload["status"], "exact_scoped_theorem_certificate")
        self.assertEqual(payload["manifest_status"], "exact scoped theorem certificate")
        self.assertEqual(payload["mathematical_status"], "scoped_necessary_condition_only")
        self.assertEqual(payload["runtime_mode"], "full")
        self.assertIs(payload["replay_complete"], True)
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        self.assertEqual(payload["q6"]["srepr_sha256"], Q6_SREPR_SHA256)
        self.assertEqual(
            payload["verifier_path"],
            PRIMARY.relative_to(ROOT).as_posix(),
        )
        self.assertTrue(PRIMARY.is_file(), f"missing current primary verifier: {PRIMARY}")
        self.assertEqual(sha256_file(PRIMARY, lf=True), PRIMARY_SHA256)
        self.assertEqual(payload["verifier_sha256"], PRIMARY_SHA256)
        self.assertEqual(
            payload["verifier_hash_semantics"],
            "verifier_sha256 is the LF-normalized tracked-source digest; "
            "verifier_raw_sha256 records checkout bytes",
        )

        # Recompute the certificate's own canonical payload digest.  This
        # catches a stale or hand-edited full certificate even when its fields
        # individually look plausible.
        stored_payload_hash = payload.pop("certificate_payload_sha256")
        canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        self.assertEqual(stored_payload_hash, CERTIFICATE_PAYLOAD_SHA256)
        self.assertEqual(sha256_bytes(canonical.encode()), stored_payload_hash)

        self.assertEqual(payload["exact_arithmetic"]["status"], "verified_exact_necessary_p_cover")
        self.assertTrue(payload["exact_arithmetic"]["factor_support_match"])
        self.assertEqual(payload["exact_arithmetic"]["factor_count"], 11)
        self.assertEqual(
            payload["local_fibre_closures"]["status"],
            "verified_exact_local_fibre_closures",
        )
        self.assertEqual(payload["p0_p1_gld102"]["claim_id"], "GLD102")
        self.assertEqual(
            payload["p0_p1_gld102"]["status"],
            "proved_exact_scoped_p01_nonzero_offset_exclusion",
        )

    def test_f40_flags_are_explicit_and_the_corrected_66_of_80_leaf_is_pinned(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        flags = payload["runtime_environment"]["implementation_flags"]
        for name in (
            "GLD103_FACTOR_MATRIX_INVERSE",
            "GLD103_FACTOR_NO_FINAL_INVERSE",
        ):
            with self.subTest(flag=name):
                self.assertIn(name, flags)
                self.assertEqual(flags[name]["effective_value"], 1)
                self.assertEqual(flags[name]["source"], name)

        plan = payload["local_fibre_plan"]
        self.assertEqual(
            plan["p2_minus_2p_plus_2"],
            "sparse total-degree Macaulay bound 3 in A[a,B,z], rank 66/80",
        )
        leaf = payload["local_fibre_closures"]["closures"]["p2_minus_2p_plus_2"]
        matrix = leaf["matrix"]
        self.assertEqual(leaf["bound"], 3)
        self.assertEqual(matrix["rank"], 66)
        self.assertEqual(matrix["columns"], 80)
        self.assertEqual(matrix["rank_with_target"], 66)
        self.assertIs(matrix["target_in_span"], True)
        self.assertIs(matrix["target_residual_zero"], True)
        self.assertIs(leaf["unit"], True)
        self.assertIn("current exact rank is 66/80", read(AUDIT))

    def test_f40_has_the_exact_quotient_relation_and_nonzero_norm(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        f40 = payload["local_fibre_closures"]["closures"]["F40"]
        self.assertEqual(f40["route"], "exact quotient-Euclid gcd of D134,D145")
        self.assertEqual(
            f40["identity"],
            "u134*D134 + u145*D145 = c; Norm_A/K(c) != 0",
        )
        self.assertIs(f40["relation_checked"], True)
        self.assertEqual(f40["relation_residual_sha256"], F40_RELATION_SHA256)
        self.assertIs(f40["unnormalized_constant_c"], True)
        self.assertIs(f40["four_by_four_multiplication_norm"], True)
        self.assertIs(f40["norm_nonzero"], True)
        self.assertEqual(f40["norm_degree_p"], 39)
        self.assertEqual(f40["q_degree_of_c"], 3)
        self.assertEqual(f40["factor_field_matrix_inverse"], 1)
        self.assertEqual(f40["factor_no_final_inverse"], 1)
        self.assertIs(f40["factor_irreducible_checked"], True)
        self.assertIs(f40["factor_primitive_checked"], True)
        self.assertIs(f40["gcd_factor_H2_checked"], True)

        f40_factor = next(
            item for item in payload["exact_arithmetic"]["factors"] if item["name"] == "F40"
        )
        self.assertEqual(f40_factor["degree_p"], 40)
        self.assertEqual(f40_factor["exponent"], 2)
        self.assertEqual(f40_factor["canonical_sha256"], F40_FACTOR_SHA256)
        self.assertRegex(f40["factor"], re.compile(r"^7424\*p\*\*40\b"))
        self.assertTrue(f40["factor"].endswith("331776"))

    def test_source_and_audit_hashes_are_current_and_audit_is_independent(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        # GLD103 stores many exact comparison digests in source constants and
        # in the emitted certificate.  A prior metadata-only defect duplicated
        # or omitted one hexadecimal nibble, so reject every hash-shaped
        # literal that is not a full SHA-256 digest.
        for path in (PRIMARY, CERTIFICATE):
            for value in re.findall(r'"([0-9a-fA-F]{50,80})"', read(path)):
                with self.subTest(hash_width_path=path.name, value=value):
                    self.assertEqual(len(value), 64)

        manifest = payload["source_manifest"]
        self.assertEqual(set(manifest), set(SOURCE_PINS))
        for name, (relative, expected_raw, expected_lf) in SOURCE_PINS.items():
            path = ROOT / Path(relative)
            with self.subTest(source=name):
                self.assertTrue(path.is_file(), f"missing pinned source: {path}")
                self.assertEqual(manifest[name]["path"], relative)
                self.assertEqual(manifest[name]["sha256"], expected_raw)
                self.assertEqual(manifest[name]["lf_sha256"], expected_lf)
                self.assertEqual(sha256_file(path), expected_raw)
                self.assertEqual(sha256_file(path, lf=True), expected_lf)

        self.assertEqual(sha256_file(AUDIT), AUDIT_SHA256)
        comparison = payload["comparison_provenance"]
        self.assertEqual(len(HELPER_SHA256), 64)
        self.assertEqual(sha256_file(HELPER, lf=True), HELPER_SHA256)
        self.assertEqual(
            comparison["physical_generators"]["comparison_helper_path"],
            HELPER.relative_to(ROOT).as_posix(),
        )
        self.assertEqual(
            comparison["physical_generators"]["comparison_helper_sha256"],
            HELPER_SHA256,
        )
        for record in (
            comparison["D145_current_representation"],
            comparison["physical_generators"],
        ):
            self.assertEqual(record["audit_verifier_sha256"], AUDIT_SHA256)
            self.assertIs(record["used_for_primary_acceptance"], False)
            self.assertIs(record["runtime_dependency"], False)

        audit_tree = ast.parse(read(AUDIT), filename=str(AUDIT))
        imported = imported_modules(AUDIT)
        forbidden = re.compile(
            r"verify_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion"
            r"|_gld103_all_zero_exact",
            re.IGNORECASE,
        )
        self.assertFalse(any(forbidden.search(name) for name in imported))
        audit_text = read(AUDIT)
        self.assertIn("does not import the GLD103 primary", audit_text)
        self.assertIn("local GLD88 chart transcription", audit_text)
        self.assertIn("independent sparse offset determinant", audit_text)
        loader_calls = [
            node
            for node in ast.walk(audit_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "spec_from_file_location"
        ]
        self.assertEqual(len(loader_calls), 1)
        self.assertIsInstance(loader_calls[0].args[0], ast.Constant)
        self.assertEqual(loader_calls[0].args[0].value, "_gld88_chart_comparison")
        self.assertIsInstance(loader_calls[0].args[1], ast.Name)
        self.assertEqual(loader_calls[0].args[1].id, "GLD88")

    def test_one_way_scope_fences_and_global_status_are_preserved(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        scope = payload["scope"]
        self.assertEqual(scope["characteristic"], 0)
        self.assertEqual(scope["parameter_a"], "symbolic/arbitrary")
        self.assertEqual(scope["open"], "D(B*H2*Delta)")
        self.assertEqual(scope["rank_condition"], "rank(M(G))<=6")

        implication = payload["implication"]
        self.assertEqual(implication["direction"], "one-way")
        self.assertIs(implication["converse_used"], False)
        self.assertIs(implication["rank_to_minor_is_not_reversed"], True)
        boundary = payload["evidence_boundary"]
        self.assertEqual(boundary["rank_to_minor_direction"], "one-way necessary implication only")
        self.assertEqual(boundary["arithmetic_independence"], "not claimed")
        self.assertIs(boundary["E31_equation_imposed"], False)
        self.assertIs(boundary["E31_inverted"], False)
        self.assertIs(boundary["physical_incidence_emptiness"], False)
        self.assertIs(boundary["global_resolution"], False)
        self.assertIs(payload["clearing_gate"]["gate_not_added_to_scope"], True)
        self.assertIs(payload["exact_arithmetic"]["support_only_comparison"], True)

        owner = read(OWNER)
        review = read(REVIEW)
        combined = owner + "\n" + review
        for phrase in ("one-way", "B=0", "E31", "Delta=0", "H2=0", "physical incidence", "global Krenn--Gu", "UNRESOLVED"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)
        self.assertRegex(
            combined,
            re.compile(r"(?:not\s+convers(?:e|es)|no\s+converse|do\s+not\s+reverse)", re.I),
        )

    def test_frontier_and_both_readmes_record_the_promoted_node_and_walls(self) -> None:
        frontier = read(FRONTIER)
        node = next(
            (line for line in frontier.splitlines() if line.startswith('  GLD103["')),
            None,
        )
        self.assertIsNotNone(node, "current frontier has no GLD103 node")
        assert node is not None
        self.assertIn("<br/>PROVED", node)
        self.assertRegex(node, re.compile(r"all[- ]zero|coefficient", re.I))
        self.assertRegex(frontier, re.compile(r"GLD103\s+-->\|", re.I))
        self.assertIn(OWNER.name, frontier)
        self.assertIn(REVIEW.name, frontier)
        self.assertRegex(frontier, re.compile(r"F40|66/80", re.I))
        self.assertRegex(frontier, re.compile(r"global\s+Krenn(?:--|–)Gu.*UNRESOLVED", re.I | re.S))

        for path in (README, ROOT_README):
            self.assertTrue(path.is_file(), f"missing GLD103 README integration: {path}")
            text = read(path)
            with self.subTest(path=path):
                self.assertIn("GLD103", text)
                self.assertIn(OWNER.name, text)
                self.assertRegex(text, re.compile(r"all[- ]zero|coefficient", re.I))
                self.assertRegex(text, re.compile(r"F40", re.I))
                self.assertIn("UNRESOLVED", text)

    def test_ledger_has_one_verified_entry_with_the_staged_owner_hash(self) -> None:
        ledger = json.loads(read(LEDGER))
        entries = [item for item in ledger["entries"] if "(GLD103)" in item["name"]]
        self.assertEqual(
            len(entries),
            1,
            "root integration must add exactly one verified GLD103 ledger entry",
        )
        entry = entries[0]
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["document_sha256_16"], staged_index_hash(OWNER))
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertEqual(entry["external_binaries"], [])
        note = entry["note"]
        for phrase in ("F40", "66/80", "one-way", "E31", "Delta", "UNRESOLVED"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)


if __name__ == "__main__":
    unittest.main()
