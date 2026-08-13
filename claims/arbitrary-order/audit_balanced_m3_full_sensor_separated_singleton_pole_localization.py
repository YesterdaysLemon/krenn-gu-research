"""Independent stdlib audit of the m=3 singleton pole localization controls.

This audit imports neither SymPy, the primary verifier, nor repository code.
It builds exterior minors with a small sparse-polynomial implementation,
checks subspace dimensions by exact Fraction row reduction, and verifies the
sharp Cramer identities after clearing their displayed denominators.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import prod

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, int]
Vector = list[Polynomial]

VARIABLE_COUNT = 9
ZERO_EXPONENT = (0,) * VARIABLE_COUNT
X0, X1, X2, Y0, Y1, Y2, R0, R1, R2 = range(VARIABLE_COUNT)


def normalize(polynomial: Polynomial) -> Polynomial:
    """Remove zero coefficients from a sparse integer polynomial."""
    return {exponent: value for exponent, value in polynomial.items() if value}


def constant(value: int) -> Polynomial:
    """Return one sparse constant."""
    return {} if value == 0 else {ZERO_EXPONENT: value}


def variable(index: int) -> Polynomial:
    """Return one coordinate variable."""
    exponent = [0] * VARIABLE_COUNT
    exponent[index] = 1
    return {tuple(exponent): 1}


VARS = tuple(variable(index) for index in range(VARIABLE_COUNT))


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add sparse polynomials."""
    answer = dict(left)
    for exponent, value in right.items():
        answer[exponent] = answer.get(exponent, 0) + value
    return normalize(answer)


