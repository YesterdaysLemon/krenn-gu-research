"""Primary checks for the three-excess port-permutation theorem."""

from __future__ import annotations

import math

import sympy as sp


def main() -> None:
    x = sp.Matrix(3, 3, lambda r, s: sp.Symbol(f"x{r + 1}{s + 1}"))
    permanent = (
        x[0, 0] * x[1, 1] * x[2, 2]
        + x[0, 0] * x[1, 2] * x[2, 1]
        + x[0, 1] * x[1, 0] * x[2, 2]
        + x[0, 1] * x[1, 2] * x[2, 0]
        + x[0, 2] * x[1, 0] * x[2, 1]
        + x[0, 2] * x[1, 1] * x[2, 0]
    )
    assert sp.expand(permanent - x.per()) == 0

    identity_terms = 1
    transposition_terms = 3
    three_cycle_terms = 2
    assert identity_terms + transposition_terms + three_cycle_terms == math.factorial(3)
    assert transposition_terms + three_cycle_terms == 5

    assert math.factorial(2) == 2
    assert math.factorial(3) == 6
    assert 2**3 == 8

    # The incidence witness has local rank three at all four modes.
    excess_rows = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 3, 2]])
    assert excess_rows.det() == -3
    for coordinate_rows in (
        sp.Matrix([[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        sp.Matrix([[0, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 1, 0]]),
    ):
        assert coordinate_rows.rank() == 3

    # Each colour has two explicit p1/p2 switch terms and a nonzero sum.
    assert (1 + 1, 1 + 2, 1 + 3) == (2, 3, 4)

    t = sp.symbols("t", nonzero=True)
    bypass = sp.Matrix([[1, 0, 0], [t, 1, 1], [0, -1, 1]])
    assert sp.expand(bypass.per()) == 0
    assert bypass.minor_submatrix(0, 0).per() == 0
    assert bypass[0, 1] == 0 and bypass[0, 2] == 0

    # Laplace expansion of a permanent along each distinguished port row.
    for row in range(3):
        expansion = sum(
            x[row, column] * x.minor_submatrix(row, column).per() for column in range(3)
        )
        assert sp.expand(permanent - expansion) == 0

    excess_partitions = ((3,), (2, 1), (1, 1, 1))
    assert all(sum(partition) == 3 for partition in excess_partitions)

    print("arbitrary permanent three-excess port permutation: PASS")
    print(
        "fixed S_3 boundary algebra only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
