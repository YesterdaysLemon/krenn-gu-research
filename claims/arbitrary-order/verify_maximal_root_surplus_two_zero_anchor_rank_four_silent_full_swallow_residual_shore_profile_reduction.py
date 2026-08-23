"""Focused exact checks for the GLS45 silent rank-four shore reduction."""

from __future__ import annotations

from itertools import permutations

from sympy import Matrix, expand, linsolve, symbols


def outer(left: Matrix, right: Matrix) -> Matrix:
    return left * right.T


def vec(matrix: Matrix) -> Matrix:
    return Matrix(matrix).reshape(9, 1)


def span_rank(matrices: list[Matrix]) -> int:
    return Matrix.hstack(*(vec(matrix) for matrix in matrices)).rank()


def tensor_basis(left: list[Matrix], right: list[Matrix]) -> list[Matrix]:
    return [outer(a, b) for a in left for b in right]


def check_zero_deck_factorization_and_polarization() -> None:
    a = Matrix(symbols("a0:3"))
    b = Matrix(symbols("b0:3"))
    x = Matrix(symbols("x0:3"))
    y = Matrix(symbols("y0:3"))
    lambda_0, lambda_1, t = symbols("lambda_0 lambda_1 t", nonzero=True)

    residual_left = [lambda_0 * a, lambda_1 * a]
    residual_right = [t * lambda_0 * b, -t * lambda_1 * b]
    q = outer(residual_left[0], residual_right[1]) + outer(
        residual_left[1], residual_right[0]
    )
    assert q.is_zero_matrix

    m_0 = outer(residual_left[0], y) + outer(x, residual_right[0])
    m_1 = outer(residual_left[1], y) + outer(x, residual_right[1])
    left_polarized = (
        lambda_1 * m_0
        + lambda_0 * m_1
        - 2 * lambda_0 * lambda_1 * outer(a, y)
    ).applyfunc(expand)
    right_polarized = (
        lambda_1 * m_0
        - lambda_0 * m_1
        - 2 * t * lambda_0 * lambda_1 * outer(x, b)
    ).applyfunc(expand)
    assert left_polarized.is_zero_matrix
    assert right_polarized.is_zero_matrix


def check_fixed_factor_diagonal_intersection() -> None:
    e = list(Matrix.eye(3).columnspace())
    diagonal = [outer(vector, vector) for vector in e]

    # A coordinate factor meets Delta in exactly its matching coordinate line.
    for index in range(3):
        fixed = tensor_basis([e[index]], e)
        assert span_rank(fixed) == 3
        assert span_rank(diagonal + fixed) == 5

    # Two- and three-colour fixed factors have zero diagonal intersection.
    for fixed_vector in (e[0] + e[1], e[0] - 2 * e[1] + 3 * e[2]):
        fixed = tensor_basis([fixed_vector], e)
        assert span_rank(diagonal + fixed) == 6

    # A two-dimensional active residual shore already contributes six columns.
    six_space = tensor_basis([e[0], e[1]], e)
    assert span_rank(six_space) == 6


def check_dense_quotient_line_endgame() -> None:
    e = list(Matrix.eye(3).columnspace())
    diagonal = [outer(vector, vector) for vector in e]
    checked = 0
    for i, j in permutations(range(3), 2):
        y_prime = e[j]
        x_prime = e[i]
        row_excess = outer(e[i], y_prime)
        column_excess = outer(x_prime, e[j])
        assert row_excess == column_excess
        assert all(row_excess[index, index] == 0 for index in range(3))
        assert span_rank(diagonal + [row_excess]) == 4

        x_space = Matrix.hstack(e[j], x_prime)
        y_space = Matrix.hstack(e[i], y_prime)
        assert x_space.rank() == y_space.rank() == 2
        assert Matrix.hstack(e[i], *x_space.columnspace()).rank() == 2
        assert Matrix.hstack(e[j], *y_space.columnspace()).rank() == 2
        checked += 1
    assert checked == 6

    # If zero-diagonal row-i and column-j tensors agree modulo Delta, they
    # agree exactly.  Solve one fully symbolic representative.
    y_1, y_2, x_0, x_2, c, d_0, d_1, d_2 = symbols(
        "y_1 y_2 x_0 x_2 c d_0 d_1 d_2"
    )
    row = outer(e[0], Matrix([0, y_1, y_2]))
    column = outer(Matrix([x_0, 0, x_2]), e[1])
    equation = row - c * column - Matrix.diag(d_0, d_1, d_2)
    solution = linsolve(list(equation), (y_1, y_2, x_0, x_2, d_0, d_1, d_2))
    assert solution == {(c * x_0, 0, x_0, 0, 0, 0, 0)}


def check_surviving_profile_boundaries() -> None:
    e = list(Matrix.eye(3).columnspace())
    zero = Matrix.zeros(3, 1)

    # Residual-free and one-common-label profiles really do have q=0; this
    # does not assert that their complete incidence image has rank four.
    fixtures = [
        (zero, zero, zero, zero),
        (e[0] + e[2], zero, -3 * e[1] + e[2], zero),
    ]
    for a_0, a_1, b_0, b_1 in fixtures:
        q = outer(a_0, b_1) + outer(a_1, b_0)
        assert q.is_zero_matrix

    # The dense fixed-factor lower bound is sharp as an ambient subspace
    # statement: this profile has rank five, so no rank-six claim is made.
    diagonal = [outer(vector, vector) for vector in e]
    sharp = [
        *diagonal,
        *tensor_basis([e[2]], [e[0], e[2]]),
        *tensor_basis([e[0], e[1]], [e[1]]),
    ]
    assert span_rank(sharp) == 5


def main() -> None:
    check_zero_deck_factorization_and_polarization()
    check_fixed_factor_diagonal_intersection()
    check_dense_quotient_line_endgame()
    check_surviving_profile_boundaries()
    print("GLS45 silent rank-four shore-profile primary checks: PASS")


if __name__ == "__main__":
    main()
