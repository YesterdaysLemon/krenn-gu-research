"""Primary exact checks for the diagonal-complete all-rank-drop boundary."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import combinations, permutations, product
from math import comb, factorial

import sympy as sp

Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


def odd_double_factorial(value: int) -> int:
    """Return value!! for odd value >= -1."""
    if value == -1:
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def perfect_matchings(vertices: Vertices) -> Iterator[Matching]:
    """Generate every labelled perfect matching recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def coefficient_by_matching(word: tuple[int, ...]) -> int:
    """Count matchings whose diagonal edges respect one colour word."""
    total = 0
    for matching in perfect_matchings(tuple(range(len(word)))):
        if all(word[left] == word[right] for left, right in matching):
            total += 1
    return total


def coefficient_formula(word: tuple[int, ...]) -> int:
    """Evaluate the unscaled double-factorial coefficient formula."""
    counts = tuple(word.count(colour) for colour in range(3))
    if any(count % 2 for count in counts):
        return 0
    result = 1
    for count in counts:
        result *= odd_double_factorial(count - 1)
    return result


def assert_tensor_coefficients() -> dict[str, int]:
    """Check the complete formula and local slices at eight vertices."""
    vertex_count = 8
    checked = 0
    for word in product(range(3), repeat=vertex_count):
        assert coefficient_by_matching(word) == coefficient_formula(word)
        checked += 1

    pure = coefficient_formula((0,) * vertex_count)
    mixed = coefficient_formula((0, 0) + (1,) * (vertex_count - 2))
    odd = coefficient_formula((0,) + (1,) * (vertex_count - 1))
    assert pure == odd_double_factorial(7) == 105
    assert mixed == odd_double_factorial(5) == 15
    assert sp.Rational(mixed, pure) == sp.Rational(1, 7)
    assert odd == 0

    for fixed_colour in range(3):
        local_slice = []
        for open_colour in range(3):
            word = (open_colour,) + (fixed_colour,) * (vertex_count - 1)
            local_slice.append(coefficient_formula(word))
        assert local_slice == [
            pure if colour == fixed_colour else 0 for colour in range(3)
        ]
    return {"words": checked, "pure": pure, "mixed": mixed}


def companion_scalar(m: int, subset_size: int) -> int:
    """Return the repeated-root multiplicity a_(m,k)."""
    return (
        comb(m, subset_size)
        * factorial(subset_size)
        * odd_double_factorial(m - subset_size - 1)
    )


def direct_companion_column(
    m: int,
    subset: tuple[int, ...],
    z_vectors: tuple[tuple[int, int, int], ...],
) -> dict[tuple[int, ...], int]:
    """Build one identity-block companion tensor from matching choices."""
    roots = tuple(range(m))
    entries: dict[tuple[int, ...], int] = {}
    for across_roots in combinations(roots, len(subset)):
        across_set = set(across_roots)
        for targets in permutations(subset):
            assignment = dict(zip(across_roots, targets, strict=True))
            retained = tuple(root for root in roots if root not in across_set)
            for matching in perfect_matchings(retained):
                for cross_colours in product(range(3), repeat=len(subset)):
                    word: list[int | None] = [None] * m
                    weight = 1
                    for (root, target), colour in zip(
                        assignment.items(), cross_colours, strict=True
                    ):
                        word[root] = colour
                        weight *= z_vectors[target][colour]
                    for internal_colours in product(
                        range(3), repeat=len(matching)
                    ):
                        completed = word.copy()
                        for (left, right), colour in zip(
                            matching, internal_colours, strict=True
                        ):
                            completed[left] = colour
                            completed[right] = colour
                        key = tuple(int(colour) for colour in completed)
                        entries[key] = entries.get(key, 0) + weight
    return entries


def polynomial_from_tensor(
    entries: dict[tuple[int, ...], int], variables: tuple[sp.Symbol, ...]
) -> sp.Expr:
    """Evaluate a root tensor on one repeated symbolic vector."""
    result = sp.Integer(0)
    for word, coefficient in entries.items():
        monomial = sp.Integer(coefficient)
        for colour in word:
            monomial *= variables[colour]
        result += monomial
    return sp.expand(result)


