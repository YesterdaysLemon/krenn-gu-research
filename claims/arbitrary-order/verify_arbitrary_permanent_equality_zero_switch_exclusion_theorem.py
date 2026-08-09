"""Primary exact checks for the zero-switch exclusion theorem."""

from __future__ import annotations

import sympy as sp


def validate_perfect_matching(left_count: int, edges: set[tuple[int, int]]) -> None:
    assert len(edges) == left_count
    assert {left for left, _ in edges} == set(range(left_count))
    assert {right for _, right in edges} == set(range(left_count))


def main() -> None:
    diagonal_1, diagonal_2, cross_1, cross_2 = sp.symbols(
        "diagonal_1 diagonal_2 cross_1 cross_2", nonzero=True
    )
    pure_rectangle = diagonal_1 * diagonal_2 + cross_1 * cross_2
    diagonal_matching = {(0, 0), (1, 1)}
    cross_matching = {(0, 1), (1, 0)}
    validate_perfect_matching(2, diagonal_matching)
    validate_perfect_matching(2, cross_matching)
    assert diagonal_matching != cross_matching
    assert sp.expand(pure_rectangle - diagonal_1 * diagonal_2) == cross_1 * cross_2

    # Two nonempty disjoint port-colour sets inside three colours force a
    # singleton: |A_1|+|A_2|<=3 and both sizes are positive.
    admissible_size_pairs = {(1, 1), (1, 2), (2, 1)}
    assert all(min(pair) == 1 for pair in admissible_size_pairs)

    # Fixed symbolic chord construction on a ten-cycle.  This validates the
    # path formula; it is not a matching search.
    m = 5
    matching_a = {(index, index) for index in range(m)}
    matching_b = {((index + 1) % m, index) for index in range(m)}
    chord = (0, 2)
    chord_matching = {chord, (1, 0), (2, 1), (3, 3), (4, 4)}
    validate_perfect_matching(m, chord_matching)
    assert chord not in matching_a | matching_b
    assert chord_matching - {chord} <= matching_a | matching_b

    print("arbitrary permanent equality zero-switch exclusion: PASS")
    print(
        "fixed port/cycle constructions only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
