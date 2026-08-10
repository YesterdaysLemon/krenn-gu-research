#!/usr/bin/env python3
"""Independent audit of component 22's complete H=h2=0 terminal closure."""

from __future__ import annotations

import json

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)



A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
f7 = (A * D + A + R) * rho + A * D - A - R
COLUMNS = (0, 1, 2, 4, 5, 7)


def gaussian_determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    work = [
        [
            field.from_sympy(sp.cancel(matrix[rows[i], COLUMNS[j]]))
            for j in range(6)
        ]
        for i in range(6)
    ]
    sign = field.one
    for column in range(6):
        pivot_row = next(
            (index for index in range(column, 6) if work[index][column]), None
        )
        if pivot_row is None:
            return sp.S.Zero
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, 6):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot
            for index in range(column, 6):
                work[row][index] -= multiplier * work[column][index]
    value = sign
    for index in range(6):
        value *= work[index][index]
    return sp.cancel(value.as_expr())


def exact_equal(left, right) -> None:
    assert sp.cancel(left - right) == 0


def main() -> None:
    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
    ).subs({h1: -1 / (2 * A), h2: 0}, simultaneous=True)

    cap_w = f7 * h0 + s - R * rho
    cover = gaussian_determinant(
        matrix, (0, 2, 3, 6, 7, 11), (A, R, D, h0, h3, rho)
    )
    exact_equal(
        cover,
        8
        * D**2
        * rho
        * s**4
        * (D - 1)
        * (D + 1)
        * (rho - 1)
        * (rho + 1) ** 2
        * cap_w,
    )
    resultant = sp.factor(sp.resultant(f7, s - R * rho, rho))
    exact_equal(resultant, 2 * A * (A + R) * (D + 1))

    h0_w = sp.cancel(-(s - R * rho) / f7)
    matrix_w = matrix.subs(h0, h0_w)
    p_minor = gaussian_determinant(
        matrix_w, (0, 2, 3, 6, 7, 10), (A, R, D, h3, rho)
    )
    p_prefactor = -4 * A * D * rho * s**2 * (D + 1) * (rho + 1) ** 2
    cap_p = sp.cancel(p_minor / p_prefactor)
    assert sp.denom(cap_p) == 1
    p_polynomial = sp.Poly(cap_p, h3)
    assert p_polynomial.degree() == 1
    p0, p1 = p_polynomial.nth(0), p_polynomial.nth(1)
    coefficient_field = sp.QQ.frac_field(A, R, D)
    p_gcd = sp.gcd(
        sp.Poly(p0, rho, domain=coefficient_field),
        sp.Poly(p1, rho, domain=coefficient_field),
    ).monic()
    exact_equal(p_gcd.as_expr(), 1)

    terminal = matrix.subs(
        {h0: h0_w, h3: sp.cancel(-p0 / p1)}, simultaneous=True
    )
    delta0 = gaussian_determinant(
        terminal, (2, 3, 6, 7, 10, 12), (A, R, D, rho)
    )
    delta1 = gaussian_determinant(
        terminal, (2, 3, 6, 7, 8, 10), (A, R, D, rho)
    )

    l1 = A * D * rho - A * D + A * rho + A + 2 * D * R * rho - 2 * D * R - R * rho - R
    l2 = A * D**2 * rho - A * D**2 - 2 * A * D * rho - 2 * A * D - 3 * A * rho + 3 * A - 2 * R * rho + 2 * R
    m1 = A * D * rho - A * D + A * rho + A + R * rho + R
    m2 = 2 * A * D * rho + 2 * A * D + 2 * A * rho - 2 * A + D**2 * R * rho - D**2 * R + R * rho - R
    m3 = A**2 * D * rho + A**2 * D - 3 * A**2 * rho + 3 * A**2 - 5 * A * R * rho + 5 * A * R - 2 * R**2 * rho + 2 * R**2
    numerator0 = -D * rho * s**3 * (D + 1) ** 2 * (rho + 1) ** 2 * l1 * l2
    numerator1 = 2 * A * D * rho * s**2 * (D + 1) ** 2 * (rho + 1) ** 2 * m1 * m2 * m3
    exact_equal(delta0, numerator0)
    exact_equal(delta1, numerator1 / f7)

    gcd = sp.gcd(
        sp.Poly(sp.fraction(delta0)[0], rho, domain=coefficient_field),
        sp.Poly(sp.fraction(delta1)[0], rho, domain=coefficient_field),
    ).monic()
    exact_equal(gcd.as_expr(), rho * (rho + 1) ** 2)

    print(
        json.dumps(
            {
                "status": "PASS",
                "method": "low-level matrix build and explicit Gaussian determinants",
                "field": "Q(A,R,D)",
                "component": 22,
                "closed_branch": "H=0, h2=0, rho*(rho+1)!=0",
                "six_by_six_determinants": 4,
                "f7_W_resultant": str(resultant),
                "P_degree_in_h3": p_polynomial.degree(),
                "P_leading_constant_gcd": str(p_gcd.as_expr()),
                "terminal_numerator_gcd": str(sp.factor(gcd.as_expr())),
                "other_H_zero_factors_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
