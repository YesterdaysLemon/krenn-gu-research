#!/usr/bin/env python3
"""Independent no-import audit for the S2BT split-lift atlas."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product

N = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(N)


def unit(index: int) -> tuple[F, ...]:
    return tuple(F(i == index) for i in range(N))


def zero() -> tuple[F, ...]:
    return (F(0),) * N


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(v[i] for v in vectors) for i in range(len(vectors[0])))


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
    *tensors: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int, int], F]:
    keys = set().union(*(value.keys() for value in tensors))
    return {
        key: total
        for key in keys
        if (total := sum(value.get(key, F(0)) for value in tensors))
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
    y: tuple[F, ...],
    w: tuple[F, ...],
    C: list[list[F]],
) -> dict[tuple[int, int, int], F]:
    return tensor_add(
        tensor(a, y, w),
        tensor_scale(-F(1), tensor(unit(S_COLOUR), b, w)),
        c_tensor(C, c),
    )


def split(v: tuple[F, ...]) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * N : (i + 1) * N] for i in range(3))


def join(a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]) -> tuple[F, ...]:
    return a + b + c


def permanent(
    u: tuple[F, ...], v: tuple[F, ...], z: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    roots = [split(value) for value in (u, v, z)]
    return tensor_add(
        *(
            tensor(
                roots[sigma[0]][0], roots[sigma[1]][1], roots[sigma[2]][2]
            )
            for sigma in permutations(range(3))
        )
    )


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
            (r for r in range(pivot_row, len(matrix)) if matrix[r][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
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


def isolated_C() -> list[list[F]]:
    return [[F(2), F(0), F(0)], [F(0), F(1), F(2)], [F(0), F(3), F(5)]]


def derivative_columns(
    y: tuple[F, ...], w: tuple[F, ...], C: list[list[F]]
) -> list[dict[tuple[int, int, int], F]]:
    columns = []
    for block in range(3):
        for colour in range(N):
            entries = [zero(), zero(), zero()]
            entries[block] = unit(colour)
            columns.append(derivative(*entries, y, w, C))
    return columns


def contraction_column(value: dict[tuple[int, int, int], F]) -> list[F]:
    # Deliberately reverse both two-factor orders relative to the primary replay.
    first = [
        value.get((D_COLOUR, j, k), F(0))
        for k in range(N)
        for j in range(N)
    ]
    third = [
        value.get((i, j, S_COLOUR), F(0))
        for j in range(N)
        for i in range(N)
    ]
    return first + third


def apply_columns(columns: list[list[F]], vector: tuple[F, ...]) -> list[F]:
    return [
        sum(vector[col] * columns[col][row] for col in range(len(columns)))
        for row in range(len(columns[0]))
    ]


def contraction_rhs(first_key: tuple[int, int] | None, third_key: tuple[int, int] | None) -> list[F]:
    first = [
        -F((j, k) == first_key)
        for k in range(N)
        for j in range(N)
    ]
    third = [
        -F((i, j) == third_key)
        for j in range(N)
        for i in range(N)
    ]
    return first + third


def audit_affine_contractions() -> None:
    d, s, t = unit(D_COLOUR), unit(S_COLOUR), unit(T_COLOUR)
    w = add(d, scale(F(5), s), scale(F(7), t))
    C = isolated_C()
    for y in (add(scale(F(2), s), scale(F(3), t)), s):
        raw = derivative_columns(y, w, C)
        assert column_rank([flatten_reverse(value) for value in raw]) == 8
        columns = [contraction_column(value) for value in raw]
        assert column_rank(columns) == 8

        syzygy = join(s, y, zero())
        assert apply_columns(columns, syzygy) == [F(0)] * 18

        vertical_d = join(zero(), zero(), scale(-F(1, 2), d))
        assert apply_columns(columns, vertical_d) == contraction_rhs(
            (D_COLOUR, D_COLOUR), None
        )

        split_s = join(zero(), scale(F(1, 5), s), zero())
        assert apply_columns(columns, split_s) == contraction_rhs(
            None, (S_COLOUR, S_COLOUR)
        )


def root_box_columns() -> list[list[F]]:
    d, s, t = unit(D_COLOUR), unit(S_COLOUR), unit(T_COLOUR)
    return [
        flatten_reverse(tensor(a, b, c))
        for a, b, c in product((s, t), (s, t), (d, t))
    ]


def audit_cell(
    y: tuple[F, ...],
    w: tuple[F, ...],
    K: list[tuple[F, ...]],
    expected: dict[tuple[int, int, int], dict[tuple[int, int, int], F]],
) -> None:
    C = isolated_C()
    found = {}
    for indices in combinations_with_replacement(range(4), 3):
        value = permanent(*(K[i] for i in indices))
        if value:
            found[indices] = value
    assert found == expected
    assert column_rank([flatten_reverse(value) for value in found.values()]) == 8

    K_columns = [list(value) for value in K]
    assert column_rank(K_columns) == 4
    for block in range(3):
        assert column_rank(
            [list(value[block * N : (block + 1) * N]) for value in K]
        ) == 2

    images = [flatten_reverse(derivative(*split(value), y, w, C)) for value in K]
    assert images[0] == [F(0)] * (N**3)
    assert column_rank(images[1:]) == 3
    L = root_box_columns()
    assert column_rank(L) == 8
    assert column_rank(images[1:] + L) == 11

    d = unit(D_COLOUR)
    C_bar = [row[:] for row in C]
    C_bar[D_COLOUR][D_COLOUR] = F(0)
    reduction = tensor_add(
        tensor_scale(F(2), tensor(d, d, d)), c_tensor(C_bar, d)
    )
    assert flatten_reverse(reduction) == images[1]


def audit_nonaligned_box() -> None:
    d, s, t, z = unit(D_COLOUR), unit(S_COLOUR), unit(T_COLOUR), zero()
    y = add(scale(F(2), s), scale(F(3), t))
    a = add(scale(F(5), s), scale(F(7), t))
    K = [
        join(s, y, z),
        join(z, z, d),
        join(z, scale(-F(1), s), z),
        join(a, z, t),
    ]
    expected = {
        (0, 0, 1): tensor_scale(F(2), tensor(s, y, d)),
        (0, 0, 3): tensor_scale(F(2), tensor(s, y, t)),
        (0, 1, 2): tensor_scale(-F(1), tensor(s, s, d)),
        (0, 1, 3): tensor(a, y, d),
        (0, 2, 3): tensor_scale(-F(1), tensor(s, s, t)),
        (0, 3, 3): tensor_scale(F(2), tensor(a, y, t)),
        (1, 2, 3): tensor_scale(-F(1), tensor(a, s, d)),
        (2, 3, 3): tensor_scale(-F(2), tensor(a, s, t)),
    }
    audit_cell(y, s, K, expected)


def audit_aligned_box() -> None:
    d, s, t, z = unit(D_COLOUR), unit(S_COLOUR), unit(T_COLOUR), zero()
    lam, alpha, beta = F(4), F(2), F(3)
    K = [
        join(s, scale(lam, s), z),
        join(z, z, d),
        join(z, scale(-F(1), s), z),
        join(scale(alpha, t), scale(beta, t), t),
    ]
    expected = {
        (0, 0, 1): tensor_scale(2 * lam, tensor(s, s, d)),
        (0, 0, 3): tensor_scale(2 * lam, tensor(s, s, t)),
        (0, 1, 2): tensor_scale(-F(1), tensor(s, s, d)),
        (0, 1, 3): tensor_add(
            tensor_scale(beta, tensor(s, t, d)),
            tensor_scale(alpha * lam, tensor(t, s, d)),
        ),
        (0, 2, 3): tensor_scale(-F(1), tensor(s, s, t)),
        (0, 3, 3): tensor_add(
            tensor_scale(2 * beta, tensor(s, t, t)),
            tensor_scale(2 * alpha * lam, tensor(t, s, t)),
        ),
        (1, 2, 3): tensor_scale(-alpha, tensor(t, s, d)),
        (1, 3, 3): tensor_scale(2 * alpha * beta, tensor(t, t, d)),
        (2, 3, 3): tensor_scale(-2 * alpha, tensor(t, s, t)),
        (3, 3, 3): tensor_scale(6 * alpha * beta, tensor(t, t, t)),
    }
    audit_cell(scale(lam, s), s, K, expected)


def main() -> None:
    audit_affine_contractions()
    audit_nonaligned_box()
    audit_aligned_box()
    print(
        "S2BT independent audit passed: exact affine contraction ranks, reverse-"
        "indexed split atlases, root-product boxes, and direct quotient."
    )


if __name__ == "__main__":
    main()
