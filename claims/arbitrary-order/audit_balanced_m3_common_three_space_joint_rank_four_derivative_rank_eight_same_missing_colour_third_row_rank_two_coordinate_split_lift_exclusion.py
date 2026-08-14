#!/usr/bin/env python3
"""Independent no-import audit for the S2BS split-lift exclusion."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product

N = 3


def unit(length: int, index: int) -> tuple[F, ...]:
    return tuple(F(i == index) for i in range(length))


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(v[i] for v in vectors) for i in range(len(vectors[0])))


def scale(scalar: F, vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(scalar * x for x in vector)


def root_tensor(
    a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    width = len(a)
    assert len(b) == len(c) == width
    return {
        (i, j, k): a[i] * b[j] * c[k]
        for i, j, k in product(range(width), repeat=3)
        if a[i] * b[j] * c[k]
    }


def tensor_add(*tensors: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    keys = set().union(*(t.keys() for t in tensors))
    return {key: value for key in keys if (value := sum(t.get(key, F(0)) for t in tensors))}


def tensor_scale(scalar: F, tensor: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    return {key: scalar * value for key, value in tensor.items() if scalar * value}


def c_tensor(C: list[list[F]], c: tuple[F, ...]) -> dict[tuple[int, int, int], F]:
    return {
        (i, j, k): C[i][j] * c[k]
        for i, j, k in product(range(N), repeat=3)
        if C[i][j] * c[k]
    }


def derivative(
    a: tuple[F, ...],
    b: tuple[F, ...],
    c: tuple[F, ...],
    C: list[list[F]],
) -> dict[tuple[int, int, int], F]:
    return tensor_add(
        root_tensor(a, unit(N, 2), unit(N, 1)),
        tensor_scale(-F(1), root_tensor(unit(N, 1), b, unit(N, 1))),
        c_tensor(C, c),
    )


def split(v: tuple[F, ...], width: int) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * width : (i + 1) * width] for i in range(3))


def permanent(
    u: tuple[F, ...], v: tuple[F, ...], w: tuple[F, ...], width: int
) -> dict[tuple[int, int, int], F]:
    triples = [split(z, width) for z in (u, v, w)]
    terms = []
    for sigma in permutations(range(3)):
        terms.append(
            root_tensor(
                triples[sigma[0]][0], triples[sigma[1]][1], triples[sigma[2]][2]
            )
        )
    return tensor_add(*terms)


def flatten(tensor: dict[tuple[int, int, int], F], width: int) -> list[F]:
    # Reverse the factor order relative to the primary replay.
    return [
        tensor.get((i, j, k), F(0))
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
            if row != pivot_row and matrix[row][col]:
                multiple = matrix[row][col]
                matrix[row] = [
                    a - multiple * b
                    for a, b in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def column_rank(columns: list[list[F]]) -> int:
    return rank([list(row) for row in zip(*columns, strict=True)])


def canonical_data() -> tuple[list[list[F]], list[tuple[F, ...]]]:
    ed, es, et = unit(N, 0), unit(N, 1), unit(N, 2)
    zero = tuple(F(0) for _ in range(N))
    C = [[F(0) for _ in range(N)] for _ in range(N)]
    C[0][0] = C[1][1] = F(1)
    K = [
        es + et + zero,
        zero + zero + ed,
        zero + scale(-F(1), es) + zero,
        et + zero + et,
    ]
    return C, K


def audit_derivative() -> None:
    C, K = canonical_data()
    zero = tuple(F(0) for _ in range(N))
    columns = []
    for i in range(N):
        columns.append(flatten(derivative(unit(N, i), zero, zero, C), N))
    for i in range(N):
        columns.append(flatten(derivative(zero, unit(N, i), zero, C), N))
    for i in range(N):
        columns.append(flatten(derivative(zero, zero, unit(N, i), C), N))
    assert column_rank(columns) == 8
    assert column_rank([list(k) for k in K]) == 4
    images = [flatten(derivative(*split(k, N), C), N) for k in K]
    assert images[0] == [F(0)] * (N**3)
    assert column_rank(images[1:]) == 3
    for block in range(3):
        projections = [list(k[block * N : (block + 1) * N]) for k in K]
        assert column_rank(projections) == 2


def audit_eight_products() -> None:
    C, K = canonical_data()
    expected = {
        (0, 0, 1): {(1, 2, 0): F(2)},
        (0, 0, 3): {(1, 2, 2): F(2)},
        (0, 1, 2): {(1, 1, 0): -F(1)},
        (0, 1, 3): {(2, 2, 0): F(1)},
        (0, 2, 3): {(1, 1, 2): -F(1)},
        (0, 3, 3): {(2, 2, 2): F(2)},
        (1, 2, 3): {(2, 1, 0): -F(1)},
        (2, 3, 3): {(2, 1, 2): -F(2)},
    }
    found = {}
    for indices in combinations_with_replacement(range(4), 3):
        value = permanent(*(K[i] for i in indices), width=N)
        if value:
            found[indices] = value
    assert found == expected
    permanent_columns = [flatten(tensor, N) for tensor in found.values()]
    U = [flatten(derivative(*split(K[i], N), C), N) for i in range(1, 4)]
    assert column_rank(permanent_columns) == 8
    assert column_rank(U) == 3
    assert column_rank(U + permanent_columns) == 11

    ddd = root_tensor(unit(N, 0), unit(N, 0), unit(N, 0))
    ssd = root_tensor(unit(N, 1), unit(N, 1), unit(N, 0))
    sss = root_tensor(unit(N, 1), unit(N, 1), unit(N, 1))
    assert flatten(tensor_add(ddd, ssd), N) == U[0]
    assert flatten(sss, N) == U[1]


def source_vector(x: F, y: F, z: F, coordinate: int = 0) -> tuple[F, ...]:
    out = [F(0)] * 6
    out[coordinate] = x
    out[2 + coordinate] = y
    out[4 + coordinate] = z
    return tuple(out)


def audit_two_source_normal_forms() -> None:
    x = source_vector(F(1), F(0), F(0))
    y = source_vector(F(0), F(1), F(0))
    z = source_vector(F(0), F(0), F(1))
    c = source_vector(F(0), F(0), F(1), coordinate=1)
    v = add(x, y)
    w = add(x, scale(-F(1), y))
    for lam, mu, nu in ((F(1), F(2), F(3)), (F(-2), F(1), F(-1))):
        u = add(scale(lam, w), z)
        r = add(scale(mu, w), c)
        q = scale(nu, w)
        assert permanent(u, u, v, 2) == {}
        assert permanent(u, r, v, 2) == {}
        assert permanent(u, q, v, 2) == {}
        assert permanent(q, v, v, 2) == {}
        square = permanent(u, u, r, 2)
        expected = tensor_add(
            tensor_scale(-F(2) * lam * lam, root_tensor((F(1), F(0)), (F(1), F(0)), (F(0), F(1)))),
            tensor_scale(-F(4) * lam * mu, root_tensor((F(1), F(0)), (F(1), F(0)), (F(1), F(0)))),
        )
        assert square == expected


def audit_three_source_normal_forms() -> None:
    x = source_vector(F(1), F(0), F(0))
    y = source_vector(F(0), F(1), F(0))
    z = source_vector(F(0), F(0), F(1))
    v = add(x, y, z)
    alpha, beta, gamma = F(1), F(1), F(-1, 2)
    u = add(scale(alpha, x), scale(beta, y), scale(gamma, z))
    assert permanent(u, u, v, 2) == {}
    assert permanent(u, v, v, 2) == tensor_scale(
        F(3), root_tensor((F(1), F(0)), (F(1), F(0)), (F(1), F(0)))
    )

    a = source_vector(F(1), F(0), F(0), coordinate=1)
    lam, mu = F(2), F(3)
    r = add(x, scale(lam, y), scale(-lam, z))
    q = add(scale(mu, y), scale(-mu, z))
    assert permanent(a, r, v, 2) == {}
    assert permanent(a, q, v, 2) == {}
    assert permanent(q, v, v, 2) == {}
    mixed = permanent(r, q, v, 2)
    assert mixed == tensor_scale(
        -F(2) * lam * mu,
        root_tensor((F(1), F(0)), (F(1), F(0)), (F(1), F(0))),
    )
    assert permanent(a, x, q, 2) == {}


def main() -> None:
    audit_derivative()
    audit_eight_products()
    audit_two_source_normal_forms()
    audit_three_source_normal_forms()
    print(
        "S2BS independent audit passed: reversed-index Fraction derivative, "
        "64 basis products, direct quotient, and all support normal forms."
    )


if __name__ == "__main__":
    main()
