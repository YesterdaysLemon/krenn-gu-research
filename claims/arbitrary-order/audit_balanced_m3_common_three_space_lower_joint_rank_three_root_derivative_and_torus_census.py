#!/usr/bin/env python3
"""Independent no-import audit for the lower-rank three-root census."""

from __future__ import annotations

from fractions import Fraction

DIM = 3
DOMAIN = 9
TARGET = 27

Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def unit(index: int) -> Vector:
    return tuple(Fraction(int(candidate == index)) for candidate in range(DIM))


def zero_vector() -> Vector:
    return (Fraction(0),) * DIM


def add_vectors(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale_vector(coefficient: int | Fraction, vector: Vector) -> Vector:
    scalar = Fraction(coefficient)
    return tuple(scalar * entry for entry in vector)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(left[row] * right[column] for column in range(DIM)) for row in range(DIM))


def add_matrices(*matrices: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum((matrix[row][column] for matrix in matrices), Fraction(0))
            for column in range(DIM)
        )
        for row in range(DIM)
    )


def scale_matrix(coefficient: int | Fraction, matrix: Matrix) -> Matrix:
    scalar = Fraction(coefficient)
    return tuple(tuple(scalar * entry for entry in row) for row in matrix)


def flatten(matrix: Matrix) -> Vector:
    return tuple(entry for row in matrix for entry in row)


def derivative(b_23: Matrix, b_13: Matrix, b_12: Matrix) -> list[list[Fraction]]:
    result = [[Fraction(0) for _ in range(DOMAIN)] for _ in range(TARGET)]
    for left in range(DIM):
        for middle in range(DIM):
            for right in range(DIM):
                row = 9 * left + 3 * middle + right
                result[row][left] = b_23[middle][right]
                result[row][DIM + middle] = b_13[left][right]
                result[row][2 * DIM + right] = b_12[left][middle]
    return result


def matrix_rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(pivot_row, len(matrix)) if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in range(len(matrix)):
            if candidate == pivot_row or not matrix[candidate][column]:
                continue
            multiplier = matrix[candidate][column]
            matrix[candidate] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[candidate], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def matvec(matrix: list[list[Fraction]], vector: Vector) -> tuple[Fraction, ...]:
    return tuple(
        sum((entry * coefficient for entry, coefficient in zip(row, vector, strict=True)), Fraction(0))
        for row in matrix
    )


def concatenate(first: Vector, second: Vector, third: Vector) -> Vector:
    return (*first, *second, *third)


def contraction(block: Matrix, left: Vector, right: Vector) -> Fraction:
    return sum(
        (
            left[row] * block[row][column] * right[column]
            for row in range(DIM)
            for column in range(DIM)
        ),
        Fraction(0),
    )


def rank_and_incidence_audit() -> None:
    e_0, e_1, e_2 = unit(0), unit(1), unit(2)
    rank_nine = derivative(outer(e_0, e_0), outer(e_1, e_1), outer(e_2, e_2))
    assert matrix_rank(rank_nine) == 9

    rank_eight = derivative(outer(e_0, e_0), scale_matrix(-1, outer(e_0, e_0)), outer(e_1, e_1))
    syzygy = concatenate(e_0, e_0, zero_vector())
    assert matrix_rank(rank_eight) == 8
    assert not any(matvec(rank_eight, syzygy))

    tangent_columns = []
    for index in range(DIM):
        tangent_columns.append(flatten(outer(unit(index), e_0)))
    for index in range(DIM):
        tangent_columns.append(flatten(outer(e_0, unit(index))))
    tangent_rows = [list(row) for row in zip(*tangent_columns, strict=True)]
    assert matrix_rank(tangent_rows) == 5
    augmented = [
        [*row, entry]
        for row, entry in zip(tangent_rows, flatten(outer(e_1, e_1)), strict=True)
    ]
    assert matrix_rank(augmented) == 6

    rank_seven = derivative(outer(e_0, e_0), scale_matrix(-1, outer(e_0, e_0)), outer(e_0, e_0))
    assert matrix_rank(rank_seven) == 7

    cases = ((3, 9), (3, 8), (3, 7), (4, 8), (4, 7))
    for joint_rank, derivative_rank in cases:
        kernel_dimension = DOMAIN - derivative_rank
        assert kernel_dimension + 3 >= joint_rank
        assert joint_rank - 3 <= kernel_dimension
    assert 4 - 3 > DOMAIN - 9
    print("independent derivative/incidence census: PASS")


