#!/usr/bin/env python3
"""Verify component 21's triple/quadruple marking-pole weighted normals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction import (
    CAP_B,
    WORDS,
    ZERO,
    add,
    contraction,
    contraction_obstruction_map,
    finite_bases,
    h31_coefficients,
    mark,
    pure_support,
    scale,
    unit_groebner,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_COMPONENT21_TRIPLE_QUADRUPLE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md"
)
PINNED = {
    ROOT / "P5_COMPONENT21_PAIRWISE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md": (
        "3655ee5dae9b04c4cf23cad1d5b968c585f9f29735cd7d07a7dc0b2ed5242c4d"
    ),
    ROOT / "verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py": (
        "e6a1045616e9e19731c04637a62085f1f9fe6d4a3add74a5cfa0b72ccadea758"
    ),
    ROOT / "audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py": (
        "732999a18eb07550d93d486f7271118214ce078aa1bd0a3e5685ab5332760028"
    ),
}
MIXED = WORDS[1:-1]
POLE_SETS = ((1, 2, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3), (0, 1, 2, 3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marking_chart_bases(
    poles: tuple[int, ...],
    inverse_markings: tuple[sp.Expr, ...],
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(
        mark(
            alpha,
            canonical_beta,
            tuple(0 if index in poles else shifts[index] for index in range(4)),
        )
    )
    for index in poles:
        beta[index] = add(
            alpha[index], scale(inverse_markings[index], canonical_beta[index])
        )
    return alpha, tuple(beta)


def weighted_normal_bases(
    poles: tuple[int, ...],
    cap_p: sp.Expr,
    cap_q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    beta = list(
        mark(
            alpha,
            canonical_beta,
            tuple(0 if index in poles else shifts[index] for index in range(4)),
        )
    )
    alpha = list(alpha)
    alpha[0] = scale(cap_p, CAP_B)
    if 0 in poles:
        beta[0] = scale(cap_p + cap_q, CAP_B)
        nonzero_poles = tuple(index for index in poles if index != 0)
    else:
        beta[0] = scale(shifts[0] * cap_p + cap_q, CAP_B)
        nonzero_poles = poles
    for index in nonzero_poles:
        alpha[index] = ZERO
        beta[index] = canonical_beta[index]
    return tuple(alpha), tuple(beta)


def h31_hall_deficiencies(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, bool]:
    extension = sp.symbols("z0:8")
    result = {}
    for distinguished in range(4):
        all_alpha = h31_coefficients(distinguished, alpha, beta, extension)[WORDS[0]]
        assert sp.expand(all_alpha) == 0
        result[f"distinguished_{distinguished}"] = True
    return result


def h22_unit_certificates(
    prefix: str,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, dict[str, int | bool]]:
    slope = sp.Symbol("lambda")
    extension = sp.symbols("z0:8")
    inverse_a, inverse_b = sp.symbols("u w")
    results = {}
    for chart in ("finite", "infinity"):
        _, _, d01 = contraction(alpha, beta, extension, "D01", chart, slope)
        d23_alpha, d23_beta, d23 = contraction(
            alpha, beta, extension, "D23", chart, slope
        )
        assert sp.expand(d01[WORDS[0]]) == 0
        vector = sp.Matrix(extension)
        mixed = sp.Matrix(
            [[sp.diff(d23[word], value) for value in extension] for word in MIXED]
        )
        equations = (
            *(d01[word] for word in WORDS[:-1]),
            sp.expand(d01[WORDS[-1]] - 1),
            *tuple(mixed * vector),
            sp.expand(inverse_a * d23[WORDS[0]] - 1),
            sp.expand(inverse_b * d23[WORDS[-1]] - 1),
            *tuple(contraction_obstruction_map(d23_alpha, d23_beta)),
        )
        chart_retained = retained + ((slope,) if chart == "finite" else ())
        label = f"{prefix}_H22_{chart}_weight"
        results[label] = unit_groebner(
            label,
            equations,
            extension + (inverse_a, inverse_b) + chart_retained,
        )
    assert len(results) == 2
    return results


def main() -> None:
    p, q, kappa, ell, cap_p, cap_q = sp.symbols("p q kappa ell P Q")
    inverse_markings = sp.symbols("s0:4")
    shifts = sp.symbols("h0:4")
    results = {}
    for poles in POLE_SETS:
        label = "_".join(f"h{index}" for index in poles) + "_infinity"
        chart_alpha, chart_beta = marking_chart_bases(
            poles, inverse_markings, p, q, kappa, ell, shifts
        )
        chart_support = pure_support(chart_alpha, chart_beta)
        nonzero_poles = tuple(index for index in poles if index != 0)
        product_s = sp.prod(inverse_markings[index] for index in nonzero_poles)
        if 0 in poles:
            expected_chart = {
                "0111": str(sp.factor(4 * product_s * p)),
                "1111": str(
                    sp.factor(4 * product_s * (p + inverse_markings[0] * q))
                ),
            }
            order = "min(v(S)+v(p), v(s_0)+v(S)+v(q))"
            monomials = ("S*p", "s_0*S*q")
        else:
            expected_chart = {
                "0111": str(sp.factor(4 * product_s * p)),
                "1111": str(sp.factor(4 * product_s * (shifts[0] * p + q))),
            }
            order = "min(v(S)+v(p), v(S)+v(q))"
            monomials = ("S*p", "S*q")
        assert chart_support == expected_chart
        boundary_inverse = tuple(
            sp.Integer(0) if index in poles else inverse_markings[index]
            for index in range(4)
        )
        boundary_alpha, boundary_beta = marking_chart_bases(
            poles, boundary_inverse, p, q, kappa, ell, shifts
        )
        assert pure_support(boundary_alpha, boundary_beta) == {}

        normal_alpha, normal_beta = weighted_normal_bases(
            poles, cap_p, cap_q, kappa, ell, shifts
        )
        normal_support = pure_support(normal_alpha, normal_beta)
        if 0 in poles:
            expected_normal = {"0111": "4*P", "1111": "4*(P + Q)"}
        else:
            expected_normal = {"0111": "4*P", "1111": "4*(P*h0 + Q)"}
        assert normal_support == expected_normal
        retained = (cap_p, cap_q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index not in poles
        )
        hall = h31_hall_deficiencies(normal_alpha, normal_beta)
        certificates = h22_unit_certificates(
            "_".join(f"h{index}" for index in poles) + "_weighted_normal",
            normal_alpha,
            normal_beta,
            retained,
        )
        results[label] = {
            "poles": list(poles),
            "homogeneous_chart_pure_support": chart_support,
            "corner_pure_support": {},
            "controlling_monomials": list(monomials),
            "dvr_puiseux_order": order,
            "weighted_normal_pure_support": normal_support,
            "h31_all_alpha_hall_deficiencies": hall,
            "h22_weighted_normal_unit_ideals": certificates,
        }

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "the four triple and one quadruple simultaneous marking-pole corners",
        "all-alpha diagonal is identically zero",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "triple_quadruple_marking_infinity_pole_sets": [
                    list(poles) for poles in POLE_SETS
                ],
                "charts": results,
                "h31_hall_deficient_orientations": 4 * len(POLE_SETS),
                "h22_unit_ideals": 2 * len(POLE_SETS),
                "pure_support_transfer_used": False,
                "all_triple_quadruple_nonzero_P4_weighted_normals_closed": True,
                "parameter_boundary_intersections_closed": False,
                "zero_P4_restriction_ambient_leading_term_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "dependency_hashes": dependency_hashes,
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
