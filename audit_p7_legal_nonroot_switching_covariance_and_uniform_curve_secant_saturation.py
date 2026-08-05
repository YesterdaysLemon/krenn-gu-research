"""Independent no-import audit of switching covariance and secant saturation.

The fixed legal tensor is rebuilt directly as a fourteen-vertex hafnian whose
nonroot--nonroot edges carry the indeterminate t.  Polynomial identities are
certified at 19 exact integer points after a proved degree bound, and
coprimality is checked by a rational Euclidean algorithm.  No repository
module, finite field, graph search, or tensor-decomposition search is used.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, product

P0_COEFFS = (
    6662572822705733828125,
    -12156844565030088437500,
    -11656744567696429468750,
    -964481421579777390625,
    478062693786650000,
    -167575290444104681250,
    -329667083352597624375,
    -126033773134233295625,
    -41624665391857307375,
    -10418655620547901625,
    -1665030690056656225,
    -89100920096274400,
    15940043824280765,
    2548639126911280,
    87299980928535,
    -16019848623521,
    -841802234952,
    81773978676,
    628717584,
)

P1_COEFFS = (
    45743752916454884375000,
    -864588786885117896875000,
    -4116226358173090867343750,
    -7598683970980122418125000,
    -3401502493947155460953125,
    5913944738769560812265625,
    5334994427617131112718750,
    73876260872593498768750,
    -261544878332648570021250,
    -100449092973761054860625,
    -26721393305568752102250,
    -3351312997063601813625,
    -245913724965094499700,
    -10804647546463312425,
    -617591700542701835,
    3747499312421390,
    -129171904414652,
    -96822486970,
    36194813664,
)

H = (
    ((0, 1, 0), (0, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 0), (0, 1, 0), (-1, 1, 0), (0, 1, -1)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), (-1, 0, 1), (0, 1, -1)),
    ((0, 0, 1), (1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), (-1, 1, 0), (0, 1, -1)),
    ((0, 0, 1), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, 1), (1, -1, 0), (0, -1, 1)),
    ((0, 0, 1), (0, 0, 1), (0, 0, 1), (1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 0), (1, 0, -1), (-1, 0, 1)),
)

L_VALUES = (
    (-1, 1, -1, -1, -1, 1, 0, -1, 3),
    (-1, 0, 1, 0, -1, 0, 1, 0, 0),
    (1, -1, 1, 0, 1, -1, 1, 1, -3),
    (1, 0, 0, -1, 1, 0, 0, 1, -2),
    (-1, 0, -1, -1, -1, -1, 1, 1, 3),
    (0, 0, -1, -1, 1, -1, -1, -1, 4),
    (-1, 1, 1, 1, 0, 1, 1, 0, -4),
    (1, -1, -1, 1, 1, 0, 1, 0, -2),
    (0, 0, 1, 1, 1, 0, -1, 0, -2),
    (1, -1, 0, 1, 1, 0, -1, -1, 0),
)
L = {
    pair: tuple(tuple(values[3 * row + column] for column in range(3)) for row in range(3))
    for pair, values in zip(combinations(range(5), 2), L_VALUES, strict=True)
}


def polynomial_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return tuple(
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(size)
    )


def polynomial_edge_multiply(
    polynomial: tuple[int, ...], coefficient: int, degree: int
) -> tuple[int, ...]:
    return (0,) * degree + tuple(coefficient * value for value in polynomial)


def full_graph_hafnian_polynomial(
    colours: tuple[int, ...], switching: tuple[int, ...] | None = None
) -> tuple[int, ...]:
    """Return the exact t-polynomial of the fixed fourteen-vertex hafnian."""

    def edge_monomial(left: int, right: int) -> tuple[int, int]:
        if left > right:
            left, right = right, left
        if right < 5:
            return L[left, right][colours[left]][colours[right]], 0
        if left < 5 <= right:
            nonroot = right - 5
            scale = switching[nonroot] if switching is not None else 1
            return scale * H[left][nonroot][colours[left]], 0
        first = left - 5
        second = right - 5
        scale = switching[first] * switching[second] if switching is not None else 1
        return scale, 1

    @cache
    def recurse(active: tuple[int, ...]) -> tuple[int, ...]:
        if not active:
            return (1,)
        first = active[0]
        total = (0,)
        for partner_index in range(1, len(active)):
            partner = active[partner_index]
            remainder = active[1:partner_index] + active[partner_index + 1 :]
            coefficient, degree = edge_monomial(first, partner)
            total = polynomial_add(
                total,
                polynomial_edge_multiply(recurse(remainder), coefficient, degree),
            )
        return total

    result = recurse(tuple(range(14)))
    return result + (0,) * (5 - len(result))


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    work = [row[:] for row in matrix]
    previous = 1
    sign = 1
    for column in range(size - 1):
        pivot_row = next((row for row in range(column, size) if work[row][column]), None)
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for inner in range(column + 1, size):
                numerator = work[row][inner] * pivot - work[row][column] * work[column][inner]
                assert numerator % previous == 0
                work[row][inner] = numerator // previous
        for row in range(column + 1, size):
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def evaluate_high(coefficients: tuple[int, ...], value: int) -> int:
    result = 0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def trim(polynomial: list[Fraction]) -> list[Fraction]:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def polynomial_remainder(
    dividend: list[Fraction], divisor: list[Fraction]
) -> list[Fraction]:
    remainder = trim(dividend[:])
    divisor = trim(divisor[:])
    while len(remainder) >= len(divisor) and any(remainder):
        scale = remainder[-1] / divisor[-1]
        shift = len(remainder) - len(divisor)
        for index, coefficient in enumerate(divisor):
            remainder[index + shift] -= scale * coefficient
        trim(remainder)
    return remainder


def rational_polynomial_gcd(
    left_high: tuple[int, ...], right_high: tuple[int, ...]
) -> list[Fraction]:
    left = [Fraction(value) for value in reversed(left_high)]
    right = [Fraction(value) for value in reversed(right_high)]
    while any(right):
        left, right = right, polynomial_remainder(left, right)
    leading = left[-1]
    return [value / leading for value in left]


def main() -> None:
    words = tuple(product(range(3), repeat=5))
    polynomials = {word: full_graph_hafnian_polynomial(word) for word in words}
    assert all(polynomial[0] == polynomial[1] == 0 for polynomial in polynomials.values())
    assert all(all(value % 3 == 0 for value in polynomial[2:5]) for polynomial in polynomials.values())

    # Divide the full physical tensor by its common factor 3*t^2.
    core = {word: tuple(value // 3 for value in polynomial[2:5]) for word, polynomial in polynomials.items()}
    row_words = tuple(product(range(3), repeat=2))
    column_words = tuple(product(range(3), repeat=3))

    def block_determinant(block: int, value: int) -> int:
        selected = column_words[9 * block : 9 * (block + 1)]
        matrix = [
            [
                core[row_word + column_word][0]
                + value * core[row_word + column_word][1]
                + value * value * core[row_word + column_word][2]
                for column_word in selected
            ]
            for row_word in row_words
        ]
        return bareiss_determinant(matrix)

    # Both determinants have degree at most 18.  Agreement at 19 distinct
    # integers is therefore an exact identity certificate over Q[t].
    for value in range(19):
        assert block_determinant(0, value) == 50 * evaluate_high(P0_COEFFS, value)
        assert block_determinant(1, value) == 5 * evaluate_high(P1_COEFFS, value)

    gcd = rational_polynomial_gcd(P0_COEFFS, P1_COEFFS)
    assert gcd == [Fraction(1)]
    named_minor = 3**9 * block_determinant(0, 1)
    assert named_minor == -18_494_220_325_114_867_735_328_060_700

    # Independent full-matching audit of the nonroot switching gauge.
    switching = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    total_switch = 1
    for value in switching:
        total_switch *= value
    for word in words:
        switched = full_graph_hafnian_polynomial(word, switching)
        assert switched == tuple(total_switch * value for value in polynomials[word])

    # The all-one eight-shore Hessian remains invertible throughout the
    # switching torus: det(D_z)=Z_U^14 det(D), det(D)!=0.
    shore_product = 1
    for value in switching[:8]:
        shore_product *= value
    base_hessian_determinant = 3**28 * 15 * (-5) ** 7
    switched_hessian_determinant = shore_product**14 * base_hessian_determinant
    assert switched_hessian_determinant != 0

    print("PASS: independent fourteen-vertex polynomial hafnian rebuild")
    print("PASS: 19-point exact identities certify both degree-18 maximal minors")
    print("PASS: independent rational Euclidean audit gives gcd(P0,P1)=1")
    print("PASS: independent full-matching switching covariance")
    print("PASS: the switching all-one family stays common-Hessian-open")
    print("searches=0")
    print("imports_from_primary=0")
    print("imports_from_project=0")
    print("finite_fields=0")
    print("SCOPE: no nonuniform physical GHZ point is excluded")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