def torus_gate_audit() -> None:
    e_0, e_1, e_2 = unit(0), unit(1), unit(2)
    ones = (Fraction(1), Fraction(1), Fraction(1))

    x = y = e_0
    w = add_vectors(e_0, e_1)
    residual = add_matrices(outer(e_0, e_0), outer(e_1, e_1))
    alpha = ones
    beta = gamma = (Fraction(1), Fraction(-1), Fraction(1))
    assert contraction(outer(y, w), beta, gamma) == 0
    assert contraction(scale_matrix(-1, outer(x, w)), alpha, gamma) == 0
    assert contraction(residual, alpha, beta) == 0

    x = y = add_vectors(e_0, e_1)
    w = e_0
    residual = add_matrices(outer(e_0, e_0), outer(e_2, e_2))
    alpha = (Fraction(1), Fraction(-1), Fraction(1))
    beta = (Fraction(1), Fraction(-1), Fraction(-1))
    gamma = ones
    assert sum((a * b for a, b in zip(alpha, x, strict=True)), Fraction(0)) == 0
    assert sum((a * b for a, b in zip(beta, y, strict=True)), Fraction(0)) == 0
    assert contraction(residual, alpha, beta) == 0
    assert contraction(outer(y, w), beta, gamma) == 0
    assert contraction(scale_matrix(-1, outer(x, w)), alpha, gamma) == 0

    monomial = outer(e_2, e_2)
    for alpha_2, beta_2 in ((Fraction(1), Fraction(1)), (Fraction(2), Fraction(-3))):
        restricted_alpha = (Fraction(1), Fraction(-1), alpha_2)
        restricted_beta = (Fraction(1), Fraction(-1), beta_2)
        assert contraction(monomial, restricted_alpha, restricted_beta) == alpha_2 * beta_2
        assert contraction(monomial, restricted_alpha, restricted_beta) != 0
    print("independent rank-eight torus gates: PASS")


def hilbert_burch_blocks(
    x: Vector, b: Vector, y: Vector, c: Vector, z: Vector, w: Vector
) -> tuple[Matrix, Matrix, Matrix]:
    return (
        add_matrices(outer(y, w), scale_matrix(-1, outer(c, z))),
        add_matrices(outer(b, z), scale_matrix(-1, outer(x, w))),
        add_matrices(outer(x, c), scale_matrix(-1, outer(b, y))),
    )


def projection_rank(first: Vector, second: Vector) -> int:
    return matrix_rank([list(first), list(second)])


def check_profile(vectors: tuple[Vector, Vector, Vector, Vector, Vector, Vector], profile: tuple[int, int, int]) -> tuple[Matrix, Matrix, Matrix]:
    x, b, y, c, z, w = vectors
    blocks = hilbert_burch_blocks(*vectors)
    shared = derivative(*blocks)
    assert matrix_rank(shared) == 7
    assert not any(matvec(shared, concatenate(x, y, z)))
    assert not any(matvec(shared, concatenate(b, c, w)))
    assert profile == (
        projection_rank(x, b),
        projection_rank(y, c),
        projection_rank(z, w),
    )
    return blocks


def hilbert_burch_audit() -> None:
    e_0, e_1, e_2 = unit(0), unit(1), unit(2)
    zero = zero_vector()
    full = (e_0, e_1, e_0, e_1, e_0, e_1)
    blocks = check_profile(full, (2, 2, 2))
    ones = (Fraction(1), Fraction(1), Fraction(1))
    assert contraction(blocks[0], ones, ones) == 0
    assert contraction(blocks[1], ones, ones) == 0
    assert contraction(blocks[2], ones, ones) == 0

    check_profile((e_0, zero, e_0, e_1, e_0, e_1), (1, 2, 2))
    check_profile((e_0, zero, zero, e_1, e_0, e_1), (1, 1, 2))
    triangle = check_profile((e_0, zero, zero, e_1, e_2, e_2), (1, 1, 1))
    assert all(sum(bool(entry) for row in block for entry in row) == 1 for block in triangle)
    print("independent Hilbert--Burch profiles: PASS")


def main() -> None:
    rank_and_incidence_audit()
    torus_gate_audit()
    hilbert_burch_audit()
    print("independent lower-rank three-root derivative/torus audit: PASS")


if __name__ == "__main__":
    main()
