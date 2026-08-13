"""Independent Fraction audit of the (1,2,2) coloop localization."""

from __future__ import annotations

from fractions import Fraction as Q


def basis(i: int, n: int = 3) -> tuple[Q, ...]:
    return tuple(Q(int(i == j)) for j in range(n))


def zero(n: int) -> tuple[Q, ...]:
    return (Q(0),) * n


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(c: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(c * value for value in vector)


def inner(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def tensor2(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a * b for a in left for b in right)


def tensor3(
    left: tuple[Q, ...], middle: tuple[Q, ...], right: tuple[Q, ...]
) -> tuple[Q, ...]:
    return tuple(a * b * c for a in left for b in middle for c in right)


def stack(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(value for vector in vectors for value in vector)


def rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def matvec(columns: list[tuple[Q, ...]], vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(
        sum((columns[j][i] * vector[j] for j in range(len(columns))), Q(0))
        for i in range(len(columns[0]))
    )


def transpose_matvec(
    columns: list[tuple[Q, ...]], vector: tuple[Q, ...]
) -> tuple[Q, ...]:
    return tuple(inner(column, vector) for column in columns)


def derivative_columns(
    y: tuple[Q, ...],
    z: tuple[Q, ...],
    w: tuple[Q, ...],
    s: int,
    t: int,
    lam: Q,
    mu: Q,
) -> list[tuple[Q, ...]]:
    b23 = add(tensor2(y, w), scale(-mu, tensor2(basis(t), z)))
    columns = [tuple(a * value for a in basis(i) for value in b23) for i in range(3)]
    columns += [scale(-lam, tensor3(basis(s), basis(j), w)) for j in range(3)]
    columns += [
        scale(lam * mu, tensor3(basis(s), basis(t), basis(k))) for k in range(3)
    ]
    return columns


def audit_gauge_and_derivative() -> None:
    lam, mu = Q(2), Q(3)
    s, t = 0, 1
    y_old = (Q(2), Q(5), Q(7))
    z_old = (Q(3), Q(4), Q(1))
    w = (Q(1), Q(2), Q(6))
    shift = y_old[t] / mu
    y = add(y_old, scale(-shift * mu, basis(t)))
    z = add(z_old, scale(-shift, w))
    assert y[t] == 0
    old_b23 = add(tensor2(y_old, w), scale(-mu, tensor2(basis(t), z_old)))
    new_b23 = add(tensor2(y, w), scale(-mu, tensor2(basis(t), z)))
    assert old_b23 == new_b23

    columns = derivative_columns(y, z, w, s, t, lam, mu)
    matrix_rows = [[column[i] for column in columns] for i in range(27)]
    assert rank(matrix_rows) == 7
    k1 = stack(scale(lam, basis(s)), y, z)
    k2 = stack(zero(3), scale(mu, basis(t)), w)
    assert matvec(columns, k1) == zero(27)
    assert matvec(columns, k2) == zero(27)
    print("independent (1,2,2) gauge/derivative: PASS")


def audit_recovery() -> None:
    lam, mu = Q(2), Q(3)
    s, t = 0, 1
    y = (Q(2), Q(0), Q(7))
    z = (Q(-4, 3), Q(2, 3), Q(-9))
    w = (Q(1), Q(2), Q(6))
    columns = derivative_columns(y, z, w, s, t, lam, mu)
    for gamma, alpha_tail, beta_tail in (
        ((Q(1), Q(2), Q(5)), (Q(3), Q(7)), (Q(4), Q(6))),
        ((Q(-2), Q(3), Q(1)), (Q(5), Q(-1)), (Q(8), Q(2))),
        ((Q(4), Q(-1), Q(6)), (Q(-3), Q(9)), (Q(7), Q(-5))),
    ):
        beta_t = -inner(gamma, w) / mu
        beta = (beta_tail[0], beta_t, beta_tail[1])
        alpha_s = -(inner(beta, y) + inner(gamma, z)) / lam
        alpha = (alpha_s, alpha_tail[0], alpha_tail[1])
        ell = stack(alpha, beta, gamma)
        got = transpose_matvec(columns, tensor3(alpha, beta, gamma))
        expected = scale(lam * mu * alpha_s * beta_t, ell)
        assert got == expected
    print("independent (1,2,2) recovery: PASS")


def audit_coordinate_atlas() -> None:
    lam, mu = Q(2), Q(3)
    s, t = 0, 1
    y = (Q(2), Q(0), Q(7))
    z = (Q(1), Q(4), Q(3))
    w = (Q(5), Q(2), Q(6))
    k1 = list(stack(scale(lam, basis(s)), y, z))
    k2 = list(stack(zero(3), scale(mu, basis(t)), w))
    assert rank([k1, k2]) == 2
    for coordinate in range(9):
        unit = [Q(0)] * 9
        unit[coordinate] = Q(1)
        assert rank([k1, k2, unit]) == 3

    # Build the seven parameter columns independently.
    parameters: list[tuple[Q, ...]] = []
    for i in range(3):
        if i != s:
            parameters.append(stack(basis(i), zero(3), zero(3)))
    for j in range(3):
        if j != t:
            parameters.append(stack(scale(-y[j] / lam, basis(s)), basis(j), zero(3)))
    for k in range(3):
        parameters.append(
            stack(
                scale(-z[k] / lam, basis(s)),
                scale(-w[k] / mu, basis(t)),
                basis(k),
            )
        )
    parameter_rows = [[column[row] for column in parameters] for row in range(9)]
    assert rank(parameter_rows) == 7
    assert all(inner(tuple(k1), column) == 0 for column in parameters)
    assert all(inner(tuple(k2), column) == 0 for column in parameters)

    r_columns = (0, 1)
    for coordinate in (s, 3, 4, 5, 6, 7, 8):
        assert all(parameters[column][coordinate] == 0 for column in r_columns)
    assert parameters[0][1] != 0 and parameters[1][2] != 0
    print("independent (1,2,2) nine-coloop atlas: PASS")


def main() -> None:
    audit_gauge_and_derivative()
    audit_recovery()
    audit_coordinate_atlas()
    print("independent (1,2,2) coordinate-coloop audit: PASS")


if __name__ == "__main__":
    main()
