"""Independent rational audit of the beta_t-coloop endpoint exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

SOURCE_DIM = 3
ROW_DIM = 3 * SOURCE_DIM
TENSOR_DIM = SOURCE_DIM**3

Vector = list[Fraction]


def zero(length: int) -> Vector:
    return [Fraction() for _ in range(length)]


def source(source_id: int, index: int) -> Vector:
    vector = zero(ROW_DIM)
    vector[source_id * SOURCE_DIM + index] = Fraction(1)
    return vector


def add(*vectors: Vector) -> Vector:
    return [sum(entries, Fraction()) for entries in zip(*vectors, strict=True)]


def scale(value: Fraction, vector: Vector) -> Vector:
    return [value * entry for entry in vector]


def component(vector: Vector, source_id: int) -> Vector:
    start = source_id * SOURCE_DIM
    return vector[start : start + SOURCE_DIM]


def tensor3(left: Vector, middle: Vector, right: Vector) -> Vector:
    out = zero(TENSOR_DIM)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(middle):
            for k, z_value in enumerate(right):
                # Deliberately use a Z-major convention, unlike the primary replay.
                out[k * 9 + j * 3 + i] += x_value * y_value * z_value
    return out


def permanent(left: Vector, middle: Vector, right: Vector) -> Vector:
    vectors = (left, middle, right)
    terms = []
    for order in permutations(range(3)):
        terms.append(
            tensor3(
                component(vectors[order[0]], 0),
                component(vectors[order[1]], 1),
                component(vectors[order[2]], 2),
            )
        )
    return add(*terms)


def matrix_rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][col]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][col]:
                continue
            value = matrix[row][col]
            matrix[row] = [
                left - value * right
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def concatenate(*vectors: Vector) -> Vector:
    out: Vector = []
    for vector in vectors:
        out.extend(vector)
    return out


def target(alpha: int, beta: int, gamma: int) -> Vector:
    values = zero(3)
    if alpha == beta == gamma:
        values[alpha] = Fraction(1)
    return values


def audit_endpoint_table() -> None:
    for t in range(3):
        for a in range(3):
            if a == t:
                continue
            b = next(i for i in range(3) if i not in (a, t))
            for i in range(3):
                assert target(i, a, b) == zero(3)
                assert target(i, a, t) == zero(3)
                assert target(i, b, t) == zero(3)
                expected = zero(3)
                if i == b:
                    expected[b] = Fraction(1)
                assert target(i, b, b) == expected
    print("independent endpoint face: PASS")


def audit_full_support() -> None:
    basis = [source(block, i) for block in range(3) for i in range(3)]
    x, y, z = source(0, 0), source(1, 0), source(2, 0)
    p = add(x, y, z)
    square = [permanent(p, p, q) for q in basis]
    assert matrix_rank(square) == 7
    radical = [add(x, scale(Fraction(-1), y)), add(x, scale(Fraction(-1), z))]
    assert all(permanent(p, p, q) == zero(TENSOR_DIM) for q in radical)

    common = [
        concatenate(permanent(v, p, radical[0]), permanent(v, p, radical[1]))
        for v in basis
    ]
    assert matrix_rank(common) == 8
    assert concatenate(
        permanent(p, p, radical[0]), permanent(p, p, radical[1])
    ) == zero(2 * TENSOR_DIM)
    print("independent full-support radical: PASS")


def audit_two_source() -> None:
    basis = [source(block, i) for block in range(3) for i in range(3)]
    x, y, z = source(0, 0), source(1, 0), source(2, 0)
    p = add(x, y)
    square = [permanent(p, p, q) for q in basis]
    assert matrix_rank(square) == SOURCE_DIM
    xy_basis = basis[: 2 * SOURCE_DIM]
    assert all(permanent(p, p, q) == zero(TENSOR_DIM) for q in xy_basis)
    mixed = [permanent(z, p, q) for q in xy_basis]
    assert matrix_rank(mixed) == 2 * SOURCE_DIM - 1
    assert permanent(z, p, add(x, scale(Fraction(-1), y))) == zero(TENSOR_DIM)
    for left in xy_basis:
        for middle in xy_basis:
            for right in xy_basis:
                assert permanent(left, middle, right) == zero(TENSOR_DIM)
    print("independent two-source fork: PASS")


def audit_pure_source() -> None:
    basis = [source(block, i) for block in range(3) for i in range(3)]
    x, q_y = source(0, 0), source(1, 0)
    mixed_y = [permanent(v, x, q_y) for v in basis]
    assert matrix_rank(mixed_y) == SOURCE_DIM
    assert all(
        permanent(v, x, q_y) == zero(TENSOR_DIM)
        for v in basis[: 2 * SOURCE_DIM]
    )

    d = add(source(0, 0), scale(Fraction(2), source(1, 1)), scale(Fraction(-3), source(2, 2)))
    q_0, q_1 = source(0, 1), source(0, 2)
    map_0 = [permanent(v, d, q_0) for v in basis]
    map_1 = [permanent(v, d, q_1) for v in basis]
    combined = [
        concatenate(left, right) for left, right in zip(map_0, map_1, strict=True)
    ]
    assert matrix_rank(map_0) == matrix_rank(map_1) == matrix_rank(combined)
    print("independent pure-source propagation: PASS")


def main() -> None:
    audit_endpoint_table()
    audit_full_support()
    audit_two_source()
    audit_pure_source()
    print("independent beta_t-coloop endpoint audit: PASS")


if __name__ == "__main__":
    main()
