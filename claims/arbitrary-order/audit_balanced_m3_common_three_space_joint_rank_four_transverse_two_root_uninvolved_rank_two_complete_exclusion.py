#!/usr/bin/env python3
"""Independent no-import audit of the rank-four q=2 exclusion identities."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, Fraction]
Component = dict[str, Polynomial]
Row = tuple[Component, Component, Component]
Tensor = dict[tuple[str, str, str], Polynomial]

ZERO_MONOMIAL: Monomial = (0, 0, 0, 0)


def clean(polynomial: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {ZERO_MONOMIAL: coefficient}


def variable(index: int) -> Polynomial:
    exponent = [0, 0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}  # type: ignore[arg-type]


def poly_add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def poly_scale(value: int | Fraction, polynomial: Polynomial) -> Polynomial:
    scalar = Fraction(value)
    return clean({monomial: scalar * coefficient for monomial, coefficient in polynomial.items()})


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_degree + right_degree
                for left_degree, right_degree in zip(left_monomial, right_monomial, strict=True)
            )
            result[monomial] = (
                result.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
            )
    return clean(result)


def component(label: str, coefficient: Polynomial | None = None) -> Component:
    return {label: constant(1) if coefficient is None else coefficient}


def row(
    x_part: Component | None = None,
    y_part: Component | None = None,
    z_part: Component | None = None,
) -> Row:
    return x_part or {}, y_part or {}, z_part or {}


def combine(*terms: tuple[Polynomial, Row]) -> Row:
    result: list[Component] = [{}, {}, {}]
    for coefficient, vector in terms:
        for source in range(3):
            for label, entry in vector[source].items():
                product = poly_multiply(coefficient, entry)
                result[source][label] = poly_add(result[source].get(label, {}), product)
    return tuple(result)  # type: ignore[return-value]


def tensor_add_entry(
    target: Tensor,
    x_part: Component,
    y_part: Component,
    z_part: Component,
    sign: int,
) -> None:
    # Store keys in Z,Y,X order, independently of the primary replay.
    for x_label, x_coefficient in x_part.items():
        for y_label, y_coefficient in y_part.items():
            for z_label, z_coefficient in z_part.items():
                coefficient = poly_scale(
                    sign,
                    poly_multiply(
                        poly_multiply(x_coefficient, y_coefficient),
                        z_coefficient,
                    ),
                )
                key = z_label, y_label, x_label
                target[key] = poly_add(target.get(key, {}), coefficient)


def permanent(left: Row, middle: Row, right: Row) -> Tensor:
    vectors = left, middle, right
    result: Tensor = {}
    for assignment in reversed(tuple(permutations(range(3)))):
        tensor_add_entry(
            result,
            vectors[assignment[0]][0],
            vectors[assignment[1]][1],
            vectors[assignment[2]][2],
            1,
        )
    return {key: clean(value) for key, value in result.items() if clean(value)}


def alternating(first: Row, second: Row, third: Row) -> Tensor:
    vectors = first, second, third
    result: Tensor = {}
    for assignment in reversed(tuple(permutations(range(3)))):
        inversions = sum(
            assignment[left_index] > assignment[right_index]
            for left_index in range(3)
            for right_index in range(left_index + 1, 3)
        )
        tensor_add_entry(
            result,
            vectors[assignment[0]][0],
            vectors[assignment[1]][1],
            vectors[assignment[2]][2],
            -1 if inversions % 2 else 1,
        )
    return {key: clean(value) for key, value in result.items() if clean(value)}


def matrix_rank(rows: list[list[Fraction]]) -> int:
    matrix = [line[:] for line in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(pivot_row, len(matrix)) if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
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


def formal_chart_audit() -> None:
    one = constant(1)
    minus_one = constant(-1)
    coefficient_a, coefficient_b, coefficient_c, coefficient_d = (
        variable(index) for index in range(4)
    )

    x = row(x_part=component("x"))
    d = row(x_part=component("d"))
    y = row(y_part=component("y"))
    e = row(y_part=component("e"))
    t = row(z_part=component("t"))
    w = combine((one, x), (minus_one, y))
    u = combine((minus_one, d), (minus_one, e), (one, t))
    v = combine((one, x), (one, y))
    q_1 = combine((one, d), (one, e), (one, t))
    u_0 = combine((coefficient_a, w), (coefficient_b, u))
    u_1 = combine((coefficient_c, w), (coefficient_d, u))

    for divisor in (w, u):
        assert permanent(divisor, v, w) == {}
        assert permanent(divisor, v, q_1) == {}

    ad = poly_multiply(coefficient_a, coefficient_d)
    bc = poly_multiply(coefficient_b, coefficient_c)
    bd = poly_multiply(coefficient_b, coefficient_d)
    ac = poly_multiply(coefficient_a, coefficient_c)

    expected_q_0 = {
        ("t", "y", "x"): poly_scale(-2, poly_add(ad, bc)),
        ("t", "y", "d"): poly_scale(2, bd),
        ("t", "e", "x"): poly_scale(-2, bd),
    }
    expected_q_1 = {
        ("t", "y", "x"): poly_scale(-2, ac),
        ("t", "e", "d"): poly_scale(-2, bd),
    }
    expected_alt = {
        ("t", "y", "x"): poly_scale(-2, poly_add(ad, poly_scale(-1, bc)))
    }
    assert permanent(u_0, u_1, w) == expected_q_0
    assert permanent(u_0, u_1, q_1) == expected_q_1
    assert alternating(u_0, u_1, v) == expected_alt
    print("independent formal chart: PASS (sparse polynomial identities)")


def scalar_row(x_value: int, y_value: int, z_value: int) -> Row:
    return row(
        x_part={} if not x_value else component("x", constant(x_value)),
        y_part={} if not y_value else component("y", constant(y_value)),
        z_part={} if not z_value else component("t", constant(z_value)),
    )


def flatten_constants(vector: Row) -> list[Fraction]:
    result: list[Fraction] = []
    for source, label in zip(vector, ("x", "y", "t"), strict=True):
        result.append(source.get(label, {}).get(ZERO_MONOMIAL, Fraction(0)))
    return result


def contained_fixture_audit() -> None:
    v = scalar_row(1, 1, 0)
    u_0 = scalar_row(0, -2, 1)
    u_1 = scalar_row(2, 0, -1)
    q_0 = scalar_row(1, -1, 0)
    q_1 = scalar_row(1, 1, 1)

    v_rows = [flatten_constants(vector) for vector in (u_0, u_1, v)]
    q_rows = [flatten_constants(vector) for vector in (q_0, q_1)]
    assert matrix_rank(v_rows) == 3
    assert matrix_rank(q_rows) == 2
    assert matrix_rank(v_rows + q_rows) == 3

    target = {("t", "y", "x"): constant(1)}
    assert permanent(v, v, q_0) == {}
    assert permanent(v, v, q_1) == {
        key: poly_scale(2, coefficient) for key, coefficient in target.items()
    }
    for left, middle in ((u_0, v), (u_1, v), (u_0, u_1)):
        assert permanent(left, middle, q_0) == {}
        assert permanent(left, middle, q_1) == {}
    assert alternating(u_0, u_1, v) == {
        key: poly_scale(4, coefficient) for key, coefficient in target.items()
    }
    print("independent contained fixture: PASS (Fraction arithmetic)")


def main() -> None:
    formal_chart_audit()
    contained_fixture_audit()
    print("independent joint-rank-four q=2 audit: PASS")


if __name__ == "__main__":
    main()
