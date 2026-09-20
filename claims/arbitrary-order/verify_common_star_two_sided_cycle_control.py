"""Exact replay of the nine-component two-sided binary cycle control.

This verifies one unordered color pair only.  It does not supply the
third-color, distinct-color S2 equations required by FB.
"""

from itertools import combinations, permutations

import sympy as sp


S, R, T = sp.symbols("s r t", nonzero=True)
FS = 3 * S**2 + 3 * S + 1
PR = (
    (3 * S + 1) * R**4
    + 12 * (S + 1) * R**3
    - 6 * (3 * S + 1) * R**2
    + 12 * (S + 1) * R
    + 3 * S
    + 1
)
ET = (
    -2 * R * (R + 1) * (3 * S + 1) * T**2
    + (3 * R**2 * S + 3 * R**2 - 6 * R * S - 10 * R + 3 * S + 3) * T
    + 6 * (R + 1) * (2 * S + 1)
)
IDEAL = sp.groebner((FS, PR, ET), T, R, S, order="lex")


def permanent(matrix, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    if not rows:
        return sp.Integer(1)
    return sum(
        sp.prod(matrix[row, column] for row, column in zip(rows, permuted))
        for permuted in permutations(columns)
    )


def source(matrix_a, matrix_b, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    return sp.together(
        sum(
            permanent(matrix_a, chosen_rows, chosen_columns)
            * permanent(matrix_b, chosen_rows, chosen_columns)
            for size in range(min(len(rows), len(columns)) + 1)
            for chosen_rows in combinations(rows, size)
            for chosen_columns in combinations(columns, size)
        )
    )


def vanishes(expression):
    numerator = sp.together(expression).as_numer_denom()[0]
    return IDEAL.reduce(numerator)[1] == 0


def equal_mod_ideal(left, right):
    return vanishes(left - right)


def matrices():
    size = 9
    q_cycle = -1 - S
    w = S / 2
    delta = -1 - 3 * w
    matrix_a = sp.zeros(size)
    matrix_b = sp.zeros(size)

    def edge(row, column, product, center=sp.Integer(1)):
        matrix_a[row, column] = center
        matrix_b[row, column] = product / center

    for row in range(3):
        edge(row, (row + 1) % 3, q_cycle)
    for row in (3, 4):
        for column in range(3):
            edge(row, column, w)
    for row in range(3):
        for column in (5, 6):
            edge(row, column, w)

    factor_block = ((R * T, T), (T, R * T))
    for row_position, row in enumerate((3, 4)):
        for column_position, column in enumerate((5, 6)):
            edge(
                row,
                column,
                delta / 2,
                factor_block[row_position][column_position],
            )
    for row in (5, 6):
        for column in (7, 8):
            edge(row, column, sp.Rational(-1, 2))
    for row in (7, 8):
        for column in (3, 4):
            edge(row, column, sp.Rational(-1, 2))
    return matrix_a, matrix_b


def check_support(matrix_a, matrix_b):
    size = matrix_a.rows
    edge_count = 0
    for row in range(size):
        for column in range(size):
            assert bool(matrix_a[row, column]) == bool(matrix_b[row, column])
            if matrix_a[row, column]:
                edge_count += 1
                assert row != column
                assert not matrix_a[column, row]
    assert edge_count == 27
    return edge_count


def check_nonzero_parameters():
    norm = sp.factor(sp.resultant(FS, PR, S) / 3)
    expected_norm = R**8 + 36 * R**6 + 134 * R**4 + 36 * R**2 + 1
    assert sp.expand(norm - expected_norm) == 0
    assert sp.gcd(sp.Poly(expected_norm, R), sp.Poly(R * (R**4 - 1), R)) == 1

    # The quadratic ET has nonzero leading and constant coefficients at every
    # admissible (s,r): r is neither 0 nor -1 and none of the displayed
    # linear expressions in s vanishes on FS.
    for expression in (S, 1 + S, 2 + 3 * S, 3 * S + 1, 2 * S + 1):
        assert sp.gcd(sp.Poly(FS, S), sp.Poly(expression, S)) == 1
    assert sp.gcd(sp.Poly(expected_norm, R), sp.Poly(R * (R + 1), R)) == 1

    # The exhibited failed-cut value is nonzero for every allowed r.
    assert sp.gcd(sp.Poly(expected_norm, R), sp.Poly(R**2 + 1, R)) == 1
    return norm


def check_s1(matrix_a, matrix_b):
    products = matrix_a.multiply_elementwise(matrix_b)
    for row in range(9):
        assert vanishes(sum(products[row, column] for column in range(9)) + 1)
    for column in range(9):
        assert vanishes(sum(products[row, column] for row in range(9)) + 1)


def check_two_sided_defects(matrix_a, matrix_b):
    cycle = (0, 1, 2)
    incoming = (3, 4)
    outgoing = (5, 6)
    q_cycle = -1 - S
    checked = 0
    for size in range(4):
        for selected in combinations(cycle, size):
            expected = (-q_cycle) ** size if size < 3 else 0
            assert equal_mod_ideal(source(matrix_a, matrix_b, incoming, selected), expected)
            assert equal_mod_ideal(source(matrix_a, matrix_b, selected, outgoing), expected)
            checked += 2
    return checked


def cut_source(matrix_a, matrix_b, selected):
    complement = tuple(index for index in range(9) if index not in selected)
    return source(matrix_a, matrix_b, selected, complement)


def check_binary_s1_s2(matrix_a, matrix_b):
    checked = 0
    for size in (1, 2, 7, 8):
        for selected in combinations(range(9), size):
            assert vanishes(cut_source(matrix_a, matrix_b, selected))
            checked += 1
    assert checked == 90
    return checked


def check_cut_identities(matrix_a, matrix_b):
    """Verify the written two-row formulas before imposing PR or ET.

    The row groups C,I,O,D give all ten unordered pair types. Cyclic
    permutation of C and simultaneous swaps of I,O cover their members.
    Checking all 36 pairs in each orientation avoids relying on symmetry
    alone for the finite case cover.
    """
    checked = 0
    for a, b, exceptional in (
        (matrix_a, matrix_b, (3, 4)),
        (matrix_a.T, matrix_b.T, (5, 6)),
    ):
        for selected in combinations(range(9), 2):
            if selected == exceptional:
                expected = PR / (16 * R**2)
            elif selected[0] in range(3) and selected[1] in exceptional:
                expected = ET / (24 * R * T)
            else:
                expected = 0
            numerator = sp.together(cut_source(a, b, selected) - expected).as_numer_denom()[0]
            assert sp.Poly(numerator, S).rem(sp.Poly(FS, S)).as_expr() == 0
            checked += 1
    return checked


def check_global_failure(matrix_a, matrix_b):
    selected = (0, 1, 3)
    expected = (R**2 + 1) / (12 * R)
    actual = cut_source(matrix_a, matrix_b, selected)
    assert equal_mod_ideal(actual, expected)
    return selected, expected


def main():
    matrix_a, matrix_b = matrices()
    edge_count = check_support(matrix_a, matrix_b)
    norm = check_nonzero_parameters()
    check_s1(matrix_a, matrix_b)
    identities = check_cut_identities(matrix_a, matrix_b)
    defect_checks = check_two_sided_defects(matrix_a, matrix_b)
    binary_checks = check_binary_s1_s2(matrix_a, matrix_b)
    failed_cut, failed_value = check_global_failure(matrix_a, matrix_b)
    print(f"legal oriented support: {edge_count} arcs")
    print(f"r norm polynomial: {norm}")
    print(f"two-sided localized equations checked: {defect_checks}")
    print(f"two-row identities checked before PR/ET specialization: {identities}")
    print(f"binary S1/S2 proper cuts checked exactly: {binary_checks}")
    print(f"failed full-binary cut: {failed_cut}, value: {failed_value}")
    print("third-color distinct-color S2: NOT SUPPLIED")


if __name__ == "__main__":
    main()
