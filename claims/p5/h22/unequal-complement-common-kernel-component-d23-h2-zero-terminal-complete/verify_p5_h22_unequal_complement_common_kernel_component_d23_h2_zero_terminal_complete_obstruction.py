#!/usr/bin/env python3
"""Verify complete closure of component 22's H=h2=0 terminal branch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2_ZERO_"
    "TERMINAL_COMPLETE_OBSTRUCTION.md"
)
COLUMNS = (0, 1, 2, 4, 5, 7)
COVER_ROWS = (0, 2, 3, 6, 7, 11)
P_ROWS = (0, 2, 3, 6, 7, 10)
TERMINAL_ROWS_0 = (2, 3, 6, 7, 10, 12)
TERMINAL_ROWS_1 = (2, 3, 6, 7, 8, 10)


def determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    data = [
        [
            field.from_sympy(sp.cancel(matrix[rows[i], COLUMNS[j]]))
            for j in range(6)
        ]
        for i in range(6)
    ]
    return sp.cancel(DomainMatrix(data, (6, 6), field).det().as_expr())


def exact_equal(left, right) -> None:
    assert sp.cancel(left - right) == 0


def main() -> None:
    base = V.mixed_matrix.subs(
        {V.h1: -1 / (2 * V.A), V.h2: 0}, simultaneous=True
    )
    cap_w = V.f7 * V.h0 + V.s - V.R * V.rho

    cover = determinant(
        base, COVER_ROWS, (V.A, V.R, V.D, V.h0, V.h3, V.rho)
    )
    cover_expected = (
        8
        * V.D**2
        * V.rho
        * V.s**4
        * (V.D - 1)
        * (V.D + 1)
        * (V.rho - 1)
        * (V.rho + 1) ** 2
        * cap_w
    )
    exact_equal(cover, cover_expected)
    resultant = sp.factor(
        sp.resultant(V.f7, V.s - V.R * V.rho, V.rho)
    )
    exact_equal(resultant, 2 * V.A * (V.A + V.R) * (V.D + 1))

    h0_w = sp.cancel(-(V.s - V.R * V.rho) / V.f7)
    matrix_w = base.subs(V.h0, h0_w)
    p_minor = determinant(
        matrix_w, P_ROWS, (V.A, V.R, V.D, V.h3, V.rho)
    )
    p_prefactor = (
        -4
        * V.A
        * V.D
        * V.rho
        * V.s**2
        * (V.D + 1)
        * (V.rho + 1) ** 2
    )
    cap_p = sp.cancel(p_minor / p_prefactor)
    assert sp.denom(cap_p) == 1
    polynomial = sp.Poly(cap_p, V.h3)
    assert polynomial.degree() == 1
    p0, p1 = polynomial.nth(0), polynomial.nth(1)
    coefficient_field = sp.QQ.frac_field(V.A, V.R, V.D)
    p_gcd = sp.gcd(
        sp.Poly(p0, V.rho, domain=coefficient_field),
        sp.Poly(p1, V.rho, domain=coefficient_field),
    ).monic()
    exact_equal(p_gcd.as_expr(), 1)

    h3_p = sp.cancel(-p0 / p1)
    terminal = base.subs(
        {V.h0: h0_w, V.h3: h3_p}, simultaneous=True
    )
    delta0 = determinant(
        terminal, TERMINAL_ROWS_0, (V.A, V.R, V.D, V.rho)
    )
    delta1 = determinant(
        terminal, TERMINAL_ROWS_1, (V.A, V.R, V.D, V.rho)
    )

    l1 = (
        V.A * V.D * V.rho
        - V.A * V.D
        + V.A * V.rho
        + V.A
        + 2 * V.D * V.R * V.rho
        - 2 * V.D * V.R
        - V.R * V.rho
        - V.R
    )
    l2 = (
        V.A * V.D**2 * V.rho
        - V.A * V.D**2
        - 2 * V.A * V.D * V.rho
        - 2 * V.A * V.D
        - 3 * V.A * V.rho
        + 3 * V.A
        - 2 * V.R * V.rho
        + 2 * V.R
    )
    m1 = (
        V.A * V.D * V.rho
        - V.A * V.D
        + V.A * V.rho
        + V.A
        + V.R * V.rho
        + V.R
    )
    m2 = (
        2 * V.A * V.D * V.rho
        + 2 * V.A * V.D
        + 2 * V.A * V.rho
        - 2 * V.A
        + V.D**2 * V.R * V.rho
        - V.D**2 * V.R
        + V.R * V.rho
        - V.R
    )
    m3 = (
        V.A**2 * V.D * V.rho
        + V.A**2 * V.D
        - 3 * V.A**2 * V.rho
        + 3 * V.A**2
        - 5 * V.A * V.R * V.rho
        + 5 * V.A * V.R
        - 2 * V.R**2 * V.rho
        + 2 * V.R**2
    )
    numerator0_expected = (
        -V.D
        * V.rho
        * V.s**3
        * (V.D + 1) ** 2
        * (V.rho + 1) ** 2
        * l1
        * l2
    )
    numerator1_expected = (
        2
        * V.A
        * V.D
        * V.rho
        * V.s**2
        * (V.D + 1) ** 2
        * (V.rho + 1) ** 2
        * m1
        * m2
        * m3
    )
    exact_equal(delta0, numerator0_expected)
    exact_equal(delta1, numerator1_expected / V.f7)

    numerator0 = sp.fraction(delta0)[0]
    numerator1 = sp.fraction(delta1)[0]
    terminal_gcd = sp.gcd(
        sp.Poly(numerator0, V.rho, domain=coefficient_field),
        sp.Poly(numerator1, V.rho, domain=coefficient_field),
    ).monic()
    exact_equal(terminal_gcd.as_expr(), V.rho * (V.rho + 1) ** 2)

    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero branch closure",
        "gcd(N0,N1)=rho*(rho+1)^2",
        "other projective/source/ambient charts",
        "remain **UNRESOLVED**",
        "No finite field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "Q(A,R,D)",
                "component": 22,
                "closed_branch": "H=0, h2=0, rho*(rho+1)!=0",
                "first_cover": ["rho=1", "f6=0", "f8=0", "W=0"],
                "f7_W_resultant": str(resultant),
                "P_degree_in_h3": polynomial.degree(),
                "P_leading_constant_gcd": str(p_gcd.as_expr()),
                "terminal_numerator_gcd": str(
                    sp.factor(terminal_gcd.as_expr())
                ),
                "other_H_zero_factors_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
