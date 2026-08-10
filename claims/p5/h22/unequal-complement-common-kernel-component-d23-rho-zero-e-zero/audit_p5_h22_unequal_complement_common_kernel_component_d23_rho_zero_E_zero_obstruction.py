#!/usr/bin/env python3
"""Independent exact-Q audit of component 22's rho=E=0 residual."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
PERMS4 = tuple(itertools.permutations(range(4)))
x = sp.symbols("x0:8")
h0, h1, h2, h3, z, tau = sp.symbols("h0 h1 h2 h3 z tau")

ROWS = (
    (0, 1, 2, 3, 4, 5, 7),
    (0, 1, 2, 3, 4, 6, 7),
    (0, 1, 2, 3, 5, 6, 7),
    (0, 1, 2, 4, 5, 6, 7),
    (0, 1, 2, 3, 4, 7, 8),
    (0, 1, 2, 3, 4, 7, 10),
    (0, 1, 2, 3, 4, 7, 11),
)
COLUMNS = (0, 1, 2, 3, 4, 5, 6)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows():
    A, R, D = sp.Integer(2), sp.Integer(1), sp.Integer(3)
    u, v = (1 - D) / 2, (1 + D) / 2
    G = -(2 * A + R) / 2
    a, c = (1, 1, 0, 0), (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (G, G, u, v)
    y0 = (0, D * (2 * A + R), -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMS4
        )
    )


def projected_rows(shifts):
    alpha, beta = component_rows()
    beta = tuple(add(beta[i], alpha[i], shifts[i]) for i in range(4))
    alpha_p = tuple((row[0], row[1], row[3], x[i]) for i, row in enumerate(alpha))
    beta_p = tuple((row[0], row[1], row[3], x[4 + i]) for i, row in enumerate(beta))
    return alpha_p, beta_p


def coefficients(alpha, beta):
    return {
        bits: permanent(tuple(beta[i] if bits[i] else alpha[i] for i in range(4)))
        for bits in BITS4
    }


def main():
    alpha, beta = projected_rows((h0, h1, h2, h3))
    values = coefficients(alpha, beta)
    mixed = sp.Matrix(
        [[sp.diff(values[bits], variable) for variable in x] for bits in BITS4[1:-1]]
    )

    prior_cofactor = mixed.extract((0, 1, 3, 4, 5, 7, 9), (1, 2, 3, 4, 5, 6, 7)).det(
        method="domain-ge"
    )
    E = sp.factor(prior_cofactor / (2184000 * h2))
    assert sp.expand(E - (7 * h0 + 34 * h1 + 5)) == 0
    h0_solution = sp.cancel(-E.subs(h0, 0) / sp.diff(E, h0))

    specialized = mixed.subs(h0, h0_solution)
    kernel = sp.Matrix((2, 2, 2, 0, 2 * h0_solution + 2, 2 * h1, 2 * h2, -2))
    assert all(sp.expand(entry) == 0 for entry in specialized * kernel)
    extension = {x[index]: tau * kernel[index] for index in range(8)}
    assert sp.expand(values[BITS4[0]].subs(h0, h0_solution).subs(extension)) == 0
    assert sp.expand(values[BITS4[-1]].subs(h0, h0_solution).subs(extension)) == 8 * tau

    seven_columns = specialized.extract(range(14), COLUMNS)
    determinants = []
    for row_indices in ROWS:
        determinant = seven_columns.extract(row_indices, range(7)).det(
            method="domain-ge"
        )
        primitive = sp.Poly(determinant, h1, h2, h3).primitive()[1].as_expr()
        determinants.append(primitive)
    basis = sp.groebner(
        [*determinants, z * h1 * h2 - 1],
        z,
        h3,
        h2,
        h1,
        order="grevlex",
    )
    assert basis.contains(sp.Integer(1))

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"A": 2, "R": 1, "D": 3},
                "independent_no_repository_imports": True,
                "E_recovered_from_prior_selected_cofactor": str(E),
                "minor_rows": ROWS,
                "minor_columns": COLUMNS,
                "minor_saturation_unit_ideal": True,
                "mixed_kernel_verified": True,
                "A_on_kernel": "0",
                "B_on_kernel": "8*tau",
                "audit_only_not_generic_proof": True,
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
