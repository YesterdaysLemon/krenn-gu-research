"""Independent F3 audit of the active-support-five equality exclusion.

This script deliberately imports neither SymPy nor the primary verifier.  It
enumerates the complete Grassmannian Gr(3,5)(F3), checks every ordered pair
with full union support, and then audits the classified equality locus by
direct modular linear algebra.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product

Vector = tuple[int, ...]
Plane = tuple[Vector, ...]

FIELD = range(3)
EDGES = tuple(combinations(range(5), 2))
FULL_SUPPORT = (1 << 5) - 1
EXPECTED_EQUALITY_CENSUS_SHA256 = (
    "971fbb787f554b9d12d844dc5551aafdeb49a3d1bfaba1ba36a2ee4c98e25901"
)


def rank_mod_three(rows: object, stop_after: int | None = None) -> int:
    """Compute matrix rank over F3 by an independent incremental RREF."""
    pivots: dict[int, Vector] = {}
    for source in rows:  # type: ignore[union-attr]
        row = [int(value) % 3 for value in source]
        for column in sorted(pivots):
            multiplier = row[column]
            if multiplier:
                pivot_row = pivots[column]
                row = [
                    (value - multiplier * pivot_value) % 3
                    for value, pivot_value in zip(row, pivot_row, strict=True)
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        inverse = row[pivot]
        row = [(inverse * value) % 3 for value in row]
        for column, old_pivot in tuple(pivots.items()):
            multiplier = old_pivot[pivot]
            if multiplier:
                pivots[column] = tuple(
                    (value - multiplier * pivot_value) % 3
                    for value, pivot_value in zip(old_pivot, row, strict=True)
                )
        pivots[pivot] = tuple(row)
        if stop_after is not None and len(pivots) > stop_after:
            return len(pivots)
    return len(pivots)


def grassmannian_three_five() -> tuple[Plane, ...]:
    """Generate every RREF representative of Gr(3,5)(F3)."""
    planes = []
    for pivots in combinations(range(5), 3):
        free_positions = tuple(
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in range(pivot + 1, 5)
            if column not in pivots
        )
        for values in product(FIELD, repeat=len(free_positions)):
            matrix = [[0] * 5 for _ in range(3)]
            for row, pivot in enumerate(pivots):
                matrix[row][pivot] = 1
            for value, (row, column) in zip(
                values,
                free_positions,
                strict=True,
            ):
                matrix[row][column] = value
            planes.append(tuple(tuple(row) for row in matrix))
    assert len(planes) == 1210
    assert len(set(planes)) == 1210
    return tuple(planes)


def support_mask(plane: Plane) -> int:
    """Return the union of coordinate supports of a plane basis."""
    return sum(
        1 << coordinate
        for coordinate in range(5)
        if any(row[coordinate] for row in plane)
    )


def square_free_product(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in the square-free algebra over F3."""
    return tuple(
        (left[first] * right[second] + left[second] * right[first]) % 3
        for first, second in EDGES
    )


def row_space(plane: Plane) -> dict[Vector, Vector]:
    """Map each vector in a plane to one local coefficient tuple."""
    result = {}
    for coefficients in product(FIELD, repeat=3):
        vector = tuple(
            sum(coefficients[row] * plane[row][column] for row in range(3)) % 3
            for column in range(5)
        )
        result[vector] = coefficients
    assert len(result) == 27
    return result


def basis_of_vectors(vectors: object, dimension: int) -> tuple[Vector, ...]:
    """Select an independent basis from vectors over F3."""
    basis: list[Vector] = []
    for vector in vectors:  # type: ignore[union-attr]
        if not any(vector):
            continue
        if rank_mod_three((*basis, vector)) > len(basis):
            basis.append(vector)
            if len(basis) == dimension:
                break
    assert len(basis) == dimension
    return tuple(basis)


def projective_plane_points() -> tuple[Vector, ...]:
    """Return normalized representatives of P^2(F3)."""
    points = []
    for first_nonzero in range(3):
        for tail in product(FIELD, repeat=2 - first_nonzero):
            points.append((0,) * first_nonzero + (1,) + tail)
    assert len(points) == 13
    return tuple(points)


def outer(left: Vector, right: Vector) -> Vector:
    """Flatten a rank-one three-by-three matrix."""
    return tuple((x * y) % 3 for x in left for y in right)


def dot(left: Vector, right: Vector) -> int:
    """Evaluate one local covector over F3."""
    return sum(x * y for x, y in zip(left, right, strict=True)) % 3


