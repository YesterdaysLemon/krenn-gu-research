#!/usr/bin/env python3
"""Verify the scoped GLD101 generic C-open selected-minor leaf.

This checker reconstructs the six named seven-by-seven syndrome minors from
the hash-pinned GLD71 relations and GLD88 equal-leaf H4 chart.  On B=0 each
minor is exactly C times a rational coefficient in QQ(p)[q]/(Q6).  The
primitive numerator of that coefficient is compared with the tracked
Singular source and placed in a 6-by-4 coefficient matrix over QQ[p].

The exact maximal-minor gcd and three exceptional-fibre gcds prove that the
six numerator equations have no common zero on D(H2*Delta).  This is a
one-way, selected-necessary-minor leaf only.  It proves neither a selector
converse nor the P8 parent theorem, full E31 wall, physical incidence claim,
or global Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATES = BASE / "certificates"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD101_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md"
)
GLD101_CANONICAL = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
)
SINGULAR_SOURCE = CERTIFICATES / "GLD101_A0_GENERIC_COPEN_UNIT_SCREEN.singular.txt"
CERTIFICATE = CERTIFICATES / "GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json"

SCHEMA_VERSION = 1
CERTIFICATE_ID = "GLD101-a0-generic-C-open-selected-minor-rank-cover"
EXPECTED_CERTIFICATE_LF_SHA256 = (
    "1f84c1d30c1c8403be477b5def91144f687cc08a4ed5406dffb3866cf6996afb"
)
EXPECTED_SOURCE_PINS = {
    "GLD71": (
        GLD71,
        "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    ),
    "GLD88": (
        GLD88,
        "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    ),
    "GLD101_owner": (
        GLD101_OWNER,
        "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
    ),
    "GLD101_canonical_verifier": (
        GLD101_CANONICAL,
        "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
    ),
    "generic_C_open_Singular_source": (
        SINGULAR_SOURCE,
        "c514d842532f99cde4488cca048c551f39e43ed5cdf2c5ce6a54dcd7aa704850",
    ),
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)

p, q, z = sp.symbols("p q z")
SELECTORS = ("T0", "T1", "T2", "T3", "Y1", "X3")
DECLARATIONS = (
    "Q6",
    "H2",
    "Delta",
    "H_T0",
    "H_T1",
    "H_T2",
    "H_T3",
    "H_Y1",
    "H_X3",
)


class VerificationError(RuntimeError):
    """Fail-closed package or exact-arithmetic mismatch."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def lf_sha256(path: Path) -> str:
    return sha256_bytes(lf_bytes(path))


def validate_source_pins() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for name, (path, expected) in EXPECTED_SOURCE_PINS.items():
        if not path.is_file():
            raise VerificationError(f"missing pinned input {name}: {path}")
        observed = lf_sha256(path)
        if observed != expected:
            raise VerificationError(
                f"{name} LF hash mismatch: expected {expected}, observed {observed}"
            )
        records[name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "lf_sha256": observed,
        }
    return records


