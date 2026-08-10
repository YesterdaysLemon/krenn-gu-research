#!/usr/bin/env python3
"""Verify component 21's normalized kappa-infinity first-normal atlas."""

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
    wedge,
)

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_KAPPA_INFINITY_FIRST_NORMAL_COMPLETE_OBSTRUCTION.md"
PQ_THEOREM = ROOT / "P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md"
PQ_PRIMARY = (
    ROOT / "verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py"
)
PQ_AUDIT = ROOT / "audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py"
PINNED = {
    PQ_THEOREM: "3e8a12b61e2c82bd380191a17170c25991726bf7bee8425ac8f5201eb484523f",
    PQ_PRIMARY: "c946ccc0bc6bf74b123dc9b41ce9ab3d6b813296161ae48ac8c436ec17d33f53",
    PQ_AUDIT: "1859953dd58a20c282dd86970a1220eca4ecd9180bdca5f41ed1ecd2c955d15d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bases(
    p: sp.Symbol,
    q: sp.Symbol,
    ell: sp.Symbol,
    ell_infinity: bool,
    regular_t: sp.Expr | None,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = add(cap_a, scale(p, cap_b))
    row_01 = add(cap_c, scale(q, cap_b))
    mode_2_beta = cap_b if regular_t is None else add(cap_a, scale(regular_t, cap_b))
    if ell_infinity:
        return (row_00, cap_a, cap_c, cap_d), (
            row_01,
            cap_c,
            mode_2_beta,
            cap_c,
        )
    return (
        row_00,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        row_01,
        cap_a,
        mode_2_beta,
        add(cap_a, scale(ell, cap_c)),
    )


def sheet_unit_certificates() -> dict[str, dict[str, int | bool]]:
    p, q, ell, slope = sp.symbols("p q ell lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    results = {}
    for ell_infinity in (False, True):
        alpha, canonical_beta = bases(p, q, ell, ell_infinity, None)
        beta = mark(alpha, canonical_beta, shifts)
        ell_label = "ell_infinity" if ell_infinity else "finite_ell"
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
            retained = (p, q) + (() if ell_infinity else (ell,)) + shifts
            label = f"H31_{ell_label}_d{distinguished}"
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
            retained = (p, q) + (() if ell_infinity else (ell,)) + shifts
            if chart == "finite":
                retained += (slope,)
            label = f"H22_{ell_label}_{chart}_weight"
            results[label] = unit_groebner(
                label,
                equations,
                extension + (inverse_a, inverse_b) + retained,
            )
    assert len(results) == 8
    return results


def main() -> None:
    p, q, ell, t, cap_p, cap_q, h2, y2 = sp.symbols("p q ell t P Q h2 y2")
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    finite_raw = bases(p, q, ell, False, t)
    infinity_raw = bases(p, q, ell, True, t)
    finite_sheet = bases(p, q, ell, False, None)
    infinity_sheet = bases(p, q, ell, True, None)
    assert pure_support(*finite_raw) == {"0111": "4*p*t", "1111": "4*q*t"}
    assert pure_support(*infinity_raw) == {
        "0111": "-4*p*t",
        "1111": "-4*q*t",
    }
    assert pure_support(*finite_sheet) == {"0111": "4*p", "1111": "4*q"}
    assert pure_support(*infinity_sheet) == {
        "0111": "-4*p",
        "1111": "-4*q",
    }

    raw_mode_2 = add(cap_a, scale(t, cap_b))
    assert wedge(cap_c, raw_mode_2) == wedge(cap_c, cap_a) + t * wedge(cap_c, cap_b)
    regular_marked_extended = sp.Matrix(
        (*add(cap_a, scale(t, add(cap_b, scale(h2, cap_c)))), t * y2)
    )
    base_extended = sp.Matrix((*cap_a, 0))
    exceptional_marked_extended = sp.Matrix((*add(cap_b, scale(h2, cap_c)), y2))
    assert sp.simplify(
        (regular_marked_extended - base_extended) / t - exceptional_marked_extended
    ) == sp.zeros(5, 1)

    double_finite_alpha = (
        add(scale(cap_q, cap_a), scale(-cap_p, cap_c)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1)),
    )
    double_finite_beta = (
        cap_b,
        cap_a,
        cap_b,
        add(cap_a, scale(ell, cap_c)),
    )
    double_infinity_alpha = (
        add(scale(cap_q, cap_a), scale(-cap_p, cap_c)),
        cap_a,
        cap_c,
        (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1)),
    )
    double_infinity_beta = (cap_b, cap_c, cap_b, cap_c)
    assert pure_support(double_finite_alpha, double_finite_beta) == {"1111": "4"}
    assert pure_support(double_infinity_alpha, double_infinity_beta) == {"1111": "-4"}

    certificates = sheet_unit_certificates()
    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "arbitrary extension valuations outside the displayed Rees chart",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "Poles of \\(p\\) or \\(q\\)",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "raw_t_chart_pure_support": {
                    "finite_ell": pure_support(*finite_raw),
                    "ell_infinity": pure_support(*infinity_raw),
                },
                "mode_2_pluecker_first_normal": "C wedge B",
                "normalized_sheet_pure_support": {
                    "finite_ell": pure_support(*finite_sheet),
                    "ell_infinity": pure_support(*infinity_sheet),
                },
                "marking_extension_rees_row_identity": True,
                "direct_unit_ideals": certificates,
                "double_normal_vertical_kappa_zero": {
                    "finite_ell": {"1111": "4"},
                    "ell_infinity": {"1111": "-4"},
                },
                "finite_p_q_dvr_puiseux_cover_complete": True,
                "p_q_poles_closed": False,
                "arbitrary_source_extension_projective_closed": False,
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
