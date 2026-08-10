#!/usr/bin/env python3
"""Verify component 21's h1/h2/h3 single-pole weighted normals."""

from __future__ import annotations

import hashlib
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
THEOREM = (
    ROOT
    / "P5_COMPONENT21_OTHER_SINGLE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md"
)
PINNED = {
    ROOT
    / "P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "77bc53e3451358bfc4764fce5e82f870040bf63846b556522a25e6e95d4da8e7"
    ),
    ROOT
    / "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "c4cebc5eb8ea6f1fe63e83d9ad472c1208cce880dff32b1c8fb75682e78c9ecb"
    ),
    ROOT
    / "audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "3336ca78627ca3bc6ef7d69954be7319e7948a7733c52eb5da6a8ad2d9c5c541"
    ),
}
ZERO = (sp.Integer(0),) * 4
CAP_A = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
CAP_C = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
CAP_B = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
CAP_D = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))


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


def finite_other_shifts(
    mode: int,
    shifts: tuple[sp.Expr, ...],
) -> tuple[sp.Expr, ...]:
    return tuple(sp.Integer(0) if index == mode else shifts[index] for index in range(4))


def homogeneous_chart_bases(
    mode: int,
    s: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, finite_other_shifts(mode, shifts)))
    beta[mode] = add(alpha[mode], scale(s, canonical_beta[mode]))
    return alpha, tuple(beta)


def first_normal_bases(
    mode: int,
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, finite_other_shifts(mode, shifts)))
    alpha = list(alpha)
    alpha[mode] = ZERO
    beta[mode] = canonical_beta[mode]
    return tuple(alpha), tuple(beta)


def weighted_normal_bases(
    mode: int,
    cap_p: sp.Expr,
    cap_q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    """Residual for leading coefficients of the monomials s_i*p and s_i*q."""
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    beta = list(mark(alpha, canonical_beta, finite_other_shifts(mode, shifts)))
    alpha = list(alpha)
    alpha[0] = scale(cap_p, CAP_B)
    beta[0] = scale(shifts[0] * cap_p + cap_q, CAP_B)
    alpha[mode] = ZERO
    beta[mode] = canonical_beta[mode]
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
    p, q, kappa, ell, s, cap_p, cap_q, t = sp.symbols(
        "p q kappa ell s P Q t"
    )
    shifts = sp.symbols("h0:4")
    results = {}
    for mode in (1, 2, 3):
        retained = (p, q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index != mode
        )
        chart_alpha, chart_beta = homogeneous_chart_bases(
            mode, s, p, q, kappa, ell, shifts
        )
        chart_support = pure_support(chart_alpha, chart_beta)
        assert chart_support == {
            "0111": "4*p*s",
            "1111": "4*s*(h0*p + q)",
        }
        boundary_alpha, boundary_beta = homogeneous_chart_bases(
            mode, 0, p, q, kappa, ell, shifts
        )
        assert pure_support(boundary_alpha, boundary_beta) == {}

        normal_alpha, normal_beta = first_normal_bases(
            mode, p, q, kappa, ell, shifts
        )
        normal_support = pure_support(normal_alpha, normal_beta)
        assert normal_support == {
            "0111": "4*p",
            "1111": "4*(h0*p + q)",
        }
        first_certificates = four_unit_certificates(
            f"h{mode}_first_normal",
            normal_alpha,
            normal_beta,
            retained,
        )

        weighted_alpha, weighted_beta = weighted_normal_bases(
            mode, cap_p, cap_q, kappa, ell, shifts
        )
        weighted_support = pure_support(weighted_alpha, weighted_beta)
        assert weighted_support == {
            "0111": "4*P",
            "1111": "4*(P*h0 + Q)",
        }
        weighted_retained = (cap_p, cap_q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index != mode
        )
        weighted_certificates = four_unit_certificates(
            f"h{mode}_sp_sq_weighted_normal",
            weighted_alpha,
            weighted_beta,
            weighted_retained,
        )

        identity_alpha, identity_beta = homogeneous_chart_bases(
            mode, t, t * cap_p, t * cap_q, kappa, ell, shifts
        )
        identity_support = pure_support(identity_alpha, identity_beta)
        assert identity_support == {
            "0111": "4*P*t**2",
            "1111": "4*t**2*(P*h0 + Q)",
        }
        results[f"h{mode}_infinity"] = {
            "homogeneous_chart_pure_support": chart_support,
            "boundary_pure_support": {},
            "first_normal_pair_at_mode": ["0", f"b{mode}"],
            "first_normal_pure_support": normal_support,
            "first_normal_zero_locus": "p=q=0",
            "first_normal_unit_ideals": first_certificates,
            "sp_sq_weighted_normal_mode0_pair": [
                "P*B",
                "(h0*P+Q)*B",
            ],
            "sp_sq_weighted_normal_pure_support": weighted_support,
            "sp_sq_weighted_normal_unit_ideals": weighted_certificates,
        }

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "single-pole charts `h1=infinity`, `h2=infinity`, and `h3=infinity`",
        "monomial `(s_i p,s_i q)` normal",
        "simultaneous marking poles remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "single_marking_infinity_modes": [1, 2, 3],
                "charts": results,
                "dvr_puiseux_order": "min(v(s_i)+v(p), v(s_i)+v(q))",
                "pure_support_transfer_used": False,
                "simultaneous_marking_poles_closed": False,
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
