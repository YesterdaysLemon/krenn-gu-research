"""Symbolic checks for the equality negative-gain graph theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    a, b, c, d = sp.symbols("A B C D", nonzero=True)
    gain_left = b / a
    gain_right = d / c
    rectangle = sp.Eq(a * d + b * c, 0)
    solved = sp.solve(rectangle, d, dict=True)
    assert solved == [{d: -b * c / a}]
    assert sp.simplify((gain_left / gain_right).subs(solved[0]) + 1) == 0

    g0 = sp.symbols("g0", nonzero=True)
    triangle = [g0]
    for _ in range(3):
        triangle.append(-triangle[-1])
    assert sp.expand(triangle[-1] - g0) == -2 * g0

    square = [g0]
    for _ in range(4):
        square.append(-square[-1])
    assert sp.expand(square[-1] - g0) == 0
    assert all(sp.expand(square[i] + square[i + 1]) == 0 for i in range(4))

    # Each individual backbone fibre may be bipartite while their union is
    # not: three one-edge fibres can glue to a triangle on shared states.
    fibre_edges = [((0, 1),), ((1, 2),), ((2, 0),)]
    assert all(len(fibre) == 1 for fibre in fibre_edges)
    glued = [edge for fibre in fibre_edges for edge in fibre]
    assert set(glued) == {(0, 1), (1, 2), (2, 0)}
    glued_values = [g0]
    for _ in glued:
        glued_values.append(-glued_values[-1])
    assert sp.expand(glued_values[-1] - g0) == -2 * g0

    print("arbitrary permanent equality negative-gain graph: symbolic checks PASS")
    print("fixed gain/gluing algebra only; no matching or word search was performed")


if __name__ == "__main__":
    main()
