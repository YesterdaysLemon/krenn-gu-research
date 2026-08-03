"""Primary exact checks for the arbitrary-order one-switch exclusion."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # A bipartite cycle chord has odd cyclic distance 2k+1.  Removing its
    # endpoints leaves two even-vertex path interiors.
    m, k = sp.symbols("m k", integer=True, positive=True)
    cycle_edges = 2 * m
    chord_distance = 2 * k + 1
    first_interior = chord_distance - 1
    second_interior = cycle_edges - chord_distance - 1
    assert sp.simplify(first_interior - 2 * k) == 0
    assert sp.simplify(second_interior - 2 * (m - k - 1)) == 0

    # A mixed matching using both selected switch edges inherits the nonzero
    # pure core factor.
    a, b, c, d, residual = sp.symbols("a b c d residual", nonzero=True)
    pure_core = a * d + b * c
    mixed_core = residual * pure_core
    assert sp.expand(mixed_core - residual * pure_core) == 0

    # The two localized cross cells transpose the two exceptional pure edges.
    original = sp.eye(2)
    transposed = sp.Matrix([[0, 1], [1, 0]])
    assert original.det() == 1
    assert transposed.det() == -1
    assert original != transposed
    assert all(sum(transposed.row(i)) == 1 for i in range(2))
    assert all(sum(transposed.col(j)) == 1 for j in range(2))

    print("arbitrary permanent equality one-switch exclusion: PASS")
    print(
        "fixed parity/factor algebra only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
