"""Focused exact checks for the GLS44 nonzero-diagonal rank-four exclusion."""

from __future__ import annotations

from itertools import product

from sympy import Matrix, symbols


def outer(left: Matrix, right: Matrix) -> Matrix:
    return left * right.T


def vec(matrix: Matrix) -> Matrix:
    return Matrix(matrix).reshape(9, 1)


def span_rank(matrices: list[Matrix]) -> int:
    if not matrices:
        return 0
    return Matrix.hstack(*(vec(matrix) for matrix in matrices)).rank()


def cross_projection(matrix: Matrix, missing: int) -> Matrix:
    support = [index for index in range(3) if index != missing]
    return Matrix(
        [
            *(matrix[index, missing] for index in support),
            *(matrix[missing, index] for index in support),
        ]
    )


def check_rank_two_symbolic_cross_block() -> None:
    a00, a01, a10, a11 = symbols("a00 a01 a10 a11")
    b00, b01, b10, b11 = symbols("b00 b01 b10 b11")
    x, y = symbols("x y")
    left = Matrix([[a00, a01], [a10, a11]])
    right = Matrix([[b00, b01], [b10, b11]])
    projected = Matrix.vstack(y * left, x * right)

    left_minor = projected.extract([0, 1], [0, 1]).det().factor()
    right_minor = projected.extract([2, 3], [0, 1]).det().factor()
    assert left_minor == y**2 * left.det()
    assert right_minor == x**2 * right.det()

    left_fixture = Matrix([[1, 2], [3, 5]])
    right_fixture = Matrix([[2, -1], [1, 1]])
    assert left_fixture.det() != 0 and right_fixture.det() != 0
    for x_value, y_value in product((-2, -1, 0, 1, 2), repeat=2):
        rank = Matrix.vstack(y_value * left_fixture, x_value * right_fixture).rank()
        assert rank == (0 if x_value == y_value == 0 else 2)


def check_rank_two_incidence_fixture() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, index] for index in range(3))
    a0, a1 = e0 + e1, e0 - e1
    b0 = (e0 - e1) / 2
    b1 = (e0 + e1) / 2
    q = outer(a0, b1) + outer(a1, b0)
    assert q == outer(e0, e0) + outer(e1, e1)
    assert q.rank() == 2

    for x_missing, y_missing in product((-2, -1, 0, 1, 2), repeat=2):
        x = Matrix([1, -1, x_missing])
        y = Matrix([2, 1, y_missing])
        residual = [outer(a, y) + outer(x, b) for a, b in ((a0, b0), (a1, b1))]
        projected = Matrix.hstack(*(cross_projection(matrix, 2) for matrix in residual))
        assert projected.rank() == (0 if x_missing == y_missing == 0 else 2)


def quotient_left(matrix: Matrix, missing: int) -> Matrix:
    rows = [index for index in range(3) if index != missing]
    return matrix.extract(rows, range(3))


def selected_column(matrix: Matrix, column: int) -> Matrix:
    return matrix[:, column]


def check_rank_one_quotient_column() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, index] for index in range(3))
    quotient_basis = [e1, e2]
    b0 = symbols("b0", nonzero=True)
    b1, b2 = symbols("b1 b2")
    b = Matrix([b0, b1, b2])

    quotient_tensors = [quotient_left(outer(vector, b), 0) for vector in quotient_basis]
    column_zero = Matrix.hstack(
        *(selected_column(matrix, 0) for matrix in quotient_tensors)
    )
    assert column_zero == b0 * Matrix.eye(2)
    assert column_zero.det() == b0**2

    projected_diagonal = [
        quotient_left(outer(e1, e1), 0),
        quotient_left(outer(e2, e2), 0),
    ]
    assert all(selected_column(matrix, 0).is_zero_matrix for matrix in projected_diagonal)

    # One extra line has selected-column image of rank at most one, while a
    # residual right vector carrying the root colour gives rank two.
    for extra in (
        Matrix([[1, 2, 3], [4, 5, 6]]),
        Matrix([[0, 0, 0], [1, -1, 2]]),
    ):
        extra_column_rank = Matrix.hstack(selected_column(extra, 0)).rank()
        assert extra_column_rank <= 1
        fixture_b = Matrix([3, -1, 2])
        images = [quotient_left(outer(vector, fixture_b), 0) for vector in quotient_basis]
        image_columns = Matrix.hstack(*(selected_column(matrix, 0) for matrix in images))
        assert image_columns.rank() == 2


def check_root_factorization_profiles() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, index] for index in range(3))

    # Rank two: both residual shore spans are the support plane.
    a0, a1 = e0 + e1, e0 - e1
    diagonal = 5 * outer(e0, e0) - 7 * outer(e1, e1)
    b0 = (5 * e0 + 7 * e1) / 2
    b1 = (5 * e0 - 7 * e1) / 2
    q = outer(a0, b1) + outer(a1, b0)
    assert q == diagonal
    assert Matrix.hstack(a0, a1).rank() == Matrix.hstack(b0, b1).rank() == 2

    # Rank one: one residual shore line is the root colour.
    a0, a1 = 2 * e2, -3 * e2
    b0, b1 = e0 + 2 * e2, (e1 + 4 * e2) / 2
    q = outer(a0, b1) + outer(a1, b0)
    # Cancel off-colour entries while retaining the e2 coordinate.
    b1 = (3 * b0 + 5 * e2) / 2
    q = outer(a0, b1) + outer(a1, b0)
    assert q == 5 * outer(e2, e2)
    assert Matrix.hstack(a0, a1).rank() == 1


def check_zero_boundary_profiles() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, index] for index in range(3))
    zero = Matrix.zeros(3, 1)
    fixtures = [
        (e0, e1, zero, zero),
        (e0 + e1, 2 * (e0 + e1), e2, -2 * e2),
    ]
    for a0, a1, b0, b1 in fixtures:
        q = outer(a0, b1) + outer(a1, b0)
        assert q.is_zero_matrix


def main() -> None:
    check_rank_two_symbolic_cross_block()
    check_rank_two_incidence_fixture()
    check_rank_one_quotient_column()
    check_root_factorization_profiles()
    check_zero_boundary_profiles()
    print("GLS44 nonzero-diagonal rank-four primary checks: PASS")


if __name__ == "__main__":
    main()
