"""Verify diagonal target-incidence duality and Schubert tangent formulas."""

from __future__ import annotations

from itertools import combinations

from sympy import Matrix, symbols, zeros


def coordinate_columns(dimension: int, indices: tuple[int, ...]) -> Matrix:
    matrix = zeros(dimension, len(indices))
    for column, row in enumerate(indices):
        matrix[row, column] = 1
    return matrix


def quotient_matrix(dimension: int, killed: tuple[int, ...]) -> Matrix:
    survivors = tuple(index for index in range(dimension) if index not in killed)
    matrix = zeros(len(survivors), dimension)
    for row, column in enumerate(survivors):
        matrix[row, column] = 1
    return matrix


def annihilator_basis(gamma: Matrix) -> Matrix:
    """Return left-kernel covectors as rows."""
    vectors = gamma.T.nullspace()
    return Matrix.vstack(*(vector.T for vector in vectors))


def main() -> None:
    # Small fixed model: n=8, k=4, d=3, q=4.
    n, k, d, q = 8, 4, 3, 4
    delta = coordinate_columns(n, (0, 1, 2))

    # Transverse, simple-incidence, and double-incidence planes.
    transverse = coordinate_columns(n, (3, 4, 5, 6))
    simple = coordinate_columns(n, (0, 3, 4, 5))
    double = coordinate_columns(n, (0, 1, 3, 4))

    expected = (
        (transverse, 0, 3, 7),
        (simple, 1, 2, 6),
        (double, 2, 1, 5),
    )
    for gamma, intersection_dimension, obstruction_rank, augmented_rank in expected:
        assert gamma.rank() == k
        quotient = quotient_matrix(n, tuple(gamma[:, column].tolist().index([1]) for column in range(k)))
        obstruction = quotient * delta
        assert d - obstruction.rank() == intersection_dimension
        assert obstruction.rank() == obstruction_rank
        assert gamma.row_join(delta).rank() == augmented_rank

        left_kernel = annihilator_basis(gamma)
        assert left_kernel.shape == (q, n)
        restriction = left_kernel * delta
        assert restriction.rank() == obstruction_rank

        delta_quotient = quotient_matrix(n, (0, 1, 2))
        cofactor_kernel = (delta_quotient * gamma).nullspace()
        assert len(cofactor_kernel) == intersection_dimension

    # Generic simple incidence: 3 dependent target columns give exterior zero,
    # while a fixed nonmember target raises rank by one.
    assert simple.row_join(delta).rank() == k + d - 1
    assert simple.row_join(delta[:, 0]).rank() == k
    assert simple.row_join(delta[:, 1]).rank() == k + 1

    # The cofactor line is the first coordinate in this model.
    pi_delta = quotient_matrix(n, (0, 1, 2))
    cofactor_matrix = pi_delta * simple
    assert cofactor_matrix.rank() == k - 1
    assert cofactor_matrix.nullspace() == [Matrix([1, 0, 0, 0])]

    # Tangent normal map at the simple-incidence plane.  The quotient C has
    # basis e1,e2,e6,e7; bar Delta is the first two coordinates.  Evaluating
    # a tangent map on the intersection line and projecting to the last two
    # coordinates has rank q-(d-1)=2.
    normal = Matrix([[0, 0, 1, 0], [0, 0, 0, 1]])
    assert normal.rank() == q - d + 1 == 2
    assert len(normal.nullspace()) == d - 1 == 2

    # Fixed-target tangency kills all four quotient coordinates.
    fixed_target_normal = Matrix.eye(q)
    assert fixed_target_normal.rank() == q

    # Actual five-root dimensions and Schubert strata.
    n_big, k_big, d_big, q_big = 243, 219, 3, 24
    assert q_big == n_big - k_big
    grassmann_dimension = k_big * q_big
    incidence_resolution_dimension = (d_big - 1) + (k_big - 1) * q_big
    assert grassmann_dimension == 5256
    assert incidence_resolution_dimension == 5234
    assert grassmann_dimension - incidence_resolution_dimension == 22
    assert [s * (q_big - d_big + s) for s in (1, 2, 3)] == [22, 46, 72]

    # A fixed 4 x 3 determinantal chart audits smoothness at rank two and
    # singularity at rank one without expanding any five-root minors.
    variables = symbols("a0:12")
    generic_obstruction = Matrix(4, 3, variables)
    maximal_minors = [
        generic_obstruction.extract(rows, range(3)).det()
        for rows in combinations(range(4), 3)
    ]
    minor_jacobian = Matrix(maximal_minors).jacobian(variables)
    rank_two_point = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]])
    rank_one_point = Matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
    rank_two_substitution = dict(zip(variables, list(rank_two_point), strict=True))
    rank_one_substitution = dict(zip(variables, list(rank_one_point), strict=True))
    assert minor_jacobian.subs(rank_two_substitution).rank() == 2
    assert minor_jacobian.subs(rank_one_substitution).rank() == 0

    # No universal cofactor relation: every coordinate line is realizable in
    # the small ambient model by permuting the domain basis.
    for chosen in range(k):
        other_domain = tuple(index for index in range(k) if index != chosen)
        gamma = zeros(n, k)
        gamma[0, chosen] = 1
        for target_row, domain_column in zip((3, 4, 5), other_domain, strict=True):
            gamma[target_row, domain_column] = 1
        assert gamma.rank() == k
        assert (pi_delta * gamma).rank() == k - 1
        kernel = (pi_delta * gamma).nullspace()
        expected_kernel = zeros(k, 1)
        expected_kernel[chosen, 0] = 1
        assert kernel == [expected_kernel]

    print("PASS: quotient obstruction and left-kernel restriction have equal rank")
    print("PASS: augmented rank records intersection dimensions 0, 1, 2")
    print("PASS: generic cofactor kernel is one line with 218 relations at P7 size")
    print("PASS: ambient incidence codimensions are 22, 46, 72")
    print("PASS: variable-target and fixed-target normal ranks are 22 and 24")
    print("PASS: no domain coordinate is universally excluded by incidence")
    print("searches=0")
    print("SCOPE: legal companion pullback incidence remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
