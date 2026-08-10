#!/usr/bin/env python3
"""Verify all six component-21 pairwise marking-pole weighted normals."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction import (
    MIXED,
    WORDS,
    add,
    contraction,
    contraction_obstruction_map,
    h31_coefficients,
    h31_obstruction_map,
    mark,
    pure_support,
    scale,
    unit_groebner,
)

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_PAIRWISE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md"
PINNED = {
    ROOT / "P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "8e3e61aac9216a0e5c1a58625a8d7c9b3c1b249de2ba4c1bd19e2e96ad420188"
    ),
    ROOT
    / "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "3763c98bff301e16823b34a55b4a40881378a1499d74e1c419e7eb1250c85004"
    ),
    ROOT
    / "audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "09ffc0a2b29491b77d25233d240db4a68feaa5f0c3f6b3089257329849db9d79"
    ),
}
ZERO = (sp.Integer(0),) * 4
CAP_A = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
CAP_C = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
CAP_B = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
CAP_D = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_bases(
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    return (
        add(CAP_A, scale(p, CAP_B)),
        add(scale(ell, CAP_A), CAP_C),
        CAP_C,
        CAP_D,
    ), (
        add(CAP_C, scale(q, CAP_B)),
        CAP_A,
        add(CAP_B, scale(kappa, CAP_A)),
        add(CAP_A, scale(ell, CAP_C)),
    )


def pair_chart_bases(
    pair: tuple[int, int],
    s: sp.Expr,
    t: sp.Expr,
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
            tuple(0 if index in pair else shifts[index] for index in range(4)),
        )
    )
    beta[pair[0]] = add(alpha[pair[0]], scale(s, canonical_beta[pair[0]]))
    beta[pair[1]] = add(alpha[pair[1]], scale(t, canonical_beta[pair[1]]))
    return alpha, tuple(beta)


def pair_weighted_normal_bases(
    pair: tuple[int, int],
    cap_p: sp.Expr,
    cap_q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    """Residual for the two monomials controlling a pairwise marking corner."""
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    beta = list(
        mark(
            alpha,
            canonical_beta,
            tuple(0 if index in pair else shifts[index] for index in range(4)),
        )
    )
    alpha = list(alpha)
    if pair[0] == 0:
        alpha[0] = scale(cap_p, CAP_B)
        beta[0] = scale(cap_p + cap_q, CAP_B)
        alpha[pair[1]] = ZERO
        beta[pair[1]] = canonical_beta[pair[1]]
    else:
        alpha[0] = scale(cap_p, CAP_B)
        beta[0] = scale(shifts[0] * cap_p + cap_q, CAP_B)
        for index in pair:
            alpha[index] = ZERO
            beta[index] = canonical_beta[index]
    return tuple(alpha), tuple(beta)


def four_unit_certificates(
    label_prefix: str,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, dict[str, int | bool]]:
    slope = sp.Symbol("lambda")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    results = {}
    for distinguished in (0, 1):
        coefficients = h31_coefficients(distinguished, alpha, beta, extension)
        assert coefficients[WORDS[0]] == 0
    for distinguished in (2, 3):
        coefficients = h31_coefficients(distinguished, alpha, beta, extension)
        vector = sp.Matrix(extension)
        mixed = sp.Matrix(
            [
                [sp.diff(coefficients[word], value) for value in extension]
                for word in MIXED
            ]
        )
        diagonal_alpha = sp.Matrix(
            [[sp.diff(coefficients[WORDS[0]], value) for value in extension]]
        )
        diagonal_beta = sp.Matrix(
            [[sp.diff(coefficients[WORDS[-1]], value) for value in extension]]
        )
        equations = tuple(mixed * vector) + (
            sp.expand((diagonal_alpha * vector)[0] - 1),
            sp.expand(inverse * (diagonal_beta * vector)[0] - 1),
            *tuple(h31_obstruction_map(distinguished, alpha, beta, extension)),
        )
        label = f"{label_prefix}_H31_d{distinguished}"
        results[label] = unit_groebner(
            label, equations, extension + (inverse,) + retained
        )
    for chart in ("finite", "infinity"):
        _, _, d01 = contraction(alpha, beta, extension, "D01", chart, slope)
        d23_alpha, d23_beta, d23 = contraction(
            alpha, beta, extension, "D23", chart, slope
        )
        assert d01[WORDS[0]] == 0
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
        label = f"{label_prefix}_H22_{chart}_weight"
        results[label] = unit_groebner(
            label,
            equations,
            extension + (inverse_a, inverse_b) + chart_retained,
        )
    assert len(results) == 4
    return results


def main() -> None:
    p, q, kappa, ell, s, t, cap_p, cap_q = sp.symbols(
        "p q kappa ell s t P Q"
    )
    shifts = sp.symbols("h0:4")
    results = {}
    for pair in PAIRS:
        label = f"h{pair[0]}_h{pair[1]}_infinity"
        chart_alpha, chart_beta = pair_chart_bases(
            pair, s, t, p, q, kappa, ell, shifts
        )
        chart_support = pure_support(chart_alpha, chart_beta)
        if pair[0] == 0:
            expected_chart = {
                "0111": "4*p*t",
                "1111": "4*t*(p + q*s)",
            }
            order = "min(v(s_j)+v(p), v(s_0)+v(s_j)+v(q))"
            monomials = ("s_j*p", "s_0*s_j*q")
        else:
            expected_chart = {
                "0111": "4*p*s*t",
                "1111": "4*s*t*(h0*p + q)",
            }
            order = "min(v(s_i)+v(s_j)+v(p), v(s_i)+v(s_j)+v(q))"
            monomials = ("s_i*s_j*p", "s_i*s_j*q")
        assert chart_support == expected_chart
        boundary_alpha, boundary_beta = pair_chart_bases(
            pair, 0, 0, p, q, kappa, ell, shifts
        )
        assert pure_support(boundary_alpha, boundary_beta) == {}

        normal_alpha, normal_beta = pair_weighted_normal_bases(
            pair, cap_p, cap_q, kappa, ell, shifts
        )
        normal_support = pure_support(normal_alpha, normal_beta)
        if pair[0] == 0:
            expected_normal = {"0111": "4*P", "1111": "4*(P + Q)"}
        else:
            expected_normal = {"0111": "4*P", "1111": "4*(P*h0 + Q)"}
        assert normal_support == expected_normal
        retained = (cap_p, cap_q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index not in pair
        )
        certificates = four_unit_certificates(
            f"h{pair[0]}_h{pair[1]}_weighted_normal",
            normal_alpha,
            normal_beta,
            retained,
        )
        results[label] = {
            "pair": list(pair),
            "homogeneous_chart_pure_support": chart_support,
            "corner_pure_support": {},
            "controlling_monomials": list(monomials),
            "dvr_puiseux_order": order,
            "weighted_normal_pure_support": normal_support,
            "weighted_normal_unit_ideals": certificates,
        }

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "all six pairwise simultaneous marking-pole corners",
        "Triple and quadruple marking poles remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "pairwise_marking_infinity_pairs": [list(pair) for pair in PAIRS],
                "charts": results,
                "unit_ideals": 4 * len(PAIRS),
                "pure_support_transfer_used": False,
                "triple_marking_poles_closed": False,
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
