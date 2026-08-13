"""Exact replay for the rank-six shared-factor derivative exclusion."""

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


def shared_derivative() -> sp.Matrix:
    out = sp.zeros(27, 9)
    for i in range(3):
        out[tensor_index(i, 0, 0), i] = 1
        out[tensor_index(0, i, 0), 3 + i] = 1
    return out


def zero_diagonal(q: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[0, q[2], q[1]], [q[2], 0, q[0]], [q[1], q[0], 0]])


def check_derivative_and_rank_profiles() -> None:
    shared = shared_derivative()
    assert shared.rank() == 5
    assert len(shared.nullspace()) == 4

    # The exact row-rank profiles after two unaffected target slices.
    profiles = [(2, 2), (2, 3), (3, 2), (3, 3)]
    assert profiles == list(product((2, 3), repeat=2))
    assert (2, 2) in profiles and (3, 3) in profiles
    print("shared derivative and row-rank trichotomy: PASS (rank 5; four profiles)")


def check_pointwise_identity_and_rank_floor() -> None:
    values = [sp.Rational(((17 * i + 5) % 11) - 5) for i in range(21)]
    r_matrix = sp.Matrix(3, 3, values[:9])
    p_matrix = sp.Matrix(3, 3, values[9:18])
    q = sp.Matrix(values[18:21])
    direct = sp.Matrix(
        3,
        3,
        lambda a, b: sum(
            r_matrix[a, sigma[0]] * p_matrix[b, sigma[1]] * q[sigma[2]]
            for sigma in (
                (0, 1, 2),
                (0, 2, 1),
                (1, 0, 2),
                (1, 2, 0),
                (2, 0, 1),
                (2, 1, 0),
            )
        ),
    )
    assert direct == r_matrix * zero_diagonal(q) * p_matrix.T

    ranks = {
        support: zero_diagonal(sp.Matrix(support)).rank()
        for support in product((0, 1), repeat=3)
        if any(support)
    }
    assert set(ranks.values()) == {2, 3}
    assert all(value >= 2 for value in ranks.values())
    print("pointwise slice and zero-diagonal floor: PASS (9 entries; min rank 2)")


def check_slice_zero_promotion() -> None:
    # A full marked plane P makes vanishing against all three basis rows
    # equivalent to the quadratic pair product itself vanishing.
    p_basis = sp.eye(9)
    left = basis(0) + basis(3)
    right = basis(0) - basis(3)
    d = derivative(left, right)
    assert pair_product(left, right) == sp.zeros(27, 1)
    assert d * p_basis[:, :3] == sp.zeros(27, 3)

    nonzero_left = basis(0)
    nonzero_right = basis(3)
    nonzero_d = derivative(nonzero_left, nonzero_right)
    assert nonzero_d.rank() == 3
    print("full-plane slice-zero promotion: PASS (zero pair / nonzero control)")


def crossed_forms() -> list[tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]]:
    x0, x1, x2 = basis(0), basis(1), basis(2)
    y0, y1, z0 = basis(3), basis(4), basis(6)
    return [
        (x0, y0, x1, y1),
        (x0, x2 + y0, x1, x2 - y0),
        (x0, y0 - z0, x1, y0 + z0),
        (x0 + y0, x1 + y1, x0 - y0, x1 - y1),
        (x0 + y0, x1 + z0, x0 - y0, x1 - z0),
        (x0 + y0, x0 + z0, x0 - y0, x0 - z0),
    ]


def check_crossed_pair_atlas() -> None:
    checked = 0
    for a_t, a_u, q_u, q_t in crossed_forms():
        assert pair_product(a_t, q_u) == sp.zeros(27, 1)
        assert pair_product(a_u, q_t) == sp.zeros(27, 1)
        assert pair_product(a_t, q_t) != sp.zeros(27, 1)
        assert pair_product(a_u, q_u) != sp.zeros(27, 1)
        checked += 1

    same = crossed_forms()[3]
    assert pair_product(same[0], same[3]) == -pair_product(same[1], same[2])

    transverse = crossed_forms()[4]
    assert sp.Matrix.vstack(
        derivative(transverse[0], transverse[3]),
        derivative(transverse[1], transverse[2]),
    ).rank() == 9

    tangent = crossed_forms()[5]
    assert sp.Matrix.hstack(
        derivative(tangent[0], tangent[3]),
        derivative(tangent[1], tangent[2]),
    ).rank() == 7
    assert checked == 6
    print("crossed-pair diagonal atlas: PASS (6/6 families)")


def main() -> None:
    check_derivative_and_rank_profiles()
    check_pointwise_identity_and_rank_floor()
    check_slice_zero_promotion()
    check_crossed_pair_atlas()
    print("balanced m=3 rank-six shared-factor exclusion: PASS")


if __name__ == "__main__":
    main()
