"""Primary exact replay for the global square-free Wick classification.

The arbitrary-support theorem is proved combinatorially in the owning
document.  This script checks its exact finite matrices, kernels, and walls.
"""

from itertools import combinations

import sympy as sp


def subsets(n: int, size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(combinations(range(n), size))


def up_matrix(coefficients, degree: int) -> sp.Matrix:
    n = len(coefficients)
    columns = subsets(n, degree)
    rows = subsets(n, degree + 1)
    data = []
    for row in rows:
        row_set = set(row)
        values = []
        for column in columns:
            missing = row_set - set(column)
            values.append(coefficients[next(iter(missing))] if len(missing) == 1 else 0)
        data.append(values)
    return sp.Matrix(data)


def wick_matrix(a, b) -> sp.Matrix:
    n = len(a)
    pairs = subsets(n, 2)
    rows = subsets(n, 4)
    data = []
    for row in rows:
        row_set = set(row)
        values = []
        for pair in pairs:
            if set(pair) <= row_set:
                left, right = tuple(row_set - set(pair))
                values.append(a[left] * b[right] + b[left] * a[right])
            else:
                values.append(0)
        data.append(values)
    return sp.Matrix(data)


def vector_from_terms(n: int, terms: dict[tuple[int, int], object]) -> sp.Matrix:
    normalized = {tuple(sorted(pair)): value for pair, value in terms.items()}
    return sp.Matrix([normalized.get(pair, 0) for pair in subsets(n, 2)])


def product_of_linear_forms(left, right) -> sp.Matrix:
    n = len(left)
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in subsets(n, 2)]
    )


def check_one_step_table_and_bases() -> None:
    n = 7
    expected_nullity = {0: 21, 1: 6, 2: 6, 3: 2, 4: 2, 5: 0, 6: 0, 7: 0}
    for support, nullity in expected_nullity.items():
        coefficients = [sp.Integer(i + 2) if i < support else 0 for i in range(n)]
        matrix = up_matrix(coefficients, 2)
        assert len(matrix.nullspace()) == nullity

    # Weighted explicit bases from Corollary 2.1.
    b4 = [sp.Integer(2), sp.Integer(3), sp.Integer(5), sp.Integer(7), 0, 0, 0]
    y = b4
    basis4 = [
        vector_from_terms(
            n,
            {
                (0, 1): y[0] * y[1],
                (2, 3): y[2] * y[3],
                (0, 3): -y[0] * y[3],
                (1, 2): -y[1] * y[2],
            },
        ),
        vector_from_terms(
            n,
            {
                (0, 2): y[0] * y[2],
                (1, 3): y[1] * y[3],
                (0, 3): -y[0] * y[3],
                (1, 2): -y[1] * y[2],
            },
        ),
    ]
    matrix4 = up_matrix(b4, 2)
    assert sp.Matrix.hstack(*basis4).rank() == 2
    assert all(matrix4 * vector == sp.zeros(matrix4.rows, 1) for vector in basis4)

    b3 = [sp.Integer(2), sp.Integer(3), sp.Integer(5), 0, 0, 0, 0]
    basis3 = [
        vector_from_terms(n, {(0, 1): 6, (1, 2): -15}),
        vector_from_terms(n, {(0, 2): 10, (1, 2): -15}),
    ]
    matrix3 = up_matrix(b3, 2)
    assert sp.Matrix.hstack(*basis3).rank() == 2
    assert all(matrix3 * vector == sp.zeros(matrix3.rows, 1) for vector in basis3)


