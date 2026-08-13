"""Independent exact audit for the repeated-outer-factor divisor theorem.

This file imports no repository module and no third-party package.  It uses
standard-library Fraction arithmetic, a z-major tensor index (different from
the primary replay), and independently assembled row reductions.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

D = 3
W = 9
T = 27


def unit(index: int, size: int = D) -> tuple[F, ...]:
    return tuple(F(int(position == index)) for position in range(size))


ZERO3 = (F(0),) * 3


def vec(
    x: tuple[F, ...] = ZERO3,
    y: tuple[F, ...] = ZERO3,
    z: tuple[F, ...] = ZERO3,
) -> tuple[F, ...]:
    return x + y + z


def block(row: tuple[F, ...], source: int) -> tuple[F, ...]:
    return row[3 * source : 3 * source + 3]


def add(*rows: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(values, F(0)) for values in zip(*rows, strict=True))


def scale(value: F, row: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(value * entry for entry in row)


def tensor(x: tuple[F, ...], y: tuple[F, ...], z: tuple[F, ...]) -> tuple[F, ...]:
    answer = [F(0)] * T
    for i in range(D):
        for j in range(D):
            for k in range(D):
                answer[k * 9 + j * 3 + i] += x[i] * y[j] * z[k]
    return tuple(answer)


def permanent(a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]) -> tuple[F, ...]:
    rows = (a, b, c)
    answer = (F(0),) * T
    for order in permutations(range(3)):
        answer = add(
            answer,
            tensor(
                block(rows[order[0]], 0),
                block(rows[order[1]], 1),
                block(rows[order[2]], 2),
            ),
        )
    return answer


def alternating(a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]) -> tuple[F, ...]:
    rows = (a, b, c)
    answer = (F(0),) * T
    for order in permutations(range(3)):
        inversions = sum(
            order[i] > order[j] for i in range(3) for j in range(i + 1, 3)
        )
        term = tensor(
            block(rows[order[0]], 0),
            block(rows[order[1]], 1),
            block(rows[order[2]], 2),
        )
        answer = add(answer, scale(F((-1) ** inversions), term))
    return answer


def columns_to_rows(columns: list[tuple[F, ...]]) -> list[list[F]]:
    return [list(row) for row in zip(*columns, strict=True)]


def rank(rows: list[list[F]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row:
                continue
            multiple = matrix[index][column]
            if multiple:
                matrix[index] = [
                    left - multiple * right
                    for left, right in zip(
                        matrix[index], matrix[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def linear_map(a: tuple[F, ...], b: tuple[F, ...]) -> list[list[F]]:
    basis = [unit(index, W) for index in range(W)]
    return columns_to_rows([permanent(a, b, q) for q in basis])


def matvec(rows: list[list[F]], vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(
        sum((entry * value for entry, value in zip(row, vector, strict=True)), F(0))
        for row in rows
    )


def repeated_derivative() -> None:
    lam, mu, nu = F(2), F(3), F(5)
    s, t = 0, 1
    z = (F(1), F(2), F(4))
    derivative_columns: list[tuple[F, ...]] = []
    for index in range(3):
        derivative_columns.append(scale(-mu, tensor(unit(index), unit(t), z)))
    for index in range(3):
        derivative_columns.append(
            scale(-lam * nu, tensor(unit(s), unit(index), unit(s)))
        )
    for index in range(3):
        derivative_columns.append(
            scale(lam * mu, tensor(unit(s), unit(t), unit(index)))
        )
    derivative = columns_to_rows(derivative_columns)
    k1 = scale(lam, unit(s)) + ZERO3 + z
    k2 = ZERO3 + scale(mu, unit(t)) + scale(nu, unit(s))
    assert matvec(derivative, k1) == (F(0),) * T
    assert matvec(derivative, k2) == (F(0),) * T
    assert rank(derivative) == 7

    alpha = (F(-7, 2), F(3), F(6))
    gamma = (F(1), F(1), F(1))
    gamma_z = sum((gamma[i] * z[i] for i in range(3)), F(0))
    assert alpha[s] == -gamma_z / lam
    beta = (F(8), -nu * gamma[s] / mu, F(9))
    ell = alpha + beta + gamma
    transpose = (
        scale(-mu * beta[t] * gamma_z, alpha)
        + scale(-lam * nu * alpha[s] * gamma[s], beta)
        + scale(lam * mu * alpha[s] * beta[t], gamma)
    )
    assert transpose == scale(nu * gamma_z * gamma[s], ell)
    print("independent derivative/recovery: PASS")


def equal_plane_and_radical() -> None:
    x, y, z = unit(0), unit(0), unit(0)
    full = vec(x, y, z)
    q1, q2 = vec(x, scale(F(-1), y), ZERO3), vec(x, ZERO3, scale(F(-1), z))
    mixed_columns = [
        permanent(full, unit(index, W), q1)
        + permanent(full, unit(index, W), q2)
        for index in range(W)
    ]
    # Stacking, not adding, is required for the actual rank-eight system.
    stacked_columns = [
        permanent(full, unit(index, W), q1)
        + permanent(full, unit(index, W), q2)
        for index in range(W)
    ]
    assert rank(columns_to_rows(mixed_columns)) <= 8
    actual = [
        list(row)
        for row in zip(
            *[
                permanent(full, unit(index, W), q1)
                + permanent(full, unit(index, W), q2)
                for index in range(W)
            ],
            strict=True,
        )
    ]
    assert rank(actual) <= 8
    # Independently stack the two 27-row systems.
    m1 = columns_to_rows([permanent(full, unit(i, W), q1) for i in range(W)])
    m2 = columns_to_rows([permanent(full, unit(i, W), q2) for i in range(W)])
    assert rank(m1 + m2) == 8
    assert stacked_columns

    v = vec(x, ZERO3, ZERO3)
    a = vec(ZERO3, y, z)
    p = vec(unit(1), y, scale(F(-1), z))
    q_basis = (
        vec(unit(1), ZERO3, ZERO3),
        vec(unit(2), ZERO3, ZERO3),
        vec(ZERO3, y, scale(F(-1), z)),
    )
    assert alternating(v, a, p) != (F(0),) * T
    assert all(permanent(v, a, q) == (F(0),) * T for q in q_basis)
    assert all(permanent(a, p, q) == (F(0),) * T for q in q_basis)
    core = columns_to_rows([permanent(v, p, q) for q in q_basis])
    assert rank(core) == 1
    assert permanent(v, p, q_basis[2]) == scale(F(-2), tensor(x, y, z))
    print("independent equal-plane/common-radical atlas: PASS")


def zero_rectangle_atlas() -> None:
    x, y, z = unit(0), unit(0), unit(0)
    pure = vec(x, ZERO3, ZERO3)
    sy, sz = vec(ZERO3, unit(1), ZERO3), vec(ZERO3, ZERO3, unit(1))
    pure_common = linear_map(pure, sy) + linear_map(pure, sz)
    assert rank(pure_common) == 6

    two = vec(x, y, ZERO3)
    k = vec(x, scale(F(-1), y), ZERO3)
    inside_xy = vec(unit(1), unit(2), ZERO3)
    inside_kz = add(k, vec(ZERO3, ZERO3, unit(1)))
    outside = vec(unit(1), ZERO3, unit(1))
    assert 9 - rank(linear_map(two, inside_xy)) >= 3
    assert 9 - rank(linear_map(two, inside_kz)) >= 3
    assert 9 - rank(linear_map(two, outside)) == 2

    a, b, v = vec(ZERO3, ZERO3, z), k, vec(ZERO3, ZERO3, z)
    q_basis = (k, vec(ZERO3, ZERO3, unit(1)), vec(ZERO3, ZERO3, unit(2)))
    assert alternating(a, b, two) != (F(0),) * T
    assert all(
        permanent(two, row, q) == (F(0),) * T
        for row in (a, b)
        for q in q_basis
    )
    assert rank(columns_to_rows([permanent(b, v, q) for q in q_basis])) == 1

    full = vec(x, y, z)
    f1 = vec(unit(1), y, scale(F(-1), z))
    f2 = vec(unit(2), scale(F(2), y), scale(F(-2), z))
    common = linear_map(full, f1) + linear_map(full, f2)
    assert rank(common) == 6
    assert alternating(f1, f2, full) != (F(0),) * T
    for qx in (vec(unit(0), ZERO3, ZERO3), vec(unit(1), ZERO3, ZERO3), vec(unit(2), ZERO3, ZERO3)):
        assert matvec(common, qx) == (F(0),) * len(common)
    assert rank(columns_to_rows([permanent(f1, f2, vec(unit(i), ZERO3, ZERO3)) for i in range(3)])) == 3

    lx = vec(unit(1), y, scale(F(-1), z))
    ly = vec(x, unit(1), scale(F(-1), z))
    lz = vec(x, scale(F(-1), y), unit(1))
    off = vec(unit(1), unit(1), z)
    assert all(9 - rank(linear_map(full, row)) >= 3 for row in (lx, ly, lz))
    assert 9 - rank(linear_map(full, off)) <= 2
    print("independent zero-rectangle rank atlas: PASS")


def main() -> None:
    repeated_derivative()
    equal_plane_and_radical()
    zero_rectangle_atlas()
    print("independent repeated-outer-factor audit: PASS")


if __name__ == "__main__":
    main()
