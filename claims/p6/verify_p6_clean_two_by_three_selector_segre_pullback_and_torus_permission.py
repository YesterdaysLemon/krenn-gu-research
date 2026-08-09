"""Primary exact checks for the clean P6 Segre-pullback selector theorem."""

from itertools import combinations

import sympy as sp

PAIR_ORDER = tuple(combinations(range(4), 2))


def fan_matrix(parameters: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Return the 2-by-3 mixed permanental fan in lexicographic pair order."""

    a = sp.Matrix([[1 for _ in parameters], list(parameters)])
    b = sp.Matrix(
        [
            [1 for _ in parameters],
            [value**2 for value in parameters],
            [value**3 for value in parameters],
        ]
    )
    columns = [
        sp.kronecker_product(a[:, i], b[:, j])
        + sp.kronecker_product(a[:, j], b[:, i])
        for i, j in PAIR_ORDER
    ]
    return sp.Matrix.hstack(*columns)


def symbolic_vandermonde_determinant_check() -> None:
    parameters = sp.symbols("t0:4")
    matrix = fan_matrix(parameters)
    vandermonde = sp.prod(
        parameters[i] - parameters[j] for i, j in combinations(range(4), 2)
    )
    expected = -2 * vandermonde**2 * sum(parameters)
    assert sp.factor(matrix.det() - expected) == 0
    assert sp.Poly(matrix.det(), parameters).total_degree() == 13
    print("symbolic fan determinant = -2 Vandermonde^2 sum(t): PASS")


def fixed_torus_permission_check() -> None:
    matrix = fan_matrix(tuple(map(sp.Integer, (1, 2, 3, 4))))
    expected_matrix = sp.Matrix(
        [
            [2, 2, 2, 2, 2, 2],
            [5, 10, 17, 13, 20, 25],
            [9, 28, 65, 35, 72, 91],
            [3, 4, 5, 5, 6, 7],
            [6, 12, 20, 30, 48, 84],
            [10, 30, 68, 78, 160, 300],
        ]
    )
    assert matrix == expected_matrix
    assert matrix.det() == -2880

    left_factors = (
        sp.Matrix([1, 1]),
        sp.Matrix([1, 1]),
        sp.Matrix([1, 2]),
    )
    right_factors = (
        sp.Matrix([1, 1, 1]),
        sp.Matrix([1, 2, 3]),
        sp.Matrix([1, 4, 9]),
    )
    face_columns = (
        sp.Matrix([14, -24, 20, 15, -29, 9]),
        sp.Matrix([10, -33, 36, 30, -58, 18]),
        sp.Matrix([2, 38, -45, -30, 73, -23]),
    )
    scales = (10, 6, 30)

    left_matrix = sp.Matrix.hstack(*left_factors)
    right_matrix = sp.Matrix.hstack(*right_factors)
    assert left_matrix.rank() == 2
    assert right_matrix.det() == 2

    for left, right, faces, scale in zip(
        left_factors, right_factors, face_columns, scales, strict=True
    ):
        target = scale * sp.kronecker_product(left, right)
        observed = matrix * faces
        assert observed == target
        assert all(entry != 0 for entry in faces)
        reshaped = sp.Matrix(2, 3, list(observed))
        assert reshaped.rank() == 1
        minors = [
            reshaped[0, i] * reshaped[1, j]
            - reshaped[0, j] * reshaped[1, i]
            for i, j in combinations(range(3), 2)
        ]
        assert minors == [0, 0, 0]

    assert all(
        entry != 0
        for value in (1, 2, 3, 4)
        for entry in (1, value, value**2, value**3)
    )
    print("fixed all-incidence fan and three full-torus GHZ slices: PASS")


def generic_segre_minor_check() -> None:
    r0, r1, s0, s1, s2 = sp.symbols("r0 r1 s0 s1 s2")
    rank_one = sp.Matrix(
        [[r0 * s0, r0 * s1, r0 * s2], [r1 * s0, r1 * s1, r1 * s2]]
    )
    for i, j in combinations(range(3), 2):
        assert sp.expand(
            rank_one[0, i] * rank_one[1, j]
            - rank_one[0, j] * rank_one[1, i]
        ) == 0

    matrix = fan_matrix(tuple(map(sp.Integer, (1, 2, 3, 4))))
    vector = sp.Matrix(list(rank_one))
    pulled_back = matrix.inv() * vector
    assert sp.simplify(matrix * pulled_back - vector) == sp.zeros(6, 1)

    complement = sp.zeros(6, 6)
    for row, pair in enumerate(PAIR_ORDER):
        opposite = tuple(vertex for vertex in range(4) if vertex not in pair)
        complement[row, PAIR_ORDER.index(opposite)] = 1
    assert complement**2 == sp.eye(6)
    assert (matrix * complement).det() != 0
    print("rank-one minors and deletion/survivor convention invariance: PASS")


def legal_shore_and_target_basis_check() -> None:
    common = sp.Matrix([1, 1, 1])
    selected_second = sp.Matrix([1, 2, 3])
    shore = sp.Matrix([[-1, 1, 0], [0, 0, 0], [0, 0, 0]])
    assert (common.T * shore * common)[0] == 0
    assert (common.T * shore * selected_second)[0] == 1

    target_coefficients = sp.Matrix([10, 3, 10])
    selected_weights = common.multiply_elementwise(selected_second)
    assert target_coefficients.multiply_elementwise(selected_weights) == sp.Matrix(
        [10, 6, 30]
    )

    active_left_basis = sp.Matrix([[1, 1, 1], [1, 1, 2]])
    active_right_basis = sp.Matrix(
        [[1, 1, 1], [1, 2, 4], [1, 3, 9]]
    )
    assert active_left_basis.rank() == 2
    assert active_right_basis.det() == 2
    assert all(entry != 0 for entry in active_left_basis)
    assert all(entry != 0 for entry in active_right_basis)
    print("zero-coupled nonzero shore and rank-(2,3) active target bases: PASS")


def main() -> None:
    symbolic_vandermonde_determinant_check()
    fixed_torus_permission_check()
    generic_segre_minor_check()
    legal_shore_and_target_basis_check()
    print("P6 clean 2x3 Segre-pullback primary verification: PASS")


if __name__ == "__main__":
    main()
