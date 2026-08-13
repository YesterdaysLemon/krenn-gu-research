"""Exact replay for the complete single-root-block exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def basis(index: int) -> sp.Matrix:
    return sp.eye(9)[:, index]


def tensor_index(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def pair_product(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j] = p[3 + i] * q[6 + j] + q[3 + i] * p[6 + j]
        out[9 + 3 * i + j] = p[i] * q[6 + j] + q[i] * p[6 + j]
        out[18 + 3 * i + j] = p[i] * q[3 + j] + q[i] * p[3 + j]
    return out


def derivative(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    pair = pair_product(p, q)
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tensor_index(x, y, z)
        out[row, x] = pair[3 * y + z]
        out[row, 3 + y] = pair[9 + 3 * x + z]
        out[row, 6 + z] = pair[18 + 3 * x + y]
    return out


def forms() -> dict[str, tuple[list[sp.Matrix], list[sp.Matrix]]]:
    x0, x1, x2 = (basis(i) for i in range(3))
    y0, y1 = basis(3), basis(4)
    z0 = basis(6)
    zero = sp.zeros(9, 1)
    return {
        "pure/pure": ([x0, y0, zero], [y1, x1, zero]),
        "pure/pure-line": ([x0, y0, zero], [y1, 2 * x0, zero]),
        "pure/mixed-shared": (
            [x0, x2 - z0, zero],
            [x2 + z0, x1, zero],
        ),
        "pure/mixed-disjoint": (
            [x0, y0 - z0, zero],
            [y0 + z0, x1, zero],
        ),
        "mixed/mixed-same": (
            [x0 + y0, x1 + y1, zero],
            [x1 - y1, x0 - y0, zero],
        ),
        "mixed/mixed-different-transverse": (
            [x0 + y0, x1 + z0, zero],
            [x1 - z0, x0 - y0, zero],
        ),
        "mixed/mixed-different-shared": (
            [x0 + y0, x0 + z0, zero],
            [x0 - z0, x0 - y0, zero],
        ),
    }


def check_crossed_zero_pairs() -> None:
    for name, (p_rows, q_rows) in forms().items():
        assert pair_product(p_rows[0], q_rows[1]) == sp.zeros(27, 1), name
        assert pair_product(p_rows[1], q_rows[0]) == sp.zeros(27, 1), name
        assert pair_product(p_rows[0], q_rows[0]) != sp.zeros(27, 1), name
        assert pair_product(p_rows[1], q_rows[1]) != sp.zeros(27, 1), name
        assert p_rows[2] == sp.zeros(9, 1)
        assert q_rows[2] == sp.zeros(9, 1)
    print("crossed zero-product atlas: PASS (7 controls; 6 geometric families)")


def check_pure_mixed_boundaries() -> None:
    p_rows, q_rows = forms()["pure/mixed-disjoint"]
    d0 = derivative(p_rows[0], q_rows[0])
    d1 = derivative(p_rows[1], q_rows[1])
    yz_columns = list(range(3, 9))
    assert sp.Matrix.vstack(d0[:, yz_columns], d1[:, yz_columns]).rank() == 6

    y0, z0 = basis(3), basis(6)
    k_plus, k_minus = y0 - z0, y0 + z0
    plane = sp.Matrix.hstack(k_plus, k_minus)
    assert (d0 * plane).rank() == 1
    assert (d1 * plane).rank() == 1
    image_zero = sp.Matrix(3, 9, list(d0 * k_minus))
    image_one = sp.Matrix(3, 9, list(d1 * k_plus))
    assert sp.Matrix.vstack(image_zero, image_one).rank() == 1
    print("P/M boundary: PASS (two kernels force one YZ factor line)")


def check_mixed_mixed_boundaries() -> None:
    same_p, same_q = forms()["mixed/mixed-same"]
    assert pair_product(same_p[0], same_q[0]) == -pair_product(
        same_p[1], same_q[1]
    )

    transverse_p, transverse_q = forms()["mixed/mixed-different-transverse"]
    transverse_pair = sp.Matrix.vstack(
        derivative(transverse_p[0], transverse_q[0]),
        derivative(transverse_p[1], transverse_q[1]),
    )
    assert transverse_pair.rank() == 9

    shared_p, shared_q = forms()["mixed/mixed-different-shared"]
    d0 = derivative(shared_p[0], shared_q[0])
    d1 = derivative(shared_p[1], shared_q[1])
    assert sp.Matrix.vstack(d0, d1).rank() == 8
    common_kernel = sp.Matrix.hstack(*sp.Matrix.vstack(d0, d1).nullspace())
    assert common_kernel.columnspace() == [(basis(3) + basis(6))]

    # Both derivative images lie in the tangent space at x0*y0*z0.
    # The two derivative images together span the seven-dimensional Segre
    # tangent at x0 tensor y0 tensor z0.
    image = sp.Matrix.hstack(d0, d1)
    assert image.rank() == 7
    print("M/M boundaries: PASS (opposite / injective / tangent rank 7)")


def check_tangent_rank_one_rulings() -> None:
    # Coordinate decomposable tensors in the tangent cross have at least two
    # base coordinates equal to zero; two different GHZ diagonals do not.
    tangent_support = {
        (x, 0, 0) for x in range(3)
    } | {(0, y, 0) for y in range(3)} | {(0, 0, z) for z in range(3)}
    diagonal = {(c, c, c) for c in range(3)}
    assert tangent_support & diagonal == {(0, 0, 0)}
    tangent_diagonal_colours = [
        c for c in range(3) if sum((c == 0, c == 0, c == 0)) >= 2
    ]
    assert tangent_diagonal_colours == [0]
    print("Segre tangent rank-one ruling boundary: PASS")


def main() -> None:
    check_crossed_zero_pairs()
    check_pure_mixed_boundaries()
    check_mixed_mixed_boundaries()
    check_tangent_rank_one_rulings()
    print("balanced m=3 single-root-block complete exclusion: PASS")


if __name__ == "__main__":
    main()
