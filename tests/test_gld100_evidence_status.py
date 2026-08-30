from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
OWNER = BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_THEOREM.md"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py"
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_REVIEW_2026-08-29.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
ROOT_README = ROOT / "README.md"
README = BASE / "README.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
Q6_DIGEST = "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"

SOURCE_MANIFEST = {
    "GLD71_verifier": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    "GLD88_verifier": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    "GLD95_owner": "1c7074a3a6c6e740832f58c37757be8231f104fa8661c05476a516302e79e1c8",
    "GLD95_verifier": "2eef9d94f251dce77b36f8d4dde479928d43087828583c3d59e52dae58c280a1",
    "GLD96_owner": "2d989620d82554197ce7f85d603269122d58dfe07c36a9ab46121a2261aabcff",
    "GLD96_verifier": "05299523e510011f25ca1dcc59cb121b4ab3c8163576788ce7bba575835ce255",
    "GLD99_owner": "f5fd49a6ff039f128f83b89bc3a7019c201001c54ba33223b2ac71e3e2289708",
    "GLD99_verifier": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
}

GAMMA_PINS = {
    "gamma0": {
        "primary": {
            "sha256": "ecc04ca65bf325abe133e0d9dabe709f16d01cc8cb2ff4711d07c683cfc76531",
            "sparse_sha256": "a8730bca93a78aeebdfd6923d4c343d44b8968d4489cbfe8bb4426fd94f3d7f8",
            "terms": 308,
            "degrees": {"p": 27, "q": 3, "a": 2},
            "scale": "4*(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
            "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
            "primitive_content": "3",
        },
        "audit": {
            "a_degree": 2,
            "p_degree": 27,
            "q_degree": 3,
            "terms": 308,
            "srepr_sha256": "ecc04ca65bf325abe133e0d9dabe709f16d01cc8cb2ff4711d07c683cfc76531",
            "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
            "quotient_scale": "4*(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
            "cleared_content": "3",
        },
    },
    "gamma1": {
        "primary": {
            "sha256": "4db77cd0ce9882b9e2f2e7694805153b9e819a8da2e425a853ba427853c65d31",
            "sparse_sha256": "9e37dd630d8d74a363c4302067ca877070b96b0bf8ae05f6d324eda561a6e6a2",
            "terms": 484,
            "degrees": {"p": 32, "q": 3, "a": 3},
            "scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
            "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
            "primitive_content": "3",
        },
        "audit": {
            "a_degree": 3,
            "p_degree": 32,
            "q_degree": 3,
            "terms": 484,
            "srepr_sha256": "4db77cd0ce9882b9e2f2e7694805153b9e819a8da2e425a853ba427853c65d31",
            "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
            "quotient_scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
            "cleared_content": "3",
        },
    },
    "gamma2": {
        "primary": {
            "sha256": "b1afa68aee1f50bf708082d6a9d2f2d6552dd222e6f69a6a5473747d11291232",
            "sparse_sha256": "88ecfc18dcc511a0c61dda5da0d4bdb208102bc0e6164d9019c19a05dc8bb3c8",
            "terms": 437,
            "degrees": {"p": 29, "q": 3, "a": 3},
            "scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
            "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
            "primitive_content": "3",
        },
        "audit": {
            "a_degree": 3,
            "p_degree": 29,
            "q_degree": 3,
            "terms": 437,
            "srepr_sha256": "b1afa68aee1f50bf708082d6a9d2f2d6552dd222e6f69a6a5473747d11291232",
            "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
            "quotient_scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
            "cleared_content": "3",
        },
    },
    "gamma3": {
        "primary": {
            "sha256": "c171b5d7205afb6d719fe5b3464fa6347968f41e84b0a829c0a81dddfb4bdb2b",
            "sparse_sha256": "6103df0e6a9e7c1279fe00b58eb48974c792f1b80801f768b99d4146bf5fdc3c",
            "terms": 308,
            "degrees": {"p": 27, "q": 3, "a": 2},
            "scale": "(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
            "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
            "primitive_content": "3",
        },
        "audit": {
            "a_degree": 2,
            "p_degree": 27,
            "q_degree": 3,
            "terms": 308,
            "srepr_sha256": "c171b5d7205afb6d719fe5b3464fa6347968f41e84b0a829c0a81dddfb4bdb2b",
            "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
            "quotient_scale": "(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
            "cleared_content": "3",
        },
    },
}

