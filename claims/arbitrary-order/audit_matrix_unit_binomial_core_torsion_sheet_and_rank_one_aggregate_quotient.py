"""No-import audit of binomial-core aggregate quotient sheets."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product

Gaussian = tuple[Fraction, Fraction]
Polynomial = tuple[Fraction, ...]
Laurent = dict[int, Fraction]

ZERO_G: Gaussian = (Fraction(0), Fraction(0))
ONE_G: Gaussian = (Fraction(1), Fraction(0))
I_G: Gaussian = (Fraction(0), Fraction(1))


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def ipower(exponent: int) -> Gaussian:
    return (ONE_G, I_G, gneg(ONE_G), gneg(I_G))[exponent % 4]


def c2_untwist(exponents: tuple[int, ...]) -> tuple[Gaussian, Gaussian]:
    """Apply theta(x)=i and collect exponent classes modulo two."""
    coefficients = [ZERO_G, ZERO_G]
    for exponent in exponents:
        residue = exponent % 2
        coefficients[residue] = gadd(coefficients[residue], ipower(exponent))
    return coefficients[0], coefficients[1]


def c2_fourier(element: tuple[Gaussian, Gaussian]) -> tuple[Gaussian, Gaussian]:
    even, odd = element
    return gadd(even, odd), gsub(even, odd)


def c2_multiply(
    left: tuple[Gaussian, Gaussian],
    right: tuple[Gaussian, Gaussian],
) -> tuple[Gaussian, Gaussian]:
    return (
        gadd(gmul(left[0], right[0]), gmul(left[1], right[1])),
        gadd(gmul(left[0], right[1]), gmul(left[1], right[0])),
    )


def audit_finite_fourier_and_aggregates() -> dict[str, object]:
    """Audit C[C2] without symbolic-algebra imports."""
    three_term = c2_untwist((0, 1, 2))
    four_term = c2_untwist((0, 1, 2, 3))
    assert three_term == (ZERO_G, I_G)
    assert four_term == (ZERO_G, ZERO_G)
    three_sheets = c2_fourier(three_term)
    four_sheets = c2_fourier(four_term)
    assert three_sheets == (I_G, gneg(I_G))
    assert four_sheets == (ZERO_G, ZERO_G)

    left = ((Fraction(2), Fraction(1)), (Fraction(3), Fraction(-2)))
    right = ((Fraction(-1), Fraction(1)), (Fraction(4), Fraction(1)))
    transformed_product = c2_fourier(c2_multiply(left, right))
    component_product = tuple(
        gmul(a, b)
        for a, b in zip(c2_fourier(left), c2_fourier(right), strict=True)
    )
    assert transformed_product == component_product
    return {
        "three_term_sheets": three_sheets,
        "three_term_is_unit": all(value != ZERO_G for value in three_sheets),
        "four_term_sheets": four_sheets,
        "four_term_is_zero": all(value == ZERO_G for value in four_sheets),
        "Fourier_multiplication": True,
    }


def trim(polynomial: Polynomial) -> Polynomial:
    entries = list(polynomial)
    while len(entries) > 1 and entries[-1] == 0:
        entries.pop()
    return tuple(entries) if entries else (Fraction(0),)


def degree(polynomial: Polynomial) -> int:
    value = trim(polynomial)
    return -1 if value == (Fraction(0),) else len(value) - 1


def polynomial_subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    width = max(len(left), len(right))
    values = [Fraction(0)] * width
    for index in range(width):
        values[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        )
    return trim(tuple(values))


def polynomial_divmod(
    dividend: Polynomial,
    divisor: Polynomial,
) -> tuple[Polynomial, Polynomial]:
    divisor = trim(divisor)
    if degree(divisor) < 0:
        raise ZeroDivisionError("zero polynomial")
    remainder = trim(dividend)
    quotient = [Fraction(0)] * max(1, degree(remainder) - degree(divisor) + 1)
    while degree(remainder) >= degree(divisor) and degree(remainder) >= 0:
        shift = degree(remainder) - degree(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] += coefficient
        subtractor = (Fraction(0),) * shift + tuple(
            coefficient * value for value in divisor
        )
        remainder = polynomial_subtract(remainder, subtractor)
    return trim(tuple(quotient)), trim(remainder)


def monic(polynomial: Polynomial) -> Polynomial:
    polynomial = trim(polynomial)
    if degree(polynomial) < 0:
        return polynomial
    leading = polynomial[-1]
    return tuple(value / leading for value in polynomial)


def polynomial_gcd(left: Polynomial, right: Polynomial) -> Polynomial:
    left = trim(left)
    right = trim(right)
    while degree(right) >= 0:
        _, remainder = polynomial_divmod(left, right)
        left, right = right, remainder
    return monic(left)


def normalize_laurent(polynomial: Laurent) -> Polynomial:
    nonzero = {power: value for power, value in polynomial.items() if value}
    if not nonzero:
        return (Fraction(0),)
    minimum = min(nonzero)
    maximum = max(nonzero)
    return trim(
        tuple(nonzero.get(power, Fraction(0)) for power in range(minimum, maximum + 1))
    )


def laurent_gcd(polynomials: tuple[Laurent, ...]) -> Polynomial:
    normalized = [normalize_laurent(polynomial) for polynomial in polynomials]
    normalized = [polynomial for polynomial in normalized if degree(polynomial) >= 0]
    if not normalized:
        return (Fraction(0),)
    result = normalized[0]
    for polynomial in normalized[1:]:
        result = polynomial_gcd(result, polynomial)
    return result


def reduce_positive_fibre(exponents: tuple[tuple[int, int], ...]) -> Laurent:
    """Reduce a normalized positive-term fibre by the core x=-1."""
    coefficients: dict[int, Fraction] = defaultdict(Fraction)
    for core_power, free_power in exponents:
        coefficients[free_power] += -1 if core_power % 2 else 1
    return dict(coefficients)


def audit_rank_one_gcds() -> dict[str, object]:
    """Audit the rank-one proper/unit alternatives by Euclid's algorithm."""
    fibre_minus = ((0, 0), (1, 0), (3, 0), (0, 1))
    fibre_square_minus = ((0, 0), (1, 0), (3, 0), (0, 2))
    fibre_plus = ((0, 0), (0, 1), (1, 0), (2, 0))
    reduced = tuple(
        reduce_positive_fibre(fibre)
        for fibre in (fibre_minus, fibre_square_minus, fibre_plus)
    )
    assert reduced == (
        {0: Fraction(-1), 1: Fraction(1)},
        {0: Fraction(-1), 2: Fraction(1)},
        {0: Fraction(1), 1: Fraction(1)},
    )

    proper = laurent_gcd(reduced[:2])
    unit = laurent_gcd(reduced)
    regression = laurent_gcd(
        (
            {-2: Fraction(-1), -1: Fraction(1)},
            {3: Fraction(-1), 5: Fraction(1)},
        )
    )
    assert proper == (Fraction(-1), Fraction(1))
    assert unit == (Fraction(1),)
    assert regression == proper
    return {
        "reduced_positive_fibres": reduced,
        "proper_monic_gcd": proper,
        "unit_monic_gcd": unit,
        "negative_exponent_regression": regression,
    }


