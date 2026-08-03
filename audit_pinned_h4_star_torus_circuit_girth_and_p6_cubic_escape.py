"""Independent stdlib audit of pinned-star circuit girth and P6 escape."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations

Quadratic = tuple[Fraction, Fraction]
ZERO: Quadratic = (Fraction(0), Fraction(0))
ONE: Quadratic = (Fraction(1), Fraction(0))
OMEGA: Quadratic = (Fraction(0), Fraction(1))
OMEGA2: Quadratic = (Fraction(-1), Fraction(-1))


def add(left: Quadratic, right: Quadratic) -> Quadratic:
    return left[0] + right[0], left[1] + right[1]


def neg(value: Quadratic) -> Quadratic:
    return -value[0], -value[1]


def mul(left: Quadratic, right: Quadratic) -> Quadratic:
    # omega^2=-omega-1
    constant = left[0] * right[0] - left[1] * right[1]
    omega_part = left[0] * right[1] + left[1] * right[0] - left[1] * right[1]
    return constant, omega_part


def inverse(value: Quadratic) -> Quadratic:
    # conjugation sends omega to omega^2=-1-omega
    norm = value[0] ** 2 - value[0] * value[1] + value[1] ** 2
    if norm == 0:
        raise ZeroDivisionError("zero in Q(omega)")
    return (value[0] - value[1]) / norm, -value[1] / norm


def divide(left: Quadratic, right: Quadratic) -> Quadratic:
    return mul(left, inverse(right))


def sum_values(values) -> Quadratic:
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def rational_rank(rows: list[list[Quadratic]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [divide(value, pivot_value) for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column] == ZERO:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                add(value, neg(mul(multiplier, pivot_entry)))
                for value, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def determinant(rows: list[list[Quadratic]]) -> Quadratic:
    matrix = [row[:] for row in rows]
    result = ONE
    for column in range(len(matrix)):
        pivot = next(row for row in range(column, len(matrix)) if matrix[row][column] != ZERO)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = neg(result)
        pivot_value = matrix[column][column]
        result = mul(result, pivot_value)
        for row in range(column + 1, len(matrix)):
            multiplier = divide(matrix[row][column], pivot_value)
            matrix[row] = [
                add(value, neg(mul(multiplier, pivot_entry)))
                for value, pivot_entry in zip(matrix[row], matrix[column], strict=True)
            ]
    return result


def canonical_core() -> dict[tuple[int, int], Quadratic]:
    return {
        (0, 1): ONE,
        (0, 2): OMEGA,
        (0, 3): ONE,
        (1, 2): ONE,
        (1, 3): ONE,
        (2, 3): OMEGA2,
        (0, 4): OMEGA,
        (1, 4): OMEGA2,
        (2, 4): OMEGA2,
        (3, 4): ONE,
    }


def cached_hafnian(weights: dict[tuple[int, int], Quadratic]):
    @cache
    def evaluate(vertices: tuple[int, ...]) -> Quadratic:
        if not vertices:
            return ONE
        first = vertices[0]
        terms = []
        for partner in vertices[1:]:
            remainder = tuple(vertex for vertex in vertices[1:] if vertex != partner)
            terms.append(mul(weights[tuple(sorted((first, partner)))], evaluate(remainder)))
        return sum_values(terms)

    return evaluate


def audit_cubic_core() -> None:
    weights = canonical_core()
    hafnian = cached_hafnian(weights)
    assert all(hafnian(subset) == ZERO for subset in combinations(range(5), 4))

    k4_matrix = [
        [ZERO, OMEGA2, ONE, ONE],
        [OMEGA2, ZERO, ONE, OMEGA],
        [ONE, ONE, ZERO, ONE],
        [ONE, OMEGA, ONE, ZERO],
    ]
    kernel = [OMEGA, OMEGA2, OMEGA2, ONE]
    assert rational_rank(k4_matrix) == 3
    assert all(
        sum_values(mul(entry, value) for entry, value in zip(row, kernel, strict=True)) == ZERO
        for row in k4_matrix
    )

    vertices = tuple(range(5))
    star_rows: list[list[Quadratic]] = []
    for triple in combinations(vertices, 3):
        row = []
        for pin in vertices:
            if pin not in triple:
                row.append(ZERO)
                continue
            pair = tuple(vertex for vertex in triple if vertex != pin)
            row.append(weights[tuple(sorted(pair))])
        star_rows.append(row)
    assert rational_rank(star_rows) == 5


def p6_weights() -> dict[tuple[int, int], Quadratic]:
    weights = canonical_core()
    for core_vertex in range(5):
        weights[(core_vertex, 5)] = ONE
        weights[(core_vertex, 6)] = neg(ONE)
    weights[(5, 6)] = ONE
    return weights


def audit_p6_escape() -> None:
    weights = p6_weights()
    assert len(weights) == 21
    assert all(value != ZERO for value in weights.values())
    hafnian = cached_hafnian(weights)
    row_sets = list(combinations(range(7), 5))
    matrix: list[list[Quadratic]] = []
    for row_set in row_sets:
        matrix.append(
            [
                hafnian(tuple(vertex for vertex in row_set if vertex != column))
                if column in row_set
                else ZERO
                for column in range(7)
            ]
        )
    kernel = [ZERO, ZERO, ZERO, ZERO, ZERO, ONE, ONE]
    assert all(
        sum_values(mul(entry, value) for entry, value in zip(row, kernel, strict=True)) == ZERO
        for row in matrix
    )
    assert rational_rank(matrix) == 6

    selected_rows = (1, 3, 5, 6, 8, 10)
    selected = [[matrix[row][column] for column in range(6)] for row in selected_rows]
    assert determinant(selected) == (Fraction(216), Fraction(0))
    assert hafnian((0, 1, 2, 5)) == add(OMEGA, (Fraction(2), Fraction(0)))
    assert hafnian((0, 1, 2, 3, 5, 6)) == (Fraction(-6), Fraction(0))


def audit_rational_incidence_ranks() -> None:
    vertices = tuple(range(5))
    edges = tuple(combinations(vertices, 2))
    triangle_rows = [
        [ONE if edge[0] in triple and edge[1] in triple else ZERO for edge in edges]
        for triple in combinations(vertices, 3)
    ]
    assert rational_rank(triangle_rows) == 10

    four_triples = [
        [ONE, ONE, ONE, ZERO],
        [ONE, ONE, ZERO, ONE],
        [ONE, ZERO, ONE, ONE],
        [ZERO, ONE, ONE, ONE],
    ]
    assert determinant(four_triples) == (Fraction(-3), Fraction(0))


def main() -> None:
    audit_cubic_core()
    print("AUDIT PASS: independent Q(omega) K5 zero deck and star rank five")
    audit_p6_escape()
    print("AUDIT PASS: independent P6 pinned rank six, determinant 216, nonzero H4/H6")
    audit_rational_incidence_ranks()
    print("AUDIT PASS: independent triangle and four-triple incidence ranks")
    print("AUDIT SCOPE: stdlib only; imports_primary=0; searches=0; finite_fields=0")
    print("AUDIT BOUNDARY: P7 support-five-through-eight circuits remain UNKNOWN")


if __name__ == "__main__":
    main()
