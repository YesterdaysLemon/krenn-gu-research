"""Primary exact checks for the common-quadratic rank-drop exclusion."""

from __future__ import annotations

from functools import cache
from itertools import combinations, product
from math import comb, factorial

import sympy as sp


@cache
def odd_double_factorial(value: int) -> int:
    """Return value!! for odd value at least -1."""
    if value <= 0:
        return 1
    return value * odd_double_factorial(value - 2)


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield all labelled perfect matchings recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def matching_coefficient(word: tuple[int, ...]) -> int:
    """Count identity-form matchings compatible with a coordinate word."""
    return sum(
        all(word[left] == word[right] for left, right in matching)
        for matching in perfect_matchings(tuple(range(len(word))))
    )


def coefficient_formula(word: tuple[int, ...]) -> int:
    """Evaluate the colour-parity double-factorial formula."""
    counts = tuple(word.count(colour) for colour in range(3))
    if any(count % 2 for count in counts):
        return 0
    result = 1
    for count in counts:
        result *= odd_double_factorial(count - 1)
    return result


def assert_coefficient_formula() -> dict[str, int]:
    """Compare the formula with every six-vertex coordinate word."""
    checked = 0
    for word in product(range(3), repeat=6):
        assert matching_coefficient(word) == coefficient_formula(word)
        checked += 1
    return {"words": checked, "matchings": odd_double_factorial(5)}


def wick_two_flattening(m: int) -> sp.Matrix:
    """Build the exact 2|(2m-2) coordinate flattening from the formula."""
    right_words = tuple(product(range(3), repeat=2 * m - 2))
    left_words = tuple(product(range(3), repeat=2))
    return sp.Matrix(
        [
            [coefficient_formula(left + right) for right in right_words]
            for left in left_words
        ]
    )


def ghz_two_flattening(m: int) -> sp.Matrix:
    """Build the corresponding ternary GHZ flattening."""
    right_words = tuple(product(range(3), repeat=2 * m - 2))
    left_words = tuple(product(range(3), repeat=2))
    return sp.Matrix(
        [
            [
                int(len(set(left + right)) == 1)
                for right in right_words
            ]
            for left in left_words
        ]
    )


def selected_right_words(m: int) -> tuple[tuple[int, ...], ...]:
    """Return the six right words used in the written rank certificate."""
    pure = tuple((colour,) * (2 * m - 2) for colour in range(3))
    mixed = []
    for left, right in combinations(range(3), 2):
        remaining = 3 - left - right
        mixed.append((left, right) + (remaining,) * (2 * m - 4))
    return pure + tuple(mixed)


def assert_flattening_ranks() -> dict[int, tuple[int, int, int]]:
    """Check full and displayed-column ranks at bounded exact orders."""
    ranks: dict[int, tuple[int, int, int]] = {}
    left_words = tuple(product(range(3), repeat=2))
    for m in range(2, 5):
        wick = wick_two_flattening(m)
        ghz = ghz_two_flattening(m)
        chosen = sp.Matrix(
            [
                [
                    coefficient_formula(left + right)
                    for right in selected_right_words(m)
                ]
                for left in left_words
            ]
        )
        assert wick.rank() == 6
        assert chosen.rank() == 6
        assert ghz.rank() == 3
        ranks[m] = (wick.rank(), chosen.rank(), ghz.rank())

    for m in range(2, 18):
        a_value = odd_double_factorial(2 * m - 1)
        b_value = odd_double_factorial(2 * m - 3)
        diagonal_certificate = sp.Matrix(
            [
                [a_value if row == column else b_value for column in range(3)]
                for row in range(3)
            ]
        )
        assert diagonal_certificate.det() == (
            (2 * m - 2) ** 2
            * (2 * m + 1)
            * b_value**3
        )
        assert diagonal_certificate.det() != 0
    return ranks