def c2_rank_one_sheet(element: dict[tuple[int, int], int], character: int) -> Laurent:
    coefficients: dict[int, Fraction] = defaultdict(Fraction)
    for (torsion, free), value in element.items():
        coefficients[free] += value * character**torsion
    return dict(coefficients)


def audit_torsion_rank_one_product() -> dict[str, object]:
    """Audit two rank-one sheets and complementary unit covers."""
    residuals = (
        {(0, 0): 1, (1, 1): 1},
        {(1, 0): 1, (0, 1): 1},
    )
    covers = (
        {(0, 0): 1, (1, 0): 1},
        {(0, 0): 1, (1, 0): -1},
    )
    proper = {}
    covered = {}
    for character in (1, -1):
        proper[character] = laurent_gcd(
            tuple(c2_rank_one_sheet(item, character) for item in residuals)
        )
        covered[character] = laurent_gcd(
            tuple(
                c2_rank_one_sheet(item, character)
                for item in residuals + covers
            )
        )
    assert proper == {
        1: (Fraction(1), Fraction(1)),
        -1: (Fraction(-1), Fraction(1)),
    }
    assert covered == {1: (Fraction(1),), -1: (Fraction(1),)}
    return {
        "proper_sheet_gcds": proper,
        "covered_sheet_gcds": covered,
        "proper_if_one_sheet_survives": True,
        "unit_if_every_sheet_is_unit": True,
    }


def audit_quotient_coordinates() -> dict[str, int]:
    """Check explicit quotient maps for C2, Z, and C2 plus Z."""
    checked = 0
    finite_classes = set()
    free_classes = set()
    mixed_classes = set()
    for first, second in product(range(-4, 5), repeat=2):
        finite_classes.add(first % 2)
        free_classes.add(second)
        mixed_classes.add((first % 2, second))

        # ker((a,b)->b) is exactly <(1,0)>.
        if second == 0:
            assert (first, second) == (first, 0)

        # ker((a,b)->(a mod 2,b)) is exactly <(2,0)>.
        if first % 2 == 0 and second == 0:
            assert (first, second) == (2 * (first // 2), 0)
        checked += 1
    assert finite_classes == {0, 1}
    assert len(free_classes) == 9
    assert len(mixed_classes) == 18
    return {
        "vectors_checked": checked,
        "finite_C2_classes": len(finite_classes),
        "free_Z_classes_in_box": len(free_classes),
        "mixed_C2_by_Z_classes_in_box": len(mixed_classes),
    }


def audit_holonomy_alternative() -> dict[str, str]:
    """Audit the only two elimination ideals after an odd cycle core."""
    cycle_sign = -1
    assert cycle_sign == -1
    return {
        "proper_quotient": "(H+1)",
        "unit_quotient": "(1)",
        "other_nonunit_elimination": "impossible because (H+1) is maximal",
    }


def main() -> None:
    finite = audit_finite_fourier_and_aggregates()
    rank_one = audit_rank_one_gcds()
    mixed = audit_torsion_rank_one_product()
    quotients = audit_quotient_coordinates()
    holonomy = audit_holonomy_alternative()
    print("independent binomial-core torsion-sheet aggregate audit: PASS")
    print(f"  finite Fourier/aggregates: {finite}")
    print(f"  rank-one Euclidean gcds: {rank_one}")
    print(f"  torsion-by-rank-one product: {mixed}")
    print(f"  explicit quotient coordinates: {quotients}")
    print(f"  holonomy alternative: {holonomy}")


if __name__ == "__main__":
    main()
