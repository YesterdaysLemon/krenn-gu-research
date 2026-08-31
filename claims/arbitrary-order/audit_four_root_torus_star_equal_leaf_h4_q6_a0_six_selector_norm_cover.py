#!/usr/bin/env python3
"""Independent direct-matrix audit of the scoped GLD101 a=0 norm cover.

This audit deliberately does not import the GLD88 verifier or the GLD101
primary verifier.  It locally transcribes only the a=0 H4 chart, rebuilds the
37 by 9 syndrome matrix from the pinned GLD71 sparse relations, computes the
six named seven-by-seven minors with SymPy matrix determinants, and then
forms the selector determinant from direct B,C coefficient extraction.  The
resultant and factor signatures are checked independently of the primary
verifier's sparse B,C determinant dynamic program.

The audit is still a computational audit of a scoped necessary condition.
It does not turn ignored Singular replay logs into independent certificates,
and it leaves the global Krenn--Gu conjecture UNRESOLVED.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD99 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py"
)
CERTIFICATE_PAYLOAD = ROOT / "claims" / "arbitrary-order" / "certificates" / (
    "GLD101_A0_NORM_COVER_CERTIFICATE.json"
)

p, q, B, C = sp.symbols("p q B C")
Kp = QQ.frac_field(p)
Kpq = QQ.frac_field(p, q)
ALL_ROWS = tuple(range(37))
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
SIX_NAMES = ("T0", "T1", "T2", "T3", "Y1", "X3")
SIX_COLUMNS = ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
NAMED = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
}
EXTRA = {
    "Y1": (0, 1, 3, 4, 5, 6, 7),
    "X3": (0, 1, 2, 3, 4, 6, 7),
}
RSTAR = (0, 1, 17, 28, 31, 32, 33)

EXPECTED_SOURCE_PINS = {
    "GLD71": (
        "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d",
        "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    ),
    "GLD88": (
        "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752",
        "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    ),
    "GLD99": (
        None,
        "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
    ),
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_Q6_SREPR_SHA256 = (
    "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"
)
EXPECTED_NORM = {
    "expression_sha256": (
        "c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431"
    ),
    "degree": 548,
    "terms": 451,
    "numerator_sha256": (
        "582f782b1fb1a1824e5d22d8374f52cb25075aab1372f7d06b9607269add79e3"
    ),
    "factors": (
        (1, 36, "fba95ee7da505d8883744a06a8933df8d8d7c4ac2cca316e4990626e92a17fed"),
        (1, 98, "148de9c5a7a44d19e56cd9ae1a554bf67847afb0c58f6e12fa29ac7ddfca9940"),
        (2, 2, "fae3e839d66db547d5697d6fa1a88aa81dfecd3e360d46204801b3b420f3d40b"),
        (2, 43, "ace5cff9ef6fef5a8a62e0a4bd98c3482a066949f3970663a5e446dae97247ca"),
        (2, 99, "eeba65c990e66c56329c3f9ddd1b7623f5b84b11683828352e0cd96b0a928bf9"),
        (4, 2, "59d876136007e0f768ece9df63d326ef21471d26d69a676013fb0eedab51c9eb"),
        (8, 1, "19e8048b6aa1a654dd24c889b7c6aea895c31bb5bba60e3a038dbcbc961ad06d"),
        (110, 1, "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016"),
    ),
}
EXPECTED_RESULTANT = (
    "27648*p**6*(p - 1)**6*(p**2 - p + 1)**19*(2*p**2 - 2*p + 1)"
)
EXPECTED_RESULTANT_SREPR_SHA256 = (
    "73f9ddbc2342851b2bfd79edc880a0c089172ae7b7d6e97a37076eba94420459"
)
EXPECTED_CERTIFICATE_PAYLOAD_SHA256 = "9213a50f96bf6bffa7a8f8fefbd8cca99317f00a1b1863b19e83d1330f79518e"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def assert_source_pins() -> dict[str, dict[str, str]]:
    paths = {"GLD71": GLD71, "GLD88": GLD88, "GLD99": GLD99}
    result = {}
    for name, path in paths.items():
        if not path.exists():
            raise AssertionError(f"missing source: {path}")
        raw = sha256_bytes(path.read_bytes())
        normalized = lf_sha256(path)
        raw_expected, lf_expected = EXPECTED_SOURCE_PINS[name]
        if raw != raw_expected and normalized != lf_expected:
            raise AssertionError(f"{name} source pin mismatch")
        if normalized != lf_expected:
            raise AssertionError(f"{name} normalized source pin mismatch")
        result[name] = {"path": str(path), "sha256": raw, "lf_sha256": normalized}
    return result


def load_gld71():
    spec = importlib.util.spec_from_file_location("gld71_for_gld101_audit", GLD71)
    if spec is None or spec.loader is None:
        raise AssertionError(GLD71)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_certificate_payload() -> dict[str, object]:
    if not CERTIFICATE_PAYLOAD.exists():
        raise AssertionError(f"missing tracked certificate payload: {CERTIFICATE_PAYLOAD}")
    digest = lf_sha256(CERTIFICATE_PAYLOAD)
    if digest != EXPECTED_CERTIFICATE_PAYLOAD_SHA256:
        raise AssertionError(f"certificate payload pin mismatch: {digest}")
    payload = json.loads(CERTIFICATE_PAYLOAD.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise AssertionError("unsupported certificate payload schema")
    if payload.get("certificate_id") != "GLD101-A0-six-selector-norm-cover":
        raise AssertionError("certificate payload id mismatch")
    if payload.get("status") != "scoped_norm_cover_evidence_manifest":
        raise AssertionError("certificate payload status mismatch")
    if payload.get("global_conjecture") != "UNRESOLVED":
        raise AssertionError("certificate payload global status mismatch")
    charts = payload.get("r110_hardchecks", {}).get("charts", {})
    if set(charts) != {"B", "C"}:
        raise AssertionError("certificate payload must contain B and C hardchecks")
    if len(payload.get("r110_hardchecks", {}).get("required_guards", [])) < 10:
        raise AssertionError("certificate payload omitted R110 guards")
    return payload


def q6_expression() -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def h4_a0_family() -> dict[str, sp.Expr]:
    h4_denominator = p + q - 1
    rank_denominator = (
        2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    )
    b_numerator = (
        p**3 * q**2 - p**3 + p**2 * q**3 - 3 * p**2 * q**2 + p**2
        - 2 * p * q**3 + 3 * p * q**2 - 2 * p + q**2 - 3 * q + 2
    )
    c_numerator = (
        p**2 * q**2 - 2 * p**2 * q - 3 * p * q**2 + p * q + p
        - q**2 + 3 * q - 2
    )
    return {
        "s": sp.cancel((p + q - p * q) / h4_denominator),
        "b": sp.cancel(-b_numerator / ((p**2 - p + 1) * rank_denominator)),
        "c": sp.cancel(-c_numerator / (h4_denominator * rank_denominator)),
        "rank_denominator": rank_denominator,
    }


def build_syndrome(gld71):
    relations = gld71.SPARSE_RELATIONS
    support_payload = [
        [index, [[list(indices), coefficient] for indices, coefficient in relations[index]]]
        for index in SUPPORT_ROWS
    ]
    support_digest = hashlib.sha256(
        json.dumps(support_payload, separators=(",", ":")).encode()
    ).hexdigest()
    if support_digest != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError(f"support digest mismatch: {support_digest}")

    family = h4_a0_family()
    leaves = [
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (p, q, family["s"]),
        (sp.Integer(0), 1 + family["b"] + B, 1 + family["c"] + C),
    ]
    matrix_rows = []
    for row in ALL_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                value = sp.Integer(0)
                for indices, coefficient in relations[row]:
                    if indices[0] != root:
                        continue
                    value += sp.Integer(coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(sp.cancel(value))
        matrix_rows.append(entries)
    return sp.Matrix(matrix_rows), family, support_digest


def direct_minors(syndrome: sp.Matrix) -> dict[str, sp.Expr]:
    result = {}
    for name, (rows, columns) in NAMED.items():
        print(f"[GLD101 audit] direct minor {name}", file=sys.stderr, flush=True)
        submatrix = syndrome.extract(list(rows), list(columns))
        value = submatrix.det(method="domain-ge")
        result[name] = sp.cancel(value)
        poly = sp.Poly(result[name], B, C, domain=Kpq)
        if poly.coeff_monomial(1) != 0:
            raise AssertionError(f"{name} has a constant offset term")
        unexpected = sorted(set(poly.monoms()) - set(SIX_COLUMNS))
        if unexpected:
            raise AssertionError(
                f"{name} has unexpected offset monomials: {unexpected}"
            )
    for name, columns in EXTRA.items():
        print(f"[GLD101 audit] direct minor {name}", file=sys.stderr, flush=True)
        submatrix = syndrome.extract(list(RSTAR), list(columns))
        value = submatrix.det(method="domain-ge")
        result[name] = sp.cancel(value)
        poly = sp.Poly(result[name], B, C, domain=Kpq)
        if poly.coeff_monomial(1) != 0:
            raise AssertionError(f"{name} has a constant offset term")
        unexpected = sorted(set(poly.monoms()) - set(SIX_COLUMNS))
        if unexpected:
            raise AssertionError(
                f"{name} has unexpected offset monomials: {unexpected}"
            )
    return result


def selector_from_direct_minors(minors: dict[str, sp.Expr]) -> sp.Expr:
    coefficient_maps = {}
    for name, value in minors.items():
        polynomial = sp.Poly(value, B, C, domain=Kpq)
        coefficient_maps[name] = {
            exp: sp.cancel(polynomial.coeff_monomial(B**exp[0] * C**exp[1]))
            for exp in SIX_COLUMNS
        }
    matrix = sp.Matrix(
        [
            [coefficient_maps[name][exp] for name in SIX_NAMES]
            for exp in SIX_COLUMNS
        ]
    )
    print("[GLD101 audit] direct selector determinant", file=sys.stderr, flush=True)
    return sp.cancel(matrix.det(method="domain-ge"))


def factor_signature(poly: sp.Poly):
    _content, factors = sp.factor_list(poly.as_expr(), p)
    return [
        (
            int(sp.degree(factor, p)),
            int(exponent),
            hashlib.sha256(str(sp.expand(factor)).encode()).hexdigest(),
        )
        for factor, exponent in factors
    ]


def quotient_reduce_rational(selector: sp.Expr, q6: sp.Expr) -> sp.Expr:
    """Canonical degree-<4 representative of a rational q-expression.

    This is an audit-local implementation.  It first forms the direct
    rational selector in QQ(p,q), then performs one denominator inversion in
    QQ(p)[q]/(Q6); the primary instead reduces every sparse arithmetic step.
    """
    numerator, denominator = sp.cancel(selector).as_numer_denom()
    modulus = sp.Poly(q6, q, domain=Kp)
    numerator_poly = sp.Poly(numerator, q, domain=Kp).rem(modulus)
    denominator_poly = sp.Poly(denominator, q, domain=Kp).rem(modulus)
    if denominator_poly.is_zero:
        raise AssertionError("direct selector denominator is zero modulo Q6")
    inverse = sp.invert(denominator_poly, modulus)
    reduced = (numerator_poly * inverse).rem(modulus)
    return sp.cancel(sp.expand(reduced.as_expr()))


def norm_record(selector: sp.Expr, q6: sp.Expr) -> dict[str, object]:
    direct_expression = sp.cancel(selector)
    expression = quotient_reduce_rational(direct_expression, q6)
    numerator, denominator = expression.as_numer_denom()
    numerator_poly = sp.Poly(numerator, p, q, domain=QQ)
    denominator_poly = sp.Poly(denominator, p, q, domain=QQ)
    result = sp.cancel(sp.resultant(q6, numerator_poly.as_expr(), q))
    result_num, result_den = result.as_numer_denom()
    result_poly = sp.Poly(result_num, p, domain=QQ)
    if result_poly.is_zero:
        raise AssertionError("direct selector norm is zero")
    _rational_content, primitive = result_poly.primitive()
    content, factors = sp.factor_list(primitive.as_expr(), p)
    return {
        "direct_expression_sha256": hashlib.sha256(
            sp.srepr(direct_expression).encode()
        ).hexdigest(),
        "expression_sha256": hashlib.sha256(
            sp.srepr(expression).encode()
        ).hexdigest(),
        "denominator": str(denominator_poly.as_expr()),
        "numerator_terms_pq": len(numerator_poly.terms()),
        "norm_denominator": str(result_den),
        "norm_numerator_degree_p": int(result_poly.degree()),
        "norm_numerator_terms_p": len(result_poly.terms()),
        "norm_numerator_sha256": hashlib.sha256(
            str(result_poly.as_expr()).encode()
        ).hexdigest(),
        "primitive_content": str(content),
        "primitive_factorization": [
            {
                "degree": degree,
                "exponent": exponent,
                "sha256": sha,
            }
            for degree, exponent, sha in factor_signature(
                sp.Poly(primitive.as_expr(), p, domain=QQ)
            )
        ],
    }


def assert_norm(record: dict[str, object]) -> None:
    if record["expression_sha256"] != EXPECTED_NORM["expression_sha256"]:
        raise AssertionError(
            "direct quotient selector expression hash mismatch: "
            f"{record['expression_sha256']}"
        )
    if record["norm_numerator_degree_p"] != EXPECTED_NORM["degree"]:
        raise AssertionError("direct norm degree mismatch")
    if record["norm_numerator_terms_p"] != EXPECTED_NORM["terms"]:
        raise AssertionError("direct norm term count mismatch")
    if record["norm_numerator_sha256"] != EXPECTED_NORM["numerator_sha256"]:
        raise AssertionError("direct norm numerator hash mismatch")
    actual = [
        (item["degree"], item["exponent"], item["sha256"])
        for item in record["primitive_factorization"]
    ]
    if actual != list(EXPECTED_NORM["factors"]):
        raise AssertionError("direct norm factor signature mismatch")


def delta_record(q6: sp.Expr, family: dict[str, sp.Expr]) -> dict[str, object]:
    delta = sp.expand(
        (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * family["rank_denominator"]
    )
    resultant = sp.factor(sp.resultant(q6, delta, q))
    if sp.cancel(resultant - sp.sympify(EXPECTED_RESULTANT)) != 0:
        raise AssertionError("direct Delta resultant mismatch")
    # Hash the canonical expanded polynomial while retaining the factored
    # expression in the human-readable report.
    digest = hashlib.sha256(sp.srepr(sp.expand(resultant)).encode()).hexdigest()
    if digest != EXPECTED_RESULTANT_SREPR_SHA256:
        raise AssertionError("direct Delta resultant hash mismatch")
    return {
        "delta": str(delta),
        "resultant": str(resultant),
        "resultant_srepr_sha256": digest,
    }


def _find_run_json(base: Path, expected_sha: str) -> Path | None:
    if not base.exists():
        return None
    matches = [
        path
        for path in base.rglob("run.json")
        if sha256_bytes(path.read_bytes()) == expected_sha
    ]
    if len(matches) != 1:
        raise AssertionError(f"run JSON pin mismatch under {base}: {len(matches)}")
    return matches[0]


def _check_replay(
    label: str,
    source_name: str,
    source_sha: str,
    run_id: str,
    run_json_sha: str,
    run_log_sha: str,
    markers: tuple[str, ...],
    require: bool,
) -> dict[str, object]:
    source = ROOT / ".research-runs" / source_name
    base = ROOT / ".research-runs" / run_id
    if not source.exists() or not base.exists():
        if require:
            raise AssertionError(f"required external replay missing: {label}")
        return {"label": label, "present": False, "required": True}
    if sha256_bytes(source.read_bytes()) != source_sha:
        raise AssertionError(f"{label} source hash mismatch")
    run_json = _find_run_json(base, run_json_sha)
    assert run_json is not None
    run_log = run_json.parent / "run.log"
    if not run_log.exists() or sha256_bytes(run_log.read_bytes()) != run_log_sha:
        raise AssertionError(f"{label} log hash mismatch")
    metadata = json.loads(run_json.read_text(encoding="utf-8"))
    if metadata.get("status") != "succeeded":
        raise AssertionError(f"{label} was not successful")
    log_text = run_log.read_text(encoding="utf-8", errors="replace")
    if any(marker not in log_text for marker in markers):
        raise AssertionError(f"{label} guard marker missing")
    return {
        "label": label,
        "present": True,
        "required": True,
        "source_sha256": source_sha,
        "run_json_sha256": run_json_sha,
        "run_log_sha256": run_log_sha,
        "markers": list(markers),
    }


def external_replays(payload: dict[str, object], require: bool) -> dict[str, object]:
    """Optionally validate ignored pins for a stronger offset-closure claim."""
    if not require:
        return {
            "checked": False,
            "strict_evidence": False,
            "reason": "external offset-fibre replays are not inputs to GLD101",
        }
    entries = []
    p0p1 = ROOT / ".research-runs" / "e31_p0_p1_exact_audit_v10.json"
    p0p1_sha = (
        "1d6bd26f22b875a6a024e8c9d357e4cc5c862efc66e61371dc22b98ec10aaf9f"
    )
    if not p0p1.exists():
        if require:
            raise AssertionError("required p=0,1 package missing")
        entries.append({"label": "p=0,1", "present": False, "required": True})
    else:
        if sha256_bytes(p0p1.read_bytes()) != p0p1_sha:
            raise AssertionError("p=0,1 package pin mismatch")
        p0p1_data = json.loads(p0p1.read_text(encoding="utf-8"))
        if p0p1_data.get("status") != "verified_exact_scoped_local_certificate":
            raise AssertionError("p=0,1 package status mismatch")
        entries.append({
            "label": "p=0,1",
            "present": True,
            "required": True,
            "sha256": p0p1_sha,
        })

    d2d4d8 = (
        ("p^2+1 B", "e31_a0_fibre_d2_fae3e839d66d_B_char0.sing", "f7e46add8faf31fd372efb61877fffedd135bc08154ed1c1aba1a97b9bd4a5b0", "e31-a0-fibre-d2-B-char0-root-v1", "1eb8ad8b7e664637d6e5bc70e729cb4295da7e097d338303a47f8389d2784496"),
        ("p^2+1 C", "e31_a0_fibre_d2_fae3e839d66d_C_char0.sing", "5907c00333f3839f28d9269611866ddb200f868e3db88cad63a4f643a77d35e8", "e31-a0-fibre-d2-C-char0-root-v1", "1f3f83d62dc657cad74a601aba119966680d632a487e6ef281112f141b0368c2"),
        ("R4 B", "e31_a0_fibre_d4_59d876136007_B_char0.sing", "e4cb61031df2185b0fd6f260295fc9e1fc041e5f785f286c71de8e78ec57887d", "e31-a0-fibre-d4-B-char0-root-v1", "f01cbeee30dda06f87d6d17af36d5d4ee36b06dca7fe4af694c486e0d71630a9"),
        ("R4 C", "e31_a0_fibre_d4_59d876136007_C_char0.sing", "d4714da5eabbed1e1e3f8db3b926becbcc581046f6309a7b550e14d0f6ada1f0", "e31-a0-fibre-d4-C-char0-root-v1", "11a058289c47171ed392bb5db6d5ccb2bcb82dc2934b01d10ec2754b161aef4a"),
        ("R8 B", "e31_a0_fibre_d8_19e8048b6aa1_B_char0.sing", "d72331f80fdc90a5be611defed4b04e7d1c631aa14973795f8a3c9e7cf44edcb", "e31-a0-fibre-d8-B-char0-root-v1", "64ec369db5d0275e1a4b32022d5973ac1e8bbf4bde9ff2a02185dc8736eb6c63"),
        ("R8 C", "e31_a0_fibre_d8_19e8048b6aa1_C_char0.sing", "a359e08897e5b1a40d8c9a072ebba8292f92997c7844dfcfcd4c7746204eaebb", "e31-a0-fibre-d8-C-char0-root-v1", "74c2d0d081442665b7008a39c50ea28d91aee6526b2fa994cbc407566c07c5e"),
    )
    for label, source, source_sha, run_id, run_sha in d2d4d8:
        entries.append(_check_replay(
            label, source, source_sha, run_id, run_sha,
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
            ("BASIS_SIZE=1", "UNIT_IDEAL=1"), require,
        ))

    guards = tuple(payload["r110_hardchecks"]["required_guards"])
    for chart_name in ("B", "C"):
        chart = payload["r110_hardchecks"]["charts"][chart_name]
        entries.append(_check_replay(
            f"R110 {chart_name} guarded identity",
            Path(chart["source"]).name,
            chart["source_sha256"], chart["run_id"],
            chart["run_json_sha256"], chart["run_log_sha256"], guards, require,
        ))
    required = [entry for entry in entries if entry["required"]]
    return {
        "checked": True,
        "strict_evidence": bool(required) and all(entry["present"] for entry in required),
        "entries": entries,
        "independence_boundary": "The guarded R110 identities are pinned Singular replays, not an independent derivation of their giant sources.",
    }


def check(require_external: bool = False) -> dict[str, object]:
    started = time.monotonic()
    source_pins = assert_source_pins()
    certificate_payload = load_certificate_payload()
    gld71 = load_gld71()
    syndrome, family, support_digest = build_syndrome(gld71)
    if syndrome.shape != (37, 9):
        raise AssertionError(f"authoritative matrix shape drift: {syndrome.shape}")
    q6 = sp.expand(q6_expression())
    q6_digest = hashlib.sha256(sp.srepr(q6).encode()).hexdigest()
    if q6_digest != EXPECTED_Q6_SREPR_SHA256:
        raise AssertionError("Q6 digest mismatch")
    minors = direct_minors(syndrome)
    selector = selector_from_direct_minors(minors)
    norm = norm_record(selector, q6)
    assert_norm(norm)
    delta = delta_record(q6, family)
    external = external_replays(certificate_payload, require_external)
    result = {
        "status": "exact_independent_audit_GLD101_a0_six_selector_norm_cover",
        "global_conjecture": "UNRESOLVED",
        "scope": {
            "branch": "a=0",
            "matrix": "direct 37x9 authoritative GLD71 syndrome",
            "chart": "locally transcribed GLD88 H4 equal-leaf chart",
            "quotient": "QQ(p)[q]/(Q6)",
            "bridge": "necessary selector implication on nonzero-offset chart only",
        },
        "source_pins": source_pins,
        "certificate_payload": {
            "path": str(CERTIFICATE_PAYLOAD),
            "sha256": EXPECTED_CERTIFICATE_PAYLOAD_SHA256,
        },
        "support_rows": list(SUPPORT_ROWS),
        "support_digest": support_digest,
        "syndrome_shape": list(syndrome.shape),
        "q6": {
            "expression": str(q6),
            "degree_q": int(sp.degree(q6, q)),
            "srepr_sha256": q6_digest,
        },
        "direct_actual_minors": {
            name: {
                "rows": list(NAMED[name][0]) if name in NAMED else list(RSTAR),
                "columns": list(NAMED[name][1]) if name in NAMED else list(EXTRA[name]),
                "expression_srepr_sha256": hashlib.sha256(
                    sp.srepr(minors[name]).encode()
                ).hexdigest(),
                "bc_support": [
                    list(exp)
                    for exp in sorted(sp.Poly(minors[name], B, C, domain=Kpq).monoms())
                ],
            }
            for name in (*NAMED.keys(), *EXTRA.keys())
        },
        "six_selector": {
            "names": list(SIX_NAMES),
            "columns": [list(exp) for exp in SIX_COLUMNS],
            "norm": norm,
        },
        "delta_resultant": delta,
        "external_replays": external,
        "external_offset_evidence_complete": bool(external.get("strict_evidence")),
        "nonclaims": [
            "The audit does not import or trust the primary GLD101 verifier.",
            "Strict external-evidence mode checks both guarded R110 B and C replays by pinned source and log guards.",
            "Ignored Singular leaves are not independently derived here; the tracked manifest records this boundary.",
            "External fibre replays are not composed into an offset-closure theorem.",
            "No selector root is asserted to be a physical rank point.",
            "The global conjecture remains unresolved.",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--require-external-fibre-evidence",
        action="store_true",
        help="also require ignored offset-fibre provenance replays",
    )
    args = parser.parse_args()
    result = check(require_external=args.require_external_fibre_evidence)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print("GLD101 a=0 six-selector direct-matrix audit: PASS")
    print(text)


if __name__ == "__main__":
    main()
