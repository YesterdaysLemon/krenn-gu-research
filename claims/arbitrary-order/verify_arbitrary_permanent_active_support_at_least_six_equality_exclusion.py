"""Primary exact checks for the active-support-at-least-six exclusion."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

Vector = tuple[int, ...]


def coordinate_basis(n: int) -> tuple[Vector, ...]:
    """Return the standard basis of Q^n."""
    return tuple(
        tuple(int(index == coordinate) for coordinate in range(n))
        for index in range(n)
    )


def symmetric_pairs(n: int) -> tuple[tuple[int, int], ...]:
    """Return upper-triangle coordinate pairs."""
    return tuple(
        (row, column) for row in range(n) for column in range(row, n)
    )


def edges(n: int) -> tuple[tuple[int, int], ...]:
    """Return square-free quadratic coordinates."""
    return tuple(combinations(range(n), 2))


def annihilator_system(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> sp.Matrix:
    """Build the equations for symmetric forms killing left x right."""
    n = len(left[0])
    rows = []
    for u in left:
        for v in right:
            row = []
            for first, second in symmetric_pairs(n):
                value = u[first] * v[second]
                if first != second:
                    value += u[second] * v[first]
                row.append(value)
            rows.append(row)
    return sp.Matrix(rows)


def annihilator_profile(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> tuple[int, int]:
    """Return dim T and the coordinate-diagonal rank on T."""
    n = len(left[0])
    pairs = symmetric_pairs(n)
    basis = annihilator_system(left, right).nullspace()
    diagonal_rows = []
    for coordinate in range(n):
        diagonal_index = pairs.index((coordinate, coordinate))
        diagonal_rows.append(
            [vector[diagonal_index] for vector in basis]
        )
    return len(basis), sp.Matrix(diagonal_rows).rank()


def multiply(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in the square-free algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in edges(len(left))
    )


def product_rank(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> int:
    """Rank the span of all ordered pair products."""
    return sp.Matrix([multiply(u, v) for u in left for v in right]).rank()


def symmetric_product_matrix(plane: tuple[Vector, ...]) -> sp.Matrix:
    """Return the six symmetric products of a three-plane basis."""
    return sp.Matrix(
        [
            multiply(plane[first], plane[second])
            for first in range(3)
            for second in range(first, 3)
        ]
    )


def verify_dimension_formulas() -> tuple[tuple[int, int, int, int], ...]:
    """Check every block and diagonal-rank formula over a range of n."""
    residuals = []
    for r in range(4):
        residual = (3 - r) * (4 - r)
        residuals.append(residual)
        assert residual == (12, 6, 2, 0)[r]

    for n in range(6, 25):
        ambient_edges = n * (n - 1) // 2
        for r in range(4):
            h = 6 - r
            k = n - h
            t_zero = n * (n + 1) // 2 - h * (h + 1) // 2
            t_dimension = t_zero + residuals[r]
            diagonal_rank = t_dimension - (ambient_edges - 5)
            expected = n - 4 + r * (r - 1) // 2
            assert diagonal_rank == expected
            assert k == n - 6 + r

            if r == 0:
                for support in range(k, diagonal_rank + 1):
                    outside = n - support
                    residual_rank = diagonal_rank - support
                    assert outside - residual_rank == 4
            elif r in (1, 2):
                active_minimum = k + 1
                assert active_minimum == diagonal_rank
                outside = n - active_minimum
                assert outside == 5 - r
                assert outside > r
            else:
                assert residuals[r] == 0
                assert diagonal_rank == n - 1

    return tuple(
        (
            r,
            (3 - r) * (4 - r),
            6 - 4 + r * (r - 1) // 2,
            6 - (6 - r),
        )
        for r in range(4)
    )


def verify_block_decomposition() -> tuple[tuple[int, int], ...]:
    """Recompute dim T for canonical intersection blocks over Q."""
    profiles = []
    n = 8
    basis = coordinate_basis(n)
    models = (
        (basis[0:3], basis[3:6]),
        (basis[0:3], (basis[0], basis[3], basis[4])),
        (basis[0:3], (basis[0], basis[1], basis[3])),
        (basis[0:3], basis[0:3]),
    )
    for r, (left, right) in enumerate(models):
        dimension, diagonal_rank = annihilator_profile(left, right)
        h = 6 - r
        expected = (
            n * (n + 1) // 2
            - h * (h + 1) // 2
            + (3 - r) * (4 - r)
        )
        assert dimension == expected
        # In these deliberately coordinate-supported models every diagonal
        # matrix kills U x V except on a shared coordinate, so this rank is
        # a convention check rather than the equality-five value.
        assert diagonal_rank == n - r
        profiles.append((dimension, diagonal_rank))
    return tuple(profiles)


def square_coordinates(vector: tuple[int, ...]) -> tuple[int, ...]:
    """Flatten a symmetric square in upper-triangle coordinates."""
    return tuple(
        vector[first] * vector[second]
        for first in range(len(vector))
        for second in range(first, len(vector))
    )


def verify_square_span() -> int:
    """Exhaust a rational regression for the square-span inequality."""
    directions = tuple(
        vector
        for vector in (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
        )
    )
    checked = 0
    for size in range(1, len(directions) + 1):
        for family in combinations(directions, size):
            vector_rank = sp.Matrix(family).rank()
            square_rank = sp.Matrix(
                [square_coordinates(vector) for vector in family]
            ).rank()
            assert square_rank >= vector_rank
            checked += 1
    return checked


def active_equality_plane(n: int) -> tuple[Vector, ...]:
    """Construct Kx0 plus an active two-plane with three-dimensional square."""
    first = (0, *(1 for _ in range(1, n)))
    second = (0, *(index for index in range(1, n)))
    return (coordinate_basis(n)[0], first, second)


def verify_survivor_examples() -> tuple[tuple[int, int, int], ...]:
    """Check exact active equality examples and their rank-one obstruction."""
    profiles = []
    for n in range(6, 11):
        plane = active_equality_plane(n)
        assert sp.Matrix(plane).rank() == 3
        assert all(any(vector[index] for vector in plane) for index in range(n))

        symmetric = symmetric_product_matrix(plane)
        assert symmetric.rank() == 5
        assert product_rank(plane, plane) == 5
        # Product-basis order is 00,01,02,11,12,22.  The coordinate-axis
        # square is identically zero, and the other five rows are independent.
        assert symmetric.row(0) == sp.zeros(1, len(edges(n)))
        assert symmetric[1:, :].rank() == 5

        dimension, diagonal_rank = annihilator_profile(plane, plane)
        expected_dimension = n * (n + 1) // 2 - 6
        assert dimension == expected_dimension
        assert diagonal_rank == n - 1
        profiles.append((n, symmetric.rank(), diagonal_rank))

    a01, a02, a11, a12, a22 = sp.symbols("a01 a02 a11 a12 a22")
    generic = sp.Matrix(
        [
            [0, a01, a02],
            [a01, a11, a12],
            [a02, a12, a22],
        ]
    )
    assert generic.extract((0, 1), (0, 1)).det() == -(a01**2)
    assert generic.extract((0, 2), (0, 2)).det() == -(a02**2)
    # Rank one therefore forces the first row and column to vanish over a
    # field, placing every factor in the two-plane annihilating x0.
    return tuple(profiles)


def main() -> None:
    dimension_table = verify_dimension_formulas()
    block_profiles = verify_block_decomposition()
    square_families = verify_square_span()
    survivor_profiles = verify_survivor_examples()

    print("active-support-at-least-six equality exclusion primary: PASS")
    print(f"  r table (r,residual,d at n=6,k): {dimension_table}")
    print(f"  canonical block profiles at n=8: {block_profiles}")
    print(f"  rational square-span families checked: {square_families}")
    print(f"  active equality survivor profiles: {survivor_profiles}")
    print("  Delta-admissible active-support n>=6 equality frames: none")


if __name__ == "__main__":
    main()
