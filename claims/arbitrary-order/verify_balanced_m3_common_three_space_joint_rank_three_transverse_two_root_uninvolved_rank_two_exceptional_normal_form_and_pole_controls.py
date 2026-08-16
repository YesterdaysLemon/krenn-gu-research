#!/usr/bin/env python3
"""Exact replay for the joint-rank-three q=2 exceptional controls."""

from __future__ import annotations

import itertools

import sympy as sp

DIM = 3
ROOT_DIM = 3 * DIM
TENSOR_DIM = DIM**3
D, C, J = 0, 1, 2


def e(index: int, size: int = DIM) -> sp.Matrix:
    return sp.eye(size)[:, index]


def root_tensor(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def split_sources(row: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return row[:DIM, :], row[DIM : 2 * DIM, :], row[2 * DIM :, :]


def permanent_rows(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    pieces = split_sources(left), split_sources(middle), split_sources(right)
    total = sp.zeros(TENSOR_DIM, 1)
    for assignment in itertools.permutations(range(3)):
        total += root_tensor(
            pieces[assignment[0]][0],
            pieces[assignment[1]][1],
            pieces[assignment[2]][2],
        )
    return sp.simplify(total)


def sign(assignment: tuple[int, int, int]) -> int:
    inversions = sum(
        assignment[left] > assignment[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def alternating_rows(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Matrix:
    pieces = split_sources(first), split_sources(second), split_sources(third)
    total = sp.zeros(TENSOR_DIM, 1)
    for assignment in itertools.permutations(range(3)):
        total += sign(assignment) * root_tensor(
            pieces[assignment[0]][0],
            pieces[assignment[1]][1],
            pieces[assignment[2]][2],
        )
    return sp.simplify(total)


def target(index: int) -> sp.Matrix:
    return root_tensor(e(index), e(index), e(index))


def transverse_derivative() -> sp.Matrix:
    b_23 = sp.kronecker_product(e(D), e(D))
    columns = [sp.kronecker_product(e(index), b_23) for index in range(DIM)]
    columns += [root_tensor(e(C), e(index), e(C)) for index in range(DIM)]
    columns += [sp.zeros(TENSOR_DIM, 1) for _ in range(DIM)]
    return sp.Matrix.hstack(*columns)


def relation_plane() -> sp.Matrix:
    first = sp.Matrix.vstack(e(D), sp.zeros(DIM, 1))
    second = sp.Matrix.vstack(sp.zeros(DIM, 1), e(C))
    third = sp.Matrix.vstack(e(J), e(J))
    return sp.Matrix.hstack(first, second, third)


def source_rows() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    x = e(J, ROOT_DIM)
    y = e(DIM + J, ROOT_DIM)
    z = e(2 * DIM + J, ROOT_DIM)
    a = -2 * y + z
    b = 2 * x - z
    v = x + y
    w = x - y
    q = (x + y + z) / 2
    return a, b, v, w, q


def root_rows(
    support: int,
) -> tuple[list[sp.Matrix], list[sp.Matrix], list[sp.Matrix]]:
    a, b, v, w, q = source_rows()
    zero = sp.zeros(ROOT_DIM, 1)
    rho = [a, zero, v]
    pi = [zero, b, v]
    if support == 1:
        theta = [zero, w, q]
    else:
        gamma = sp.Rational(2)
        theta = [w, gamma * w, q]
    return rho, pi, theta


def conjugate_normalization() -> None:
    lam, mu = sp.symbols("lambda mu", nonzero=True)
    x = e(J, ROOT_DIM)
    y = e(DIM + J, ROOT_DIM)
    z = e(2 * DIM + J, ROOT_DIM)
    w = x - y
    u = -lam * x - mu * y + z
    q_1 = lam * x + mu * y + z
    shift = (mu - lam) / 2
    nu = (lam + mu) / 2

    shifted_q = sp.simplify(q_1 + shift * w)
    shifted_u = sp.simplify(u - shift * w)
    assert shifted_q == nu * (x + y) + z
    assert shifted_u == -nu * (x + y) + z

    a, b, v, normalized_w, q = source_rows()
    assert a == normalized_w + (-x - y + z)
    assert b == normalized_w - (-x - y + z)
    assert permanent_rows(v, v, normalized_w) == sp.zeros(TENSOR_DIM, 1)
    assert permanent_rows(v, v, q) == target(J)
    for left, middle in ((a, v), (v, b), (a, b)):
        assert permanent_rows(left, middle, normalized_w) == sp.zeros(TENSOR_DIM, 1)
        assert permanent_rows(left, middle, q) == sp.zeros(TENSOR_DIM, 1)
    assert alternating_rows(a, b, v) == 4 * target(J)
    print("conjugate normalization: PASS (unique w+u / w-u chart)")


def derivative_and_singletons() -> tuple[sp.Matrix, sp.Matrix]:
    derivative = transverse_derivative()
    plane = relation_plane()
    assert derivative.rank() == 6
    assert plane.rank() == 3
    singleton_basis = derivative[:, : 2 * DIM] * plane
    expected = sp.Matrix.hstack(
        target(D),
        target(C),
        root_tensor(e(J), e(D), e(D)) + root_tensor(e(C), e(J), e(C)),
    )
    assert singleton_basis == expected
    assert singleton_basis.rank() == 3
    assert sp.Matrix.hstack(singleton_basis, target(J)).rank() == 4
    print("derivative/relation plane: PASS (rank six / singleton rank three)")
    return derivative, singleton_basis


def coefficient_projection(rows: list[sp.Matrix], source_index: int) -> sp.Matrix:
    return sp.Matrix([entry[source_index] for entry in rows])


def control_projection(
    rho: list[sp.Matrix], pi: list[sp.Matrix]
) -> sp.Matrix:
    columns = []
    for source_index in (J, DIM + J, 2 * DIM + J):
        columns.append(
            sp.Matrix.vstack(
                coefficient_projection(rho, source_index),
                coefficient_projection(pi, source_index),
            )
        )
    return sp.Matrix.hstack(*columns)


def check_control(support: int, derivative: sp.Matrix, singleton_basis: sp.Matrix) -> None:
    rho, pi, theta = root_rows(support)
    all_rows = sp.Matrix.hstack(*rho, *pi, *theta)
    theta_matrix = sp.Matrix.hstack(*theta)
    assert all_rows.rank() == 3
    assert theta_matrix.rank() == 2
    kernel = theta_matrix.nullspace()
    assert len(kernel) == 1
    if support == 1:
        assert kernel[0].cross(e(D)) == sp.zeros(DIM, 1)
    else:
        assert all(entry != 0 for entry in kernel[0][:2, :])
        assert kernel[0][2] == 0

    nonzero_cells: list[tuple[int, int, int]] = []
    for left, middle, right in itertools.product(range(DIM), repeat=3):
        value = permanent_rows(rho[left], pi[middle], theta[right])
        expected = target(J) if (left, middle, right) == (J, J, J) else sp.zeros(
            TENSOR_DIM, 1
        )
        assert value == expected
        if value != sp.zeros(TENSOR_DIM, 1):
            nonzero_cells.append((left, middle, right))
    assert nonzero_cells == [(J, J, J)]

    projection = control_projection(rho, pi)
    plane = relation_plane()
    assert projection.rank() == 3
    assert sp.Matrix.hstack(projection, plane).rank() == 3
    physical_singletons = derivative[:, : 2 * DIM] * projection
    coordinates = singleton_basis.gauss_jordan_solve(physical_singletons)[0]
    expected_coordinates = sp.Matrix(
        [
            [0, -2, 1],
            [2, 0, -1],
            [1, 1, 0],
        ]
    )
    assert coordinates == expected_coordinates
    print(f"support-{support} physical control: PASS (all 27 empty cells)")


def pair_lift() -> None:
    x, y, z, target_d, target_c = sp.symbols("x y z T_d T_c", nonzero=True)
    singleton_matrix = sp.Matrix(
        [
            [0, -2 * y, z],
            [2 * x, 0, -z],
            [x, y, 0],
        ]
    )
    assert sp.factor(singleton_matrix.det()) == 4 * x * y * z
    coefficients = sp.Matrix(
        [
            (target_d + target_c) / (4 * x),
            -(target_d + target_c) / (4 * y),
            (target_d - target_c) / (2 * z),
        ]
    )
    assert sp.simplify(singleton_matrix * coefficients) == sp.Matrix(
        [target_d, target_c, 0]
    )
    assert sp.simplify(
        singleton_matrix.inv() * sp.Matrix([target_d, target_c, 0]) - coefficients
    ) == sp.zeros(3, 1)
    denominators = [sp.factor(sp.denom(sp.together(entry))) for entry in coefficients]
    assert denominators == [4 * x, 4 * y, 2 * z]
    assert all(
        sp.factor(sp.numer(sp.together(entry))).subs(divisor, 0) != 0
        for entry, divisor in zip(coefficients, (x, y, z), strict=True)
    )
    print("rational pair lift: PASS (unique coefficients / x*y*z poles)")


def main() -> None:
    conjugate_normalization()
    derivative, singleton_basis = derivative_and_singletons()
    check_control(1, derivative, singleton_basis)
    check_control(2, derivative, singleton_basis)
    pair_lift()
    print("joint-rank-three q=2 exceptional-control replay: PASS")


if __name__ == "__main__":
    main()
