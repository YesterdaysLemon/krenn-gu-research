#!/usr/bin/env python3
"""Independent no-import audit for the lower-rank q=1 pair-pole theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

DIM = 3
TOTAL = 3 * DIM
NVARIABLES = 9

Vector = tuple[Fraction, ...]
SparseTensor = dict[tuple[int, int, int], Fraction]
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def unit(source: int, index: int) -> Vector:
    position = source * DIM + index
    return tuple(Fraction(int(candidate == position)) for candidate in range(TOTAL))


def add_vectors(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale_vector(coefficient: Fraction, vector: Vector) -> Vector:
    return tuple(coefficient * entry for entry in vector)


def split(vector: Vector) -> tuple[Vector, Vector, Vector]:
    return vector[:DIM], vector[DIM : 2 * DIM], vector[2 * DIM :]


def sparse_tensor(left: Vector, middle: Vector, right: Vector) -> SparseTensor:
    result: SparseTensor = {}
    for left_index, middle_index, right_index in product(range(DIM), repeat=3):
        coefficient = left[left_index] * middle[middle_index] * right[right_index]
        if coefficient:
            result[left_index, middle_index, right_index] = coefficient
    return result


def add_tensors(*tensors: SparseTensor) -> SparseTensor:
    result: SparseTensor = {}
    for tensor_value in tensors:
        for key, coefficient in tensor_value.items():
            result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def scale_tensor(coefficient: Fraction, tensor_value: SparseTensor) -> SparseTensor:
    return {
        key: coefficient * value
        for key, value in tensor_value.items()
        if coefficient * value
    }


def permanent(first: Vector, second: Vector, third: Vector) -> SparseTensor:
    rows = split(first), split(second), split(third)
    pieces = []
    for assignment in permutations(range(3)):
        pieces.append(
            sparse_tensor(
                rows[assignment[0]][0],
                rows[assignment[1]][1],
                rows[assignment[2]][2],
            )
        )
    return add_tensors(*pieces)


def alternating(first: Vector, second: Vector, third: Vector) -> SparseTensor:
    rows = split(first), split(second), split(third)
    pieces = []
    for assignment in permutations(range(3)):
        inversions = sum(
            assignment[left] > assignment[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        sign = Fraction(-1 if inversions % 2 else 1)
        pieces.append(
            scale_tensor(
                sign,
                sparse_tensor(
                    rows[assignment[0]][0],
                    rows[assignment[1]][1],
                    rows[assignment[2]][2],
                ),
            )
        )
    return add_tensors(*pieces)


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


def kernel_map(v: Vector, q: Vector) -> list[list[Fraction]]:
    columns = [permanent(unit(source, index), v, q) for source in range(3) for index in range(DIM)]
    keys = sorted(set().union(*(column.keys() for column in columns)))
    return [[column.get(key, Fraction(0)) for column in columns] for key in keys]


def assert_zero(*tensors: SparseTensor) -> None:
    assert all(not tensor_value for tensor_value in tensors)


def source_atlas_audit() -> None:
    x, x_1 = unit(0, 0), unit(0, 1)
    y, y_1, y_2 = unit(1, 0), unit(1, 1), unit(1, 2)
    z, z_1, z_2 = unit(2, 0), unit(2, 1), unit(2, 2)

    v_two = add_vectors(x, z)
    q_two = add_vectors(x_1, y, z_1)
    a_two = add_vectors(scale_vector(Fraction(-1), x), z)
    b_two = add_vectors(scale_vector(Fraction(-1), x_1), y, scale_vector(Fraction(-1), z_1))
    assert_zero(permanent(a_two, v_two, q_two), permanent(b_two, v_two, q_two))
    assert alternating(a_two, b_two, v_two) == {(0, 0, 0): Fraction(-2)}

    q_conjugate = y
    a_conjugate = add_vectors(a_two, y_1)
    b_conjugate = y_2
    assert_zero(
        permanent(a_conjugate, v_two, q_conjugate),
        permanent(b_conjugate, v_two, q_conjugate),
        permanent(a_conjugate, b_conjugate, q_conjugate),
    )
    assert alternating(a_conjugate, b_conjugate, v_two) == {
        (0, 2, 0): Fraction(-2)
    }

    v_three = add_vectors(x, y, z)
    q_transverse = add_vectors(x, y, z_1, scale_vector(Fraction(-2), z))
    a_transverse = add_vectors(x, y, z, scale_vector(Fraction(-1), z_1))
    b_transverse = add_vectors(x, scale_vector(Fraction(-1), y))
    assert_zero(
        permanent(a_transverse, v_three, q_transverse),
        permanent(b_transverse, v_three, q_transverse),
        permanent(a_transverse, b_transverse, q_transverse),
    )
    assert alternating(a_transverse, b_transverse, v_three) == {
        (0, 0, 1): Fraction(-2)
    }

    skew_q = add_vectors(x, scale_vector(Fraction(-1), y), z_1)
    skew_map = kernel_map(v_three, skew_q)
    assert matrix_rank(skew_map) == 6
    for z_column in range(2 * DIM, 3 * DIM):
        assert all(row[z_column] == 0 for row in skew_map)

    pure_q = z_1
    exceptional_a = add_vectors(scale_vector(Fraction(-1), x), y)
    exceptional_b = z_2
    assert_zero(
        permanent(exceptional_a, v_three, pure_q),
        permanent(exceptional_b, v_three, pure_q),
        permanent(exceptional_a, exceptional_b, pure_q),
    )
    assert alternating(exceptional_a, exceptional_b, v_three) == {
        (0, 0, 2): Fraction(2)
    }

    q_regular = v_three
    a_regular = add_vectors(x, scale_vector(Fraction(-1), y))
    b_regular = add_vectors(x, y, scale_vector(Fraction(-2), z))
    assert_zero(
        permanent(a_regular, v_three, q_regular),
        permanent(b_regular, v_three, q_regular),
        permanent(a_regular, b_regular, q_regular),
    )
    assert alternating(a_regular, b_regular, v_three) == {(0, 0, 0): Fraction(6)}

    q_one_zero = x
    a_one_zero = x_1
    b_one_zero = add_vectors(y, scale_vector(Fraction(-1), z))
    assert_zero(
        permanent(a_one_zero, v_three, q_one_zero),
        permanent(b_one_zero, v_three, q_one_zero),
        permanent(a_one_zero, b_one_zero, q_one_zero),
    )
    assert alternating(a_one_zero, b_one_zero, v_three) == {
        (1, 0, 0): Fraction(2)
    }

    q_two_zero = add_vectors(x, y, scale_vector(Fraction(-1), z))
    a_two_zero = add_vectors(x_1, y_1)
    b_two_zero = add_vectors(x_1, scale_vector(Fraction(-1), y_1))
    assert_zero(
        permanent(a_two_zero, v_three, q_two_zero),
        permanent(b_two_zero, v_three, q_two_zero),
        permanent(a_two_zero, b_two_zero, q_two_zero),
    )
    assert alternating(a_two_zero, b_two_zero, v_three) == {
        (1, 1, 0): Fraction(-2)
    }
    print("independent source atlas: PASS")


def zero_exponent() -> Exponent:
    return (0,) * NVARIABLES


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if not coefficient else {zero_exponent(): coefficient}


def variable(index: int) -> Polynomial:
    exponent = [0] * NVARIABLES
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add_polynomials(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Fraction(0)) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def scale_polynomial(coefficient: int | Fraction, polynomial: Polynomial) -> Polynomial:
    scalar = Fraction(coefficient)
    return {
        exponent: scalar * value
        for exponent, value in polynomial.items()
        if scalar * value
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_value + right_value
                for left_value, right_value in zip(left_exponent, right_exponent, strict=True)
            )
            result[exponent] = result.get(exponent, Fraction(0)) + left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    terms = []
    for assignment in permutations(range(3)):
        inversions = sum(
            assignment[left] > assignment[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        term = constant(-1 if inversions % 2 else 1)
        for row in range(3):
            term = multiply(term, matrix[row][assignment[row]])
        terms.append(term)
    return add_polynomials(*terms)


def replace_column(
    matrix: list[list[Polynomial]], column: int, replacement: list[Polynomial]
) -> list[list[Polynomial]]:
    return [
        [replacement[row] if candidate == column else matrix[row][candidate] for candidate in range(3)]
        for row in range(3)
    ]


def valuation(polynomial: Polynomial, variable_index: int) -> int:
    assert polynomial
    return min(exponent[variable_index] for exponent in polynomial)


def cramer_pole_audit() -> None:
    xs, xt, xu, ys, yt, yu, zs, zt, zu = (variable(index) for index in range(9))
    target_t = multiply(multiply(xt, yt), zt)
    target_u = multiply(multiply(xu, yu), zu)
    residual = [target_t, target_u, constant(0)]

    charts: list[tuple[str, list[list[Polynomial]], list[tuple[int, int]]]] = [
        (
            "regular-two-source",
            [
                [scale_polynomial(-1, xs), constant(0), zs],
                [scale_polynomial(-1, xs), ys, constant(0)],
                [xs, constant(0), zs],
            ],
            [(0, 0), (2, 6)],
        ),
        (
            "conjugate-two-source",
            [
                [scale_polynomial(-1, xs), constant(0), zs],
                [constant(0), yt, constant(0)],
                [xs, constant(0), zs],
            ],
            [(0, 0), (2, 6)],
        ),
        (
            "transverse-target",
            [
                [scale_polynomial(-1, xs), ys, constant(0)],
                [constant(0), constant(0), zu],
                [xs, ys, zt],
            ],
            [(0, 0), (1, 3)],
        ),
        (
            "one-zero-weight",
            [
                [xt, constant(0), constant(0)],
                [constant(0), ys, scale_polynomial(-1, zs)],
                [xs, ys, zs],
            ],
            [(1, 3), (2, 6)],
        ),
        (
            "two-zero-weight",
            [
                [xt, yt, constant(0)],
                [xt, scale_polynomial(-1, yt), constant(0)],
                [xs, ys, zs],
            ],
            [(2, 6)],
        ),
    ]

    for name, matrix, pole_checks in charts:
        denominator = determinant(matrix)
        assert denominator
        for column, coordinate in pole_checks:
            numerator = determinant(replace_column(matrix, column, residual))
            assert numerator
            assert valuation(denominator, coordinate) >= 1
            assert valuation(numerator, coordinate) == 0
        print(f"independent Cramer chart {name}: PASS")


def main() -> None:
    source_atlas_audit()
    cramer_pole_audit()
    print("independent lower-rank q=1 pair-pole audit: PASS")


if __name__ == "__main__":
    main()
