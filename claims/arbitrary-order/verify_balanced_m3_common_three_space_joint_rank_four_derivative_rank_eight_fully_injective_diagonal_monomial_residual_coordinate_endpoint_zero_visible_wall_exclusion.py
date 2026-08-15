#!/usr/bin/env python3
"""Exact replay for the diagonal-endpoint zero-visible-wall exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def basis_vector(size: int, index: int) -> sp.Matrix:
    out = sp.zeros(size, 1)
    out[index] = 1
    return out


def tensor3(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        out[9 * i + 3 * j + k] = u[i] * v[j] * w[k]
    return out


def row(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return x.col_join(y).col_join(z)


def blocks(value: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return value[:3, :], value[3:6, :], value[6:9, :]


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[i] > sigma[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def alternating_tensor(rows: tuple[sp.Matrix, ...]) -> sp.Matrix:
    values = tuple(blocks(value) for value in rows)
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        out += permutation_sign(sigma) * tensor3(
            values[sigma[0]][0],
            values[sigma[1]][1],
            values[sigma[2]][2],
        )
    return sp.simplify(out)


def visible_zero(
    x_support: frozenset[int], y_support: frozenset[int]
) -> bool:
    return (
        x_support != {0}
        and y_support != {0}
        and (1 in x_support or 1 in y_support)
    )


def visible_one(
    x_support: frozenset[int], y_support: frozenset[int]
) -> bool:
    return (
        x_support != {1}
        and y_support != {1}
        and (0 in x_support or 0 in y_support)
    )


def check_support_wall_cover() -> None:
    supports = tuple(
        frozenset(index for index in range(3) if mask & (1 << index))
        for mask in range(1, 8)
        if mask != (1 << 2)
    )
    zero_visible = []
    for x_support, y_support in product(supports, repeat=2):
        if not visible_zero(x_support, y_support) and not visible_one(
            x_support, y_support
        ):
            zero_visible.append((x_support, y_support))
    assert zero_visible == [
        (frozenset({0}), frozenset({1})),
        (frozenset({1}), frozenset({0})),
    ]


def corrected_cube_value(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    k: int,
    lam: sp.Expr,
    target: sp.Matrix,
    source: sp.Matrix,
) -> sp.Matrix:
    return alpha[k] * beta[k] * target + lam * alpha[2] * beta[2] * source


def check_crossed_cube_radicals() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    targets = [basis_vector(6, index) for index in range(3)]
    sources = [basis_vector(6, 3 + index) for index in range(3)]
    zero = sp.zeros(6, 1)

    coefficient_count = 0
    for x_index, y_index, alpha_index in ((0, 1, 1), (1, 0, 0)):
        x = basis_vector(3, x_index)
        y = basis_vector(3, y_index)
        alpha = basis_vector(3, alpha_index)
        beta_basis = tuple(
            basis_vector(3, index)
            for index in range(3)
            if index != y_index
        )
        assert alpha.dot(x) == 0
        assert len(beta_basis) == 2
        assert sp.Matrix.hstack(*beta_basis).rank() == 2
        for beta in beta_basis:
            assert beta.dot(y) == 0
            for k in range(3):
                value = corrected_cube_value(
                    alpha, beta, k, lam, targets[k], sources[k]
                )
                assert sp.simplify(value) == zero
                coefficient_count += 1
    assert coefficient_count == 12


def canonical_derivative(
    x: sp.Matrix, y: sp.Matrix, lam: sp.Expr
) -> sp.Matrix:
    derivative = sp.zeros(27, 9)
    for i, j in product(range(3), repeat=2):
        derivative[9 * i + 3 * j + 0, i] += y[j]
        derivative[9 * i + 3 * j + 0, 3 + j] -= x[i]
    for k in range(3):
        derivative[9 * 2 + 3 * 2 + k, 6 + k] = lam
    return derivative


def check_full_sensor_three_space_interface() -> None:
    e_0, e_1, e_2 = (basis_vector(3, index) for index in range(3))
    zero = sp.zeros(3, 1)
    lam = sp.symbols("lambda", nonzero=True)
    derivative = canonical_derivative(e_0, e_1, lam)
    n = row(e_0, e_1, zero)
    assert derivative.rank() == 8
    assert derivative * n == sp.zeros(27, 1)

    graph_columns = (
        row(e_1, e_0, e_0),
        row(e_2, e_2, e_1),
        row(zero, zero, e_2),
    )
    k_matrix = sp.Matrix.hstack(n, *graph_columns)
    assert k_matrix.rank() == 4
    assert (derivative * k_matrix).rank() == 3
    assert k_matrix[:3, :].rank() == 3
    assert k_matrix[3:6, :].rank() == 3
    assert k_matrix[6:9, :].rank() == 3

    l_basis = sp.Matrix.hstack(*sp.Matrix([list(n)]).nullspace())
    assert l_basis.rank() == 8
    restriction = k_matrix.T * l_basis
    assert restriction.rank() == 3

    third_covectors = sp.zeros(9, 3)
    third_covectors[6:9, :] = sp.eye(3)
    third_restriction = k_matrix.T * third_covectors
    assert third_restriction.rank() == 3
    assert restriction.row_join(third_restriction).rank() == 3

    x_row = row(e_0, zero, zero)
    y_row = row(zero, e_0, zero)
    z_row = row(zero, zero, e_0)
    extra = row(e_1, e_1, e_1)
    embedding = sp.Matrix.hstack(extra, x_row, y_row, z_row)
    q_rows = tuple(
        embedding * third_restriction[:, index] for index in range(3)
    )
    assert sp.Matrix.hstack(*q_rows).rank() == 3
    alt_q = alternating_tensor(q_rows)
    assert alt_q == tensor3(e_0, e_0, e_0)

    coefficients = sp.Matrix(3, 3, sp.symbols("g0:9"))
    changed = tuple(
        sum(
            (coefficients[i, j] * q_rows[j] for j in range(3)),
            sp.zeros(9, 1),
        )
        for i in range(3)
    )
    assert sp.simplify(
        alternating_tensor(changed) - coefficients.det() * alt_q
    ) == sp.zeros(27, 1)


def check_radical_dimension_interface() -> None:
    # Injectivity preserves the two-dimensional y-perpendicular plane.
    p_0 = basis_vector(3, 0)
    p_2 = basis_vector(3, 2)
    radical_shore = sp.Matrix.hstack(p_0, p_2)
    assert radical_shore.rank() == 2
    # S2CG Corollary 2 gives rank at most one for a radical shore of any
    # nonzero row in an Alt-nonzero three-space.  The theorem owns that
    # analytic inequality; this replay verifies the incompatible input rank.
    s2cg_radical_bound = 1
    assert radical_shore.rank() > s2cg_radical_bound


def main() -> None:
    check_support_wall_cover()
    check_crossed_cube_radicals()
    check_full_sensor_three_space_interface()
    check_radical_dimension_interface()
    print(
        "PASS: exhaustive zero-visible support masks, twelve crossed-cube "
        "zeros, full-sensor alternating-three-space interface, and "
        "two-dimensional radical-shore contradiction"
    )


if __name__ == "__main__":
    main()
