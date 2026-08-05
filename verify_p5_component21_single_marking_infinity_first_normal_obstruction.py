#!/usr/bin/env python3
"""Verify the component-21 h0-infinity boundary and its joint normal."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

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
THEOREM = ROOT / "P5_COMPONENT21_SINGLE_MARKING_INFINITY_FIRST_NORMAL_OBSTRUCTION.md"
PINNED = {
    ROOT
    / "P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "41b9f45ef5f65efc6706a3757d5def9318015ec2c25dcda5c111a13aa5c16495"
    ),
    ROOT
    / "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "a395cefece221d2c6df797b55b9f900144a0cea95d568d8633ffb89ab495aaff"
    ),
    ROOT
    / "audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "c098f94bf73f9a58b060314647c6048324bef2198509511561f87ec670831d8a"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_bases(
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        add(cap_a, scale(p, cap_b)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        add(cap_c, scale(q, cap_b)),
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )


def h0_infinity_bases(
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    other_shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, (sp.Integer(0),) + other_shifts))
    beta[0] = alpha[0]
    return alpha, tuple(beta)


def joint_normal_bases(
    cap_p: sp.Expr,
    cap_s: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    other_shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    """First coefficient after p=tP, s=tS at (p,s)=(0,0)."""
    alpha, canonical_beta = finite_bases(sp.Integer(0), q, kappa, ell)
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    alpha = list(alpha)
    beta = list(mark(tuple(alpha), canonical_beta, (sp.Integer(0),) + other_shifts))
    alpha[0] = scale(cap_p, cap_b)
    beta[0] = add(scale(cap_p, cap_b), scale(cap_s, add(cap_c, scale(q, cap_b))))
    return tuple(alpha), tuple(beta)


def monomial_normal_bases(
    cap_p: sp.Expr,
    cap_r: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    other_shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    """Leading pure pair for the monomial ideal (p, s*q)."""
    alpha, canonical_beta = finite_bases(sp.Integer(0), sp.Integer(0), kappa, ell)
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    alpha = list(alpha)
    beta = list(mark(tuple(alpha), canonical_beta, (sp.Integer(0),) + other_shifts))
    alpha[0] = scale(cap_p, cap_b)
    beta[0] = scale(cap_p + cap_r, cap_b)
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
    p, q, kappa, ell, cap_p, cap_s, cap_r, t = sp.symbols("p q kappa ell P S R t")
    h1, h2, h3 = sp.symbols("h1 h2 h3")
    other_shifts = (h1, h2, h3)

    finite_alpha, finite_beta = finite_bases(p, q, kappa, ell)
    finite_marked = mark(finite_alpha, finite_beta, (sp.Integer(0),) + other_shifts)
    h0_chart_beta = list(finite_marked)
    h0_chart_beta[0] = add(finite_alpha[0], scale(t, finite_beta[0]))
    h0_chart_support = pure_support(finite_alpha, tuple(h0_chart_beta))
    assert h0_chart_support == {"0111": "4*p", "1111": "4*(p + q*t)"}

    boundary_alpha, boundary_beta = h0_infinity_bases(p, q, kappa, ell, other_shifts)
    boundary_support = pure_support(boundary_alpha, boundary_beta)
    assert boundary_support == {"0111": "4*p", "1111": "4*p"}
    boundary_certificates = four_unit_certificates(
        "h0_infinity_boundary",
        boundary_alpha,
        boundary_beta,
        (p, q, kappa, ell, h1, h2, h3),
    )

    normal_alpha, normal_beta = joint_normal_bases(
        cap_p, cap_s, q, kappa, ell, other_shifts
    )
    normal_support = pure_support(normal_alpha, normal_beta)
    assert normal_support == {
        "0111": "4*P",
        "1111": "4*(P + S*q)",
    }

    # This is a coefficient identity for the whole pure tensor, not a claim
    # that a row-wise subtraction is a legal basis change at the central point.
    joint_alpha, joint_canonical_beta = finite_bases(t * cap_p, q, kappa, ell)
    joint_marked = list(
        mark(joint_alpha, joint_canonical_beta, (sp.Integer(0),) + other_shifts)
    )
    joint_marked[0] = add(joint_alpha[0], scale(t * cap_s, joint_canonical_beta[0]))
    joint_support = pure_support(joint_alpha, tuple(joint_marked))
    assert joint_support == {
        "0111": "4*P*t",
        "1111": "4*t*(P + S*q)",
    }

    normal_certificates = four_unit_certificates(
        "joint_normal",
        normal_alpha,
        normal_beta,
        (cap_p, cap_s, q, kappa, ell, h1, h2, h3),
    )

    monomial_alpha, monomial_beta = monomial_normal_bases(
        cap_p, cap_r, kappa, ell, other_shifts
    )
    monomial_support = pure_support(monomial_alpha, monomial_beta)
    assert monomial_support == {
        "0111": "4*P",
        "1111": "4*(P + R)",
    }
    monomial_certificates = four_unit_certificates(
        "p_sq_monomial_normal",
        monomial_alpha,
        monomial_beta,
        (cap_p, cap_r, kappa, ell, h1, h2, h3),
    )

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "joint `(s,p)`-normal residual",
        "monomial `(p,sq)` normal",
        "does not use pure support as a transfer theorem",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "h0_infinity_chart_pure_support": h0_chart_support,
                "h0_infinity_boundary_pure_support": boundary_support,
                "h0_infinity_boundary_unit_ideals": boundary_certificates,
                "joint_normal_residual_pair": [
                    "P*B",
                    "P*B + S*(C+q*B)",
                ],
                "joint_normal_pure_support": normal_support,
                "joint_normal_unit_ideals": normal_certificates,
                "joint_normal_projective_direction": "[S:P]",
                "p_sq_monomial_normal_residual_pair": [
                    "P*B",
                    "(P+R)*B",
                ],
                "p_sq_monomial_normal_pure_support": monomial_support,
                "p_sq_monomial_normal_unit_ideals": monomial_certificates,
                "dvr_puiseux_order": "min(v(p), v(s)+v(q))",
                "pure_support_transfer_used": False,
                "other_marking_infinities_closed": False,
                "multiple_marking_extension_source_ambient_closed": False,
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
