#!/usr/bin/env python3
"""Verify the scoped GLD91 two-leaf rank-eight slice exclusion.

The verifier reconstructs the exact GLD84 rank-eight Schur chart from the
committed moving-response builder, including the fixed Gaussian offsets in
the GLD72 centre base.  It derives the two lifted residuals, computes their
exact Q(i) Groebner elimination on

    x9=1, x10=x11=x12=0, x13=t, x14=u,

and checks the finite fibre classification recorded in the companion
certificate.  The sole Schur/frame-open fibre is the GLD85 point, whose
full-intrinsic rank-45 certificate is pinned as an upstream dependency.

This proves only the two-leaf slice statement.  It does not prove that the
full six-leaf pullback is unit or that the global Krenn--Gu conjecture is
resolved.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_survivor_moving_response_builder.py"
CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_certificate.json"
CERTIFICATE_SHA256 = "6b3fb7fbd0b62e88b9027f8d94fcf31d86331e67a3d439dc4ef9bb0d03bbf82f"
GLD75_CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
GLD75_CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"
GLD85_CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_certificate.json"
GLD85_CERTIFICATE_SHA256 = "b037dc23ceebfdbce3db3ee9a48eda1e981d627c044eef45d7d87b86414adf59"

PRIMES = (1_000_000_007, 10_000_019)
EXPECTED_PIVOTS = (0, 1, 2, 3, 4, 5, 7, 8, 12, 17, 19, 26, 52)
EXPECTED_SELECTED_COLUMNS = (
    252, 257, 259, 260, 261, 263, 264, 267, 272, 275,
    284, 285, 286, 288, 289, 431, 433, 434, 435, 437, 438,
    441, 446, 449, 458, 459, 460, 462, 703, 704, 705, 707,
    708, 711, 716, 719, 728, 729, 805, 806, 808, 809, 812,
    855, 2784,
)
EXPECTED_MINOR_RESIDUES = {
    "1000000007": [9_639_769, 249_939_722],
    "10000019": [1_610_829, 5_232_695],
}
ZERO = [0, 1, 0, 1]


def _load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("gld91_moving_builder", BUILDER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.build_moving_response_builder()


def _decode_gaussian(raw: Iterable[int]) -> sp.Expr:
    values = tuple(int(value) for value in raw)
    assert len(values) == 4 and values[1] and values[3]
    return sp.Rational(values[0], values[1]) + sp.I * sp.Rational(values[2], values[3])


def _encode_gaussian(value: sp.Expr) -> list[int]:
    real, imaginary = sp.expand(value).as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    return [int(real.p), int(real.q), int(imaginary.p), int(imaginary.q)]


def _expression_hash(expression: sp.Expr) -> str:
    return hashlib.sha256(sp.srepr(sp.expand(expression)).encode("utf-8")).hexdigest().upper()


def _decode_polynomial(payload: dict[str, Any], variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    assert tuple(payload["variables"]) == tuple(str(variable) for variable in variables)
    expression = 0
    for term in payload["terms"]:
        exponents = tuple(int(value) for value in term["exponents"])
        assert len(exponents) == len(variables)
        value = _decode_gaussian(term["coefficient"])
        for variable, exponent in zip(variables, exponents, strict=True):
            value *= variable**exponent
        expression += value
    polynomial = sp.Poly(sp.expand(expression), *variables, extension=sp.I)
    assert int(payload["degree"]) == polynomial.total_degree()
    assert int(payload["term_count"]) == len(polynomial.terms())
    return polynomial


def _assert_polynomial(
    artifact: dict[str, Any],
    name: str,
    actual: sp.Poly,
    variables: tuple[sp.Symbol, ...],
) -> sp.Poly:
    stored = _decode_polynomial(artifact["polynomials"][name], variables)
    assert stored == actual
    return stored


def _canonical_file_hash(path: Path) -> tuple[str, int]:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest(), len(raw)


def _read_artifact() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "gld91-rank-eight-two-leaf-slice-q-i-v1"
    assert payload["theorem_id"] == "GLD91"
    assert payload["field"] == "Q(i)"
    return payload


def _specialize_residuals(builder: Any, t: sp.Symbol, u: sp.Symbol):
    shifts = builder.chart.shifts
    leaves = {
        shifts[8]: 0,
        shifts[9]: 1,
        shifts[10]: 0,
        shifts[11]: 0,
        shifts[12]: 0,
        shifts[13]: t,
        shifts[14]: u,
    }
    generators = tuple(
        sp.expand(value.subs(shifts[8], 0))
        for value in builder.chart.survivor_generators
    )
    coefficient = sp.Matrix(generators).jacobian(shifts[:8])
    inhomogeneous = sp.Matrix(generators).subs({value: 0 for value in shifts[:8]})
    A = coefficient.subs(leaves).applyfunc(sp.expand)
    q = inhomogeneous.subs(leaves).applyfunc(sp.expand)
    A8 = A[:8, :]
    mu = sp.Poly(sp.expand(A8.det()), t, u, extension=sp.I)
    adj = A8.adjugate()
    residuals = tuple(
        sp.Poly(
            sp.expand(mu.as_expr() * q[row, 0] - (A[row, :] * adj * q[:8, :])[0, 0]),
            t,
            u,
            extension=sp.I,
        )
        for row in (8, 9)
    )
    numerator = -(adj * q[:8, :])
    base_center = builder.chart.centre.subs({shift: 0 for shift in shifts})
    expected_base = sp.Matrix(
        [[-2 - 2 * sp.I, -1 + 2 * sp.I, 3], [0, -3 + 3 * sp.I, 0], [0, -1 + 2 * sp.I, 1]]
    )
    assert base_center == expected_base
    center = sp.Matrix(3, 3, [*list(numerator), 0]) / mu.as_expr() + base_center
    center_num = sp.Poly(
        sp.expand(sp.together(center.det()).as_numer_denom()[0]),
        t,
        u,
        extension=sp.I,
    )
    leaf_det = sp.Poly(sp.expand(builder.chart.leaf.subs(leaves).det()), t, u, extension=sp.I)
    return shifts, leaves, A, q, numerator, mu, residuals, center, center_num, leaf_det


def _q5_and_affine(
    residuals: tuple[sp.Poly, sp.Poly],
    t: sp.Symbol,
    u: sp.Symbol,
):
    basis = sp.groebner([value.as_expr() for value in residuals], u, t, extension=sp.I, order="lex")
    expressions = [poly.as_expr() for poly in basis.polys]
    eliminant = sp.Poly(expressions[-1], t, extension=sp.I).monic()
    factors = sp.factor_list(eliminant.as_expr(), extension=sp.I)[1]
    q5 = next(
        sp.Poly(factor, t, extension=sp.I).monic()
        for factor, multiplicity in factors
        if sp.degree(factor, t) == 5 and multiplicity == 1
    )
    divisor = sp.Poly(t + sp.Rational(2, 3), u, t, extension=sp.I)
    affine = None
    for expression in expressions:
        quotient, remainder = sp.Poly(expression, u, t, extension=sp.I).div(divisor)
        if remainder.is_zero and quotient.degree(u) == 1:
            affine_expression = sp.expand(quotient.as_expr())
            coefficient_u = affine_expression.coeff(u)
            assert coefficient_u != 0
            affine = sp.Poly(sp.expand(affine_expression / coefficient_u), u, t, extension=sp.I)
            break
    assert affine is not None
    u_q5 = sp.Poly(sp.expand(-affine.as_expr().subs(u, 0)), t, extension=sp.I)
    resultant = sp.Poly(
        sp.resultant(residuals[0].as_expr(), residuals[1].as_expr(), u),
        t,
        extension=sp.I,
    ).monic()
    return basis, eliminant, q5, affine, u_q5, resultant


def _reduce(expression: sp.Expr, t: sp.Symbol, modulus: sp.Poly) -> sp.Poly:
    return sp.Poly(sp.expand(expression), t, extension=sp.I).rem(modulus)


def _linear_roots() -> tuple[tuple[sp.Expr, str], ...]:
    return (
        (sp.Integer(0), "t=0"),
        (-sp.Rational(2, 3), "t=-2/3"),
        (-sp.Rational(1, 5) - 3 * sp.I / 5, "t=-1/5-3i/5"),
        (-sp.Rational(6, 13) - 4 * sp.I / 13, "t=-6/13-4i/13"),
        (-1 + sp.I, "t=-1+i"),
    )


def _classify_linear_fibres(
    artifact: dict[str, Any],
    builder: Any,
    shifts: tuple[sp.Symbol, ...],
    A: sp.Matrix,
    q: sp.Matrix,
    numerator: sp.Matrix,
    mu: sp.Poly,
    residuals: tuple[sp.Poly, sp.Poly],
    center_num: sp.Poly,
    leaf_det: sp.Poly,
    t: sp.Symbol,
    u: sp.Symbol,
) -> list[dict[str, Any]]:
    actual_items = []
    center_shifts = tuple(sp.cancel(numerator[index, 0] / mu.as_expr()) for index in range(8))
    for root, label in _linear_roots():
        left = sp.Poly(residuals[0].as_expr().subs(t, root), u, extension=sp.I)
        right = sp.Poly(residuals[1].as_expr().subs(t, root), u, extension=sp.I)
        common = sp.gcd(left, right)
        for u_root in sp.solve(common.as_expr(), u):
            mu_value = sp.factor(mu.as_expr().subs({t: root, u: u_root}), extension=sp.I)
            centre_num_value = sp.factor(center_num.as_expr().subs({t: root, u: u_root}), extension=sp.I)
            leaf_value = sp.factor(leaf_det.as_expr().subs({t: root, u: u_root}), extension=sp.I)
            item = {
                "label": label,
                "t": _encode_gaussian(root),
                "u": _encode_gaussian(u_root),
                "mu": _encode_gaussian(mu_value),
                "centre_det_numerator": _encode_gaussian(centre_num_value),
                "leaf_det": _encode_gaussian(leaf_value),
                "schur_open": mu_value != 0,
                "centre_frame_open": mu_value != 0 and centre_num_value != 0,
                "leaf_frame_open": leaf_value != 0,
            }
            if mu_value == 0:
                item["reason"] = "schur_boundary"
            elif centre_num_value == 0:
                item["reason"] = "centre_frame_boundary"
            else:
                item["reason"] = "pinned_full_intrinsic_rank_point"
                item["full_intrinsic_rank"] = 45
            expected = artifact["fibre_classification"][len(actual_items)]
            assert item == expected
            if mu_value != 0:
                frame_substitutions = {
                    shifts[8]: 0,
                    shifts[9]: 1,
                    shifts[10]: 0,
                    shifts[11]: 0,
                    shifts[12]: 0,
                    shifts[13]: root,
                    shifts[14]: u_root,
                }
                frame_substitutions.update(
                    {shifts[index]: center_shifts[index].subs({t: root, u: u_root}) for index in range(8)}
                )
                frame_determinants = tuple(
                    sp.factor(frame.det().subs(frame_substitutions), extension=sp.I)
                    for frame in builder.chart.frames
                )
                assert frame_determinants[0] == 0 if centre_num_value == 0 else frame_determinants[0] != 0
                assert all(value == leaf_value for value in frame_determinants[1:])
            actual_items.append(item)
    assert len(actual_items) == len(artifact["fibre_classification"]) == 6
    return actual_items


def _check_upstream_gld85(artifact: dict[str, Any]) -> dict[str, Any]:
    raw = GLD85_CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == GLD85_CERTIFICATE_SHA256
    payload = json.loads(raw)
    upstream = artifact["upstream_gld85"]
    assert upstream["certificate_sha256"] == GLD85_CERTIFICATE_SHA256.upper()
    assert tuple(upstream["selected_columns"]) == EXPECTED_SELECTED_COLUMNS
    assert upstream["full_intrinsic_rank"] == 45
    assert upstream["denominator_slots_checked"] == {
        str(prime): 6240 for prime in PRIMES
    }
    assert upstream["minor_residues"] == EXPECTED_MINOR_RESIDUES
    assert payload["selected_columns"] == list(EXPECTED_SELECTED_COLUMNS)
    for record in payload["primes"]:
        assert record["denominator_count"] == 6240
        assert record["denominator_nonzero_count"] == 6240
        assert record["selected_minor_residue"] == EXPECTED_MINOR_RESIDUES[str(record["prime"])]
    return {
        "certificate_sha256": GLD85_CERTIFICATE_SHA256.upper(),
        "full_intrinsic_rank": 45,
        "selected_columns": list(EXPECTED_SELECTED_COLUMNS),
        "minor_residues": EXPECTED_MINOR_RESIDUES,
    }


def check() -> dict[str, Any]:
    artifact = _read_artifact()
    for key, expected_path, expected_hash in (
        ("gld75_certificate", GLD75_CERTIFICATE, GLD75_CERTIFICATE_SHA256.upper()),
        ("gld85_certificate", GLD85_CERTIFICATE, GLD85_CERTIFICATE_SHA256.upper()),
    ):
        path_record = artifact["source_files"][key]
        assert path_record["path"] == str(expected_path.relative_to(ROOT)).replace("\\", "/")
        digest, byte_count = _canonical_file_hash(expected_path)
        assert digest.upper() == expected_hash
        assert path_record["sha256"] == expected_hash
        assert path_record["bytes"] == byte_count

    builder = _load_builder()
    t, u = sp.symbols("t u")
    shifts, leaves, A, q, numerator, mu, residuals, _center, center_num, leaf_det = _specialize_residuals(builder, t, u)
    assert leaves[shifts[8]] == 0 and leaves[shifts[9]] == 1
    assert A.shape == (10, 8) and q.shape == (10, 1)
    expected_base = sp.Matrix(
        [[-2 - 2 * sp.I, -1 + 2 * sp.I, 3], [0, -3 + 3 * sp.I, 0], [0, -1 + 2 * sp.I, 1]]
    )
    stored_base = sp.Matrix(
        [[_decode_gaussian(value) for value in row] for row in artifact["chart"]["centre_base"]]
    )
    assert stored_base == expected_base
    _assert_polynomial(artifact, "rho8", residuals[0], (t, u))
    _assert_polynomial(artifact, "rho9", residuals[1], (t, u))
    _assert_polynomial(artifact, "mu", mu, (t, u))
    _assert_polynomial(artifact, "centre_det_numerator", center_num, (t, u))
    _assert_polynomial(artifact, "leaf_det", leaf_det, (t, u))
    assert _expression_hash(mu.as_expr()) == artifact["canonical_expression_hashes"]["mu"]
    assert _expression_hash(center_num.as_expr()) == artifact["canonical_expression_hashes"]["centre_det_numerator"]

    basis, eliminant, q5, affine, u_q5, resultant = _q5_and_affine(residuals, t, u)
    frame_basis = sp.groebner(
        [residuals[0].as_expr(), residuals[1].as_expr(), center_num.as_expr()],
        u,
        t,
        extension=sp.I,
        order="lex",
    )
    frame_elimination = [poly.as_expr() for poly in frame_basis.polys if not poly.as_expr().has(u)]
    assert len(frame_elimination) == 1
    frame_eliminant = sp.Poly(frame_elimination[0], t, extension=sp.I).monic()
    _assert_polynomial(artifact, "residual_eliminant", eliminant, (t,))
    _assert_polynomial(artifact, "residual_resultant", resultant, (t,))
    _assert_polynomial(artifact, "frame_eliminant", frame_eliminant, (t,))
    _assert_polynomial(artifact, "q5", q5, (t,))
    _assert_polynomial(artifact, "affine_relation", affine, (u, t))
    _assert_polynomial(artifact, "u_q5", u_q5, (t,))
    groebner_metadata = artifact["groebner"]
    assert len(basis.polys) == groebner_metadata["residual_basis_length"] == 3
    assert [poly.total_degree() for poly in basis.polys] == groebner_metadata["residual_basis_degrees"] == [9, 9, 10]
    assert [len(poly.terms()) for poly in basis.polys] == groebner_metadata["residual_basis_term_counts"] == [12, 12, 10]
    assert eliminant.degree() == groebner_metadata["residual_eliminant_degree"] == 10
    assert resultant.degree() == groebner_metadata["residual_resultant_degree"] == 11
    assert len(frame_basis.polys) == groebner_metadata["frame_basis_length"] == 2
    assert frame_eliminant.degree() == groebner_metadata["frame_eliminant_degree"] == 10
    assert frame_eliminant == eliminant
    assert sp.gcd(q5, q5.diff()).degree() == 0
    assert groebner_metadata["q5_squarefree"] is True
    assert _encode_gaussian(q5.eval(-sp.Rational(2, 3))) == groebner_metadata["q5_at_minus_two_thirds"]
    assert _expression_hash(q5.as_expr()) == artifact["canonical_expression_hashes"]["q5"]
    assert _expression_hash(affine.as_expr()) == artifact["canonical_expression_hashes"]["affine_relation"]
    assert _expression_hash(u_q5.as_expr()) == artifact["canonical_expression_hashes"]["u_q5"]

    reductions = {
        "rho8": _reduce(residuals[0].as_expr().subs(u, u_q5.as_expr()), t, q5),
        "rho9": _reduce(residuals[1].as_expr().subs(u, u_q5.as_expr()), t, q5),
        "mu": _reduce(mu.as_expr().subs(u, u_q5.as_expr()), t, q5),
        "centre_det_numerator": _reduce(center_num.as_expr().subs(u, u_q5.as_expr()), t, q5),
    }
    for name, value in reductions.items():
        stored = _decode_polynomial(artifact["q5_reductions"][name], (t,))
        assert stored == value and value.is_zero

    fibres = _classify_linear_fibres(
        artifact,
        builder,
        shifts,
        A,
        q,
        numerator,
        mu,
        residuals,
        center_num,
        leaf_det,
        t,
        u,
    )
    upstream = _check_upstream_gld85(artifact)
    open_slice = artifact["open_slice"]
    assert open_slice["linear_fibre_count"] == 6
    assert open_slice["q5_component_degree"] == 5
    assert open_slice["resultant_length"] == 11
    assert open_slice["schur_frame_open_count"] == 1
    assert open_slice["open_label"] == "t=-2/3,u=0"
    scope = artifact["scope"]
    q5_component = artifact["q5_component"]
    assert q5_component["degree"] == 5
    assert q5_component["residual_point_count_over_algebraic_closure"] == 5
    assert q5_component["mu_reduction_is_zero"] is True
    assert scope["full_chart_unit_ideal_proved"] is False
    assert scope["full_chart_residual_proved_empty"] is False
    assert scope["slice_residual_fitting_zero_locus_empty_on_schur_frame_open"] is True
    assert scope["omitted_offset_bug_corrected"] is True
    assert scope["global_conjecture_resolved"] is False
    return {
        "status": "exact_characteristic_zero_rank_eight_two_leaf_slice_intrinsic_fitting_exclusion",
        "theorem_id": "GLD91",
        "field": "Q(i)",
        "slice": "x9=1, x10=x11=x12=0, x13=t, x14=u, x8=0",
        "residual_groebner_basis": {
            "length": len(basis.polys),
            "degrees": [poly.total_degree() for poly in basis.polys],
            "terms": [len(poly.terms()) for poly in basis.polys],
            "eliminant_degree": eliminant.degree(),
            "resultant_degree": resultant.degree(),
        },
        "linear_fibre_count": len(fibres),
        "q5_component_degree": q5.degree(),
        "schur_frame_open_fibre_count": open_slice["schur_frame_open_count"],
        "schur_frame_open_fibre": open_slice["open_label"],
        "upstream_gld85": upstream,
        "conclusion": "V(I_Pl) is empty on this two-leaf slice after restricting to the named Schur/frame open",
        "full_chart_unit_ideal_proved": False,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    print("four-root rank-eight two-leaf slice GLD91 primary: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
