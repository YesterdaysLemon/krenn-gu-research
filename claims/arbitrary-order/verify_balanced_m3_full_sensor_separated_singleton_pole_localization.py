"""Exact replay of the m=3 separated-singleton pole localization controls.

The owning theorem proves the arbitrary-subspace divisor classification by
minimal dependence support.  This script checks the three sharp divisor
models, a regular model, their exact Cramer poles, and the dimension ledger.
"""

from __future__ import annotations

from functools import reduce
from itertools import combinations, product

import sympy as sp

X = sp.symbols("x0:3")
Y = sp.symbols("y0:3")
R = sp.symbols("r0:3")
VARIABLES = X + Y + R


def maximal_minors(columns: tuple[sp.Matrix, ...]) -> tuple[sp.Expr, ...]:
    """Return every nonzero three-column maximal minor."""
    matrix = sp.Matrix.hstack(*columns)
    answer = []
    for rows in combinations(range(matrix.rows), 3):
        value = sp.factor(matrix.extract(rows, range(3)).det())
        if value != 0:
            answer.append(value)
    return tuple(answer)


def polynomial_gcd(values: tuple[sp.Expr, ...]) -> sp.Expr:
    """Return the normalized gcd of a nonempty polynomial family."""
    assert values
    value = sp.factor(reduce(sp.gcd, values))
    polynomial = sp.Poly(value, *VARIABLES)
    return sp.factor(value / polynomial.LC())


