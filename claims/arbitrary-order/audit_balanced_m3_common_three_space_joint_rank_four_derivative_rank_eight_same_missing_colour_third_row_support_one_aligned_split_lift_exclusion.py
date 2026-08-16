#!/usr/bin/env python3
"""Independent no-import audit for the S2BU aligned exclusion."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product


def unit(width: int, index: int) -> tuple[F, ...]:
    return tuple(F(i == index) for i in range(width))


def zero(width: int) -> tuple[F, ...]:
    return (F(0),) * width


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(value[i] for value in vectors) for i in range(len(vectors[0])))


def scale(scalar: F, vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(scalar * value for value in vector)


def tensor(
    a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    width = len(a)
    return {
        (i, j, k): value
        for i, j, k in product(range(width), repeat=3)
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


def flatten_reverse(
    value: dict[tuple[int, int, int], F], width: int
) -> list[F]:
    return [
        value.get((i, j, k), F(0))
        for k in range(width)
        for j in range(width)
        for i in range(width)
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


ROOT_WIDTH = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(ROOT_WIDTH)


def c_tensor(
    C: list[list[F]], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    return {
        (i, j, k): value
        for i, j, k in product(range(ROOT_WIDTH), repeat=3)
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
        tensor_scale(-F(1), tensor(unit(ROOT_WIDTH, S_COLOUR), b, w)),
        c_tensor(C, c),
    )


def split_root(v: tuple[F, ...]) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * ROOT_WIDTH : (i + 1) * ROOT_WIDTH] for i in range(3))


def join_root(
    a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]
) -> tuple[F, ...]:
    return a + b + c


def audit_direct_root_box() -> None:
    d = unit(ROOT_WIDTH, D_COLOUR)
    s = unit(ROOT_WIDTH, S_COLOUR)
    t = unit(ROOT_WIDTH, T_COLOUR)
    z = zero(ROOT_WIDTH)
    lam, alpha, beta = F(2), F(3), F(5)
    wd, ws, wt = F(7), F(11), F(13)
    y = scale(lam, s)
    w = add(scale(wd, d), scale(ws, s), scale(wt, t))
    C = [[F(17), F(0), F(0)], [F(0), F(19), F(23)], [F(0), F(29), F(31)]]
    K = [
        join_root(s, y, z),
        join_root(z, z, d),
        join_root(z, scale(-F(1), s), z),
        join_root(scale(alpha, t), scale(beta, t), t),
    ]
    images = [derivative(*split_root(value), y, w, C) for value in K]
    U = [flatten_reverse(value, ROOT_WIDTH) for value in images[1:]]
    L = [
        flatten_reverse(tensor(a, b, c), ROOT_WIDTH)
        for a, b, c in product((s, t), (s, t), (d, t))
    ]
    assert images[0] == {}
    assert column_rank(U) == 3
    assert column_rank(L) == 8
    assert column_rank(U + L) == 11

    C_bar = [row[:] for row in C]
    C_bar[D_COLOUR][D_COLOUR] = F(0)
    rep_d = tensor_scale(-F(1, 17), c_tensor(C_bar, d))
    lhs_d = tensor_add(tensor(d, d, d), tensor_scale(-F(1), rep_d))
    assert lhs_d == tensor_scale(F(1, 17), images[1])

    rep_s = tensor_add(
        tensor_scale(-wd / ws, tensor(s, s, d)),
        tensor_scale(-wt / ws, tensor(s, s, t)),
    )
    lhs_s = tensor_add(tensor(s, s, s), tensor_scale(-F(1), rep_s))
    assert lhs_s == tensor_scale(F(1) / ws, images[2])


SOURCE_WIDTH = 2


def split_source(v: tuple[F, ...]) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * SOURCE_WIDTH : (i + 1) * SOURCE_WIDTH] for i in range(3))


def source_permanent(
    u: tuple[F, ...], v: tuple[F, ...], z: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    roots = [split_source(value) for value in (u, v, z)]
    return tensor_add(
        *(
            tensor(
                roots[sigma[0]][0], roots[sigma[1]][1], roots[sigma[2]][2]
            )
            for sigma in permutations(range(3))
        )
    )


def source_basis(block: int, coordinate: int) -> tuple[F, ...]:
    return unit(3 * SOURCE_WIDTH, SOURCE_WIDTH * block + coordinate)


def audit_row_coefficients() -> None:
    vectors = [
        tuple(F((i + 2 * j + 1) % 7 - 3) for i in range(3 * SOURCE_WIDTH))
        for j in range(4)
    ]
    g0, g1, g2, g3 = vectors
    lam, alpha, beta = F(2), F(3), F(5)
    r_s, r_t = g0, scale(alpha, g3)
    p_s, p_t = add(scale(lam, g0), scale(-F(1), g2)), scale(beta, g3)
    q_d, q_t = g1, g3

    assert source_permanent(r_s, p_t, q_t) == tensor_scale(
        beta, source_permanent(g0, g3, g3)
    )
    assert source_permanent(r_t, p_s, q_t) == tensor_add(
        tensor_scale(alpha * lam, source_permanent(g0, g3, g3)),
        tensor_scale(-alpha, source_permanent(g2, g3, g3)),
    )
    assert source_permanent(r_t, p_t, q_t) == tensor_scale(
        alpha * beta, source_permanent(g3, g3, g3)
    )
    assert source_permanent(r_t, p_t, q_d) == tensor_scale(
        alpha * beta, source_permanent(g1, g3, g3)
    )


def audit_tangent_kernel() -> None:
    x = source_basis(0, 0)
    y = source_basis(1, 0)
    z = source_basis(2, 0)
    v = add(x, y, z)
    target_t = tensor(unit(SOURCE_WIDTH, 0), unit(SOURCE_WIDTH, 0), unit(SOURCE_WIDTH, 0))
    target_d = tensor(unit(SOURCE_WIDTH, 1), unit(SOURCE_WIDTH, 1), unit(SOURCE_WIDTH, 1))
    assert source_permanent(v, v, v) == tensor_scale(F(6), target_t)

    phi = [
        flatten_reverse(source_permanent(source_basis(block, coordinate), v, v), SOURCE_WIDTH)
        for block in range(3)
        for coordinate in range(SOURCE_WIDTH)
    ]
    assert column_rank(phi) == 4
    assert column_rank(phi + [flatten_reverse(target_d, SOURCE_WIDTH)]) == 5

    kernel_a = add(x, scale(-F(1), y))
    kernel_b = add(x, scale(-F(1), z))
    assert source_permanent(kernel_a, v, v) == {}
    assert source_permanent(kernel_b, v, v) == {}
    assert column_rank([list(kernel_a), list(kernel_b), list(v)]) == 3

    g0 = add(scale(F(2), kernel_a), scale(F(3), kernel_b))
    g1 = add(scale(F(5), kernel_a), scale(F(7), kernel_b))
    g2 = add(scale(F(11), kernel_a), scale(F(13), kernel_b))
    assert column_rank([list(g0), list(g1), list(g2), list(v)]) == 3


def main() -> None:
    audit_direct_root_box()
    audit_row_coefficients()
    audit_tangent_kernel()
    print(
        "S2BU independent audit passed: reverse-indexed arbitrary-w quotient, "
        "four row coefficients, tangent kernel, and rank contradiction."
    )


if __name__ == "__main__":
    main()
