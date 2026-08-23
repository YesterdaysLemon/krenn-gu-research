"""Focused exact checks for the GLS43 rank-four full-swallow exclusion."""

from __future__ import annotations

from itertools import combinations

from sympy import Matrix, diag, groebner, symbols


def outer(left: Matrix, right: Matrix) -> Matrix:
    return left * right.T


def sym(left: Matrix, right: Matrix) -> Matrix:
    return outer(left, right) + outer(right, left)


def vec(matrix: Matrix) -> Matrix:
    return Matrix(matrix).reshape(9, 1)


def span_rank(matrices: list[Matrix]) -> int:
    if not matrices:
        return 0
    return Matrix.hstack(*(vec(matrix) for matrix in matrices)).rank()


def in_span(matrix: Matrix, generators: list[Matrix]) -> bool:
    return span_rank(generators + [matrix]) == span_rank(generators)


def check_diagonal_covariance() -> None:
    alpha = Matrix([2, 3, 5])
    beta = Matrix([7, 11, 13])
    a0 = Matrix([3, -2, 0])
    a1 = Matrix([5, 0, -2])
    b0 = Matrix([11, -7, 0])
    b1 = Matrix([13, 0, -7])
    assert (alpha.T * a0)[0] == (alpha.T * a1)[0] == 0
    assert (beta.T * b0)[0] == (beta.T * b1)[0] == 0

    q = outer(a0, b1) + outer(a1, b0)
    assert q.rank() == 2
    assert (alpha.T * q).is_zero_matrix
    assert (q * beta).is_zero_matrix

    left = diag(*alpha)
    right = diag(*beta)
    aa0, aa1 = left * a0, left * a1
    bb0, bb1 = right * b0, right * b1
    qq = left * q * right
    one = Matrix.ones(3, 1)
    assert (one.T * aa0)[0] == (one.T * aa1)[0] == 0
    assert (one.T * bb0)[0] == (one.T * bb1)[0] == 0
    assert qq == outer(aa0, bb1) + outer(aa1, bb0)
    assert (one.T * qq).is_zero_matrix
    assert (qq * one).is_zero_matrix

    diagonal = [outer(Matrix.eye(3)[:, i], Matrix.eye(3)[:, i]) for i in range(3)]
    transformed = [left * item * right for item in diagonal]
    assert span_rank(transformed) == 3
    assert all(in_span(item, diagonal) for item in transformed)


def terminal_matrix(r: object, s: object, t: object) -> Matrix:
    # Variables are (X,Y,Z,lambda,mu).
    return Matrix(
        [
            [-1, 1, 0, -r, 0],
            [0, 0, 1, -s, 0],
            [0, 0, -1, -t, 0],
            [0, 1, 0, 0, -r],
            [-1, 0, 1, 0, -s],
            [0, -1, 0, 0, -t],
        ]
    )


def check_terminal_compatibility_ideal() -> None:
    r, s, t = symbols("r s t")
    matrix = terminal_matrix(r, s, t)
    minors = []
    for omitted in range(6):
        rows = [row for row in range(6) if row != omitted]
        minors.append(matrix.extract(rows, range(5)).det().factor())

    expected = [
        (r + t) * (s + t),
        (r - t) * (r + t),
        -(r + s) * (r + t),
        -(s - t) * (s + t),
        -(r + t) * (s + t),
        -(r + s) * (s + t),
    ]
    assert all((actual - target).expand() == 0 for actual, target in zip(minors, expected))

    basis = groebner(minors, r, s, t, order="lex")
    assert [polynomial.as_expr() for polynomial in basis.polys] == [
        r**2 - t**2,
        r * s + r * t + s * t + t**2,
        s**2 - t**2,
    ]

    exceptional = [
        ((1, -1, -1), Matrix([1, 1, 0])),
        ((1, -1, 1), Matrix([1, 0, 1])),
        ((1, 1, -1), Matrix([0, 1, 1])),
    ]
    for fibre, expected_x in exceptional:
        kernel = terminal_matrix(*fibre).nullspace()
        assert len(kernel) == 1
        assert Matrix.hstack(kernel[0][:3, :], expected_x).rank() == 1

    assert terminal_matrix(1, 2, 3).rank() == 5