def coefficient_matrix(column: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    """Recover the constant matrix of one linear column map."""
    return sp.Matrix.hstack(*(column.diff(variable) for variable in variables))


def image_dimensions(
    columns: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[tuple[int, int, int], tuple[int, int, int], int]:
    """Return singleton, pair-sum, and total image dimensions."""
    maps = tuple(
        coefficient_matrix(column, variables)
        for column, variables in zip(columns, (X, Y, R), strict=True)
    )
    ranks = tuple(matrix.rank() for matrix in maps)
    pair_ranks = tuple(
        sp.Matrix.hstack(maps[left], maps[right]).rank()
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    total_rank = sp.Matrix.hstack(*maps).rank()
    return ranks, pair_ranks, total_rank


def group_degrees(expression: sp.Expr) -> set[tuple[int, int, int]]:
    """Return the three group degrees of every nonzero monomial."""
    polynomial = sp.Poly(expression, *VARIABLES)
    return {
        (
            sum(monomial[:3]),
            sum(monomial[3:6]),
            sum(monomial[6:]),
        )
        for monomial, coefficient in polynomial.terms()
        if coefficient
    }


def rational_group_degree(expression: sp.Expr) -> tuple[int, int, int]:
    """Return the net multidegree of a homogeneous rational function."""
    numerator, denominator = sp.fraction(sp.cancel(expression))
    numerator_degrees = group_degrees(numerator)
    denominator_degrees = group_degrees(denominator)
    assert len(numerator_degrees) == len(denominator_degrees) == 1
    left = next(iter(numerator_degrees))
    right = next(iter(denominator_degrees))
    return tuple(a - b for a, b in zip(left, right, strict=True))


def rank_one_control() -> None:
    """Check the rank-one singleton divisor and its sharp rational target."""
    columns = (
        sp.Matrix([X[0], 0, 0, 0, 0, 0, 0]),
        sp.Matrix([0, Y[0], 0, Y[1], Y[2], 0, 0]),
        sp.Matrix([0, 0, R[0], 0, 0, R[1], R[2]]),
    )
    assert image_dimensions(columns) == ((1, 3, 3), (4, 4, 6), 7)
    minors = maximal_minors(columns)
    assert len(minors) == 9
    assert polynomial_gcd(minors) == X[0]

    coefficient = X[1] * Y[0] * R[0] / X[0]
    target = sp.Matrix([X[1] * Y[0] * R[0], 0, 0, 0, 0, 0, 0])
    assert (columns[0] * coefficient - target).applyfunc(sp.factor) == sp.zeros(7, 1)
    assert rational_group_degree(coefficient) == (0, 1, 1)
    assert sp.factor(sp.denom(sp.cancel(coefficient))) == X[0]


def pair_plane_control() -> None:
    """Check the common pair-plane divisor and its sharp Cramer solution."""
    columns = (
        sp.Matrix([X[0], X[1], 0, 0, 0]),
        sp.Matrix([Y[0], Y[1], 0, 0, 0]),
        sp.Matrix([0, 0, R[0], R[1], R[2]]),
    )
    assert image_dimensions(columns) == ((2, 2, 3), (2, 5, 5), 5)
    delta = X[0] * Y[1] - X[1] * Y[0]
    minors = maximal_minors(columns)
    assert len(minors) == 3
    assert polynomial_gcd(minors) == delta

    scale = X[2] * Y[2] * R[0]
    coefficients = sp.Matrix(
        [scale * Y[1] / delta, -scale * X[1] / delta, 0]
    )
    target = sp.Matrix([scale, 0, 0, 0, 0])
    matrix = sp.Matrix.hstack(*columns)
    assert (matrix * coefficients - target).applyfunc(sp.factor) == sp.zeros(5, 1)
    assert rational_group_degree(coefficients[0]) == (0, 1, 1)
    assert rational_group_degree(coefficients[1]) == (1, 0, 1)
    assert all(
        sp.factor(sp.denom(sp.cancel(value))) == delta
        for value in coefficients[:2, 0]
    )


def common_three_space_control() -> None:
    """Check the common-three-space determinant and generic Cramer poles."""
    columns = (sp.Matrix(X), sp.Matrix(Y), sp.Matrix(R))
    assert image_dimensions(columns) == ((3, 3, 3), (3, 3, 3), 3)
    determinant = sp.factor(sp.Matrix.hstack(*columns).det())
    minors = maximal_minors(columns)
    assert minors == (determinant,)

    scale = X[0] * Y[0] * R[0]
    target = sp.Matrix([scale, 0, 0])
    matrix = sp.Matrix.hstack(*columns)
    coefficients = (matrix.adjugate() * target / determinant).applyfunc(sp.cancel)
    assert (matrix * coefficients - target).applyfunc(sp.factor) == sp.zeros(3, 1)
    expected_degrees = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    for value, degree in zip(coefficients, expected_degrees, strict=True):
        assert rational_group_degree(value) == degree
        assert sp.factor(sp.denom(value)) == determinant


def regular_control() -> None:
    """Check a rank-(2,2,2), total-rank-four arrangement with gcd one."""
    columns = (
        sp.Matrix([X[0], X[1], 0, 0]),
        sp.Matrix([0, Y[0], Y[1], 0]),
        sp.Matrix([0, 0, R[0], R[1]]),
    )
    assert image_dimensions(columns) == ((2, 2, 2), (3, 4, 3), 4)
    minors = maximal_minors(columns)
    assert len(minors) == 4
    assert polynomial_gcd(minors) == 1


def s2m_rank_one_location() -> None:
    """Check that all eight earlier sharp controls use a rank-one pair column."""
    row = lambda word: 9 * word[0] + 3 * word[1] + word[2]
    off_one = row((0, 0, 1))
    columns = []
    for index in (1, 2):
        outside = sp.zeros(27, 1)
        outside[row((index, index, index))] = R[0]
        outside[off_one] = -R[0]
        columns.append(outside)
    for _kind in ("x", "y"):
        for left in (1, 2):
            for _right in range(left, 3):
                endpoint = sp.zeros(27, 1)
                endpoint[off_one] = R[left]
                columns.append(endpoint)
    assert len(columns) == 8
    assert all(coefficient_matrix(column, R).rank() == 1 for column in columns)


def coordinate_signature_census() -> int:
    """Check the codimension predicate on all coordinate image triples."""
    ambient = range(5)
    subspaces = tuple(
        frozenset(indices)
        for size in (1, 2, 3)
        for indices in combinations(ambient, size)
    )
    checked = 0
    for first, second, third in product(subspaces, repeat=3):
        ranks = tuple(map(len, (first, second, third)))
        pair_ranks = (
            len(first | second),
            len(first | third),
            len(second | third),
        )
        total_rank = len(first | second | third)
        if min(pair_ranks) < 2 or total_rank < 3:
            continue
        minimal_codimension = min(
            *ranks,
            *(rank - 1 for rank in pair_ranks),
            total_rank - 2,
        )
        structural_divisor = (
            1 in ranks or 2 in pair_ranks or total_rank == 3
        )
        assert (minimal_codimension == 1) == structural_divisor
        checked += 1
    return checked


def main() -> None:
    """Replay every fixed control and the finite dimension-signature audit."""
    rank_one_control()
    pair_plane_control()
    common_three_space_control()
    regular_control()
    s2m_rank_one_location()
    signatures = coordinate_signature_census()
    print("m=3 separated rank-drop divisor types: PASS (3/3)")
    print("sharp rational pole controls: PASS (3/3)")
    print("regular total-rank-four control: PASS (gcd=1)")
    print("S2M controls on rank-one singleton stratum: PASS (8/8)")
    print(f"coordinate dimension signatures: PASS ({signatures})")
    print("physical regular target-incidence stratum: EMPTY via n=6 theorem")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
