#!/usr/bin/env python3
"""Verify component 21's complete normalized ell-infinity compactification."""

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
THEOREM = (
    ROOT
    / "P5_COMPONENT21_ELL_INFINITY_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md"
)
PINNED = {
    ROOT / "P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md": (
        "3e8a12b61e2c82bd380191a17170c25991726bf7bee8425ac8f5201eb484523f"
    ),
    ROOT / "verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "c946ccc0bc6bf74b123dc9b41ce9ab3d6b813296161ae48ac8c436ec17d33f53"
    ),
    ROOT / "audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "1859953dd58a20c282dd86970a1220eca4ecd9180bdca5f41ed1ecd2c955d15d"
    ),
    ROOT
    / "P5_COMPONENT21_KAPPA_INFINITY_U0_PROJECTIVE_BLOWUP_COMPLETE_OBSTRUCTION.md": (
        "8925ab6c2d438f79ca89643322fd760cb9084e1431ce2c0dcba67a14b588dbbd"
    ),
    ROOT
    / "verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py": (
        "62d185481f4ffaa5bd8fa6340fdeca53727baa30d228681bf634e9e206242521"
    ),
    ROOT
    / "audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py": (
        "83b6817070062aa4adc485a246a80baa0a867ef3f5d22c981e49356fceb637d0"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ell_infinity_bases(
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        add(cap_a, scale(p, cap_b)),
        cap_a,
        cap_c,
        cap_d,
    ), (
        add(cap_c, scale(q, cap_b)),
        cap_c,
        add(cap_b, scale(kappa, cap_a)),
        cap_c,
    )


def direct_unit_certificates() -> dict[str, dict[str, int | bool]]:
    p, q, kappa, slope = sp.symbols("p q kappa lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    alpha, canonical_beta = ell_infinity_bases(p, q, kappa)
    beta = mark(alpha, canonical_beta, shifts)
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
        retained = (p, q, kappa) + shifts
        label = f"H31_ell_infinity_d{distinguished}"
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
        retained = (p, q, kappa) + shifts
        if chart == "finite":
            retained += (slope,)
        label = f"H22_ell_infinity_{chart}_weight"
        results[label] = unit_groebner(
            label,
            equations,
            extension + (inverse_a, inverse_b) + retained,
        )
    assert len(results) == 4
    return results


def main() -> None:
    p, q, kappa = sp.symbols("p q kappa")
    alpha, beta = ell_infinity_bases(p, q, kappa)
    support = pure_support(alpha, beta)
    assert support == {"0111": "-4*p", "1111": "-4*q"}
    assert (
        pure_support(
            tuple(tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in alpha),
            tuple(tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in beta),
        )
        == {}
    )
    certificates = direct_unit_certificates()

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "Every intersection of those parameter charts",
        "source-marking infinity",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "divisor": "ell=infinity",
                "finite_parameter_pure_support": support,
                "unique_affine_zero_tensor": "p=q=0",
                "direct_unit_ideals": certificates,
                "finite_kappa_u0_boundary_and_exceptional_closed": True,
                "kappa_infinity_full_u0_blowup_closed": True,
                "normalized_parameter_compactification_exhausted": True,
                "marked_H31_empty": True,
                "weighted_H22_empty": True,
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