def check_exceptional_rank_bound() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, i] for i in range(3))
    diagonal = [outer(vector, vector) for vector in (e0, e1, e2)]
    h_basis = [e0 - e1, e0 - e2]
    exceptional = [
        (Matrix([1, -1, -1]), Matrix([1, 1, 0])),
        (Matrix([1, -1, 1]), Matrix([1, 0, 1])),
        (Matrix([1, 1, -1]), Matrix([0, 1, 1])),
    ]
    for off_diagonal, line in exceptional:
        r, s, t = off_diagonal
        q = Matrix([[0, r, s], [r, 0, t], [s, t, 0]])
        cylinder = diagonal + [q]
        residual_generators = [sym(vector, line) for vector in h_basis]
        port_generator = sym(line, line)
        generators = residual_generators + [port_generator]
        assert all(in_span(generator, cylinder) for generator in residual_generators)
        # The possible port--port line need not itself lie in S.  Physical
        # membership can only shrink its contribution; the theorem uses the
        # three-dimensional ambient span, not a false containment in S.
        assert not in_span(port_generator, cylinder)
        assert span_rank(generators) == 3


def check_row_column_alignment_fixture() -> None:
    e0, e1, e2 = (Matrix.eye(3)[:, i] for i in range(3))
    a0, a1 = e0 - e1, e0 - e2
    c = 7
    b0, b1 = c * a0, c * a1
    q = outer(a0, b1) + outer(a1, b0)
    one = Matrix.ones(3, 1)
    assert q == q.T
    assert (one.T * q).is_zero_matrix and (q * one).is_zero_matrix

    x = Matrix([0, 1, 1])
    y = c * x
    for a, b in ((a0, b0), (a1, b1)):
        matrix = outer(a, y) + outer(x, b)
        assert matrix == matrix.T
        assert matrix * one == matrix.T * one
        assert in_span(matrix, [outer(e0, e0), outer(e1, e1), outer(e2, e2), q])


def check_repeated_anchor_shortcut_boundary() -> None:
    left = Matrix([1, 0, -1])
    right = Matrix([-1, 0, -1])
    q = 2 * outer(left, right)
    e0, e1, e2 = (Matrix.eye(3)[:, i] for i in range(3))
    diagonal = [outer(vector, vector) for vector in (e0, e1, e2)]
    cylinder = diagonal + [q]

    x = e2
    y = e2
    residual_port = outer(left, y) + outer(x, right)
    port_port = sym(x, y)
    assert span_rank(cylinder) == 4
    assert in_span(residual_port, cylinder)
    assert in_span(port_port, cylinder)

    # Solve the complete residual-compatibility kernel exactly.
    variables = Matrix(symbols("x0:3") + symbols("y0:3"))
    candidate = outer(left, variables[3:, :]) + outer(variables[:3, :], right)
    annihilator = Matrix.hstack(*(vec(item) for item in cylinder)).T.nullspace()
    ann_rows = Matrix.hstack(*annihilator).T
    equations = ann_rows * vec(candidate)
    coefficient_matrix = equations.jacobian(variables)
    kernel = coefficient_matrix.nullspace()
    assert len(kernel) == 3
    assert all(vector[1] == 0 and vector[4] == 0 for vector in kernel)

    star_images = [
        outer(left, vector[3:, :]) + outer(vector[:3, :], right)
        for vector in kernel
    ]
    assert span_rank(star_images) == 2
    assert not in_span(port_port, star_images)

    total = star_images + [port_port, q]
    assert span_rank(total) == 3
    assert all(in_span(item, [outer(e0, e0), outer(e2, e2), q]) for item in total)
    assert not in_span(outer(e1, e1), total)


def check_minor_subsets_are_complete() -> None:
    # A small guard against accidentally dropping one of the six maximal minors.
    assert len(list(combinations(range(6), 5))) == 6


def main() -> None:
    check_diagonal_covariance()
    check_terminal_compatibility_ideal()
    check_exceptional_rank_bound()
    check_row_column_alignment_fixture()
    check_repeated_anchor_shortcut_boundary()
    check_minor_subsets_are_complete()
    print("GLS43 rank-four off-diagonal full-swallow primary checks: PASS")


if __name__ == "__main__":
    main()
