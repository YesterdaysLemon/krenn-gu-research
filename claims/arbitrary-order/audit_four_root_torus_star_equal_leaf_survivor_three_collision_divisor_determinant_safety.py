#!/usr/bin/env python3
"""Independent exact audit of the GLD87 H1--H3 calculation.

This file intentionally imports neither a repository module nor SymPy.  It
rebuilds the 11 transformed H1 rows from compact polynomial formulas, uses a
small sparse polynomial ring over ``Q``, and independently expands the base
4-minors, difference minors, exceptional 7-minor, exceptional 6-minor, and
kernel identities.  The primary verifier remains responsible for replaying
the pinned GLD71 relation basis and the GLD86 upstream certificate.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEOREM = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_THREE_COLLISION_DIVISOR_DETERMINANT_SAFETY_THEOREM.md"
)

N_VARIABLES = 5  # p, s, a, b, c
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]
ZERO = Fraction(0)
ONE = Fraction(1)


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(0,) * N_VARIABLES: coefficient}


def variable(index: int) -> Polynomial:
    exponent = [0] * N_VARIABLES
    exponent[index] = 1
    return {tuple(exponent): ONE}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    output = dict(left)
    for exponent, coefficient in right.items():
        value = output.get(exponent, ZERO) + coefficient
        if value == 0:
            output.pop(exponent, None)
        else:
            output[exponent] = value
    return output


def negate(value: Polynomial) -> Polynomial:
    return {exponent: -coefficient for exponent, coefficient in value.items()}


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
            value = output.get(exponent, ZERO) + left_coefficient * right_coefficient
            if value == 0:
                output.pop(exponent, None)
            else:
                output[exponent] = value
    return output


def scale(value: Polynomial, coefficient: int | Fraction) -> Polynomial:
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


def determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    if size == 1:
        return matrix[0][0]
    pivot = min(range(size), key=lambda row: sum(bool(entry) for entry in matrix[row]))
    output: Polynomial = {}
    for column, entry in enumerate(matrix[pivot]):
        if not entry:
            continue
        minor = [
            [value for index, value in enumerate(row) if index != column]
            for index, row in enumerate(matrix)
            if index != pivot
        ]
        term = multiply(entry, determinant(minor))
        if (pivot + column) % 2:
            term = negate(term)
        output = add(output, term)
    return output


def extract(
    matrix: list[list[Polynomial]], rows: tuple[int, ...], columns: tuple[int, ...]
) -> list[list[Polynomial]]:
    return [[matrix[row][column] for column in columns] for row in rows]


def substitute(value: Polynomial, replacements: list[Polynomial]) -> Polynomial:
    output: Polynomial = {}
    for exponent, coefficient in value.items():
        term = constant(coefficient)
        for index, exponent_value in enumerate(exponent):
            term = multiply(term, power(replacements[index], exponent_value))
        output = add(output, term)
    return output


def s_power_mod_relation(exponent: int) -> tuple[Fraction, Fraction]:
    """Return s**exponent modulo s**2-s+1 as (constant, s) coefficients."""

    constant_part, s_part = ONE, ZERO
    for _ in range(exponent):
        constant_part, s_part = -s_part, constant_part + s_part
    return constant_part, s_part


def reduce_s_relation(value: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for exponent, coefficient in value.items():
        constant_part, s_part = s_power_mod_relation(exponent[1])
        for power_value, multiplier in ((0, constant_part), (1, s_part)):
            if multiplier == 0:
                continue
            reduced_exponent = list(exponent)
            reduced_exponent[1] = power_value
            term = {tuple(reduced_exponent): coefficient * multiplier}
            output = add(output, term)
    return output


def variables() -> tuple[Polynomial, ...]:
    return tuple(variable(index) for index in range(N_VARIABLES))


def transformed_h1_rows() -> list[list[Polynomial]]:
    """Compact exact rows after q=p and T0=(1,0,0;-1,1,0;0,0,1)."""

    p, s, a, b, c = variables()
    zero = constant(0)
    row0 = [zero, zero, zero, zero, power(p, 3), power(s, 3), zero, zero, zero]
    row1 = [zero, constant(1), constant(1), zero, zero, zero, zero, zero, zero]
    row2 = [
        zero,
        zero,
        zero,
        zero,
        zero,
        zero,
        negate(multiply(subtract(a, b), subtract(power(p, 2), constant(1)))),
        negate(multiply(b, subtract(power(p, 2), constant(1)))),
        negate(multiply(c, subtract(power(s, 2), constant(1)))),
    ]
    row3 = [
        zero,
        multiply(p, subtract(p, constant(1))),
        multiply(s, subtract(s, constant(1))),
        zero,
        sum_polynomials(scale(power(p, 2), -2), scale(p, 2), constant(-1)),
        sum_polynomials(scale(power(s, 2), -2), scale(s, 2), constant(-1)),
        zero,
        zero,
        zero,
    ]
    row4 = [
        zero,
        multiply(p, sum_polynomials(power(p, 2), scale(p, -2), constant(2))),
        multiply(s, sum_polynomials(power(s, 2), scale(s, -2), constant(2))),
        zero,
        multiply(p, subtract(p, constant(1))),
        multiply(s, subtract(s, constant(1))),
        zero,
        zero,
        zero,
    ]
    p_diff = subtract(p, b)
    s_diff = subtract(s, c)
    row5 = [
        zero,
        zero,
        zero,
        multiply(subtract(a, b), subtract(scale(p, 2), constant(1))),
        negate(multiply(p_diff, subtract(scale(p, 2), constant(1)))),
        negate(multiply(s_diff, subtract(scale(s, 2), constant(1)))),
        negate(multiply(subtract(a, b), subtract(scale(p, 2), constant(1)))),
        multiply(p_diff, subtract(scale(p, 2), constant(1))),
        multiply(s_diff, subtract(scale(s, 2), constant(1))),
    ]
    row6_factor = multiply(p, subtract(p, constant(2)))
    row6_s_factor = multiply(s, subtract(s, constant(2)))
    row6 = [
        multiply(subtract(a, b), row6_factor),
        multiply(subtract(b, constant(1)), row6_factor),
        multiply(subtract(c, constant(1)), row6_s_factor),
        zero,
        zero,
        zero,
        negate(multiply(subtract(a, b), row6_factor)),
        negate(multiply(subtract(b, constant(1)), row6_factor)),
        negate(multiply(subtract(c, constant(1)), row6_s_factor)),
    ]
    row7 = [
        zero,
        zero,
        zero,
        scale(
            multiply(
                subtract(a, b), sum_polynomials(power(p, 2), scale(p, 2), constant(-2))
            ),
            6,
        ),
        scale(
            sum_polynomials(
                scale(multiply(b, power(p, 2)), 3),
                scale(multiply(b, p), 6),
                scale(b, -6),
                scale(p, -3),
                constant(4),
            ),
            2,
        ),
        scale(
            sum_polynomials(
                scale(multiply(c, power(s, 2)), 3),
                scale(multiply(c, s), 6),
                scale(c, -6),
                scale(s, -3),
                constant(4),
            ),
            2,
        ),
        zero,
        scale(power(p, 3), 6),
        scale(power(s, 3), 6),
    ]
    row8 = [
        scale(
            multiply(
                subtract(a, b),
                sum_polynomials(scale(power(p, 2), 2), scale(p, -2), constant(-1)),
            ),
            6,
        ),
        negate(
            scale(
                sum_polynomials(
                    scale(multiply(b, power(p, 2)), -6),
                    scale(multiply(b, p), 6),
                    scale(b, 3),
                    scale(power(p, 3), 4),
                    scale(power(p, 2), -3),
                ),
                2,
            )
        ),
        negate(
            scale(
                sum_polynomials(
                    scale(multiply(c, power(s, 2)), -6),
                    scale(multiply(c, s), 6),
                    scale(c, 3),
                    scale(power(s, 3), 4),
                    scale(power(s, 2), -3),
                ),
                2,
            )
        ),
        zero,
        zero,
        zero,
        zero,
        constant(-6),
        constant(-6),
    ]
    row9 = [
        zero,
        zero,
        zero,
        zero,
        scale(sum_polynomials(scale(power(p, 2), 3), scale(p, -3), constant(1)), 4),
        scale(sum_polynomials(scale(power(s, 2), 3), scale(s, -3), constant(1)), 4),
        zero,
        scale(multiply(p, subtract(p, constant(1))), -12),
        scale(multiply(s, subtract(s, constant(1))), -12),
    ]
    row10 = [
        zero,
        zero,
        zero,
        scale(multiply(subtract(a, b), subtract(scale(p, 2), constant(1))), 12),
        negate(
            scale(
                sum_polynomials(
                    scale(multiply(b, p), -6),
                    scale(b, 3),
                    scale(power(p, 2), 3),
                    constant(-1),
                ),
                4,
            )
        ),
        negate(
            scale(
                sum_polynomials(
                    scale(multiply(c, s), -6),
                    scale(c, 3),
                    scale(power(s, 2), 3),
                    constant(-1),
                ),
                4,
            )
        ),
        scale(multiply(p, multiply(subtract(a, b), subtract(p, constant(2)))), 12),
        scale(multiply(p, sum_polynomials(multiply(b, p), scale(b, -2), p)), 12),
        scale(multiply(s, sum_polynomials(multiply(c, s), scale(c, -2), s)), 12),
    ]
    return [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]


def h1_base_and_difference(
    matrix: list[list[Polynomial]],
) -> tuple[list[list[Polynomial]], list[list[Polynomial]]]:
    base_rows = (0, 1, 3, 4, 9)
    base_columns = (1, 2, 4, 5, 7, 8)
    difference_rows = (2, 5, 6, 7, 8, 10)
    difference_columns = (0, 3, 6)
    base = extract(matrix, base_rows, base_columns)
    delta = [
        [constant(0), constant(0), subtract(constant(1), power(variable(0), 2))],
        [
            constant(0),
            subtract(scale(variable(0), 2), constant(1)),
            subtract(constant(1), scale(variable(0), 2)),
        ],
        [
            multiply(variable(0), subtract(variable(0), constant(2))),
            constant(0),
            negate(multiply(variable(0), subtract(variable(0), constant(2)))),
        ],
        [
            constant(0),
            scale(
                sum_polynomials(
                    power(variable(0), 2), scale(variable(0), 2), constant(-2)
                ),
                6,
            ),
            constant(0),
        ],
        [
            scale(
                sum_polynomials(
                    scale(power(variable(0), 2), 2),
                    scale(variable(0), -2),
                    constant(-1),
                ),
                6,
            ),
            constant(0),
            constant(0),
        ],
        [
            constant(0),
            scale(subtract(scale(variable(0), 2), constant(1)), 12),
            scale(multiply(variable(0), subtract(variable(0), constant(2))), 12),
        ],
    ]
    actual_difference = extract(matrix, difference_rows, difference_columns)
    expected_difference = [
        [multiply(subtract(variable(2), variable(3)), entry) for entry in row]
        for row in delta
    ]
    assert actual_difference == expected_difference
    return base, delta


def substitute_p_one_minus_s(value: Polynomial) -> Polynomial:
    _p, s, a, b, c = variables()
    return substitute(value, [subtract(constant(1), s), s, a, b, c])


def exceptional_substitution(value: Polynomial) -> Polynomial:
    _p, s, a, b, _c = variables()
    return substitute(
        value,
        [subtract(constant(1), s), s, a, b, scale(add(s, constant(1)), Fraction(1, 3))],
    )


def zero_at_eisenstein_pair(value: Polynomial) -> bool:
    return not reduce_s_relation(substitute_p_one_minus_s(value))


def univariate_gcd(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    def trim(value: dict[int, Fraction]) -> dict[int, Fraction]:
        return {
            degree: coefficient for degree, coefficient in value.items() if coefficient
        }

    def divide(
        dividend: dict[int, Fraction], divisor: dict[int, Fraction]
    ) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
        remainder = trim(dividend)
        quotient: dict[int, Fraction] = {}
        divisor_degree = max(divisor)
        divisor_lead = divisor[divisor_degree]
        while remainder and max(remainder) >= divisor_degree:
            degree = max(remainder) - divisor_degree
            coefficient = remainder[max(remainder)] / divisor_lead
            quotient[degree] = quotient.get(degree, ZERO) + coefficient
            for index, value in divisor.items():
                new_degree = index + degree
                remainder[new_degree] = (
                    remainder.get(new_degree, ZERO) - coefficient * value
                )
                if remainder[new_degree] == 0:
                    remainder.pop(new_degree)
        return trim(quotient), trim(remainder)

    left, right = trim(left), trim(right)
    while right:
        _quotient, remainder = divide(left, right)
        left, right = right, remainder
    if not left:
        return {}
    lead = left[max(left)]
    return {degree: coefficient / lead for degree, coefficient in left.items()}


def specialize_p_only(value: Polynomial) -> dict[int, Fraction]:
    output: dict[int, Fraction] = {}
    for exponent, coefficient in value.items():
        assert exponent[1:] == (0, 0, 0, 0)
        output[exponent[0]] = output.get(exponent[0], ZERO) + coefficient
    return {
        degree: coefficient for degree, coefficient in output.items() if coefficient
    }


def audit() -> None:
    matrix = transformed_h1_rows()
    base, delta = h1_base_and_difference(matrix)

    # The independent base replay sees all 37 nonzero 4-minors and confirms
    # p=s is a factor of each one.  It also checks the surviving Eisenstein
    # candidate directly in the quotient s^2-s+1.
    nonzero = 0
    for rows in combinations(range(5), 4):
        for columns in combinations(range(6), 4):
            minor = determinant(extract(base, rows, columns))
            if not minor:
                continue
            nonzero += 1
            assert not substitute(
                minor, [variable(1), variable(1), variable(2), variable(3), variable(4)]
            )
            assert zero_at_eisenstein_pair(minor)
    assert nonzero == 37

    delta_witnesses = (
        (0, 1, 2),
        (0, 1, 4),
        (2, 3, 4),
    )
    delta_minors = [
        determinant(extract(delta, rows, (0, 1, 2))) for rows in delta_witnesses
    ]
    gcd = specialize_p_only(delta_minors[0])
    for minor in delta_minors[1:]:
        gcd = univariate_gcd(gcd, specialize_p_only(minor))
    assert gcd == {0: ONE}

    relation = s_power_mod_relation
    del relation  # Keep the quotient reduction name explicit below.
    minor7 = determinant(extract(matrix, (0, 1, 9, 2, 5, 6, 8), (1, 2, 4, 7, 0, 3, 6)))
    reduced7 = reduce_s_relation(substitute_p_one_minus_s(minor7))
    _p, s, a, b, c = variables()
    expected7 = scale(
        multiply(power(subtract(a, b), 3), subtract(add(multiply(c, s), c), s)), -648
    )
    assert reduced7 == expected7

    minor6 = determinant(extract(matrix, (0, 1, 2, 5, 6, 7), (0, 1, 3, 4, 6, 7)))
    reduced6 = reduce_s_relation(substitute_p_one_minus_s(minor6))
    expected6 = scale(
        multiply(power(subtract(a, b), 3), subtract(scale(s, 2), constant(1))), 36
    )
    assert reduced6 == expected6

    kernel = [
        subtract(add(scale(b, 3), s), constant(2)),
        negate(scale(subtract(a, b), 3)),
        scale(subtract(a, b), 3),
    ]
    for block in (0, 3, 6):
        for row in matrix:
            value = sum_polynomials(
                *(multiply(row[block + index], kernel[index]) for index in range(3))
            )
            assert not reduce_s_relation(exceptional_substitution(value))

    relation_poly = {2: ONE, 1: Fraction(-1), 0: ONE}
    assert univariate_gcd({1: ONE, 0: ONE}, relation_poly) == {0: ONE}
    assert univariate_gcd({1: Fraction(2), 0: Fraction(-1)}, relation_poly) == {0: ONE}

    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "GLD87",
        "H_1",
        "H_2",
        "H_3",
        "H_4",
        "M(G) C=0",
        "C_8=1",
        "det(C)",
        "**UNRESOLVED**",
    ):
        assert phrase in theorem


def main() -> None:
    audit()
    print("independent no-import GLD87 H1-H3 polynomial audit: PASS")
    print(
        "exact base/difference minors, exceptional minors, and kernel identities: PASS"
    )
    print(
        "scope: H1-H3 determinant safety only; H4 and the global conjecture remain open"
    )


if __name__ == "__main__":
    main()