def monomials_of_degree(m: int, variables: tuple[sp.Symbol, ...]):
    """List ternary monomials of total degree m."""
    x, y, z = variables
    return tuple(
        x**first * y**second * z ** (m - first - second)
        for first in range(m + 1)
        for second in range(m - first + 1)
    )


def companion_scalar(m: int, subset_size: int) -> int:
    """Return the repeated-root companion multiplicity."""
    return (
        comb(m, subset_size)
        * factorial(subset_size)
        * odd_double_factorial(m - subset_size - 1)
    )


def companion_polynomials(m: int) -> list[sp.Expr]:
    """Build uniform-form companion diagonals on a deterministic chart."""
    variables = sp.symbols("x y z")
    quadratic = sum(variable**2 for variable in variables)
    z_vectors = tuple((1, value, value**2) for value in range(1, m + 1))
    polynomials = []
    for size in range(m + 1):
        if size % 2 != m % 2:
            continue
        for subset in combinations(range(m), size):
            polynomial = sp.Integer(companion_scalar(m, size))
            polynomial *= quadratic ** ((m - size) // 2)
            for target in subset:
                polynomial *= sum(
                    z_vectors[target][colour] * variables[colour]
                    for colour in range(3)
                )
            polynomials.append(sp.expand(polynomial))
    return polynomials


def polynomial_rank(polynomials: list[sp.Expr], m: int) -> int:
    """Return coefficient rank in Sym^m of the ternary space."""
    variables = sp.symbols("x y z")
    monomials = monomials_of_degree(m, variables)
    matrix = sp.Matrix(
        [
            [
                sp.Poly(polynomial, *variables).coeff_monomial(monomial)
                for polynomial in polynomials
            ]
            for monomial in monomials
        ]
    )
    return matrix.rank()


def assert_balanced_sensor_bound() -> dict[int, tuple[int, int, int]]:
    """Check the common-quadratic sensor ranks and column inequalities."""
    ledger: dict[int, tuple[int, int, int]] = {}
    x, y, z = sp.symbols("x y z")
    quadratic = x**2 + y**2 + z**2
    for m in range(3, 7):
        polynomials = companion_polynomials(m)
        columns = 2 ** (m - 1)
        bound = comb(m, 2) + 1
        assert len(polynomials) == columns
        for polynomial in polynomials[:-1]:
            _, remainder = sp.div(polynomial, quadratic, x, y, z)
            assert sp.expand(remainder) == 0
        rank = polynomial_rank(polynomials, m)
        assert rank == min(columns, bound)
        if m >= 4:
            assert rank <= bound < columns
        ledger[m] = (columns, rank, bound)
    return ledger


def assert_degenerate_local_rank() -> dict[int, int]:
    """Check one-vertex ranks for diagonal forms of ranks one through three."""
    vertices = tuple(range(6))
    rest_words = tuple(product(range(3), repeat=5))
    results: dict[int, int] = {}
    for form_rank in range(1, 4):
        matrix = []
        for first_colour in range(3):
            row = []
            for rest in rest_words:
                word = (first_colour,) + rest
                total = 0
                for matching in perfect_matchings(vertices):
                    if all(
                        word[left] == word[right] < form_rank
                        for left, right in matching
                    ):
                        total += 1
                row.append(total)
            matrix.append(row)
        rank = sp.Matrix(matrix).rank()
        assert rank == form_rank
        results[form_rank] = rank
    return results


def main() -> None:
    coefficients = assert_coefficient_formula()
    flattenings = assert_flattening_ranks()
    sensors = assert_balanced_sensor_bound()
    degenerate = assert_degenerate_local_rank()
    print("balanced common-quadratic primary checks: PASS")
    print(f"  coefficient ledger: {coefficients}")
    print(f"  (Wick, selected, GHZ) flattening ranks: {flattenings}")
    print(f"  (columns, rank, bound) sensor ledger: {sensors}")
    print(f"  degenerate one-flattening ranks: {degenerate}")


if __name__ == "__main__":
    main()