def expected_companion_polynomial(
    m: int,
    subset: tuple[int, ...],
    z_vectors: tuple[tuple[int, int, int], ...],
    variables: tuple[sp.Symbol, ...],
) -> sp.Expr:
    """Return the lambda-free right side of the symmetric formula."""
    quadratic = sum(variable**2 for variable in variables)
    result = sp.Integer(companion_scalar(m, len(subset)))
    result *= quadratic ** ((m - len(subset)) // 2)
    for target in subset:
        result *= sum(
            z_vectors[target][colour] * variables[colour]
            for colour in range(3)
        )
    return sp.expand(result)


def polynomial_rank(polynomials: list[sp.Expr], m: int) -> int:
    """Compute the exact coefficient rank of ternary degree-m forms."""
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    monomials = [
        variables[0] ** first
        * variables[1] ** second
        * variables[2] ** (m - first - second)
        for first in range(m + 1)
        for second in range(m - first + 1)
    ]
    matrix = sp.Matrix(
        [
            [sp.Poly(polynomial, *variables).coeff_monomial(monomial) for polynomial in polynomials]
            for monomial in monomials
        ]
    )
    return matrix.rank()


def assert_direct_four_root_companions() -> dict[str, int]:
    """Compare all eight direct m=4 columns with the symmetric formula."""
    m = 4
    variables = sp.symbols("x y z")
    z_vectors = tuple((1, value, value**2) for value in range(1, m + 1))
    subsets = [
        subset
        for size in range(m + 1)
        if size % 2 == m % 2
        for subset in combinations(range(m), size)
    ]
    polynomials = []
    for subset in subsets:
        entries = direct_companion_column(m, subset, z_vectors)
        actual = polynomial_from_tensor(entries, variables)
        expected = expected_companion_polynomial(
            m, subset, z_vectors, variables
        )
        assert sp.expand(actual - expected) == 0
        polynomials.append(actual)
    assert len(subsets) == 8
    assert polynomial_rank(polynomials, m) == 7
    return {"columns": len(subsets), "rank": 7}


def generic_companion_polynomials(m: int) -> list[sp.Expr]:
    """Build the symmetric columns on a deterministic Vandermonde chart."""
    variables = sp.symbols("x y z")
    z_vectors = tuple((1, value, value**2) for value in range(1, m + 1))
    return [
        expected_companion_polynomial(m, subset, z_vectors, variables)
        for size in range(m + 1)
        if size % 2 == m % 2
        for subset in combinations(range(m), size)
    ]


def assert_rank_and_divisibility() -> dict[int, int]:
    """Check the exact generic ranks and the common quadratic factor."""
    x, y, z = sp.symbols("x y z")
    quadratic = x**2 + y**2 + z**2
    ranks: dict[int, int] = {}
    for m in range(3, 7):
        polynomials = generic_companion_polynomials(m)
        assert len(polynomials) == 2 ** (m - 1)
        for polynomial in polynomials[:-1]:
            _, remainder = sp.div(polynomial, quadratic, x, y, z)
            assert sp.expand(remainder) == 0
        rank = polynomial_rank(polynomials, m)
        assert rank == comb(m, 2) + 1
        ranks[m] = rank
    assert ranks == {3: 4, 4: 7, 5: 11, 6: 16}
    return ranks


def assert_dimension_inequality() -> int:
    """Check the strict rank bound over a broad exact integer ledger."""
    checked = 0
    for m in range(4, 65):
        assert comb(m, 2) + 1 < 2 ** (m - 1)
        assert 2 ** (m - 1) - m > 0
        checked += 1
    return checked


def main() -> None:
    coefficients = assert_tensor_coefficients()
    direct = assert_direct_four_root_companions()
    ranks = assert_rank_and_divisibility()
    inequalities = assert_dimension_inequality()
    print("balanced diagonal-complete rank-drop primary checks: PASS")
    print(f"  eight-vertex coefficient ledger: {coefficients}")
    print(f"  direct four-root sensor: {direct}")
    print(f"  generic symmetric ranks: {ranks}")
    print(f"  strict dimension inequalities: {inequalities}")


if __name__ == "__main__":
    main()
