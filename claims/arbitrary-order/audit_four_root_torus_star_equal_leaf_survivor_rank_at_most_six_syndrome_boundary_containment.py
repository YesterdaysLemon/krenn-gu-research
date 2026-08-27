#!/usr/bin/env python3
"""Independent no-import audit of the GLD86 boundary certificate.

This audit deliberately does not import any repository Python module or call
SymPy.  It rebuilds the displayed 7-by-7 submatrix of the GLD71 syndrome map
from its compact coefficient formulas and expands its determinant with a
small sparse polynomial engine over ``Q(i)``.  A separate exact Gaussian
matrix fixture checks the column-replacement sign convention.  The owning
GLD75 certificate is only read as immutable JSON metadata; its full
bidirectional replay remains an upstream GLD75 check.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import permutations
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
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md"
)
EXPECTED_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"

N_VARIABLES = 6
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
Gaussian = tuple[Fraction, Fraction]
Polynomial = dict[tuple[int, ...], Gaussian]


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gaussian_negate(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gaussian_multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def constant(value: Gaussian) -> Polynomial:
    return {} if value == ZERO else {(0,) * N_VARIABLES: value}


def variable(index: int) -> Polynomial:
    exponent = [0] * N_VARIABLES
    exponent[index] = 1
    return {tuple(exponent): ONE}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    output = dict(left)
    for exponent, coefficient in right.items():
        value = gaussian_add(output.get(exponent, ZERO), coefficient)
        if value == ZERO:
            output.pop(exponent, None)
        else:
            output[exponent] = value
    return output


def negate(value: Polynomial) -> Polynomial:
    return {exponent: gaussian_negate(coefficient) for exponent, coefficient in value.items()}


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, negate(right))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_power + right_power
                for left_power, right_power in zip(
                    left_exponent, right_exponent, strict=True
                )
            )
            coefficient = gaussian_add(
                output.get(exponent, ZERO),
                gaussian_multiply(left_coefficient, right_coefficient),
            )
            if coefficient == ZERO:
                output.pop(exponent, None)
            else:
                output[exponent] = coefficient
    return output


def scale(value: Polynomial, coefficient: Gaussian) -> Polynomial:
    return multiply(value, constant(coefficient))


def power(value: Polynomial, exponent: int) -> Polynomial:
    output = constant(ONE)
    for _ in range(exponent):
        output = multiply(output, value)
    return output


def sum_polynomials(*values: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for value in values:
        output = add(output, value)
    return output


def square_minus_self(value: Polynomial) -> Polynomial:
    return subtract(power(value, 2), value)


def cube(value: Polynomial) -> Polynomial:
    return power(value, 3)


def survivor_quadratic(value: Polynomial) -> Polynomial:
    return sum_polynomials(
        scale(power(value, 2), (-2, 0)),
        scale(value, (2, 0)),
        constant((-1, 0)),
    )


def determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    output: Polynomial = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = constant(ONE)
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        if inversions % 2:
            term = negate(term)
        output = add(output, term)
    return output


def p_minus_one_times(value: Polynomial) -> Polynomial:
    return multiply(value, subtract(value, constant(ONE)))


def compact_selected_matrix() -> list[list[Polynomial]]:
    """Return rows (0,1,17,19,31,32,33), columns (2,...,8) of M(G)."""

    p, q, r, a, b, c = (variable(index) for index in range(6))
    s = sum_polynomials(constant((1, 1)), r)
    r2 = multiply(sum_polynomials(r, constant((0, 1))), s)
    row17_r = scale(
        multiply(
            sum_polynomials(scale(r, (1, -1)), constant(ONE)),
            sum_polynomials(scale(r, (1, -1)), constant((2, 1))),
        ),
        (0, -1),
    )
    row19_r = multiply(multiply(r, sum_polynomials(r, constant((0, 2)))), s)

    row31_p = scale(
        sum_polynomials(
            scale(multiply(a, power(p, 2)), (3, 0)),
            scale(multiply(a, p), (6, 0)),
            scale(a, (-6, 0)),
            scale(p, (-3, 0)),
            constant((4, 0)),
        ),
        (2, 0),
    )
    row31_q = scale(
        sum_polynomials(
            scale(multiply(b, power(q, 2)), (3, 0)),
            scale(multiply(b, q), (6, 0)),
            scale(b, (-6, 0)),
            scale(power(q, 2), (3, 0)),
            scale(q, (3, 0)),
            constant((-2, 0)),
        ),
        (2, 0),
    )
    row31_r = scale(
        sum_polynomials(
            scale(multiply(c, power(r, 2)), (3, 0)),
            scale(multiply(c, r), (12, 6)),
            scale(c, (0, 12)),
            scale(power(r, 2), (3, 0)),
            scale(r, (9, 6)),
            constant((1, 9)),
        ),
        (2, 0),
    )
    row32_r = scale(
        sum_polynomials(
            scale(multiply(c, power(r, 2)), (-6, 0)),
            scale(multiply(c, r), (-6, -12)),
            scale(c, (9, -6)),
            scale(power(r, 3), (4, 0)),
            scale(power(r, 2), (3, 12)),
            scale(r, (-12, 6)),
            constant((1, -4)),
        ),
        (-2, 0),
    )
    row33_p = scale(
        sum_polynomials(scale(power(p, 2), (3, 0)), scale(p, (-3, 0)), constant(ONE)),
        (4, 0),
    )
    row33_q = scale(
        sum_polynomials(scale(power(q, 2), (3, 0)), scale(q, (-3, 0)), constant(ONE)),
        (4, 0),
    )
    row33_r = scale(
        sum_polynomials(
            scale(power(r, 2), (3, 0)),
            scale(r, (3, 6)),
            constant((-2, 3)),
        ),
        (4, 0),
    )
    zero = constant(ZERO)
    minus_six = constant((-6, 0))
    minus_twelve_p2 = scale(square_minus_self(p), (-12, 0))
    minus_twelve_q2 = scale(square_minus_self(q), (-12, 0))
    minus_twelve_r2 = scale(r2, (-12, 0))

    full_rows = [
        [zero, zero, zero, cube(p), cube(q), cube(s), zero, zero, zero],
        [constant(ONE), constant(ONE), constant(ONE), zero, zero, zero, zero, zero, zero],
        [
            zero,
            zero,
            r2,
            survivor_quadratic(p),
            survivor_quadratic(q),
            row17_r,
            zero,
            zero,
            zero,
        ],
        [
            zero,
            zero,
            row19_r,
            square_minus_self(p),
            square_minus_self(q),
            r2,
            zero,
            zero,
            zero,
        ],
        [
            zero,
            zero,
            zero,
            row31_p,
            row31_q,
            row31_r,
            scale(cube(p), (6, 0)),
            scale(cube(q), (6, 0)),
            scale(cube(s), (6, 0)),
        ],
        [
            row32_r,
            zero,
            zero,
            zero,
            zero,
            zero,
            minus_six,
            minus_six,
            minus_six,
        ],
        [
            zero,
            zero,
            zero,
            row33_p,
            row33_q,
            row33_r,
            minus_twelve_p2,
            minus_twelve_q2,
            minus_twelve_r2,
        ],
    ]
    return [[row[column] for column in range(2, 9)] for row in full_rows]


def check_column_replacement_fixture() -> None:
    """Check the C8=1 column replacement sign on an exact constant matrix."""

    matrix = [
        [constant((row + column + 1, row - column)) for column in range(9)]
        for row in range(7)
    ]
    # The fixture has nine columns numbered 0,...,8; use column 8 as the
    # distinguished C8 column and columns 0,1 as the possible replacements.

    for c0, c1 in ((0, 0), (1, 0), (0, 1), (2, -3)):
        last = []
        for row in range(7):
            value = constant((0, 0))
            for column, coefficient in enumerate(
                (c0, c1, 0, 0, 0, 0, 0, 0, 1)
            ):
                value = add(value, scale(matrix[row][column], (coefficient, 0)))
            last.append(value)
        replacement = [
            [matrix[row][column] for column in (2, 3, 4, 5, 6, 7)] + [last[row]]
            for row in range(7)
        ]
        d8 = determinant(
            [
                [matrix[row][column] for column in (2, 3, 4, 5, 6, 7)]
                + [matrix[row][8]]
                for row in range(7)
            ]
        )
        d0 = determinant(
            [
                [matrix[row][column] for column in (2, 3, 4, 5, 6, 7)]
                + [matrix[row][0]]
                for row in range(7)
            ]
        )
        d1 = determinant(
            [
                [matrix[row][column] for column in (2, 3, 4, 5, 6, 7)]
                + [matrix[row][1]]
                for row in range(7)
            ]
        )
        expected = add(add(d8, scale(d0, (c0, 0))), scale(d1, (c1, 0)))
        assert determinant(replacement) == expected


def audit() -> None:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert payload["variable_order"] == [f"x{index}" for index in range(15)]
    assert payload["incidence_generator_count"] == 37
    assert payload["basis_generator_count"] == 10
    assert payload["forward_shape"] == [37, 10]
    assert payload["reverse_shape"] == [10, 37]
    assert sum(len(entry["terms"]) for entry in payload["forward"]) == 27
    assert sum(len(entry["terms"]) for entry in payload["reverse"]) == 63

    matrix = compact_selected_matrix()
    determinant_value = determinant(matrix)
    p, q, r, _a, _b, _c = (variable(index) for index in range(6))
    s = sum_polynomials(constant((1, 1)), r)
    divisors = (
        subtract(p, q),
        subtract(p, s),
        subtract(q, s),
        subtract(
            sum_polynomials(multiply(p, q), multiply(p, s), multiply(q, s)),
            sum_polynomials(p, q, s),
        ),
    )
    expected = constant((432, 0))
    for divisor in divisors:
        expected = multiply(expected, power(divisor, 2))
    assert determinant_value == expected
    assert all(
        exponent[3:] == (0, 0, 0) for exponent in determinant_value
    )
    check_column_replacement_fixture()

    theorem = THEOREM.read_text(encoding="utf-8")
    required = (
        "GLD86",
        "B=0 iff M(G)C=0",
        "C_8=1",
        "p-q",
        "p-s",
        "q-s",
        "p q+p s+q s-p-q-s",
        "V(I_7(A))",
        "D(Omega)",
        "none of the four divisors is excluded",
        "GLD83",
        "**UNRESOLVED**",
    )
    for phrase in required:
        assert phrase in theorem


def main() -> None:
    audit()
    print("independent no-import GLD86 syndrome-minor replay: PASS")
    print("exact factorization and C8=1 column replacement fixture: PASS")
    print(
        "scope: rank-at-most-six containment in four named divisors; "
        "Omega-saturated divisor emptiness and pulled-back Fitting remain open"
    )


if __name__ == "__main__":
    main()
