"""Primary exact checks for the active-support-five equality exclusion."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

Vector = tuple[int, ...]

EDGES = tuple(combinations(range(5), 2))
SYMMETRIC_PAIRS = tuple(
    (row, column) for row in range(5) for column in range(row, 5)
)


def symmetric_matrix(coordinates: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Build a symmetric five-by-five matrix from upper-triangle entries."""
    result = sp.zeros(5)
    for value, (row, column) in zip(
        coordinates,
        SYMMETRIC_PAIRS,
        strict=True,
    ):
        result[row, column] = value
        result[column, row] = value
    return result


def annihilator_equations(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> sp.Matrix:
    """Return the linear system for symmetric forms killing left x right."""
    rows = []
    for u in left:
        for v in right:
            row = []
            for first, second in SYMMETRIC_PAIRS:
                value = u[first] * v[second]
                if first != second:
                    value += u[second] * v[first]
                row.append(value)
            rows.append(row)
    return sp.Matrix(rows)


def annihilator_basis(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> tuple[sp.Matrix, ...]:
    """Compute a basis of S(left,right) in symmetric-matrix coordinates."""
    equations = annihilator_equations(left, right)
    return tuple(symmetric_matrix(tuple(vector)) for vector in equations.nullspace())


def diagonal_rank(basis: tuple[sp.Matrix, ...]) -> int:
    """Rank the coordinate-diagonal map on a symmetric-form basis."""
    return sp.Matrix(
        [[matrix[index, index] for matrix in basis] for index in range(5)]
    ).rank()


def symmetrized_product(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in the square-free algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def symmetric_products(basis: tuple[Vector, ...]) -> sp.Matrix:
    """Return the six symmetric products of a three-plane basis."""
    return sp.Matrix(
        [
            symmetrized_product(basis[first], basis[second])
            for first in range(3)
            for second in range(first, 3)
        ]
    )


def tensor_products(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> sp.Matrix:
    """Return the nine ordered products for the pair multiplication map."""
    return sp.Matrix(
        [symmetrized_product(u, v) for u in left for v in right]
    )


def flattened(matrix: sp.Matrix) -> sp.Matrix:
    """Flatten a three-by-three matrix in row-major tensor coordinates."""
    return sp.Matrix([matrix[row, column] for row in range(3) for column in range(3)])


def verify_intersection_blocks() -> tuple[int, int, int, int]:
    """Check the r=1 and r=2 block-annihilator and diagonal calculations."""
    e = tuple(
        tuple(int(index == coordinate) for coordinate in range(5))
        for index in range(5)
    )

    # r=1: E=R+A+C, U=R+A, V=R+C.  The six free entries are
    # precisely the two symmetric two-by-two diagonal blocks.
    left_one = (e[0], e[1], e[2])
    right_one = (e[0], e[3], e[4])
    basis_one = annihilator_basis(left_one, right_one)
    assert len(basis_one) == 6
    assert diagonal_rank(basis_one) == 4
    a_squares = sp.Matrix([[1, 0, 0], [0, 0, 1]])
    assert a_squares.rank() == 2

    # r=2 with c=(1,1,0,0,0): the c symmetric-tensor E* block has
    # diagonal rank two.  The two residual squares make the full diagonal
    # rank larger than two in this active-support representative.
    common = (e[2], e[3])
    left_two = (*common, (1, -1, 0, 0, 0))
    right_two = (*common, e[4])
    basis_two = annihilator_basis(left_two, right_two)
    assert len(basis_two) == 7
    assert diagonal_rank(basis_two) == 3

    c = sp.Matrix([1, 1, 0, 0, 0])
    c_block = []
    for index in range(5):
        coordinate = sp.eye(5).col(index)
        c_block.append(c * coordinate.T + coordinate * c.T)
    assert sp.Matrix(
        [[matrix[index, index] for matrix in c_block] for index in range(5)]
    ).rank() == 2

    # If both residual square diagonals stayed in those first two
    # coordinates, c, alpha, beta would all be supported there.  Their
    # common kernel would contain e2,e3,e4 and have dimension at least
    # three, contradicting the required two-dimensional intersection.
    c_alpha_beta = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
        ]
    )
    outside_axes = sp.eye(5)[:, 2:]
    assert c_alpha_beta * outside_axes == sp.zeros(3, 3)
    assert c_alpha_beta.rank() == 2
    assert outside_axes.rank() == 3

    return len(basis_one), diagonal_rank(basis_one), len(basis_two), diagonal_rank(
        basis_two
    )


def verify_relation_rank_lemmas() -> tuple[int, int]:
    """Replay the rank-three and rank-two orthogonality obstructions."""
    # A vector orthogonal to a nondegenerate orthogonal basis is zero.
    q_three = sp.diag(2, 3, 5)
    extra = sp.Matrix(sp.symbols("z0:3"))
    equations = sp.Matrix([(sp.eye(3).col(i).T * q_three * extra)[0] for i in range(3)])
    assert sp.solve(tuple(equations), tuple(extra), dict=True) == [
        {extra[0]: 0, extra[1]: 0, extra[2]: 0}
    ]

    # In rank two, take two independent quotient vectors and three nonzero
    # radical multiples.  All pairwise off-diagonal conditions leave the
    # two independent diagonal tensors diag(a,b,0).
    coordinate_forms = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 0, 2),
        (0, 0, 3),
    )
    pairs = tuple((i, j) for i in range(3) for j in range(i, 3))
    rows = []
    for first, second in combinations(coordinate_forms, 2):
        row = []
        for i, j in pairs:
            value = first[i] * second[j]
            if i != j:
                value += first[j] * second[i]
            row.append(value)
        rows.append(row)
    relation_space = sp.Matrix(rows).nullspace()
    assert len(relation_space) == 2
    assert {tuple(vector) for vector in relation_space} == {
        (1, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0),
    }
    return q_three.rank(), len(relation_space)


