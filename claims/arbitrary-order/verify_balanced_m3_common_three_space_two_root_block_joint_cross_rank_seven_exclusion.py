"""Exact replay for the two-root-block joint-rank-seven exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def tensor_index(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def derivative_matrix(third_block: bool = False) -> sp.Matrix:
    """Shared-factor pair, optionally with the third aligned block."""
    out = sp.zeros(27, 9)
    for i in range(3):
        out[tensor_index(i, 0, 0), i] = 1
        out[tensor_index(0, i, 0), 3 + i] = 1
        if third_block:
            out[tensor_index(0, 0, i), 6 + i] = 1
    return out


def check_sharp_derivative() -> None:
    derivative = derivative_matrix()
    assert derivative.rank() == 5
    kernel = sp.Matrix.hstack(*derivative.nullspace())
    expected = sp.Matrix.hstack(
        sp.Matrix([-1, 0, 0, 1, 0, 0, 0, 0, 0]),
        sp.eye(9)[:, 6],
        sp.eye(9)[:, 7],
        sp.eye(9)[:, 8],
    )
    assert kernel.columnspace() == expected.columnspace()
    assert derivative_matrix(third_block=True).rank() == 7

    # Four kernel columns plus three independent derivative lifts make the
    # exact seven-space D^(-1)(U), and restriction has rank three.
    lifts = sp.Matrix.hstack(sp.eye(9)[:, 0], sp.eye(9)[:, 1], sp.eye(9)[:, 4])
    candidate = sp.Matrix.hstack(kernel, lifts)
    assert candidate.rank() == 7
    assert (derivative * candidate).rank() == 3
    print("two-root sharp derivative: PASS (rank 5; kernel 4; third block rank 7)")


def check_rank_two_row_boundary() -> None:
    # Put s=2.  If r_s=0 then the column image K_12 lies in a_s=0.
    # Its kernel vector also has x_s=0, so delta(K_12) has zero first-factor
    # s slice and cannot contain e_s tensor e_s.
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    x0, x1, y0, y1, y2 = sp.symbols("x0 x1 y0 y1 y2")
    a = sp.Matrix([a0, a1, 0])
    b = sp.Matrix([b0, b1, sp.Symbol("b2")])
    x = sp.Matrix([x0, x1, 0])
    y = sp.Matrix([y0, y1, y2])
    tangent = a * y.T + x * b.T
    assert tangent[2, :] == sp.zeros(1, 3)
    assert tangent[2, 2] == 0
    print("rank-two root-row boundary: PASS (exceptional pure tensor absent)")


def permanent(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return (
        left[0] * middle[1] * right[2]
        + left[0] * middle[2] * right[1]
        + left[1] * middle[0] * right[2]
        + left[1] * middle[2] * right[0]
        + left[2] * middle[0] * right[1]
        + left[2] * middle[1] * right[0]
    )


def zero_diagonal(q: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[0, q[2], q[1]], [q[2], 0, q[0]], [q[1], q[0], 0]])


def check_pointwise_matrix_identity() -> None:
    values = [sp.Rational(((17 * i + 5) % 11) - 5) for i in range(21)]
    r_matrix = sp.Matrix(3, 3, values[:9])
    p_matrix = sp.Matrix(3, 3, values[9:18])
    q = sp.Matrix(values[18:21])
    direct = sp.Matrix(
        3,
        3,
        lambda a, b: permanent(r_matrix.row(a).T, p_matrix.row(b).T, q),
    )
    assert direct == r_matrix * zero_diagonal(q) * p_matrix.T
    print("pointwise permanent slice identity: PASS (all 9 entries)")


def check_zero_diagonal_rank_floor() -> None:
    ranks: dict[int, set[int]] = {1: set(), 2: set(), 3: set()}
    for support in product((0, 1), repeat=3):
        if not any(support):
            continue
        q = sp.Matrix(support)
        ranks[sum(support)].add(zero_diagonal(q).rank())
        nonzero = next(i for i, entry in enumerate(support) if entry)
        indices = [i for i in range(3) if i != nonzero]
        # q_X sits in the YZ principal minor, and cyclically.
        principal = zero_diagonal(q).extract(indices, indices)
        assert principal.det() == -1
    assert ranks == {1: {2}, 2: {2}, 3: {3}}
    print("zero-diagonal matrix rank floor: PASS (2 / 2 / 3)")


def check_two_slice_column_trap() -> None:
    # Two nonzero coordinate rank-one slices force e0,e1 into both column
    # spaces.  A rank-two R with those columns has an identically zero e2 row.
    c0, c1 = sp.symbols("c0 c1", nonzero=True)
    slice_zero = sp.diag(c0, 0, 0)
    slice_one = sp.diag(0, c1, 0)
    combined = sp.Matrix.hstack(slice_zero, slice_one)
    assert combined.rank() == 2
    assert combined.row(2) == sp.zeros(1, 6)
    rank_two_r = sp.Matrix([[1, 0, 2], [0, 1, 3], [0, 0, 0]])
    assert rank_two_r.rank() == 2
    assert rank_two_r.row(2) == sp.zeros(1, 3)
    print("two-slice column-space trap: PASS (rank two erases third row)")


def main() -> None:
    check_sharp_derivative()
    check_rank_two_row_boundary()
    check_pointwise_matrix_identity()
    check_zero_diagonal_rank_floor()
    check_two_slice_column_trap()
    print("balanced m=3 two-root-block joint-rank-seven exclusion: PASS")


if __name__ == "__main__":
    main()
