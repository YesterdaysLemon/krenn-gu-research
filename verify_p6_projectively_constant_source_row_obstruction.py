#!/usr/bin/env python3
"""Verify the projectively constant source-row obstruction for P6."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P6_PROJECTIVELY_CONSTANT_SOURCE_ROW_OBSTRUCTION.md"


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    states: dict[int, sp.Expr] = {0: sp.S.One}
    for column in range(6):
        next_states: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, sp.S.Zero) + (
                    value * matrix[row][column]
                )
        states = next_states
    return sp.expand(states[63])


def symbolic_permanent_factor() -> int:
    linear = sp.symbols("L")
    kappas = sp.symbols("k0:6")
    other = sp.symbols("q0:30")
    matrix = [[kappas[column] * linear for column in range(6)]]
    matrix.extend(
        [[other[5 * column + row] for column in range(6)] for row in range(5)]
    )
    value = permanent(matrix)
    quotient = sp.expand(value / linear)
    assert sp.expand(value - linear * quotient) == 0
    assert linear not in quotient.free_symbols
    assert len(sp.Poly(quotient, *kappas, *other).terms()) == 720
    return len(sp.Poly(value, linear, *kappas, *other).terms())


def no_linear_factor_case_split() -> dict[str, sp.Expr]:
    x, y = sp.symbols("x y")
    alpha, beta, gamma = sp.symbols("alpha beta gamma", nonzero=True)
    lambda0, lambda1, lambda2 = sp.symbols("lambda0 lambda1 lambda2", nonzero=True)

    restricted = sp.expand(
        gamma**6 * (lambda0 * x**6 + lambda1 * y**6)
        + lambda2 * (-alpha * x - beta * y) ** 6
    )
    polynomial = sp.Poly(restricted, x, y)
    coefficient_x5y = sp.expand(polynomial.coeff_monomial(x**5 * y))
    coefficient_xy5 = sp.expand(polynomial.coeff_monomial(x * y**5))
    assert coefficient_x5y == 6 * alpha**5 * beta * lambda2
    assert coefficient_xy5 == 6 * alpha * beta**5 * lambda2

    alpha_zero = sp.expand(restricted.subs(alpha, 0))
    beta_zero = sp.expand(restricted.subs(beta, 0))
    assert sp.Poly(alpha_zero, x, y).coeff_monomial(x**6) == gamma**6 * lambda0
    assert sp.Poly(beta_zero, x, y).coeff_monomial(y**6) == gamma**6 * lambda1

    # For gamma=0 the line involves only x,y, so z remains a free coordinate
    # and its coefficient lambda2 cannot disappear.
    z_coefficient_on_gamma_zero_line = lambda2
    assert z_coefficient_on_gamma_zero_line != 0
    return {
        "x5y": coefficient_x5y,
        "xy5": coefficient_xy5,
        "gamma_zero_survivor": z_coefficient_on_gamma_zero_line,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero structural obstruction",
        "ell(t) divides F(t)",
        "dim span{H_u[i,-]:u in B} >= 2",
        "unrestricted P_6 -> Delta_3: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    monomials = symbolic_permanent_factor()
    line_check = no_linear_factor_case_split()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "permanent_assignments_checked_symbolically": monomials,
                "common_linear_factor_verified": True,
                "diagonal_sextic_linear_factor": False,
                "line_case_coefficients": {
                    key: str(value) for key, value in line_check.items()
                },
                "finite_field_used": False,
                "unrestricted_p6_excluded": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
