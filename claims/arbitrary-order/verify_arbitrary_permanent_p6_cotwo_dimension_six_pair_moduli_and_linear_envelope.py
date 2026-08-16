"""Primary exact replay for the P6 dimension-six pair-moduli boundary.

The written theorem proves the open-family and orbit-dimension statements.
This bounded replay checks the named rational frame, its radical, and the
maximal linear complementary envelope.
"""

from __future__ import annotations

from itertools import combinations

from sympy import Matrix

N = 6
EDGES = tuple(combinations(range(N), 2))


def squarefree_product(left: tuple[int, ...], right: tuple[int, ...]) -> Matrix:
    """Multiply two linear forms in the square-free algebra Z_6."""

    assert len(left) == len(right) == N
    return Matrix([left[i] * right[j] + left[j] * right[i] for i, j in EDGES])


def explicit_basis() -> tuple[tuple[int, ...], ...]:
    """Return the three full-support block-pair forms from the theorem."""

    return (
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 1, 0),
        (0, 0, 1, 0, 0, 1),
    )


def verify_named_minor(products: dict[tuple[int, int], Matrix]) -> int:
    """Check the determinant-eight witness for injective Sym^2(U)."""

    column_keys = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    row_edges = ((0, 3), (1, 4), (2, 5), (0, 1), (0, 2), (1, 2))
    full = Matrix.hstack(*(products[key] for key in column_keys))
    minor = full.extract([EDGES.index(edge) for edge in row_edges], range(6))
    assert minor == Matrix.diag(2, 2, 2, 1, 1, 1)
    determinant = int(minor.det())
    assert determinant == 8
    assert full.rank() == 6
    return determinant


def verify_pair_level_frame(
    products: dict[tuple[int, int], Matrix],
) -> dict[str, int]:
    """Check the mixed radical and diagonal quotient ranks."""

    mixed = Matrix.hstack(products[(0, 1)], products[(0, 2)], products[(1, 2)])
    diagonal = Matrix.hstack(products[(0, 0)], products[(1, 1)], products[(2, 2)])
    assert mixed.rank() == 3
    assert mixed.row_join(diagonal).rank() == 6

    ordered_mixed = Matrix.hstack(
        *(products[tuple(sorted((c, d)))] for c in range(3) for d in range(3) if c != d)
    )
    assert ordered_mixed.rank() == 3
    return {
        "pair_dimension": mixed.row_join(diagonal).rank(),
        "mixed_dimension": mixed.rank(),
        "quotient_dimension": mixed.row_join(diagonal).rank() - mixed.rank(),
    }


def verify_linear_envelope(
    products: dict[tuple[int, int], Matrix],
) -> dict[str, int]:
    """Build M^perp and check the rank-three complement pairing."""

    mixed_rows = Matrix.vstack(
        products[(0, 1)].T,
        products[(0, 2)].T,
        products[(1, 2)].T,
    )
    envelope_basis = mixed_rows.nullspace()
    assert len(envelope_basis) == 12
    envelope = Matrix.hstack(*envelope_basis)
    assert envelope.shape == (15, 12)
    assert mixed_rows * envelope == Matrix.zeros(3, 12)

    pair_rows = Matrix.vstack(
        products[(0, 1)].T,
        products[(0, 2)].T,
        products[(1, 2)].T,
        products[(0, 0)].T,
        products[(1, 1)].T,
        products[(2, 2)].T,
    )
    restricted = pair_rows * envelope
    assert restricted[:3, :] == Matrix.zeros(3, 12)
    assert restricted.rank() == 3
    assert restricted[3:, :].rank() == 3
    return {
        "ambient_degree_two_dimension": len(EDGES),
        "linear_envelope_dimension": len(envelope_basis),
        "restricted_pairing_rank": restricted.rank(),
        "dimension_sum": 6 + len(envelope_basis),
    }


def verify_geometry_arithmetic() -> dict[str, int]:
    """Audit the Grassmann and effective monomial-group dimensions."""

    grassmann_dimension = 3 * (6 - 3)
    effective_monomial_dimension = 6 - 1
    orbit_codimension = grassmann_dimension - effective_monomial_dimension
    assert grassmann_dimension == 9
    assert effective_monomial_dimension == 5
    assert orbit_codimension == 4
    return {
        "grassmann_open_dimension": grassmann_dimension,
        "max_monomial_orbit_dimension": effective_monomial_dimension,
        "minimum_orbit_codimension": orbit_codimension,
    }


def main() -> None:
    """Run the exact bounded replay."""

    basis = explicit_basis()
    assert len(basis) == 3
    assert Matrix.hstack(*(Matrix(vector) for vector in basis)).rank() == 3
    assert {
        index for vector in basis for index, value in enumerate(vector) if value
    } == set(range(6))

    products = {
        (c, d): squarefree_product(basis[c], basis[d])
        for c in range(3)
        for d in range(c, 3)
    }
    determinant = verify_named_minor(products)
    pair = verify_pair_level_frame(products)
    envelope = verify_linear_envelope(products)
    geometry = verify_geometry_arithmetic()

    assert envelope["dimension_sum"] == 18
    print("P6 co-two dimension-six pair-moduli primary: PASS")
    print(f"  named Sym^2 minor determinant: {determinant}")
    print(f"  pair-level dimensions: {pair}")
    print(f"  maximal linear envelope: {envelope}")
    print(f"  orbit-dimension boundary: {geometry}")
    print("  four-mode product factorization: NOT CLAIMED")
    print("  simultaneous fifteen-pair incidence: OPEN")
    print("  unrestricted P6 -> Delta_3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
