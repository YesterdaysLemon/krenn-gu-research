#!/usr/bin/env python3
"""Exact replay for the lower-rank transverse q=1 pair-pole exclusion."""

from __future__ import annotations

import itertools

import sympy as sp

DIM = 3
TOTAL = 3 * DIM
TENSOR_DIM = DIM**3


def e(source: int, index: int) -> sp.Matrix:
    vector = sp.zeros(TOTAL, 1)
    vector[source * DIM + index] = 1
    return vector


def split(row: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return row[:DIM, :], row[DIM : 2 * DIM, :], row[2 * DIM :, :]


def tensor(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def permanent(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Matrix:
    pieces = split(first), split(second), split(third)
    result = sp.zeros(TENSOR_DIM, 1)
    for assignment in itertools.permutations(range(3)):
        result += tensor(
            pieces[assignment[0]][0],
            pieces[assignment[1]][1],
            pieces[assignment[2]][2],
        )
    return sp.simplify(result)


def permutation_sign(assignment: tuple[int, int, int]) -> int:
    inversions = sum(
        assignment[left] > assignment[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def alternating(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Matrix:
    pieces = split(first), split(second), split(third)
    result = sp.zeros(TENSOR_DIM, 1)
    for assignment in itertools.permutations(range(3)):
        result += permutation_sign(assignment) * tensor(
            pieces[assignment[0]][0],
            pieces[assignment[1]][1],
            pieces[assignment[2]][2],
        )
    return sp.simplify(result)


def source_kernel_matrix(v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(permanent(e(source, index), v, q) for source in range(3) for index in range(DIM))
    )


def two_source_atlas() -> None:
    p_0, p_1, r_0, r_1 = sp.symbols("p_0 p_1 r_0 r_1")
    x, x_1 = e(0, 0), e(0, 1)
    y, y_1, y_2 = e(1, 0), e(1, 1), e(1, 2)
    z, z_1 = e(2, 0), e(2, 1)
    p = p_0 * x + p_1 * x_1
    r = r_0 * z + r_1 * z_1
    v = x + z
    q = p + y + r
    a_0 = -x + z
    b_0 = -p + y - r

    zero = sp.zeros(TENSOR_DIM, 1)
    assert permanent(a_0, v, q) == zero
    assert permanent(b_0, v, q) == zero
    assert alternating(a_0, b_0, v) == -2 * tensor(split(x)[0], split(y)[1], split(z)[2])

    exceptional_q = y
    exceptional_a = a_0 + y_1
    exceptional_b = y_2
    assert permanent(exceptional_a, v, exceptional_q) == zero
    assert permanent(exceptional_b, v, exceptional_q) == zero
    assert permanent(exceptional_a, exceptional_b, exceptional_q) == zero
    expected = -2 * tensor(split(x)[0], split(y_2)[1], split(z)[2])
    assert alternating(exceptional_a, exceptional_b, v) == expected
    assert source_kernel_matrix(v, exceptional_q).rank() == 5
    print("two-source atlas: PASS (regular xyz / conjugate xYz determinants)")


def transverse_target_atlas() -> None:
    x, y, z = e(0, 0), e(1, 0), e(2, 0)
    target_z, extra_z = e(2, 1), e(2, 2)
    v = x + y + z

    # alpha=beta=1: the two displayed common zeros also obey the last
    # one-cell mixed equation and have determinant on the target xyz_s line.
    q = x + y + target_z - 2 * z
    a = x + y + z - target_z
    b = x - y
    zero = sp.zeros(TENSOR_DIM, 1)
    assert permanent(a, v, q) == zero
    assert permanent(b, v, q) == zero
    assert permanent(a, b, q) == zero
    assert alternating(a, b, v) == -2 * tensor(split(x)[0], split(y)[1], split(target_z)[2])

    # alpha+beta=0, alpha!=0 has kernel exactly the whole Z summand.
    skew_q = x - y + target_z
    kernel = source_kernel_matrix(v, skew_q).nullspace()
    assert len(kernel) == DIM
    assert all(vector[: 2 * DIM, :] == sp.zeros(2 * DIM, 1) for vector in kernel)

    # alpha=beta=0 is the exceptional x*y*L_Z determinant chart.
    pure_q = target_z
    exceptional_a = -x + y
    exceptional_b = extra_z
    assert permanent(exceptional_a, v, pure_q) == zero
    assert permanent(exceptional_b, v, pure_q) == zero
    assert permanent(exceptional_a, exceptional_b, pure_q) == zero
    assert alternating(exceptional_a, exceptional_b, v) == 2 * tensor(
        split(x)[0], split(y)[1], split(extra_z)[2]
    )
    print("three-source transverse-target atlas: PASS (all alpha+beta charts)")


def aligned_target_atlas() -> None:
    x, x_1 = e(0, 0), e(0, 1)
    y, y_1 = e(1, 0), e(1, 1)
    z = e(2, 0)
    v = x + y + z
    zero = sp.zeros(TENSOR_DIM, 1)

    # No zero h-weight: q=x+y+z and an exact orthogonal kernel basis.
    q_regular = x + y + z
    a_regular = x - y
    b_regular = x + y - 2 * z
    assert permanent(a_regular, v, q_regular) == zero
    assert permanent(b_regular, v, q_regular) == zero
    assert permanent(a_regular, b_regular, q_regular) == zero
    assert alternating(a_regular, b_regular, v) == 6 * tensor(
        split(x)[0], split(y)[1], split(z)[2]
    )

    # Exactly h_X=0: q=x, kernel X direct-sum span(y-z).
    q_one_zero = x
    a_one_zero = x_1
    b_one_zero = y - z
    assert permanent(a_one_zero, v, q_one_zero) == zero
    assert permanent(b_one_zero, v, q_one_zero) == zero
    assert permanent(a_one_zero, b_one_zero, q_one_zero) == zero
    assert alternating(a_one_zero, b_one_zero, v) == 2 * tensor(
        split(x_1)[0], split(y)[1], split(z)[2]
    )

    # h_X=h_Y=0: q=x+y-z, kernel X direct-sum Y.
    q_two_zero = x + y - z
    a_two_zero = x_1 + y_1
    b_two_zero = x_1 - y_1
    assert permanent(a_two_zero, v, q_two_zero) == zero
    assert permanent(b_two_zero, v, q_two_zero) == zero
    assert permanent(a_two_zero, b_two_zero, q_two_zero) == zero
    assert alternating(a_two_zero, b_two_zero, v) == -2 * tensor(
        split(x_1)[0], split(y_1)[1], split(z)[2]
    )
    print("three-source aligned-target atlas: PASS (zero-weight census)")


def cramer_data(matrix: sp.Matrix, residual: sp.Matrix) -> tuple[sp.Expr, list[sp.Expr]]:
    determinant = sp.factor(matrix.det())
    numerators: list[sp.Expr] = []
    for column in range(3):
        replaced = matrix.copy()
        replaced[:, column] = residual
        numerators.append(sp.factor(replaced.det()))
    return determinant, numerators


def assert_coordinate_pole(
    determinant: sp.Expr, numerator: sp.Expr, coordinate: sp.Symbol
) -> None:
    assert sp.expand(determinant).subs(coordinate, 0) == 0
    assert sp.expand(numerator).subs(coordinate, 0) != 0


def cramer_residues() -> None:
    xs, xt, xu = sp.symbols("x_s x_t x_u")
    ys, yt, yu = sp.symbols("y_s y_t y_u")
    zs, zt, zu = sp.symbols("z_s z_t z_u")
    target_t = xt * yt * zt
    target_u = xu * yu * zu
    residual = sp.Matrix([target_t, target_u, 0])

    # Regular two-source chart: all three missing-colour factors occur.
    regular = sp.Matrix([[-xs, 0, zs], [-xs, ys, 0], [xs, 0, zs]])
    determinant, numerators = cramer_data(regular, residual)
    assert determinant == -2 * xs * ys * zs
    assert_coordinate_pole(determinant, numerators[0], xs)
    assert_coordinate_pole(determinant, numerators[2], zs)

    # Conjugate two-source chart: the surviving Y component cannot remove
    # both coprime residual target monomials.
    conjugate = sp.Matrix([[-xs, 0, zs], [0, yt, 0], [xs, 0, zs]])
    determinant, numerators = cramer_data(conjugate, residual)
    assert determinant == -2 * xs * yt * zs
    assert_coordinate_pole(determinant, numerators[0], xs)
    assert_coordinate_pole(determinant, numerators[2], zs)

    # Transverse target factor: Delta has x_s,y_s but not necessarily z_s.
    transverse = sp.Matrix([[-xs, ys, 0], [0, 0, zu], [xs, ys, zt]])
    determinant, numerators = cramer_data(transverse, residual)
    assert determinant == 2 * xs * ys * zu
    assert_coordinate_pole(determinant, numerators[0], xs)
    assert_coordinate_pole(determinant, numerators[1], ys)

    # Exactly one zero h-weight: the y_s,z_s residues are unavoidable.
    one_zero = sp.Matrix([[xt, 0, 0], [0, ys, -zs], [xs, ys, zs]])
    determinant, numerators = cramer_data(one_zero, residual)
    assert determinant == 2 * xt * ys * zs
    assert_coordinate_pole(determinant, numerators[1], ys)
    assert_coordinate_pole(determinant, numerators[2], zs)

    # Exactly two zero h-weights: the sole z_s numerator is nonzero whenever
    # the alternating XY factor is nonzero.
    two_zero = sp.Matrix([[xt, yt, 0], [xt, -yt, 0], [xs, ys, zs]])
    determinant, numerators = cramer_data(two_zero, residual)
    assert determinant == -2 * xt * yt * zs
    assert_coordinate_pole(determinant, numerators[2], zs)

    a, b, c, d, x, y, z, target_left, target_right = sp.symbols(
        "A B C D x y z T_t T_u"
    )
    general_two_zero = sp.Matrix([[a, c, 0], [b, d, 0], [x, y, z]])
    determinant, numerators = cramer_data(
        general_two_zero, sp.Matrix([target_left, target_right, 0])
    )
    assert determinant == z * (a * d - b * c)
    assert sp.expand(numerators[2]) == sp.expand(
        target_right * (x * c - y * a) + target_left * (y * b - x * d)
    )
    print("Cramer residues: PASS (all atlas divisor types have a pole)")


def main() -> None:
    two_source_atlas()
    transverse_target_atlas()
    aligned_target_atlas()
    cramer_residues()
    print("lower-rank transverse q=1 complete pair-pole exclusion replay: PASS")


if __name__ == "__main__":
    main()