def negate(polynomial: Polynomial) -> Polynomial:
    """Negate a sparse polynomial."""
    return {exponent: -value for exponent, value in polynomial.items()}


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    """Subtract sparse polynomials."""
    return add(left, negate(right))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse polynomials."""
    answer: Polynomial = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            exponent = tuple(
                a + b for a, b in zip(first, second, strict=True)
            )
            answer[exponent] = answer.get(exponent, 0) + first_value * second_value
    return normalize(answer)


def product_polynomials(*values: Polynomial) -> Polynomial:
    """Multiply a finite polynomial family."""
    answer = constant(1)
    for value in values:
        answer = multiply(answer, value)
    return answer


def determinant3(matrix: list[list[Polynomial]]) -> Polynomial:
    """Return a directly expanded three-by-three determinant."""
    positive = add(
        product_polynomials(matrix[0][0], matrix[1][1], matrix[2][2]),
        add(
            product_polynomials(matrix[0][1], matrix[1][2], matrix[2][0]),
            product_polynomials(matrix[0][2], matrix[1][0], matrix[2][1]),
        ),
    )
    negative = add(
        product_polynomials(matrix[0][2], matrix[1][1], matrix[2][0]),
        add(
            product_polynomials(matrix[0][1], matrix[1][0], matrix[2][2]),
            product_polynomials(matrix[0][0], matrix[1][2], matrix[2][1]),
        ),
    )
    return subtract(positive, negative)


def maximal_minors(columns: tuple[Vector, Vector, Vector]) -> list[Polynomial]:
    """Compute every nonzero exterior coordinate of three columns."""
    answer = []
    for rows in combinations(range(len(columns[0])), 3):
        matrix = [[columns[column][row] for column in range(3)] for row in rows]
        value = determinant3(matrix)
        if value:
            answer.append(value)
    return answer


def common_monomial_factor(polynomials: list[Polynomial]) -> Exponent:
    """Return the greatest monomial dividing every term of every input."""
    exponents = [exponent for value in polynomials for exponent in value]
    assert exponents
    return tuple(min(exponent[index] for exponent in exponents) for index in range(VARIABLE_COUNT))


def scale_vector(scalar: Polynomial, vector: Vector) -> Vector:
    """Multiply every vector coordinate by a polynomial."""
    return [multiply(scalar, value) for value in vector]


def add_vectors(*vectors: Vector) -> Vector:
    """Add equally sized polynomial vectors."""
    return [
        sum_polynomials(*(vector[index] for vector in vectors))
        for index in range(len(vectors[0]))
    ]


def sum_polynomials(*values: Polynomial) -> Polynomial:
    """Add a finite polynomial family."""
    answer: Polynomial = {}
    for value in values:
        answer = add(answer, value)
    return answer


def evaluate(polynomial: Polynomial, values: tuple[int, ...]) -> int:
    """Evaluate a sparse polynomial at integer coordinates."""
    return sum(
        coefficient
        * prod(
            value**power
            for value, power in zip(values, exponent, strict=True)
        )
        for exponent, coefficient in polynomial.items()
    )


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    """Compute exact rank by independent Gauss--Jordan reduction."""
    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def subspace_dimensions(
    maps: tuple[list[list[int]], list[list[int]], list[list[int]]],
) -> tuple[tuple[int, int, int], tuple[int, int, int], int]:
    """Compute image and image-sum dimensions from constant map matrices."""
    def rank_of(selected: tuple[int, ...]) -> int:
        rows = len(maps[0])
        matrix = [
            [
                Fraction(value)
                for index in selected
                for value in maps[index][row]
            ]
            for row in range(rows)
        ]
        return matrix_rank(matrix)

    ranks = tuple(rank_of((index,)) for index in range(3))
    pair_ranks = tuple(rank_of(pair) for pair in ((0, 1), (0, 2), (1, 2)))
    return ranks, pair_ranks, rank_of((0, 1, 2))


def zero_vector(size: int) -> Vector:
    """Return a sparse-polynomial zero vector."""
    return [{} for _ in range(size)]


def rank_one_case() -> None:
    """Audit the rank-one divisor, dimensions, and cleared pole identity."""
    columns = (
        [VARS[X0], {}, {}, {}, {}, {}, {}],
        [{}, VARS[Y0], {}, VARS[Y1], VARS[Y2], {}, {}],
        [{}, {}, VARS[R0], {}, {}, VARS[R1], VARS[R2]],
    )
    maps = (
        [[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1]],
    )
    assert subspace_dimensions(maps) == ((1, 3, 3), (4, 4, 6), 7)
    minors = maximal_minors(columns)
    assert len(minors) == 9
    expected_factor = [0] * VARIABLE_COUNT
    expected_factor[X0] = 1
    assert common_monomial_factor(minors) == tuple(expected_factor)

    numerator = product_polynomials(VARS[X1], VARS[Y0], VARS[R0])
    target = [numerator] + [{} for _ in range(6)]
    cleared_left = scale_vector(numerator, columns[0])
    cleared_right = scale_vector(VARS[X0], target)
    assert cleared_left == cleared_right


def pair_plane_case() -> None:
    """Audit the pair-plane divisor and its cleared two-column solution."""
    columns = (
        [VARS[X0], VARS[X1], {}, {}, {}],
        [VARS[Y0], VARS[Y1], {}, {}, {}],
        [{}, {}, VARS[R0], VARS[R1], VARS[R2]],
    )
    maps = (
        [[1, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
    )
    assert subspace_dimensions(maps) == ((2, 2, 3), (2, 5, 5), 5)
    delta = subtract(multiply(VARS[X0], VARS[Y1]), multiply(VARS[X1], VARS[Y0]))
    minors = maximal_minors(columns)
    assert minors == [multiply(delta, VARS[index]) for index in (R0, R1, R2)]

    scale = product_polynomials(VARS[X2], VARS[Y2], VARS[R0])
    target = [scale] + [{} for _ in range(4)]
    cleared = add_vectors(
        scale_vector(multiply(scale, VARS[Y1]), columns[0]),
        scale_vector(negate(multiply(scale, VARS[X1])), columns[1]),
    )
    assert cleared == scale_vector(delta, target)


def common_three_space_case() -> None:
    """Audit the trilinear determinant and a genuine Cramer pole point."""
    columns = (
        [VARS[X0], VARS[X1], VARS[X2]],
        [VARS[Y0], VARS[Y1], VARS[Y2]],
        [VARS[R0], VARS[R1], VARS[R2]],
    )
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert subspace_dimensions((identity, identity, identity)) == (
        (3, 3, 3),
        (3, 3, 3),
        3,
    )
    determinant = maximal_minors(columns)
    assert len(determinant) == 1
    determinant = determinant[0]

    scale = product_polynomials(VARS[X0], VARS[Y0], VARS[R0])
    target = [scale, {}, {}]
    numerators: list[Polynomial] = []
    for replaced in range(3):
        replacement = tuple(
            target if index == replaced else columns[index]
            for index in range(3)
        )
        numerators.append(maximal_minors(replacement)[0])
    cleared = add_vectors(
        *(scale_vector(numerators[index], columns[index]) for index in range(3))
    )
    assert cleared == scale_vector(determinant, target)

    singular_point = (1, 1, 1, 1, 2, 1, 2, 3, 2)
    assert evaluate(determinant, singular_point) == 0
    assert any(evaluate(numerator, singular_point) != 0 for numerator in numerators)


def regular_case() -> None:
    """Audit the safe four-space arrangement and its unit monomial gcd."""
    columns = (
        [VARS[X0], VARS[X1], {}, {}],
        [{}, VARS[Y0], VARS[Y1], {}],
        [{}, {}, VARS[R0], VARS[R1]],
    )
    maps = (
        [[1, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0]],
    )
    assert subspace_dimensions(maps) == ((2, 2, 2), (3, 4, 3), 4)
    minors = maximal_minors(columns)
    assert len(minors) == 4
    assert common_monomial_factor(minors) == ZERO_EXPONENT


def s2m_rank_one_location() -> None:
    """Independently check the selected-column ranks of all eight S2M controls."""
    outside_maps = [
        [[1, 0, 0], [-1, 0, 0]],
        [[1, 0, 0], [-1, 0, 0]],
    ]
    endpoint_maps = [
        [[0, 1 if left == 1 else 0, 1 if left == 2 else 0]]
        for _kind in range(2)
        for left in (1, 1, 2)
    ]
    maps = outside_maps + endpoint_maps
    assert len(maps) == 8
    assert all(
        matrix_rank([[Fraction(value) for value in row] for row in matrix]) == 1
        for matrix in maps
    )


def coordinate_signature_census() -> int:
    """Independently exhaust coordinate-subspace dimension signatures."""
    ambient = range(5)
    subspaces = tuple(
        frozenset(indices)
        for size in (1, 2, 3)
        for indices in combinations(ambient, size)
    )
    count = 0
    for first, second, third in product(subspaces, repeat=3):
        ranks = tuple(map(len, (first, second, third)))
        pairs = (
            len(first | second),
            len(first | third),
            len(second | third),
        )
        total = len(first | second | third)
        if min(pairs) < 2 or total < 3:
            continue
        codimensions = ranks + tuple(value - 1 for value in pairs) + (total - 2,)
        predicted = min(codimensions) == 1
        named = 1 in ranks or 2 in pairs or total == 3
        assert predicted == named
        count += 1
    return count


def main() -> None:
    """Run the independent exact controls and dimension census."""
    rank_one_case()
    pair_plane_case()
    common_three_space_case()
    regular_case()
    s2m_rank_one_location()
    signatures = coordinate_signature_census()
    print("independent separated divisor audit: PASS (3/3)")
    print("independent cleared pole identities: PASS (3/3)")
    print("independent regular four-space control: PASS")
    print("independent S2M rank-one location: PASS (8/8)")
    print(f"independent coordinate signatures: PASS ({signatures})")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