PAIR_PINS = {
    "01": {
        "primary": {
            "resultant_a_sha256": "f01526b8ade89e9474e3a9425f7a87220aa8599b694f2339a64ff1c2681f94e5",
            "remainder_sha256": "0c0abdc92c1b9479a265aa492060965cb046fcd8d13eb2d6c32b6d77fe4149a3",
            "remainder_terms": 576,
            "content": "p**3*(p**2 - p + 1)**10",
            "scale": "(2*p**2 - 2*p + 1)**12",
            "eliminant_degree": 544,
            "eliminant_sha256": "8f1666c2cc18c3c96b2eb2502533593ded9ef2870261c04be057b5a7d32ee32b",
        },
        "audit": {
            "resultant_a_p_degree": 135,
            "resultant_a_q_degree": 15,
            "resultant_a_terms": 2047,
            "resultant_a_sha256": "f01526b8ade89e9474e3a9425f7a87220aa8599b694f2339a64ff1c2681f94e5",
            "q6_remainder_scale": "(2*p**2 - 2*p + 1)**12",
            "q6_remainder_p_content": "p**3*(p**2 - p + 1)**10",
            "q6_remainder_p_content_srepr_sha256": "be67e76c94fec2e342b14a0c533cd6f881429c600e9696b8a324278af4eb0d8d",
            "q6_remainder_p_degree": 144,
            "q6_remainder_q_degree": 3,
            "q6_remainder_terms": 576,
            "q6_remainder_sha256": "0c0abdc92c1b9479a265aa492060965cb046fcd8d13eb2d6c32b6d77fe4149a3",
            "p_eliminant_degree": 544,
            "p_eliminant_sha256": "8f1666c2cc18c3c96b2eb2502533593ded9ef2870261c04be057b5a7d32ee32b",
            "q_resultant_rational_content": "17837583236744824004702123713604783826989481984",
        },
    },
    "02": {
        "primary": {
            "resultant_a_sha256": "a2db7ada8d86e3529cc58a617449c154f016b0b0fbaa209ae29860cd4d92a6fe",
            "remainder_sha256": "53e8eff8d4196bba8a65afa522da5410ca5f6193c99d41fb17efbb04406fe7f4",
            "remainder_terms": 580,
            "content": "(p**2 - p + 1)**10",
            "scale": "(2*p**2 - 2*p + 1)**12",
            "eliminant_degree": 552,
            "eliminant_sha256": "13f408ae39f9df64130f4ade389f3b1835ba6863278b303d0808fdeaf54f6ef7",
        },
        "audit": {
            "resultant_a_p_degree": 133,
            "resultant_a_q_degree": 15,
            "resultant_a_terms": 2074,
            "resultant_a_sha256": "a2db7ada8d86e3529cc58a617449c154f016b0b0fbaa209ae29860cd4d92a6fe",
            "q6_remainder_scale": "(2*p**2 - 2*p + 1)**12",
            "q6_remainder_p_content": "(p**2 - p + 1)**10",
            "q6_remainder_p_content_srepr_sha256": "700320feda3e3b7523253d948ff02de8c5228a2196f525645b3d8bc677ad34d0",
            "q6_remainder_p_degree": 145,
            "q6_remainder_q_degree": 3,
            "q6_remainder_terms": 580,
            "q6_remainder_sha256": "53e8eff8d4196bba8a65afa522da5410ca5f6193c99d41fb17efbb04406fe7f4",
            "p_eliminant_degree": 552,
            "p_eliminant_sha256": "13f408ae39f9df64130f4ade389f3b1835ba6863278b303d0808fdeaf54f6ef7",
            "q_resultant_rational_content": "17837583236744824004702123713604783826989481984",
        },
    },
    "03": {
        "primary": {
            "resultant_a_sha256": "b3bcbbddba13d6434a764aa7ff579fbfc075e10c523c65ae575e4b288e8d39c2",
            "remainder_sha256": "c3b126f686bd1e437710354e1134fd795ba14193df56a50ebd0eddd4c1a591c3",
            "remainder_terms": 418,
            "content": "p*(p**2 - p + 1)**8",
            "scale": "(2*p**2 - 2*p + 1)**9",
            "eliminant_degree": 406,
            "eliminant_sha256": "24ea888f45f850c676c4c89e01bfa01af72ead3abe01cd2103bab9d98f47767e",
        },
        "audit": {
            "resultant_a_p_degree": 98,
            "resultant_a_q_degree": 12,
            "resultant_a_terms": 1219,
            "resultant_a_sha256": "b3bcbbddba13d6434a764aa7ff579fbfc075e10c523c65ae575e4b288e8d39c2",
            "q6_remainder_scale": "(2*p**2 - 2*p + 1)**9",
            "q6_remainder_p_content": "p*(p**2 - p + 1)**8",
            "q6_remainder_p_content_srepr_sha256": "811c703d9ac35298089376c661354c36b15aef36ab8202c71103242bef072524",
            "q6_remainder_p_degree": 105,
            "q6_remainder_q_degree": 3,
            "q6_remainder_terms": 418,
            "q6_remainder_sha256": "c3b126f686bd1e437710354e1134fd795ba14193df56a50ebd0eddd4c1a591c3",
            "p_eliminant_degree": 406,
            "p_eliminant_sha256": "24ea888f45f850c676c4c89e01bfa01af72ead3abe01cd2103bab9d98f47767e",
            "q_resultant_rational_content": "14836019612485612895559393214464",
        },
    },
}

