"""Primary exact checks for principal four-hafnian edge tomography.

The matrices at n=6 and n=9 audit an arbitrary-order symbolic kernel proof.
No graph support or parameter family is searched.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def edges(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def four_sets(n: int) -> list[tuple[int, int, int, int]]:
    return list(combinations(range(n), 4))


def inclusion_jacobian(n: int) -> sp.Matrix:
    edge_list = edges(n)
    return sp.Matrix(
        [[int(set(edge).issubset(four)) for edge in edge_list] for four in four_sets(n)]
    )


def verify_symbolic_four_hafnian() -> None:
    a12, a13, a14, a23, a24, a34 = sp.symbols("a12 a13 a14 a23 a24 a34")
    variables = (a12, a13, a14, a23, a24, a34)
    hafnian = a12 * a34 + a13 * a24 + a14 * a23
    gradient_at_one = [sp.diff(hafnian, variable).subs(dict.fromkeys(variables, 1)) for variable in variables]
    assert gradient_at_one == [1] * 6
    assert sp.expand(hafnian.subs({variable: -variable for variable in variables})) == hafnian


def verify_rank(n: int, expected_rank: int, expected_minor: int) -> None:
    jacobian = inclusion_jacobian(n)
    assert jacobian.shape == (sp.binomial(n, 4), sp.binomial(n, 2))
    assert jacobian.rank() == expected_rank
    _, pivot_rows = jacobian.T.rref()
    assert len(pivot_rows) == expected_rank
    square_minor = jacobian[list(pivot_rows), :]
    assert square_minor.det() == expected_minor


def verify_one_edge_line() -> None:
    t = sp.symbols("t")
    weights = {(0, 1): t}
    for four in four_sets(6):
        i, j, k, ell = four
        value = (
            weights.get((i, j), 0) * weights.get((k, ell), 0)
            + weights.get((i, k), 0) * weights.get((j, ell), 0)
            + weights.get((i, ell), 0) * weights.get((j, k), 0)
        )
        assert value == 0


def verify_p7_label_capacity() -> None:
    deck_size = sp.binomial(9, 4)
    assert 2**5 < deck_size <= 3**5


def main() -> None:
    verify_symbolic_four_hafnian()
    print("PASS: symbolic four-hafnian derivative and global sign symmetry")
    verify_rank(6, 15, 2 * 3**6)
    print("PASS: W_(2,4)(6) rank 15 with a minor 2*3^6")
    verify_rank(9, 36, 2 * 3**9)
    print("PASS: P7 nine-nonroot rank 36 with a minor 2*3^9")
    verify_one_edge_line()
    print("PASS: one-edge affine line lies in the zero four-hafnian fibre")
    verify_p7_label_capacity()
    print("PASS: P7 deck exceeds one two-plane jet but fits the full root tensor")
    print("SCOPE: labeled P7 depth-five exposure and singular-locus exclusion remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