def verify_exact_example() -> tuple[int, int, int, int]:
    """Check the displayed rational equality pair and its dual obstruction."""
    plane: tuple[Vector, ...] = (
        (1, 0, 0, 0, -1),
        (0, 1, 1, 0, 1),
        (0, 0, 0, 1, 0),
    )
    assert sp.Matrix(plane).rank() == 3
    assert all(any(vector[index] for vector in plane) for index in range(5))

    symmetric = symmetric_products(plane)
    assert symmetric.rank() == 5
    kernel = symmetric.T.nullspace()
    assert len(kernel) == 1
    assert tuple(kernel[0]) == (0, 0, 0, 0, 0, 1)

    w_plane = plane[:2]
    w_products = sp.Matrix(
        [
            symmetrized_product(w_plane[0], w_plane[0]),
            symmetrized_product(w_plane[0], w_plane[1]),
            symmetrized_product(w_plane[1], w_plane[1]),
        ]
    )
    assert w_products.rank() == 3
    assert all(any(vector[index] for vector in w_plane) for index in (0, 1, 2, 4))
    assert all(vector[3] == 0 for vector in w_plane)

    ordered = tensor_products(plane, plane)
    assert ordered.rank() == 5
    dual_image = sp.Matrix.hstack(*ordered.columnspace())
    symmetric_zero_axis = (
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    )
    expected = sp.Matrix.hstack(*(flattened(matrix) for matrix in symmetric_zero_axis))
    assert dual_image.rank() == expected.rank() == 5
    assert dual_image.row_join(expected).rank() == 5

    a00, a01, a02, a11, a12 = sp.symbols("a00 a01 a02 a11 a12")
    generic = sp.Matrix(
        [
            [a00, a01, a02],
            [a01, a11, a12],
            [a02, a12, 0],
        ]
    )
    assert generic.extract((0, 2), (0, 2)).det() == -(a02**2)
    assert generic.extract((1, 2), (1, 2)).det() == -(a12**2)
    # Thus rank one forces a02=a12=0 over a field.  Every factor covector
    # annihilates the third basis vector x3, so all factors span at most two.

    return symmetric.rank(), w_products.rank(), ordered.rank(), expected.rank()


def main() -> None:
    block_profile = verify_intersection_blocks()
    relation_profile = verify_relation_rank_lemmas()
    example_profile = verify_exact_example()

    print("active-support-five equality exclusion primary checks: PASS")
    print(
        "  annihilator/diagonal profiles "
        f"(r=1,r=2): {(block_profile[:2], block_profile[2:])}"
    )
    print(
        "  relation-rank obstruction profile "
        f"(nondegenerate rank, rank-two relation dimension): {relation_profile}"
    )
    print(
        "  exact Q example ranks "
        f"(U^2,W^2,U tensor U,dual): {example_profile}"
    )
    print("  rank-one dual factors all annihilate the coordinate-axis summand")
    print("  field scope of theorem: characteristic not two")


if __name__ == "__main__":
    main()