FULL_GCD_PIN = {
    "degree": 374,
    "sha256": "f8bfaa97e9d980852df37e1c98bc82769aba0ab3a762452b55bb0696697d42d2",
    "radical_degree": 18,
    "radical_sha256": "dd930e75eaf842e522b08b661739c53693bb5a7de45414851651e36f291d4361",
    "factors": [
        ("p - 1", 44),
        ("p", 84),
        ("p**2 + 1", 1),
        ("p**2 - 2*p + 2", 3),
        ("p**2 - p + 1", 31),
        ("2*p**2 - 2*p + 1", 84),
        ("5*p**4 - 16*p**3 + 30*p**2 - 16*p + 5", 1),
        ("8*p**4 - 16*p**3 + 12*p**2 - 4*p + 5", 1),
    ],
}
COMMON_GCD_PIN = {
    "degree": 372,
    "srepr_sha256": "f2fb7f0eaaf3a9b44b4bde6c1486b0cba843141c84eddb9c891c10d5b2cd57aa",
}

REQUIRED_FIBRE_HASH_KEYS = {
    "p_zero": {"q_certificate_sha256", "record_sha256"},
    "p_one": {"q_certificate_sha256", "record_sha256"},
    "p2_minus_2p_plus_2": {
        "q_certificate_sha256",
        "gamma_certificate_sha256",
        "record_sha256",
    },
    "p2_plus_1": {
        "q_certificate_sha256",
        "gamma_certificate_sha256",
        "record_sha256",
    },
    "quartic_A": {
        "q_certificate_sha256",
        "gamma_certificate_sha256",
        "record_sha256",
    },
    "quartic_C": {
        "q_certificate_sha256",
        "gamma_certificate_sha256",
        "record_sha256",
    },
    "P": {"Delta_quotient_sha256", "record_sha256"},
    "H2": {"record_sha256"},
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def staged_index_hash(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()[:16]


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(read(path), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def status_section(text: str) -> str:
    match = re.search(
        r"^## Status(?: and exact scope)?\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError("GLD100 owner has no status section")
    return match.group(1)


class GLD100EvidenceStatusTests(unittest.TestCase):
    def test_owner_and_review_are_promoted_only_at_scoped_status(self) -> None:
        owner = read(OWNER)
        status = status_section(owner)
        self.assertIn(
            "**Proved exact scoped characteristic-zero theorem (`GLD100`).**",
            status,
        )
        self.assertNotRegex(status, re.compile(r"\b(candidate|experimental|pending)\b", re.I))
        self.assertRegex(
            status,
            re.compile(
                r"global\s+Krenn(?:--|–)Gu\s+conjecture\s+remains\s+\*\*UNRESOLVED\*\*",
                re.I,
            ),
        )

        self.assertTrue(REVIEW.is_file(), f"missing GLD100 review: {REVIEW}")
        review = read(REVIEW)
        self.assertRegex(
            review,
            re.compile(r"Verdict:\s*(?:\*\*)?PASS for the exact `GLD100` scope", re.I),
        )
        self.assertRegex(
            review,
            re.compile(
                r"global\s+Krenn(?:--|–)Gu\s+conjecture\s+remains\s+\*\*UNRESOLVED\*\*",
                re.I,
            ),
        )

    def test_fibre_hashes_are_nonempty_and_checked_without_a_truthiness_bypass(self) -> None:
        primary_text = read(PRIMARY)
        primary = load_module(PRIMARY, "gld100_primary_fibre_status_test")
        hashes = primary.EXPECTED_FIBRE_CERTIFICATE_HASHES
        self.assertIsInstance(hashes, dict)
        self.assertTrue(hashes, "GLD100 fibre certificate hashes must be populated")
        self.assertEqual(set(hashes), set(REQUIRED_FIBRE_HASH_KEYS))
        for fibre, keys in REQUIRED_FIBRE_HASH_KEYS.items():
            with self.subTest(fibre=fibre):
                self.assertEqual(set(hashes[fibre]), keys)
                for key in keys:
                    self.assertRegex(hashes[fibre][key], r"^[0-9a-f]{64}$")

        tree = ast.parse(primary_text, filename=str(PRIMARY))
        check_fibres = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "check_fibres"
        )
        conditions = [
            ast.unparse(node.test)
            for node in ast.walk(check_fibres)
            if isinstance(node, ast.If)
        ]
        self.assertTrue(
            any(
                re.search(
                    r"(?:actual_hashes\s*!=\s*EXPECTED_FIBRE_CERTIFICATE_HASHES|EXPECTED_FIBRE_CERTIFICATE_HASHES\s*!=\s*actual_hashes)",
                    condition,
                )
                for condition in conditions
            ),
            "check_fibres must compare actual and expected fibre hashes directly",
        )
        self.assertNotRegex(
            primary_text,
            re.compile(
                r"if\s+EXPECTED_FIBRE_CERTIFICATE_HASHES\s+(?:and|or)\b|if\s+not\s+EXPECTED_FIBRE_CERTIFICATE_HASHES\b",
                re.I,
            ),
        )

    def test_source_gamma_pair_and_gcd_pins_are_exact_in_both_replays(self) -> None:
        primary = load_module(PRIMARY, "gld100_primary_pin_test")
        audit = load_module(AUDIT, "gld100_audit_pin_test")

        self.assertEqual(primary.EXPECTED_SUPPORT_DIGEST, SUPPORT_DIGEST)
        self.assertEqual(audit.EXPECTED_SUPPORT_DIGEST, SUPPORT_DIGEST)
        self.assertEqual(tuple(primary.SUPPORT_ROWS), SUPPORT_ROWS)
        self.assertEqual(tuple(audit.SUPPORT_ROWS), SUPPORT_ROWS)
        self.assertEqual(primary.EXPECTED_SOURCE_MANIFEST, SOURCE_MANIFEST)
        manifest_paths = {
            "GLD71_verifier": BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py",
            "GLD88_verifier": BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py",
            "GLD95_owner": BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_THEOREM.md",
            "GLD95_verifier": BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py",
            "GLD96_owner": BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md",
            "GLD96_verifier": BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py",
            "GLD99_owner": BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md",
            "GLD99_verifier": BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py",
        }
        self.assertEqual(
            {name: lf_sha256(path) for name, path in manifest_paths.items()},
            SOURCE_MANIFEST,
        )
        self.assertEqual(primary.EXPECTED_Q6_SHA256, Q6_DIGEST)
        self.assertEqual(primary.digest(primary.q6_polynomial()), Q6_DIGEST)

        for name, pin in GAMMA_PINS.items():
            with self.subTest(gamma=name, replay="primary"):
                self.assertEqual(
                    {
                        key: primary.EXPECTED_GAMMAS[name][key]
                        for key in pin["primary"]
                    },
                    pin["primary"],
                )
                self.assertEqual(
                    set(primary.EXPECTED_GAMMAS[name]["quotient_witness"]),
                    {
                        "numerator_remainder_sha256",
                        "denominator_remainder_sha256",
                        "inverse_sha256",
                        "reduced_sha256",
                        "relation_sha256",
                    },
                )
            with self.subTest(gamma=name, replay="audit"):
                self.assertEqual(audit.EXPECTED_GENERIC_GAMMAS[name], pin["audit"])

        for name, pin in PAIR_PINS.items():
            with self.subTest(pair=name, replay="primary"):
                self.assertEqual(
                    {
                        key: primary.EXPECTED_PAIRS[name][key]
                        for key in pin["primary"]
                    },
                    pin["primary"],
                )
                self.assertRegex(
                    primary.EXPECTED_PAIRS[name]["primitive_clearing_sha256"],
                    r"^[0-9a-f]{64}$",
                )
            with self.subTest(pair=name, replay="audit"):
                self.assertEqual(audit.EXPECTED_PAIR_RESULTANTS[name], pin["audit"])

        self.assertEqual(primary.EXPECTED_FULL_GCD, FULL_GCD_PIN)
        self.assertEqual(audit.EXPECTED_COMMON_GCD, COMMON_GCD_PIN)
        self.assertEqual(audit.EXPECTED_FULL_CONTENT_GCD["degree"], FULL_GCD_PIN["degree"])
        self.assertEqual(
            audit.EXPECTED_FULL_CONTENT_GCD["srepr_sha256"], FULL_GCD_PIN["sha256"]
        )
        self.assertEqual(audit.EXPECTED_COVER_RADICAL_DIGEST, FULL_GCD_PIN["radical_sha256"])
        self.assertEqual(tuple(audit.COVER_FACTORS), (
            "p", "p_minus_1", "P", "H2", "Q_gamma", "Q_other", "A4", "C4"
        ))

    def test_primary_and_audit_are_separate_and_audit_has_no_forbidden_imports(self) -> None:
        primary_modules = imported_modules(PRIMARY)
        audit_modules = imported_modules(AUDIT)
        self.assertTrue(
            all("audit_four_root_torus_star_equal_leaf_h4_q6" not in name.lower() for name in primary_modules)
        )
        forbidden = re.compile(
            r"(?:verify|audit)_four_root_torus_star_equal_leaf_h4_q6|(?:^|[._])gld(?:71|88|96|99|100)(?:$|[._])",
            re.I,
        )
        self.assertFalse(
            any(forbidden.search(name) for name in audit_modules),
            f"GLD100 audit imports a forbidden replay module: {sorted(audit_modules)}",
        )
        self.assertNotIn("importlib", audit_modules)
        self.assertNotIn("importlib.util", audit_modules)

        audit_text = read(AUDIT)
        self.assertIn('"gld_identifier": "GLD100"', audit_text)
        self.assertIn('"global_conjecture": "UNRESOLVED"', audit_text)
        self.assertRegex(audit_text, re.compile(r'"status":\s*"independent_[^"]+"'))
        self.assertNotIn('"status": "candidate_exact_independent_fibre_audit"', audit_text)
        self.assertIn("GLD100 independent exact audit: PASS", audit_text)

    def test_frontier_and_readmes_record_the_promoted_node_and_exact_walls(self) -> None:
        frontier = read(FRONTIER)
        node = next(
            (line for line in frontier.splitlines() if line.startswith('  GLD100["')),
            None,
        )
        self.assertIsNotNone(node, "current frontier has no GLD100 node")
        assert node is not None
        self.assertIn("<br/>PROVED", node)
        self.assertRegex(node, re.compile(r"g0", re.I))
        self.assertRegex(node, re.compile(r"E31|Delta", re.I))
        self.assertRegex(
            frontier,
            re.compile(r"GLD96\s+-->\|[^|]*g0[^|]*\|\s+GLD100", re.I),
        )
        self.assertRegex(frontier, re.compile(r"GLD100\s+-->\|", re.I))
        self.assertIn("The global Krenn–Gu conjecture is **UNRESOLVED**", frontier)

        for path in (README, ROOT_README):
            text = read(path)
            with self.subTest(path=path):
                self.assertIn("GLD100", text)
                self.assertRegex(text, re.compile(r"g0", re.I))
                self.assertRegex(text, re.compile(r"E31|Delta", re.I))
                self.assertRegex(text, re.compile(r"Omega", re.I))
                self.assertIn("UNRESOLVED", text)

    def test_ledger_has_one_verified_entry_with_staged_owner_hash(self) -> None:
        ledger = json.loads(read(LEDGER))
        entries = [item for item in ledger["entries"] if "(GLD100)" in item["name"]]
        self.assertEqual(
            len(entries),
            1,
            "root integration must add exactly one verified GLD100 ledger entry",
        )
        entry = entries[0]
        self.assertEqual(entry["document_sha256_16"], staged_index_hash(OWNER))
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertIn("UNRESOLVED", entry["note"])


if __name__ == "__main__":
    unittest.main()
