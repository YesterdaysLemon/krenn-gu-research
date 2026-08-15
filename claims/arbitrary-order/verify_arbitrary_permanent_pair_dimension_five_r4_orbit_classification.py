"""Primary exact verifier for the pair-dimension-five r=4 classification.

This script replays the characteristic-zero linear algebra with SymPy.  The
classification proof itself is the accompanying theorem document; these
checks guard its normal forms, product tables, dual spaces, and orbit
invariants against transcription errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import sympy as sp

Vector = tuple[int, ...]
MatrixRows = tuple[Vector, ...]

EDGES = tuple(combinations(range(4), 2))


@dataclass(frozen=True)
class Orbit:
    """One unbased equality-five normal form."""

    name: str
    alpha: Vector
    beta: Vector
    left: MatrixRows
    right: MatrixRows
    degrees: Vector
    admissible: bool


def quadratic_product(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in the degree-two part of Z_4."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def product_table(left: MatrixRows, right: MatrixRows) -> tuple[MatrixRows, ...]:
    """Return the 3 by 3 table of quadratic coefficient vectors."""
    return tuple(
        tuple(quadratic_product(left_colour, right_colour) for right_colour in right)
        for left_colour in left
    )


def vector_rank(vectors: list[Vector] | tuple[Vector, ...]) -> int:
    """Return the exact row rank of a vector family."""
    return int(sp.Matrix(vectors).rank()) if vectors else 0


def flatten_table(table: tuple[MatrixRows, ...]) -> list[Vector]:
    """Flatten a product table in row-major colour order."""
    return [table[row][column] for row in range(3) for column in range(3)]


def proportional(left: Vector, right: Vector) -> bool:
    """Check exact projective equality for two nonzero vectors."""
    matrix = sp.Matrix([left, right])
    return matrix.rank() == 1


def assert_hyperplane_basis(basis: MatrixRows, normal: Vector) -> None:
    """Check that three vectors are a basis of the stated hyperplane."""
    assert vector_rank(basis) == 3
    assert all(sum(a * b for a, b in zip(row, normal, strict=True)) == 0 for row in basis)


def annihilator(table: tuple[MatrixRows, ...]) -> Vector:
    """Return the normalized unique annihilator of an equality-five table."""
    kernel = sp.Matrix(flatten_table(table)).nullspace()
    assert len(kernel) == 1
    column = kernel[0]
    denominator = sp.ilcm(*(value.q for value in column))
    entries = [int(value * denominator) for value in column]
    common = sp.igcd(*entries)
    entries = [value // common for value in entries]
    first = next(value for value in entries if value)
    if first < 0:
        entries = [-value for value in entries]
    return tuple(entries)


def graph_degrees(edge_vector: Vector) -> Vector:
    """Return the sorted support-graph degree multiset."""
    degrees = [0, 0, 0, 0]
    for value, (first, second) in zip(edge_vector, EDGES, strict=True):
        if value:
            degrees[first] += 1
            degrees[second] += 1
    return tuple(sorted(degrees, reverse=True))


def dual_space(table: tuple[MatrixRows, ...]) -> list[sp.Matrix]:
    """Return the six edge-coordinate bilinear matrices spanning L."""
    return [
        sp.Matrix(3, 3, lambda row, column: table[row][column][edge])
        for edge in range(6)
    ]


def flatten_matrix(matrix: sp.Matrix) -> tuple[sp.Expr, ...]:
    """Flatten a 3 by 3 matrix in row-major order."""
    return tuple(matrix[row, column] for row in range(3) for column in range(3))


def assert_same_matrix_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> None:
    """Check equality of two exact matrix subspaces."""
    left_rows = [flatten_matrix(matrix) for matrix in left]
    right_rows = [flatten_matrix(matrix) for matrix in right]
    left_rank = sp.Matrix(left_rows).rank()
    right_rank = sp.Matrix(right_rows).rank()
    joined_rank = sp.Matrix([*left_rows, *right_rows]).rank()
    assert left_rank == right_rank == joined_rank


def matrix_unit(row: int, column: int) -> sp.Matrix:
    """Return a 3 by 3 matrix unit."""
    result = sp.zeros(3, 3)
    result[row, column] = 1
    return result


def canonical_orbits() -> tuple[Orbit, ...]:
    """Return explicit bases for all five unbased normal forms."""
    return (
        Orbit(
            "P3",
            (1, 1, 1, 0),
            (1, 1, 1, 0),
            ((-1, 1, 0, 0), (-1, 0, 1, 0), (0, 0, 0, 1)),
            ((-1, 1, 0, 0), (-1, 0, 1, 0), (0, 0, 0, 1)),
            (3, 1, 1, 1),
            False,
        ),
        Orbit(
            "(2,1)",
            (1, 1, 0, 0),
            (1, -1, 0, 0),
            ((-1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
            ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
            (1, 1, 0, 0),
            False,
        ),
        Orbit(
            "(3,1)",
            (1, 1, 1, 0),
            (1, -1, -1, 0),
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
            (2, 1, 1, 0),
            True,
        ),
        Orbit(
            "(4,1)",
            (1, 1, 1, 1),
            (1, -1, -1, -1),
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
            (3, 1, 1, 1),
            True,
        ),
        Orbit(
            "(4,2)",
            (1, 1, 1, 1),
            (1, 1, -1, -1),
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
            (2, 2, 2, 2),
            True,
        ),
    )


def assert_unbased_normal_forms() -> dict[str, Vector]:
    """Check hyperplanes, equality five, and separating graph invariants."""
    annihilators: dict[str, Vector] = {}
    for orbit in canonical_orbits():
        assert_hyperplane_basis(orbit.left, orbit.alpha)
        assert_hyperplane_basis(orbit.right, orbit.beta)
        table = product_table(orbit.left, orbit.right)
        assert vector_rank(flatten_table(table)) == 5
        kernel = annihilator(table)
        assert graph_degrees(kernel) == orbit.degrees
        annihilators[orbit.name] = kernel

    distinct_degrees = {
        orbit.degrees for orbit in canonical_orbits() if orbit.name != "P3"
    }
    assert len(distinct_degrees) == 4
    p3 = canonical_orbits()[0]
    split_41 = canonical_orbits()[3]
    assert p3.degrees == split_41.degrees
    assert proportional(p3.alpha, p3.beta)
    assert not proportional(split_41.alpha, split_41.beta)
    return annihilators


def assert_annihilator_equations() -> None:
    """Replay the square-ratio and support logic for all sign normal forms."""
    for orbit in canonical_orbits()[1:]:
        alpha = orbit.alpha
        beta = orbit.beta
        equations = [alpha[index] ** 2 - beta[index] ** 2 for index in range(4)]
        assert equations == [0, 0, 0, 0]
        assert {index for index, value in enumerate(alpha) if value} == {
            index for index, value in enumerate(beta) if value
        }
        ratios = {
            beta[index] // alpha[index]
            for index in range(4)
            if alpha[index]
        }
        assert ratios == {-1, 1}

    # In the coincident support-three case, the zero-diagonal constraints
    # 2 alpha_i z_i=0 leave exactly one free z-coordinate.
    alpha = canonical_orbits()[0].alpha
    assert sum(value == 0 for value in alpha) == 1


def assert_dual_obstructions() -> None:
    """Check the two exact dual spaces and their decisive rank-one minors."""
    p3, split_21 = canonical_orbits()[:2]

    p3_expected = [
        matrix_unit(0, 0),
        matrix_unit(0, 1) + matrix_unit(1, 0),
        matrix_unit(0, 2) + matrix_unit(2, 0),
        matrix_unit(1, 1),
        matrix_unit(1, 2) + matrix_unit(2, 1),
    ]
    assert_same_matrix_span(dual_space(product_table(p3.left, p3.right)), p3_expected)

    a, b, c, d, e = sp.symbols("a b c d e")
    p3_matrix = sp.Matrix(((a, b, c), (b, d, e), (c, e, 0)))
    assert p3_matrix.extract((0, 2), (0, 2)).det() == -c**2
    assert p3_matrix.extract((1, 2), (1, 2)).det() == -e**2

    split_expected = [
        matrix_unit(0, 1),
        matrix_unit(0, 2),
        matrix_unit(1, 0),
        matrix_unit(2, 0),
        matrix_unit(1, 2) + matrix_unit(2, 1),
    ]
    assert_same_matrix_span(
        dual_space(product_table(split_21.left, split_21.right)), split_expected
    )

    split_matrix = sp.Matrix(((0, a, b), (c, 0, e), (d, e, 0)))
    assert split_matrix.extract((1, 2), (1, 2)).det() == -e**2
    after_e_zero = split_matrix.subs(e, 0)
    decisive_minors = (
        after_e_zero.extract((0, 1), (0, 1)).det(),
        after_e_zero.extract((0, 2), (0, 1)).det(),
        after_e_zero.extract((0, 1), (0, 2)).det(),
        after_e_zero.extract((0, 2), (0, 2)).det(),
    )
    assert decisive_minors == (-a * c, -a * d, -b * c, -b * d)


def assert_admissible_frames() -> dict[str, dict[str, object]]:
    """Replay every product and direct-sum assertion in the three frames."""
    expected_tables: dict[str, tuple[MatrixRows, ...]] = {
        "(3,1)": (
            (
                (0, 0, 0, 2, 0, 0),
                (1, -1, 0, -1, 0, 0),
                (0, 0, 0, 0, 1, -1),
            ),
            (
                (0, 0, 0, 0, -1, 1),
                (0, 0, 1, 0, 1, 0),
                (0, 0, 0, 0, 0, 0),
            ),
            (
                (1, -1, 0, -1, 0, 0),
                (-1, 1, 0, 1, 0, 0),
                (0, 0, -1, 0, 0, 1),
            ),
        ),
        "(4,1)": (
            (
                (-1, 2, -1, 1, 0, 1),
                (-1, 1, 0, 1, 0, 0),
                (1, -1, 0, -1, 0, 0),
            ),
            (
                (1, -1, 0, 0, -1, 1),
                (1, 0, -1, 0, -1, 0),
                (-1, 1, 0, 0, 1, -1),
            ),
            (
                (1, -1, 0, -2, 1, -1),
                (1, -1, 0, -1, 0, 0),
                (0, 0, 0, 2, 0, 0),
            ),
        ),
        "(4,2)": (
            (
                (1, 1, 0, 0, -1, -1),
                (0, 1, -1, 0, 0, -1),
                (0, 1, -1, 0, 0, -1),
            ),
            (
                (0, 0, 0, 1, -1, -1),
                (1, 0, -1, 1, 0, -1),
                (0, 0, 0, 1, -1, -1),
            ),
            (
                (0, 0, 0, 1, -1, -1),
                (0, 1, -1, 0, 0, -1),
                (0, 0, 0, 0, 0, -2),
            ),
        ),
    }

    summaries: dict[str, dict[str, object]] = {}
    for orbit in canonical_orbits():
        if not orbit.admissible:
            continue
        table = product_table(orbit.left, orbit.right)
        assert table == expected_tables[orbit.name]
        mixed = [
            table[row][column]
            for row in range(3)
            for column in range(3)
            if row != column
        ]
        diagonal = [table[index][index] for index in range(3)]
        assert vector_rank(mixed) == 2
        assert vector_rank(flatten_table(table)) == 5
        assert vector_rank([*mixed, *diagonal]) == 5
        summaries[orbit.name] = {
            "mixed_rank": 2,
            "product_rank": 5,
            "annihilator": annihilator(table),
        }
    return summaries


def main() -> None:
    """Run all primary exact checks."""
    annihilators = assert_unbased_normal_forms()
    assert_annihilator_equations()
    assert_dual_obstructions()
    admissible = assert_admissible_frames()

    print("PASS: exact r=4 pair-dimension-five orbit classification")
    print("unbased_orbits=P3,(2,1),(3,1),(4,1),(4,2)")
    print("delta_admissible=(3,1),(4,1),(4,2)")
    print(f"annihilators={annihilators}")
    print(f"admissible_frame_checks={admissible}")


if __name__ == "__main__":
    main()
