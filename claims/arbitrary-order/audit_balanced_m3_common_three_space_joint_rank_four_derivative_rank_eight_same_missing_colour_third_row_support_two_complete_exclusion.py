#!/usr/bin/env python3
"""Independent no-import audit for the S2BW support-two exclusion."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

N = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(N)


def unit(index: int) -> tuple[F, ...]:
    return tuple(F(i == index) for i in range(N))


def zero() -> tuple[F, ...]:
    return (F(0),) * N


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(value[i] for value in vectors) for i in range(len(vectors[0])))


def scale(scalar: F, vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(scalar * value for value in vector)


def tensor(
    a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    return {
        (i, j, k): value
        for i, j, k in product(range(N), repeat=3)
        if (value := a[i] * b[j] * c[k])
    }


def tensor_add(
    *values: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int, int], F]:
    keys = set().union(*(value.keys() for value in values))
    return {
        key: total
        for key in keys
        if (total := sum(value.get(key, F(0)) for value in values))
    }


def tensor_scale(
    scalar: F, value: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int, int], F]:
    return {key: scalar * item for key, item in value.items() if scalar * item}


def c_tensor(
    C: list[list[F]], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    return {
        (i, j, k): value
        for i, j, k in product(range(N), repeat=3)
        if (value := C[i][j] * c[k])
    }


def derivative(
    a: tuple[F, ...],
    b: tuple[F, ...],
    c: tuple[F, ...],
    w: tuple[F, ...],
    C: list[list[F]],
) -> dict[tuple[int, int, int], F]:
    return tensor_add(
        tensor(a, unit(T_COLOUR), w),
        tensor_scale(-F(1), tensor(unit(S_COLOUR), b, w)),
        c_tensor(C, c),
    )


def join(a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]) -> tuple[F, ...]:
    return a + b + c


def split(v: tuple[F, ...]) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * N : (i + 1) * N] for i in range(3))


def flatten_reverse(value: dict[tuple[int, int, int], F]) -> list[F]:
    return [
        value.get((i, j, k), F(0))
        for k in range(N)
        for j in range(N)
        for i in range(N)
    ]


def rank(rows: list[list[F]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for col in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][col]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][col]:
                continue
            multiple = matrix[row][col]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def column_rank(columns: list[list[F]]) -> int:
    return rank([list(row) for row in zip(*columns, strict=True)])


def constraint_column(
    value: dict[tuple[int, int, int], F], eta: tuple[F, ...]
) -> list[F]:
    first = [
        value.get((D_COLOUR, j, k), F(0))
        for k in range(N)
        for j in range(N)
    ]
    third = [
        sum(eta[k] * value.get((i, j, k), F(0)) for k in range(N))
        for j in range(N)
        for i in range(N)
    ]
    return first + third


def apply_columns(columns: list[list[F]], vector: tuple[F, ...]) -> list[F]:
    return [
        sum(vector[col] * columns[col][row] for col in range(len(columns)))
        for row in range(len(columns[0]))
    ]


def rhs(
    first_key: tuple[int, int] | None,
    third_key: tuple[int, int] | None,
    third_scalar: F = F(1),
) -> list[F]:
    first = [
        -F((j, k) == first_key)
        for k in range(N)
        for j in range(N)
    ]
    third = [
        -third_scalar * F((i, j) == third_key)
        for j in range(N)
        for i in range(N)
    ]
    return first + third


def audit_affine_systems() -> None:
    d, s, t = unit(D_COLOUR), unit(S_COLOUR), unit(T_COLOUR)
    eta = add(s, scale(F(2), t))
    w = add(s, t)
    C = [[F(2), F(0), F(0)], [F(0), F(5), F(7)], [F(0), F(11), F(13)]]
    raw_columns = []
    for block in range(3):
        for colour in range(N):
            entries = [zero(), zero(), zero()]
            entries[block] = unit(colour)
            raw_columns.append(derivative(*entries, w, C))
    assert column_rank([flatten_reverse(value) for value in raw_columns]) == 8
    columns = [constraint_column(value, eta) for value in raw_columns]
    assert column_rank(columns) == 8

    syzygy = join(s, t, zero())
    assert apply_columns(columns, syzygy) == [F(0)] * 18

    vertical_d = join(zero(), zero(), scale(-F(1, 2), d))
    split_s = join(zero(), scale(F(1, 3), s), zero())
    split_t = join(scale(-F(2, 3), t), zero(), zero())
    assert apply_columns(columns, vertical_d) == rhs((D_COLOUR, D_COLOUR), None)
    assert apply_columns(columns, split_s) == rhs(None, (S_COLOUR, S_COLOUR))
    assert apply_columns(columns, split_t) == rhs(
        None, (T_COLOUR, T_COLOUR), F(2)
    )

    forced = [list(value) for value in (syzygy, vertical_d, split_s, split_t)]
    assert column_rank(forced) == 4
    third_projections = [value[2 * N :] for value in forced]
    assert column_rank([list(value) for value in third_projections]) == 1
    assert column_rank([list(value[:N]) for value in forced]) == 2
    assert column_rank([list(value[N : 2 * N]) for value in forced]) == 2


def main() -> None:
    audit_affine_systems()
    print(
        "S2BW independent audit passed: reverse-indexed three-correction "
        "systems, common syzygy, forced basis, and projection contradiction."
    )


if __name__ == "__main__":
    main()
