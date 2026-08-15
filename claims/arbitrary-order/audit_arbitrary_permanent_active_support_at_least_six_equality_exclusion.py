"""Independent no-import audit of the active-support >=6 exclusion.

This file intentionally does not import the primary verifier or SymPy.  It
uses a small finite-field row reducer and reconstructs all matrices directly.
"""

from __future__ import annotations

from itertools import combinations, product

PRIME = 5

Vector = tuple[int, ...]
Matrix = list[list[int]]


def rank_mod(matrix: Matrix, prime: int = PRIME) -> int:
    """Return exact row rank over F_prime without external algebra code."""
    if not matrix:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
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
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [
            entry * inverse % prime for entry in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    (left - coefficient * right) % prime
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def standard_basis(n: int) -> tuple[Vector, ...]:
    """Return the coordinate basis over F_5."""
    return tuple(
        tuple(int(index == coordinate) for coordinate in range(n))
        for index in range(n)
    )


def upper_pairs(n: int, include_diagonal: bool) -> tuple[tuple[int, int], ...]:
    """Return symmetric or square-free coordinate pairs."""
    offset = 0 if include_diagonal else 1
    return tuple(
        (first, second)
        for first in range(n)
        for second in range(first + offset, n)
    )


def restriction_rows(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
    *,
    include_diagonal: bool,
) -> Matrix:
    """Build symmetric-form restriction equations from scratch."""
    pairs = upper_pairs(len(left[0]), include_diagonal)
    rows = []
    for u in left:
        for v in right:
            row = []
            for first, second in pairs:
                value = u[first] * v[second]
                if first != second:
                    value += u[second] * v[first]
                row.append(value % PRIME)
            rows.append(row)
    return rows


def intersection_dimension(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> int:
    """Compute dim(left intersect right) over F_5."""
    combined = [list(vector) for vector in (*left, *right)]
    return 6 - rank_mod(combined)


def canonical_intersection_models(n: int) -> tuple[tuple[Vector, ...], ...]:
    """Return pairs with intersection dimensions 0,1,2,3."""
    basis = standard_basis(n)
    return (
        (*basis[0:3], *basis[3:6]),
        (*basis[0:3], basis[0], basis[3], basis[4]),
        (*basis[0:3], basis[0], basis[1], basis[3]),
        (*basis[0:3], *basis[0:3]),
    )


def audit_block_dimensions() -> tuple[tuple[int, int, int], ...]:
    """Independently recover the annihilator and residual dimension table."""
    profiles = []
    n = 7
    variable_count = n * (n + 1) // 2
    for expected_r, packed in enumerate(canonical_intersection_models(n)):
        left = packed[:3]
        right = packed[3:]
        actual_r = intersection_dimension(left, right)
        assert actual_r == expected_r

        equation_rank = rank_mod(
            restriction_rows(left, right, include_diagonal=True)
        )
        annihilator_dimension = variable_count - equation_rank
        h = 6 - expected_r
        invisible = variable_count - h * (h + 1) // 2
        residual = annihilator_dimension - invisible
        assert residual == (12, 6, 2, 0)[expected_r]
        profiles.append((actual_r, annihilator_dimension, residual))
    return tuple(profiles)


def projective_points(dimension: int) -> tuple[Vector, ...]:
    """Enumerate normalized nonzero projective points over F_5."""
    points = []
    for vector in product(range(PRIME), repeat=dimension):
        if not any(vector):
            continue
        first = next(entry for entry in vector if entry)
        inverse = pow(first, -1, PRIME)
        normalized = tuple(entry * inverse % PRIME for entry in vector)
        if normalized not in points:
            points.append(normalized)
    return tuple(points)


def symmetric_square(vector: Vector) -> list[int]:
    """Flatten v^2 in upper-triangle coordinates."""
    return [
        vector[first] * vector[second] % PRIME
        for first, second in upper_pairs(len(vector), True)
    ]


def audit_square_span() -> tuple[int, int]:
    """Exhaust every independent subfamily needed for the square-span lemma."""
    points = projective_points(3)
    assert len(points) == (PRIME**3 - 1) // (PRIME - 1) == 31
    checked = 0
    for size in (1, 2, 3):
        for family in combinations(points, size):
            vector_rank = rank_mod([list(vector) for vector in family])
            square_rank = rank_mod([symmetric_square(vector) for vector in family])
            assert square_rank >= vector_rank
            checked += 1
    return len(points), checked


def audit_case_arithmetic() -> int:
    """Check every support boundary in the arbitrary-n case split."""
    checked = 0
    for n in range(6, 41):
        for r in range(4):
            k = n - 6 + r
            diagonal_rank = n - 4 + r * (r - 1) // 2
            residual_dimension = (3 - r) * (4 - r)
            assert diagonal_rank >= k
            if r == 0:
                for support in range(k, diagonal_rank + 1):
                    quotient_rank = diagonal_rank - support
                    outside_axes = n - support
                    assert quotient_rank <= residual_dimension
                    # The projection of these axes to H/V has dimension at
                    # most quotient_rank, leaving four axes inside V.
                    assert outside_axes - quotient_rank == 4 > 3
                    checked += 1
            elif r in (1, 2):
                minimum_active_support = k + 1
                assert minimum_active_support == diagonal_rank
                quotient_rank = diagonal_rank - minimum_active_support
                outside_axes = n - minimum_active_support
                assert quotient_rank == 0
                assert outside_axes == 5 - r > r
                checked += 1
            else:
                assert residual_dimension == 0
                assert diagonal_rank == n - 1
                checked += 1
    return checked


def survivor_plane(n: int) -> tuple[Vector, ...]:
    """Build an active common plane K e0 plus a two-plane."""
    axis = standard_basis(n)[0]
    first = (0, *(1 for _ in range(n - 1)))
    second = (0, *(index % PRIME for index in range(1, n)))
    return axis, first, second


def audit_survivors() -> tuple[tuple[int, int, int, int], ...]:
    """Recompute equality and diagonal ranks over F_5 without SymPy."""
    profiles = []
    for n in range(6, 10):
        plane = survivor_plane(n)
        assert rank_mod([list(vector) for vector in plane]) == 3
        assert all(any(vector[index] for vector in plane) for index in range(n))

        full_rows = restriction_rows(plane, plane, include_diagonal=True)
        edge_rows = restriction_rows(plane, plane, include_diagonal=False)
        full_restriction_rank = rank_mod(full_rows)
        product_dimension = rank_mod(edge_rows)
        assert full_restriction_rank == 6
        assert product_dimension == 5

        full_variables = n * (n + 1) // 2
        edge_variables = n * (n - 1) // 2
        t_dimension = full_variables - full_restriction_rank
        zero_diagonal_kernel = edge_variables - product_dimension
        diagonal_rank = t_dimension - zero_diagonal_kernel
        assert diagonal_rank == n - 1
        profiles.append(
            (n, full_restriction_rank, product_dimension, diagonal_rank)
        )
    return tuple(profiles)


def audit_rank_one_locus() -> tuple[int, int]:
    """Exhaust the rank-one locus of symmetric matrices with entry 00 zero."""
    nonzero_rank_one = 0
    bad = 0
    for entries in product(range(PRIME), repeat=5):
        a01, a02, a11, a12, a22 = entries
        matrix = [
            [0, a01, a02],
            [a01, a11, a12],
            [a02, a12, a22],
        ]
        if rank_mod(matrix) != 1:
            continue
        nonzero_rank_one += 1
        if a01 or a02:
            bad += 1
    assert nonzero_rank_one > 0
    assert bad == 0
    return nonzero_rank_one, bad


def main() -> None:
    block_profiles = audit_block_dimensions()
    projective_count, square_families = audit_square_span()
    boundary_cases = audit_case_arithmetic()
    survivor_profiles = audit_survivors()
    rank_one_count, bad_rank_one = audit_rank_one_locus()

    print("active-support-at-least-six equality exclusion no-import audit: PASS")
    print(f"  F5 block profiles (r,dim T,residual): {block_profiles}")
    print(
        "  F5 projective square-span audit: "
        f"{projective_count} points, {square_families} families"
    )
    print(f"  arbitrary-n support boundary cases checked: {boundary_cases}")
    print(f"  F5 survivor profiles: {survivor_profiles}")
    print(
        "  rank-one hyperplane locus: "
        f"{rank_one_count} nonzero matrices, {bad_rank_one} bad"
    )


if __name__ == "__main__":
    main()