def check_union_and_common_row_controls() -> None:
    a7 = [sp.Integer(1)] * 7
    b7 = [sp.Integer(1)] * 5 + [sp.Integer(0), sp.Integer(0)]
    global_matrix = wick_matrix(a7, b7)
    assert global_matrix.shape == (35, 21)
    assert global_matrix.rank() == 21

    zero_pair = {5, 6}
    windows = [window for window in subsets(7, 6) if zero_pair <= set(window)]
    assert len(windows) == 5
    for window in windows:
        restricted_a = [a7[i] for i in window]
        restricted_b = [b7[i] for i in window]
        local = wick_matrix(restricted_a, restricted_b)
        assert local.det() == 0

    # Coincident five-support union: exact global nullity five at n=7.
    a5 = [sp.Integer(1)] * 5 + [sp.Integer(0), sp.Integer(0)]
    b5 = [sp.Integer(2)] * 5 + [sp.Integer(0), sp.Integer(0)]
    coincident = wick_matrix(a5, b5)
    assert coincident.rank() == 16
    assert len(coincident.nullspace()) == 5


def check_distinct_five_support_wall() -> None:
    t0, t1, t2, t3 = sp.symbols("t0 t1 t2 t3")
    t = [t0, t1, t2, t3, sp.Integer(0)]
    one = [sp.Integer(1)] * 5
    phi = up_matrix(one, 3) * up_matrix(t, 2) * up_matrix(t, 1)
    expected = (
        192
        * (t0 * t1 * t2 * t3) ** 2
        * (t0 * t1 + t0 * t2 + t0 * t3 + t1 * t2 + t1 * t3 + t2 * t3)
    )
    assert sp.factor(phi.det() - expected) == 0

    e2 = t0 * t1 + t0 * t2 + t0 * t3 + t1 * t2 + t1 * t3 + t2 * t3
    u = sp.Matrix([-1, -1, -1, -1, 1])
    candidate_residual = phi * u - sp.Matrix([-4 * e2, 0, 0, 0, 0])
    assert all(sp.expand(entry) == 0 for entry in candidate_residual)
    gradient = [sp.diff(e2, variable) for variable in (t0, t1, t2, t3)]
    total = t0 + t1 + t2 + t3
    assert gradient == [total - variable for variable in (t0, t1, t2, t3)]

    values = [sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Integer(-1)]
    a = [sp.Integer(1)] * 5 + [sp.Integer(0)]
    b = values + [sp.Integer(0), sp.Integer(1)]
    matrix = wick_matrix(a, b)
    assert matrix.rank() == 14

    ell_c = values + [sp.Integer(0), sp.Integer(0)]
    x_y_minus_c = [-value for value in ell_c]
    x_y_minus_c[5] = 1
    x_d_minus_sum_c = [sp.Integer(-1)] * 4 + [sp.Integer(1), sp.Integer(0)]
    kernel = product_of_linear_forms(x_y_minus_c, x_d_minus_sum_c)
    assert kernel != sp.zeros(15, 1)
    assert matrix * kernel == sp.zeros(15, 1)


def check_nested_six_five_wall() -> None:
    a = [sp.Integer(1)] * 6
    b = [sp.Integer(3), sp.Integer(3), sp.Integer(3), sp.Integer(-5), sp.Integer(6), 0]
    matrix = wick_matrix(a, b)
    assert matrix.rank() == 14
    kernel = vector_from_terms(
        6,
        {
            (0, 1): 6,
            (0, 2): 6,
            (1, 2): 6,
            (0, 3): 2,
            (1, 3): 2,
            (2, 3): 2,
            (0, 4): -9,
            (1, 4): -9,
            (2, 4): -9,
            (0, 5): -3,
            (1, 5): -3,
            (2, 5): -3,
            (3, 4): -13,
            (3, 5): 1,
            (4, 5): 12,
        },
    )
    assert matrix * kernel == sp.zeros(15, 1)
    assert all(a[i] * b[j] + b[i] * a[j] != 0 for i, j in combinations(range(6), 2))


def main() -> None:
    check_one_step_table_and_bases()
    check_union_and_common_row_controls()
    check_distinct_five_support_wall()
    check_nested_six_five_wall()
    print("global square-free physical Wick primary replay: PASS")
    print("seven-port global rank 21; all five selected six-window determinants zero")
    print("union-five nullity 5; two union-six rank-14 walls replayed exactly")


if __name__ == "__main__":
    main()
