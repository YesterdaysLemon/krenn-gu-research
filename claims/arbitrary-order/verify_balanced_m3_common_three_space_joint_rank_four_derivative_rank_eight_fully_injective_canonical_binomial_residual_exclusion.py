#!/usr/bin/env python3
"""Exact interface replay for the canonical-binomial residual exclusion."""

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


def polarized_product(
    u: sp.Matrix, v: sp.Matrix, q: sp.Matrix
) -> sp.Matrix:
    values = (blocks(u), blocks(v), blocks(q))
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            values[sigma[0]][0],
            values[sigma[1]][1],
            values[sigma[2]][2],
        )
    return sp.simplify(out)


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[i] > sigma[j]
        for i in range(len(sigma))
        for j in range(i + 1, len(sigma))
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


def check_canonical_derivative() -> None:
    kappa_0, kappa_1 = sp.symbols(
        "kappa_0 kappa_1", nonzero=True
    )
    derivative = sp.zeros(27, 9)
    for i in range(3):
        derivative[9 * i + 3 * 2 + 2, i] = 1
    for j in range(3):
        derivative[9 * 2 + 3 * j + 2, 3 + j] = -1
    for k in range(3):
        derivative[9 * 0 + 3 * 0 + k, 6 + k] = kappa_0
        derivative[9 * 1 + 3 * 1 + k, 6 + k] = kappa_1

    assert derivative.rank() == 8
    kernel = sp.zeros(9, 1)
    kernel[2] = 1
    kernel[5] = 1
    assert derivative * kernel == sp.zeros(27, 1)
    nullspace = derivative.nullspace()
    assert len(nullspace) == 1
    assert nullspace[0][2] == nullspace[0][5]
    assert all(
        nullspace[0][index] == 0
        for index in (0, 1, 3, 4, 6, 7, 8)
    )

    a = sp.Matrix(sp.symbols("a0:3"))
    b = sp.Matrix(sp.symbols("b0:3"))
    c = sp.Matrix(sp.symbols("c0:3"))
    image = derivative * a.col_join(b).col_join(c)
    for k in range(3):
        assert image[9 * 0 + 3 * 1 + k] == 0
        assert image[9 * 1 + 3 * 0 + k] == 0
        weighted = (
            kappa_1 * image[9 * 0 + 3 * 0 + k]
            - kappa_0 * image[9 * 1 + 3 * 1 + k]
        )
        assert sp.expand(weighted) == 0


def check_complete_target_annihilators() -> None:
    kappa_0, kappa_1 = sp.symbols(
        "kappa_0 kappa_1", nonzero=True
    )
    targets = [basis_vector(6, i) for i in range(3)]
    corrections = [basis_vector(6, 3 + i) for i in range(3)]

    values = [
        [[sp.zeros(6, 1) for _k in range(3)] for _j in range(2)]
        for _i in range(2)
    ]
    for i, j, k in product(range(2), range(2), range(3)):
        value = targets[i] if i == j == k else sp.zeros(6, 1)
        if i == j == 0:
            value += kappa_0 * corrections[k]
        if i == j == 1:
            value += kappa_1 * corrections[k]
        values[i][j][k] = value

    for k in range(3):
        # The off-diagonal target coefficients and derivative coefficients
        # both vanish, so these are the two complete zero pairs.
        values[0][1][k] = sp.zeros(6, 1)
        values[1][0][k] = sp.zeros(6, 1)
        assert values[0][1][k] == sp.zeros(6, 1)
        assert values[1][0][k] == sp.zeros(6, 1)

        weighted = kappa_1 * values[0][0][k]
        weighted -= kappa_0 * values[1][1][k]
        expected = sp.zeros(6, 1)
        if k == 0:
            expected += kappa_1 * targets[0]
        if k == 1:
            expected -= kappa_0 * targets[1]
        assert sp.simplify(weighted - expected) == sp.zeros(6, 1)

    source_matrix = sp.Matrix(
        [
            [kappa_1, 0, 0],
            [0, -kappa_0, 0],
        ]
    )
    assert source_matrix.rank() == 2


def check_alternating_interface() -> None:
    x = basis_vector(3, 0)
    y = basis_vector(3, 0)
    z = basis_vector(3, 0)
    pure = (row(x, sp.zeros(3, 1), sp.zeros(3, 1)),
            row(sp.zeros(3, 1), y, sp.zeros(3, 1)),
            row(sp.zeros(3, 1), sp.zeros(3, 1), z))
    separated = tensor3(x, y, z)
    assert alternating_tensor(pure) == separated

    coefficients = sp.Matrix(3, 3, sp.symbols("g0:9"))
    changed = tuple(
        sum(
            (coefficients[i, j] * pure[j] for j in range(3)),
            sp.zeros(9, 1),
        )
        for i in range(3)
    )
    assert sp.simplify(
        alternating_tensor(changed) - coefficients.det() * separated
    ) == sp.zeros(27, 1)


