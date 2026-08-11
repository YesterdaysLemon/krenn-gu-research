"""Independent no-import audit for the diagonal-complete rank-drop boundary."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial

Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, Fraction]
Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


def odd_double_factorial(value: int) -> int:
    """Compute the odd double factorial with (-1)!!=1."""
    if value == -1:
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def perfect_matchings(vertices: Vertices):
    """Generate perfect matchings without importing repository code."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two sparse ternary polynomials."""
    result = left.copy()
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, Fraction(0)) + coefficient
        if not result[exponent]:
            del result[exponent]
    return result


def scale(value: Polynomial, scalar: Fraction | int) -> Polynomial:
    """Scale one sparse polynomial."""
    return {
        exponent: coefficient * Fraction(scalar)
        for exponent, coefficient in value.items()
        if coefficient
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse polynomials exactly."""
    result: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_exponent[index] + right_exponent[index]
                for index in range(3)
            )
            result[exponent] = result.get(exponent, Fraction(0)) + (
                left_coefficient * right_coefficient
            )
    return {exponent: value for exponent, value in result.items() if value}


def power(value: Polynomial, exponent: int) -> Polynomial:
    """Raise one sparse polynomial to a nonnegative integer power."""
    result: Polynomial = {(0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        result = multiply(result, value)
    return result


def linear_form(values: tuple[int, int, int]) -> Polynomial:
    """Create values[0]x+values[1]y+values[2]z."""
    return {
        (1, 0, 0): Fraction(values[0]),
        (0, 1, 0): Fraction(values[1]),
        (0, 0, 1): Fraction(values[2]),
    }


QUADRATIC: Polynomial = {
    (2, 0, 0): Fraction(1),
    (0, 2, 0): Fraction(1),
    (0, 0, 2): Fraction(1),
}


def repeated_companion_by_choices(
    m: int,
    subset: tuple[int, ...],
    linear_forms: tuple[Polynomial, ...],
) -> Polynomial:
    """Reconstruct repeated-root evaluation from all matching choices."""
    roots = tuple(range(m))
    result: Polynomial = {}
    for across_roots in combinations(roots, len(subset)):
        retained = tuple(root for root in roots if root not in across_roots)
        for targets in permutations(subset):
            cross_product: Polynomial = {(0, 0, 0): Fraction(1)}
            for target in targets:
                cross_product = multiply(cross_product, linear_forms[target])
            for _matching in perfect_matchings(retained):
                internal = power(QUADRATIC, len(retained) // 2)
                result = add(result, multiply(cross_product, internal))
    return result


def formula_companion(
    m: int,
    subset: tuple[int, ...],
    linear_forms: tuple[Polynomial, ...],
) -> Polynomial:
    """Build the displayed symmetric formula independently."""
    scalar = (
        comb(m, len(subset))
        * factorial(len(subset))
        * odd_double_factorial(m - len(subset) - 1)
    )
    result = power(QUADRATIC, (m - len(subset)) // 2)
    for target in subset:
        result = multiply(result, linear_forms[target])
    return scale(result, scalar)


def row_rank(columns: list[Polynomial], degree: int) -> int:
    """Compute exact coefficient rank by hand-written Fraction elimination."""
    monomials = [
        (first, second, degree - first - second)
        for first in range(degree + 1)
        for second in range(degree - first + 1)
    ]
    rows = [
        [column.get(monomial, Fraction(0)) for column in columns]
        for monomial in monomials
    ]
    pivot_row = 0
    for column in range(len(columns)):
        selected = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                left - factor * right
                for left, right in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def audit_companion_ranks() -> dict[int, int]:
    """Audit direct m=4 choices and formula ranks through m=6."""
    ranks: dict[int, int] = {}
    for m in range(3, 7):
        forms = tuple(
            linear_form((1, value, value**2)) for value in range(1, m + 1)
        )
        subsets = [
            subset
            for size in range(m + 1)
            if size % 2 == m % 2
            for subset in combinations(range(m), size)
        ]
        columns = [formula_companion(m, subset, forms) for subset in subsets]
        assert len(columns) == 2 ** (m - 1)
        for subset, column in zip(subsets[:-1], columns[:-1], strict=True):
            exponent = (m - len(subset)) // 2
            assert exponent >= 1
            scalar = (
                comb(m, len(subset))
                * factorial(len(subset))
                * odd_double_factorial(m - len(subset) - 1)
            )
            quotient = power(QUADRATIC, exponent - 1)
            for target in subset:
                quotient = multiply(quotient, forms[target])
            assert multiply(QUADRATIC, scale(quotient, scalar)) == column
        rank = row_rank(columns, m)
        assert rank == comb(m, 2) + 1
        ranks[m] = rank

        if m == 4:
            direct = [
                repeated_companion_by_choices(m, subset, forms)
                for subset in subsets
            ]
            assert direct == columns
            assert row_rank(direct, m) == 7
    assert ranks == {3: 4, 4: 7, 5: 11, 6: 16}
    return ranks


def audit_tensor_coefficients() -> dict[str, int]:
    """Build the full eight-vertex word ledger from matching edge colours."""
    vertex_count = 8
    coefficients: dict[tuple[int, ...], int] = defaultdict(int)
    matching_count = 0
    for matching in perfect_matchings(tuple(range(vertex_count))):
        matching_count += 1
        for edge_colours in product(range(3), repeat=vertex_count // 2):
            word = [-1] * vertex_count
            for (left, right), colour in zip(
                matching, edge_colours, strict=True
            ):
                word[left] = colour
                word[right] = colour
            coefficients[tuple(word)] += 1
    assert matching_count == 105

    for word in product(range(3), repeat=vertex_count):
        counts = tuple(word.count(colour) for colour in range(3))
        expected = 0
        if all(count % 2 == 0 for count in counts):
            expected = 1
            for count in counts:
                expected *= odd_double_factorial(count - 1)
        assert coefficients.get(word, 0) == expected

    pure = coefficients[(0,) * vertex_count]
    mixed = coefficients[(0, 0) + (1,) * 6]
    assert (pure, mixed) == (105, 15)
    assert Fraction(mixed, pure) == Fraction(1, 7)

    for colour in range(3):
        local = tuple(
            coefficients.get((open_colour,) + (colour,) * 7, 0)
            for open_colour in range(3)
        )
        expected = tuple(pure if index == colour else 0 for index in range(3))
        assert local == expected
    return {"matchings": matching_count, "words": 3**8, "mixed": mixed}


def audit_dimension_inequality() -> int:
    """Audit the strict all-rank-drop inequality exactly."""
    checked = 0
    for m in range(4, 80):
        assert comb(m, 2) + 1 < 2 ** (m - 1)
        checked += 1
    return checked


def main() -> None:
    ranks = audit_companion_ranks()
    coefficients = audit_tensor_coefficients()
    inequalities = audit_dimension_inequality()
    print("balanced diagonal-complete independent audit: PASS")
    print(f"  sparse companion ranks: {ranks}")
    print(f"  direct coefficient ledger: {coefficients}")
    print(f"  strict dimension inequalities: {inequalities}")


if __name__ == "__main__":
    main()