def load_canonical_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "gld101_canonical_for_generic_copen_primary", GLD101_CANONICAL
    )
    if spec is None or spec.loader is None:
        raise VerificationError(f"cannot load {GLD101_CANONICAL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_singular_source() -> dict[str, sp.Poly]:
    """Parse declarations from the hash-pinned, generated Singular source."""
    result: dict[str, sp.Poly] = {}
    local = {"p": p, "q": q, "z": z}
    for line in SINGULAR_SOURCE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("poly "):
            continue
        body = line[len("poly ") :]
        if not body.endswith(";") or "=" not in body:
            raise VerificationError(f"malformed Singular declaration: {line[:80]}")
        name, expression = body[:-1].split("=", 1)
        if name not in DECLARATIONS or name in result:
            raise VerificationError(f"unexpected or duplicate declaration: {name}")
        parsed = sp.sympify(expression.replace("^", "**"), locals=local)
        result[name] = sp.Poly(sp.expand(parsed), q, p, z, domain=QQ)
    if tuple(result) != DECLARATIONS:
        raise VerificationError(
            f"Singular declarations drift: {tuple(result)} != {DECLARATIONS}"
        )
    return result


def canonical_primitive(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=QQ)
    if polynomial.is_zero:
        return polynomial
    _denominator, integral = polynomial.clear_denoms(convert=True)
    _content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def term_table(polynomial: sp.Poly) -> list[list[Any]]:
    return [
        [list(monomial), [int(coefficient.p), int(coefficient.q)]]
        for monomial, coefficient in polynomial.terms()
    ]


def polynomial_record(polynomial: sp.Poly, *, include_expression: bool = False) -> dict[str, Any]:
    table = term_table(polynomial)
    record: dict[str, Any] = {
        "sha256": sha256_bytes(
            json.dumps(table, separators=(",", ":")).encode("ascii")
        ),
        "term_count": len(table),
        "total_degree": int(polynomial.total_degree()) if table else -1,
    }
    if include_expression:
        record["expression"] = str(polynomial.as_expr())
    return record


def denominator_record(expression: sp.Expr) -> dict[str, Any]:
    polynomial = sp.Poly(sp.expand(expression), p, domain=QQ)
    if sp.Poly(sp.expand(expression), p, q, domain=QQ).degree(q) != 0:
        raise VerificationError("a selected-minor coefficient denominator depends on q")
    _content, factors = sp.factor_list(polynomial.as_expr(), p)
    allowed = {
        sp.Poly(p**2 - p + 1, p, domain=QQ).monic().as_expr(): "P",
        sp.Poly(2 * p**2 - 2 * p + 1, p, domain=QQ).monic().as_expr(): "H2",
    }
    records = []
    for factor, exponent in factors:
        monic = sp.Poly(factor, p, domain=QQ).monic().as_expr()
        if monic not in allowed:
            raise VerificationError(f"denominator factor outside P*H2: {factor}")
        records.append(
            {
                "name": allowed[monic],
                "factor": str(monic),
                "exponent": int(exponent),
            }
        )
    records.sort(key=lambda item: item["name"])
    return {
        "expression": str(sp.factor(polynomial.as_expr())),
        "factors": records,
        "unit_on_D(H2*Delta)": True,
    }


def reconstruct_equations(canonical: Any) -> tuple[dict[str, sp.Poly], dict[str, Any], Any, Any]:
    algebra, rows, chart, support_digest = canonical.q6_and_source()
    if support_digest != EXPECTED_SUPPORT_DIGEST:
        raise VerificationError(f"support digest mismatch: {support_digest}")

    equations: dict[str, sp.Poly] = {}
    selector_records: dict[str, Any] = {}
    allowed_offset_terms = set(canonical.SIX_COLUMNS)
    for name in SELECTORS:
        if name in canonical.NAMED:
            row_indices, columns = canonical.NAMED[name]
        else:
            row_indices, columns = canonical.RSTAR, canonical.EXTRA[name]
        matrix = [[rows[row][column] for column in columns] for row in row_indices]
        determinant = canonical.det_bc(matrix, f"generic-C-open-{name}")
        unexpected = sorted(set(determinant.terms) - allowed_offset_terms)
        if unexpected:
            raise VerificationError(f"{name} has unexpected offset terms {unexpected}")
        b_zero_terms = {
            exponent: value
            for exponent, value in determinant.terms.items()
            if exponent[0] == 0
        }
        if set(b_zero_terms) != {(0, 1)}:
            raise VerificationError(
                f"{name}|_(B=0) is not exactly C times one coefficient: {sorted(b_zero_terms)}"
            )
        coefficient = sp.cancel(algebra.as_expr(b_zero_terms[(0, 1)]))
        numerator, denominator = coefficient.as_numer_denom()
        primitive = canonical_primitive(numerator, (q, p))
        if primitive.is_zero or primitive.degree(q) > 3:
            raise VerificationError(f"invalid C coefficient numerator for {name}")
        equations[name] = primitive
        selector_records[name] = {
            "rows": list(row_indices),
            "columns": list(columns),
            "B_zero_offset_terms": [[0, 1]],
            "C_coefficient_numerator": polynomial_record(primitive),
            "C_coefficient_denominator": denominator_record(denominator),
        }
    return equations, selector_records, algebra, chart


def primitive_univariate(polynomial: sp.Poly) -> sp.Poly:
    if polynomial.is_zero:
        return polynomial
    _denominator, integral = polynomial.clear_denoms(convert=True)
    _content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def rank_cover(equations: dict[str, sp.Poly], q6: sp.Expr, delta: sp.Expr) -> dict[str, Any]:
    matrix = sp.Matrix(
        [
            [sp.Poly(equations[name].as_expr(), q).nth(degree) for degree in (3, 2, 1, 0)]
            for name in SELECTORS
        ]
    )
    minors: list[dict[str, Any]] = []
    common: sp.Poly | None = None
    for subset in combinations(range(len(SELECTORS)), 4):
        determinant = sp.Poly(
            sp.expand(matrix[list(subset), :].det(method="domain-ge")), p, domain=QQ
        )
        if determinant.is_zero:
            raise VerificationError(f"zero maximal minor for row subset {subset}")
        primitive = primitive_univariate(determinant)
        record = {
            "selectors": [SELECTORS[index] for index in subset],
            **polynomial_record(primitive),
        }
        minors.append(record)
        common = primitive if common is None else primitive_univariate(sp.gcd(common, primitive))
    assert common is not None
    expected = sp.Poly(
        p**15
        * (p - 1) ** 6
        * (p + 1) ** 2
        * (p**2 - p + 1) ** 11
        * (2 * p**2 - 2 * p + 1) ** 14,
        p,
        domain=QQ,
    )
    if common.monic() != expected.monic():
        raise VerificationError(
            f"maximal-minor gcd mismatch: {sp.factor(common.as_expr())}"
        )
    combined_digest = sha256_bytes(
        json.dumps(minors, separators=(",", ":"), sort_keys=True).encode("ascii")
    )

    special: dict[str, Any] = {}
    expected_common = {
        -1: sp.Poly(1, q, domain=QQ),
        0: sp.Poly(q**2, q, domain=QQ),
        1: sp.Poly((q - 1) ** 2, q, domain=QQ),
    }
    for p_value in (-1, 0, 1):
        q6_fibre = sp.Poly(sp.expand(q6.subs(p, p_value)), q, domain=QQ)
        fibre_common = q6_fibre
        for name in SELECTORS:
            fibre_common = sp.gcd(
                fibre_common,
                sp.Poly(equations[name].as_expr().subs(p, p_value), q, domain=QQ),
            )
        fibre_common = fibre_common.monic()
        if fibre_common != expected_common[p_value].monic():
            raise VerificationError(f"unexpected p={p_value} common q-gcd")
        delta_fibre = sp.Poly(sp.expand(delta.subs(p, p_value)), q, domain=QQ)
        q6_delta = sp.gcd(q6_fibre, delta_fibre).monic()
        if p_value in (0, 1) and q6_delta != fibre_common:
            raise VerificationError(f"p={p_value} common roots are not Delta-closed")
        if p_value == -1 and fibre_common.degree() != 0:
            raise VerificationError("p=-1 retains a common root")
        special[str(p_value)] = {
            "common_q_gcd": polynomial_record(fibre_common, include_expression=True),
            "gcd_Q6_Delta": polynomial_record(q6_delta, include_expression=True),
            "disposition": (
                "no common q root"
                if p_value == -1
                else "every common Q6 root lies in Delta=0"
            ),
        }

    return {
        "coefficient_matrix_shape": [6, 4],
        "coefficient_order": ["q^3", "q^2", "q", "1"],
        "maximal_minors": minors,
        "maximal_minors_combined_sha256": combined_digest,
        "maximal_minor_gcd": {
            **polynomial_record(primitive_univariate(common), include_expression=True),
            "factorization": (
                "p^15*(p-1)^6*(p+1)^2*(p^2-p+1)^11*"
                "(2*p^2-2*p+1)^14"
            ),
        },
        "generic_fibre_argument": (
            "off the displayed gcd factors some 4x4 maximal minor is nonzero, "
            "so the six cubics span QQ[p]-specialized polynomials of degree at "
            "most three and cannot have a common q zero"
        ),
        "localization_exclusions": {
            "p^2-p+1": "P is a factor of Delta",
            "2*p^2-2*p+1": "this is H2",
        },
        "special_fibres": special,
        "no_common_zero_on_D(H2*Delta)": True,
    }


def build_certificate() -> dict[str, Any]:
    source_pins = validate_source_pins()
    declarations = parse_singular_source()
    canonical = load_canonical_module()
    equations, selector_records, algebra, chart = reconstruct_equations(canonical)

    q6 = sp.expand(algebra.q6_expr)
    h2 = sp.expand(2 * p**2 - 2 * p + 1)
    delta = sp.expand(canonical.delta_expression(chart))
    expected_base = {"Q6": q6, "H2": h2, "Delta": delta}
    for name, expression in expected_base.items():
        source_expression = declarations[name].as_expr()
        if sp.expand(source_expression - expression) != 0:
            raise VerificationError(f"tracked Singular {name} declaration drift")

    equation_records: dict[str, Any] = {}
    for name in SELECTORS:
        source_poly = canonical_primitive(declarations[f"H_{name}"].as_expr(), (q, p))
        if source_poly != equations[name]:
            raise VerificationError(f"tracked H_{name} differs from reconstructed minor")
        equation_records[name] = polynomial_record(equations[name])

    cover = rank_cover(equations, q6, delta)
    return {
        "schema_version": SCHEMA_VERSION,
        "certificate_id": CERTIFICATE_ID,
        "status": "scoped_exact_selected_necessary_minor_leaf_certificate",
        "global_conjecture": "UNRESOLVED",
        "mathematical_scope": {
            "branch": "normalized a=0 equal-leaf H4 chart with Q6=0",
            "locus": "B=0 and C!=0",
            "open": "D(H2*Delta), including every GLD88 chart denominator encoded in Delta",
            "parameter": "arbitrary p over an algebraically closed field of characteristic zero",
            "selected_necessary_minors": list(SELECTORS),
            "bridge": (
                "rank(M)<=6 makes each selected seven-minor vanish; on B=0 "
                "each selected minor is exactly C times the recorded coefficient, "
                "and C!=0 makes its primitive numerator vanish because its rational "
                "denominator is a unit on D(H2*Delta)"
            ),
            "conclusion": (
                "the six selected-minor numerator equations have no common point "
                "with Q6=0 on B=0, C!=0, D(H2*Delta)"
            ),
            "base_change": (
                "all reconstructed identities and rank-cover calculations are exact "
                "over QQ, hence base-change to any algebraically closed characteristic-zero field"
            ),
            "nonclaims": [
                "no converse from the six selected minors to syndrome rank",
                "no claim on B!=0, C=0, arbitrary a, endpoints, or physical incidence",
                "no P8 parent theorem, full E31 wall closure, or live-frontier promotion",
                "no global Krenn-Gu resolution",
            ],
        },
        "source_pins": source_pins,
        "support_digest": EXPECTED_SUPPORT_DIGEST,
        "selector_definitions": selector_records,
        "equations": equation_records,
        "rank_cover": cover,
        "provenance": {
            "tracked_Singular_source_role": (
                "durable exact coefficient disclosure; its archived Singular process and transcript "
                "are not required by this certificate"
            ),
            "load_bearing_evidence": (
                "canonical syndrome-minor reconstruction, exact source equality, all 15 maximal "
                "minor records, their gcd, and the p=-1,0,1 fibre gcds"
            ),
            "failed_lineage": [
                {
                    "versions": ["generic-copen-cross-audit-v1", "generic-copen-cross-audit-v2"],
                    "status": "failed_non_evidence",
                    "reason": "their archived process-identity checks were not portable or sound",
                },
                {
                    "version": "generic-copen-cross-audit-v3",
                    "status": "accepted_historical_scoped_audit",
                    "role": "source provenance only; this package replaces transcript dependence with the exact rank cover",
                },
            ],
        },
        "reproducible_commands": [
            "python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py",
            "python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py",
            "python -m unittest -v tests.test_gld101_generic_copen_portable_leaf",
        ],
    }


def canonical_json(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def check(write_certificate: bool = False) -> dict[str, Any]:
    payload = build_certificate()
    encoded = canonical_json(payload)
    digest = sha256_bytes(encoded)
    if write_certificate:
        CERTIFICATE.write_bytes(encoded)
    else:
        if not CERTIFICATE.is_file():
            raise VerificationError(f"missing certificate: {CERTIFICATE}")
        observed = lf_bytes(CERTIFICATE)
        if observed != encoded:
            raise VerificationError("tracked certificate differs from exact regeneration")
        if digest != EXPECTED_CERTIFICATE_LF_SHA256:
            raise VerificationError(
                f"certificate pin mismatch: expected {EXPECTED_CERTIFICATE_LF_SHA256}, observed {digest}"
            )
    return {
        "status": "exact_scoped_generic_C_open_rank_cover_verified",
        "global_conjecture": "UNRESOLVED",
        "certificate_lf_sha256": digest,
        "selectors": list(SELECTORS),
        "coefficient_matrix_shape": payload["rank_cover"]["coefficient_matrix_shape"],
        "maximal_minors_checked": len(payload["rank_cover"]["maximal_minors"]),
        "special_fibres_checked": sorted(payload["rank_cover"]["special_fibres"]),
        "no_common_zero_on_D(H2*Delta)": payload["rank_cover"][
            "no_common_zero_on_D(H2*Delta)"
        ],
        "certificate_written": write_certificate,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="regenerate the deterministic tracked certificate before its hash is pinned",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(check(write_certificate=args.write_certificate), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