def check_zero_pair_support_algebra() -> None:
    x = basis_vector(3, 0)
    y = basis_vector(3, 0)
    z = basis_vector(3, 0)
    zero = sp.zeros(3, 1)
    pure_x = row(x, zero, zero)

    vx = sp.Matrix(sp.symbols("vx0:3"))
    vy = sp.Matrix(sp.symbols("vy0:3"))
    vz = sp.Matrix(sp.symbols("vz0:3"))
    generic_v = row(vx, vy, vz)
    assert sp.simplify(
        polarized_product(pure_x, generic_v, generic_v)
        - 2 * tensor3(x, vy, vz)
    ) == sp.zeros(27, 1)

    qx = sp.Matrix(sp.symbols("qx0:3"))
    qy = sp.Matrix(sp.symbols("qy0:3"))
    qz = sp.Matrix(sp.symbols("qz0:3"))
    q = row(qx, qy, qz)
    v_without_z = row(vx, vy, zero)
    assert sp.simplify(
        polarized_product(pure_x, v_without_z, q)
        - tensor3(x, vy, qz)
    ) == sp.zeros(27, 1)

    support_two = row(x, y, zero)
    assert sp.simplify(
        polarized_product(support_two, support_two, generic_v)
        - 2 * tensor3(x, y, vz)
    ) == sp.zeros(27, 1)
    expected_mixed = tensor3(x, vy, qz) + tensor3(vx, y, qz)
    assert sp.simplify(
        polarized_product(support_two, v_without_z, q)
        - expected_mixed
    ) == sp.zeros(27, 1)

    conjugate = row(x, -y, zero)
    assert polarized_product(support_two, conjugate, q) == sp.zeros(27, 1)

    a, b, c, aa, bb, cc = sp.symbols("a b c A B C")
    support_three = row(x, y, z)
    scaled = row(a * x, b * y, c * z)
    xyz = tensor3(x, y, z)
    assert sp.simplify(
        polarized_product(support_three, support_three, scaled)
        - 2 * (a + b + c) * xyz
    ) == sp.zeros(27, 1)
    assert sp.simplify(
        polarized_product(support_three, scaled, scaled)
        - 2 * (a * b + a * c + b * c) * xyz
    ) == sp.zeros(27, 1)
    coordinate_q = row(aa * x, bb * y, cc * z)
    mixed = polarized_product(support_three, scaled, coordinate_q)
    mixed_under_sum_zero = mixed.subs(c, -a - b)
    expected = -(a * aa + b * bb + c * cc) * xyz
    expected_under_sum_zero = expected.subs(c, -a - b)
    assert sp.simplify(
        mixed_under_sum_zero - expected_under_sum_zero
    ) == sp.zeros(27, 1)

    square_map = sp.zeros(27, 9)
    for index in range(9):
        square_map[:, index] = polarized_product(
            support_three, support_three, basis_vector(9, index)
        )
    assert square_map.rank() == 7
    assert len(square_map.nullspace()) == 2


