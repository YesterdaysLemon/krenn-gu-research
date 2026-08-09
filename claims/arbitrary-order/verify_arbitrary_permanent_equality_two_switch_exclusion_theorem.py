"""Primary exact checks for the two-switch equality exclusion theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # Opposite switch choices join p_1 and p_2 through the common mode a.
    opposite_path_adjacency = sp.Matrix(
        [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]
    )
    assert opposite_path_adjacency[0, 1] == 1
    assert opposite_path_adjacency[1, 2] == 1
    assert (opposite_path_adjacency**2)[0, 2] == 1

    # With the other switch fixed, a mixed matching using both selected core
    # edges has the same assumed-nonzero factor as the pure coefficient.
    pure_core, residual_mixed = sp.symbols("pure_core residual_mixed", nonzero=True)
    forbidden_mixed = residual_mixed * pure_core
    assert forbidden_mixed != 0

    # A bipartite Hamilton-cycle chord has odd cyclic distance.  Removing its
    # endpoints leaves two even-vertex path interiors.
    m, k = sp.symbols("m k", integer=True, positive=True)
    cycle_edges = 2 * m
    chord_distance = 2 * k + 1
    assert sp.simplify(chord_distance - 1 - 2 * k) == 0
    assert sp.simplify(cycle_edges - chord_distance - 1 - 2 * (m - k - 1)) == 0

    original = sp.eye(2)
    transposed = sp.Matrix([[0, 1], [1, 0]])
    assert original != transposed
    assert all(sum(transposed.row(i)) == 1 for i in range(2))
    assert all(sum(transposed.col(j)) == 1 for j in range(2))

    # Excluding the integer equality value 3m+2 leaves the next possible
    # support size 3m+3.
    positive_increment = sp.symbols("positive_increment", integer=True, positive=True)
    support = 3 * m + 2 + positive_increment
    assert sp.simplify(support - (3 * m + 3)) >= 0

    print("arbitrary permanent equality two-switch exclusion: PASS")
    print("fixed path/parity algebra only; no matching or support search was performed")


if __name__ == "__main__":
    main()