def multiplication_dual_columns(
    plane: Plane,
    product_table: dict[tuple[Vector, Vector], Vector],
) -> tuple[Vector, ...]:
    """Return ten spanning columns for Im(mu*) in local tensor coordinates."""
    ordered_products = tuple(
        product_table[(left, right)] for left in plane for right in plane
    )
    return tuple(
        tuple(ordered_products[row][column] for row in range(9))
        for column in range(10)
    )


def audit_equality_plane(
    plane: Plane,
    product_table: dict[tuple[Vector, Vector], Vector],
    projective_points: tuple[Vector, ...],
) -> int:
    """Check the coordinate-axis normal form and rank-one obstruction."""
    space = row_space(plane)
    axes = []
    for coordinate in range(5):
        axis = tuple(int(index == coordinate) for index in range(5))
        if axis in space:
            axes.append((coordinate, space[axis]))
    assert len(axes) == 1
    axis_coordinate, axis_coefficients = axes[0]

    w_space = tuple(
        vector for vector in space if vector[axis_coordinate] == 0
    )
    assert len(w_space) == 9
    w_basis = basis_of_vectors(w_space, 2)
    w_support = support_mask(w_basis)
    assert w_support == FULL_SUPPORT ^ (1 << axis_coordinate)
    w_products = (
        square_free_product(w_basis[0], w_basis[0]),
        square_free_product(w_basis[0], w_basis[1]),
        square_free_product(w_basis[1], w_basis[1]),
    )
    assert rank_mod_three(w_products) == 3

    dual_columns = multiplication_dual_columns(plane, product_table)
    dual_basis = basis_of_vectors(dual_columns, 5)
    assert rank_mod_three(dual_basis) == 5
    rank_one = []
    for left in projective_points:
        for right in projective_points:
            tensor = outer(left, right)
            if rank_mod_three((*dual_basis, tensor)) == 5:
                rank_one.append((left, right))
    assert len(rank_one) == 4
    assert all(dot(left, axis_coefficients) == 0 for left, _ in rank_one)
    assert all(dot(right, axis_coefficients) == 0 for _, right in rank_one)
    for selected in combinations(rank_one, 3):
        assert rank_mod_three(left for left, _ in selected) < 3
        assert rank_mod_three(right for _, right in selected) < 3
    return len(rank_one)


def main() -> None:
    planes = grassmannian_three_five()
    supports = tuple(support_mask(plane) for plane in planes)
    projective_vectors = sorted({row for plane in planes for row in plane})
    assert len(projective_vectors) == 65
    product_table = {
        (left, right): square_free_product(left, right)
        for left in projective_vectors
        for right in projective_vectors
    }

    equality_pairs: list[tuple[int, int]] = []
    full_union_pairs = 0
    for left_index, left in enumerate(planes):
        for right_index, right in enumerate(planes):
            if supports[left_index] | supports[right_index] != FULL_SUPPORT:
                continue
            full_union_pairs += 1
            generators = (
                product_table[(u, v)] for u in left for v in right
            )
            if rank_mod_three(generators, stop_after=5) == 5:
                equality_pairs.append((left_index, right_index))

    assert len(equality_pairs) == 340
    assert all(left == right for left, right in equality_pairs)
    equality_indices = tuple(left for left, _ in equality_pairs)
    assert len(set(equality_indices)) == 340
    assert all(supports[index] == FULL_SUPPORT for index in equality_indices)

    projective_points = projective_plane_points()
    rank_one_counts = tuple(
        audit_equality_plane(planes[index], product_table, projective_points)
        for index in equality_indices
    )
    assert rank_one_counts == (4,) * 340

    payload = ";".join(
        ",".join("".join(map(str, row)) for row in planes[index])
        for index in equality_indices
    )
    digest = sha256(payload.encode("ascii")).hexdigest()
    assert digest == EXPECTED_EQUALITY_CENSUS_SHA256

    print("active-support-five equality exclusion independent F3 audit: PASS")
    print(f"  Grassmannian size: {len(planes)}")
    print(f"  ordered pairs checked: {len(planes) ** 2}")
    print(f"  full-union-support ordered pairs: {full_union_pairs}")
    print(f"  equality-five ordered pairs: {len(equality_pairs)}")
    print("  all equality-five pairs have U=V and individual support five")
    print("  every equality plane contains exactly one coordinate axis")
    print("  every complementary W has dim(W^2)=3")
    print("  every dual rank-one locus has four projective F3 points")
    print("  no equality pair passes the independent-factor criterion")
    print(f"  equality-plane census SHA-256: {digest}")
    print("  finite-field census is audit evidence, not the char!=2 proof")


if __name__ == "__main__":
    main()
