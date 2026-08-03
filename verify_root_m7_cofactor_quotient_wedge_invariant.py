"""Symbolic checks for the root m=7 cofactor quotient-wedge invariant."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def main() -> None:
    u = sp.symbols("u0:4")
    s, t = sp.symbols("s t")
    c_row = [s * value for value in u]
    e_row = [t * value for value in u]
    minors = [
        sp.expand(c_row[i] * e_row[j] - c_row[j] * e_row[i])
        for i, j in combinations(range(4), 2)
    ]
    assert all(minor == 0 for minor in minors)

    # On the chart C0 != 0, the minors with column zero give the converse.
    c = sp.symbols("c0:4", nonzero=True)
    e = sp.symbols("e0:4")
    chart_equations = [sp.Eq(c[0] * e[j] - c[j] * e[0], 0) for j in range(1, 4)]
    solved = sp.solve(chart_equations, e[1:], dict=True)
    assert solved == [
        {
            e[1]: c[1] * e[0] / c[0],
            e[2]: c[2] * e[0] / c[0],
            e[3]: c[3] * e[0] / c[0],
        }
    ]

    # Matrix units lie on the rank-one variety and span the ambient space.
    units = []
    for row in range(2):
        for column in range(4):
            unit = sp.zeros(2, 4)
            unit[row, column] = 1
            assert unit.rank() == 1
            units.append(sp.Matrix(8, 1, list(unit)))
    assert sp.Matrix.hstack(*units).rank() == 8

    # Exactly two zero sectors force every four-sector product, but not the
    # product of the three inactive sectors.
    delta = [sp.S.Zero, sp.S.Zero, *sp.symbols("d2:5", nonzero=True)]
    four_products = [
        sp.prod(delta[k] for k in subset) for subset in combinations(range(5), 4)
    ]
    assert all(product == 0 for product in four_products)
    assert sp.prod(delta[k] for k in (2, 3, 4)) != 0

    print("root m=7 cofactor quotient-wedge invariant: symbolic checks PASS")
    print("fixed-size rank-one algebra only; no word or support search was performed")


if __name__ == "__main__":
    main()
