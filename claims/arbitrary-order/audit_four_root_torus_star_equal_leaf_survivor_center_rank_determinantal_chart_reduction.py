#!/usr/bin/env python3
"""Independent no-import audit of the GLD84 center-rank reduction.

This standard-library script imports no repository Python module.  It parses
the pinned GLD75 sparse basis over Q(i), verifies center-linearity after
x8=0, and independently recomputes the Gaussian ranks, named minors,
scale-fixed tangent, directional determinant, chart counts, and scope fences.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
THEOREM = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_CENTER_RANK_DETERMINANTAL_CHART_REDUCTION_THEOREM.md"
)
EXPECTED_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"

Gaussian = tuple[Fraction, Fraction]
Polynomial = dict[tuple[int, ...], Gaussian]
ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def negate(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def dot(left: list[Gaussian], right: list[Gaussian]) -> Gaussian:
    assert len(left) == len(right)
    output = ZERO
    for left_value, right_value in zip(left, right, strict=True):
        output = add(output, multiply(left_value, right_value))
    return output


def divide(left: Gaussian, right: Gaussian) -> Gaussian:
    norm = right[0] * right[0] + right[1] * right[1]
    assert norm != 0
    return (
        (left[0] * right[0] + left[1] * right[1]) / norm,
        (left[1] * right[0] - left[0] * right[1]) / norm,
    )


def parse_gaussian(raw: str) -> Gaussian:
    text = str(raw).strip().replace(" ", "")
    while len(text) >= 2 and text[0] == "(" and text[-1] == ")":
        depth = 0
        outer = True
        for index, character in enumerate(text):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0 and index != len(text) - 1:
                    outer = False
                    break
        if not outer or depth:
            break
        text = text[1:-1]
    terms: list[str] = []
    start = 0
    for index, character in enumerate(text):
        if index and character in "+-":
            terms.append(text[start:index])
            start = index
    terms.append(text[start:])
    real = Fraction(0)
    imaginary = Fraction(0)
    for term in terms:
        if not term:
            continue
        if "i" in term:
            coefficient = term.replace("*i", "").replace("i", "")
            if coefficient in ("", "+"):
                coefficient = "1"
            elif coefficient == "-":
                coefficient = "-1"
            imaginary += Fraction(coefficient)
        else:
            real += Fraction(term)
    return real, imaginary


def encoded_polynomial(encoded: list[list[object]]) -> Polynomial:
    output: Polynomial = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        exponent = [0] * 15
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < 15 and power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        coefficient = parse_gaussian(str(raw_coefficient))
        assert coefficient != ZERO and key not in output
        output[key] = coefficient
    return output


def rref(matrix: list[list[Gaussian]]) -> tuple[list[list[Gaussian]], tuple[int, ...]]:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, rows) if work[row][column] != ZERO),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [divide(value, pivot) for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                subtract(value, multiply(factor, pivot_value))
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, tuple(pivot_columns)


def rank(matrix: list[list[Gaussian]]) -> int:
    return len(rref(matrix)[1])


def determinant(matrix: list[list[Gaussian]]) -> Gaussian:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    output = ONE
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            return ZERO
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            output = negate(output)
        pivot_value = work[column][column]
        output = multiply(output, pivot_value)
        for row in range(column + 1, size):
            if work[row][column] == ZERO:
                continue
            factor = divide(work[row][column], pivot_value)
            for index in range(column, size):
                work[row][index] = subtract(
                    work[row][index], multiply(factor, work[column][index])
                )
    return output


def submatrix(
    matrix: list[list[Gaussian]], rows: tuple[int, ...], columns: tuple[int, ...]
) -> list[list[Gaussian]]:
    return [[matrix[row][column] for column in columns] for row in rows]


def determinant_directional_derivative(
    matrix: list[list[Gaussian]], derivative: list[list[Gaussian]]
) -> Gaussian:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    assert len(derivative) == size and all(len(row) == size for row in derivative)
    output = ZERO
    for column in range(size):
        replaced = [row[:] for row in matrix]
        for row in range(size):
            replaced[row][column] = derivative[row][column]
        output = add(output, determinant(replaced))
    return output


def linear_coefficient(polynomial: Polynomial, variable: int) -> Gaussian:
    exponent = [0] * 15
    exponent[variable] = 1
    return polynomial.get(tuple(exponent), ZERO)


def center_matrix_at_origin(basis: list[Polynomial]) -> list[list[Gaussian]]:
    return [[linear_coefficient(polynomial, column) for column in range(8)] for polynomial in basis]


def center_matrix_derivative(
    basis: list[Polynomial], variable: int
) -> list[list[Gaussian]]:
    output: list[list[Gaussian]] = []
    for polynomial in basis:
        row = []
        for center in range(8):
            exponent = [0] * 15
            exponent[center] = 1
            exponent[variable] = 1
            row.append(polynomial.get(tuple(exponent), ZERO))
        output.append(row)
    return output


def tangent_with_free_coordinate(
    reduced: list[list[Gaussian]], pivots: tuple[int, ...], free_column: int
) -> list[Gaussian]:
    assert free_column not in pivots
    vector = [ZERO] * 15
    vector[free_column] = ONE
    for row, pivot in enumerate(pivots):
        vector[pivot] = negate(reduced[row][free_column])
    return vector


def audit() -> None:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert payload["variable_order"] == [f"x{index}" for index in range(15)]
    basis = [encoded_polynomial(encoded) for encoded in payload["basis"]]
    assert len(basis) == 10

    # After x8=0, every surviving term has center degree at most one.
    for polynomial in basis:
        for exponent in polynomial:
            if exponent[8]:
                continue
            assert sum(exponent[:8]) <= 1

    coefficient = center_matrix_at_origin(basis)
    assert rank(coefficient) == 7
    gaussian_kernel = [
        ONE,
        negate(ONE),
        ZERO,
        ZERO,
        ZERO,
        ZERO,
        ONE,
        ZERO,
    ]
    assert all(dot(row, gaussian_kernel) == ZERO for row in coefficient)
    rows7 = tuple(range(7))
    columns7 = (0, 1, 2, 3, 4, 5, 7)
    assert determinant(submatrix(coefficient, rows7, columns7)) == (
        Fraction(12),
        Fraction(0),
    )
    rows8 = tuple(range(8))
    columns8 = tuple(range(8))
    block8 = submatrix(coefficient, rows8, columns8)
    assert determinant(block8) == ZERO

    jacobian: list[list[Gaussian]] = []
    for polynomial in basis:
        row = []
        for variable in range(15):
            row.append(ZERO if variable == 8 else linear_coefficient(polynomial, variable))
        jacobian.append(row)
    scale_row = [ZERO] * 15
    scale_row[8] = ONE
    jacobian.append(scale_row)
    reduced, pivots = rref(jacobian)
    assert len(pivots) == 11
    free = tuple(index for index in range(15) if index not in pivots)
    assert free == (6, 12, 13, 14)
    tangent = tangent_with_free_coordinate(reduced, pivots, 14)
    for free_column in (6, 12, 13):
        assert tangent[free_column] == ZERO
    assert tangent[14] == ONE

    directional_full = [[ZERO for _column in range(8)] for _row in range(10)]
    for variable in range(9, 15):
        derivative = center_matrix_derivative(basis, variable)
        for row in range(10):
            for column in range(8):
                directional_full[row][column] = add(
                    directional_full[row][column],
                    multiply(tangent[variable], derivative[row][column]),
                )
    directional8 = submatrix(directional_full, rows8, columns8)
    assert determinant_directional_derivative(block8, directional8) == (
        Fraction(0),
        Fraction(48),
    )
    partial_x14 = submatrix(center_matrix_derivative(basis, 14), rows8, columns8)
    assert determinant_directional_derivative(block8, partial_x14) == ZERO

    assert math.comb(10, 8) == 45
    assert math.comb(10, 7) * math.comb(8, 7) == 960

    theorem = THEOREM.read_text(encoding="utf-8")
    required = (
        "g(z,c)=A(z)c+q(z)",
        "B^[8]",
        "B^[7]",
        "B^[<=6]",
        "nu_(R_7,C_7)(F_0)=12",
        "d mu_0(F_0)(tau_14)=48i",
        "V(I_Pl,I_7(A)) intersect D(Omega)",
        "does **not** compute the pulled-back",
        "**UNRESOLVED**",
    )
    for phrase in required:
        assert phrase in theorem


def main() -> None:
    audit()
    print("independent sparse Q(i) center-linear replay: PASS")
    print("Gaussian rank-seven and tangent rank-eight controls: PASS")
    print("finite chart counts and GLD83 residual scope fences: PASS")
    print(
        "scope: exact GLD84 equal-leaf parameter reduction; pulled-back Fitting "
        "ideals, other components, and global Krenn-Gu remain open"
    )


if __name__ == "__main__":
    main()