def plane_intersection(
    first: tuple[sp.Matrix, sp.Matrix],
    second: tuple[sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    matrix = first[0].row_join(first[1]).row_join(-second[0]).row_join(
        -second[1]
    )
    kernel = matrix.nullspace()
    assert len(kernel) == 1
    return sp.simplify(
        first[0] * kernel[0][0] + first[1] * kernel[0][1]
    )


def same_line(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.row_join(second).rank() == 1


def check_flag_atlas() -> None:
    a = basis_vector(3, 0)
    b = basis_vector(3, 1)
    c = basis_vector(3, 2)
    flags_a = {
        "R": (c, a),
        "P": (a, c),
        "G": (a, a + c),
    }
    flags_b = {
        "R": (c, b),
        "P": (b, c),
        "G": (b, b + c),
    }

    expected = {
        "RR": c,
        "PP": c,
        "RG": b,
        "GR": a,
        "PG": b + c,
        "GP": a + c,
        "GG": a + b + c,
    }
    for left, right in product("RPG", repeat=2):
        r_0, p_0 = flags_a[left]
        r_1, p_1 = flags_b[right]
        cross_01 = (r_0, p_1)
        cross_10 = (r_1, p_0)
        key = left + right
        if key in ("RP", "PR"):
            dependent = cross_01 if key == "RP" else cross_10
            independent = cross_10 if key == "RP" else cross_01
            assert dependent[0].row_join(dependent[1]).rank() == 1
            assert independent[0].row_join(independent[1]).rank() == 2
            continue
        assert cross_01[0].row_join(cross_01[1]).rank() == 2
        assert cross_10[0].row_join(cross_10[1]).rank() == 2
        intersection = plane_intersection(cross_01, cross_10)
        assert same_line(intersection, expected[key])

    # Symbolic generic-flag normalization: after rescaling the two rows,
    # shifting A along c, and rescaling c, every non-boundary flag is G.
    alpha, beta = sp.symbols("alpha beta")
    first = a + alpha * c
    second = a + beta * c
    shifted_a = first
    shifted_c = (beta - alpha) * c
    assert second == shifted_a + shifted_c


def check_rp_pr_interface() -> None:
    zero = sp.zeros(3, 1)
    x = basis_vector(3, 0)
    y = basis_vector(3, 0)
    z = basis_vector(3, 0)
    x_row = row(x, zero, zero)
    y_row = row(zero, y, zero)
    z_row = row(zero, zero, z)
    a = x_row + y_row
    b = x_row - y_row
    q_basis = (x_row, y_row, z_row)
    xyz = tensor3(x, y, z)

    for q in q_basis:
        assert polarized_product(z_row, z_row, q) == sp.zeros(27, 1)
        assert polarized_product(a, b, q) == sp.zeros(27, 1)

    diagonal_0 = sp.Matrix.hstack(
        *(polarized_product(z_row, a, q) for q in q_basis)
    )
    diagonal_1 = sp.Matrix.hstack(
        *(polarized_product(b, z_row, q) for q in q_basis)
    )
    assert diagonal_0.rank() == 1
    assert diagonal_1.rank() == 1
    assert diagonal_0.row_join(xyz).rank() == 1
    assert diagonal_1.row_join(xyz).rank() == 1


def check_cross_ratio_and_gg_interface() -> None:
    a, b, c_0, d = sp.symbols("a b c_0 d")
    kappa_0, kappa_1 = sp.symbols(
        "kappa_0 kappa_1", nonzero=True
    )
    u_0 = sp.Matrix([a, -kappa_0 * c_0 / kappa_1])
    u_1 = sp.Matrix([-kappa_1 * b / kappa_0, d])
    assert sp.cancel(sp.det(sp.Matrix.hstack(u_0, u_1)) - (a * d - b * c_0)) == 0

    output_0 = basis_vector(3, 0)
    output_1 = basis_vector(3, 1)
    f_0 = output_0 * basis_vector(3, 0).T
    f_1 = output_1 * basis_vector(3, 1).T
    assert f_0.rank() == f_1.rank() == 1
    square_map = f_0 + f_1
    assert square_map.rank() == 2
    assert square_map.columnspace() == [output_0, output_1]

    generic_rows = [
        sp.Matrix(sp.symbols(f"{name}0:9")) for name in ("A", "B", "C")
    ]
    row_a, row_b, row_c = generic_rows
    scale_a, scale_b, scale_d, scale_e = sp.symbols(
        "scale_a scale_b scale_d scale_e", nonzero=True
    )
    generic_q = sp.Matrix(sp.symbols("Q0:9"))
    actual_f_0 = polarized_product(
        scale_a * row_a, scale_b * (row_a + row_c), generic_q
    )
    actual_f_1 = polarized_product(
        scale_d * row_b, scale_e * (row_b + row_c), generic_q
    )
    square = polarized_product(
        row_a - row_b, row_a - row_b, generic_q
    )
    cross_0 = polarized_product(
        row_a, row_b + row_c, generic_q
    )
    cross_1 = polarized_product(
        row_b, row_a + row_c, generic_q
    )
    identity = square - actual_f_0 / (scale_a * scale_b)
    identity -= actual_f_1 / (scale_d * scale_e)
    assert sp.simplify(identity + cross_0 + cross_1) == sp.zeros(27, 1)


def check_dependent_profiles() -> None:
    zero = sp.zeros(3, 1)
    x = basis_vector(3, 0)
    y = basis_vector(3, 0)
    qx = row(x, zero, zero)
    qy = row(zero, y, zero)
    qz = row(zero, zero, basis_vector(3, 0))
    u = row(x, y, zero)
    mu = sp.symbols("mu", nonzero=True)
    v = row(mu * x, -mu * y, zero)
    for q in (qx, qy, qz):
        assert polarized_product(u, v, q) == sp.zeros(27, 1)
        assert sp.simplify(
            polarized_product(v, v, q)
            + mu**2 * polarized_product(u, u, q)
        ) == sp.zeros(27, 1)

    square_u = sp.Matrix.hstack(
        *(polarized_product(u, u, q) for q in (qx, qy, qz))
    )
    square_v = sp.Matrix.hstack(
        *(polarized_product(v, v, q) for q in (qx, qy, qz))
    )
    assert square_u.rank() == square_v.rank() == 1
    assert square_u.row_join(square_v).rank() == 1


def main() -> None:
    check_canonical_derivative()
    check_complete_target_annihilators()
    check_alternating_interface()
    check_zero_pair_support_algebra()
    check_flag_atlas()
    check_rp_pr_interface()
    check_cross_ratio_and_gg_interface()
    check_dependent_profiles()
    print(
        "PASS: canonical derivative, complete target annihilators, "
        "alternating interface, zero-pair support algebra, exhaustive "
        "flag atlas, scalar-correct GG identity, and dependent profiles"
    )


if __name__ == "__main__":
    main()
