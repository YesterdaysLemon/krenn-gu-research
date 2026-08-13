"""Exact replay of the m=3 common-quotient P3 orbit theorem."""

from itertools import combinations, permutations, product

import sympy as sp


def permanent_trilinear(x, y, z):
    """Evaluate the order-three permanent tensor."""
    return sp.expand(
        sum(x[sigma[0]] * y[sigma[1]] * z[sigma[2]] for sigma in permutations(range(3)))
    )


def cayley_hyperdet(entries):
    """Cayley's 2x2x2 hyperdeterminant in lexicographic order."""
    x0, x1, x2, x3, x4, x5, x6, x7 = entries
    return sp.expand(
        x0**2 * x7**2
        + x1**2 * x6**2
        + x2**2 * x5**2
        + x4**2 * x3**2
        - 2
        * (
            x0 * x7 * (x1 * x6 + x2 * x5 + x4 * x3)
            + x1 * x6 * x2 * x5
            + x1 * x6 * x4 * x3
            + x2 * x5 * x4 * x3
        )
        + 4 * (x0 * x3 * x5 * x6 + x7 * x4 * x2 * x1)
    )


def quotient_entries(a, b):
    u = sp.Matrix((-a, 1, 0))
    v = sp.Matrix((-b, 0, 1))
    basis = (u, v)
    return {
        index: permanent_trilinear(*(basis[i] for i in index))
        for index in product(range(2), repeat=3)
    }


def flatten(entries, mode):
    other_modes = [position for position in range(3) if position != mode]
    matrix = sp.zeros(2, 4)
    for row in range(2):
        for column, pair in enumerate(product(range(2), repeat=2)):
            index = [0, 0, 0]
            index[mode] = row
            index[other_modes[0]] = pair[0]
            index[other_modes[1]] = pair[1]
            matrix[row, column] = entries[tuple(index)]
    return matrix


def check_singleton_common_kernel():
    root_covectors = [sp.symbols(f"a{i}_0:3") for i in range(3)]
    root_blocks = {
        (0, 1): sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"b01_{i}{j}")),
        (0, 2): sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"b02_{i}{j}")),
        (1, 2): sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"b12_{i}{j}")),
    }
    cross_vectors = [sp.symbols(f"h{i}_0:3") for i in range(3)]

    a0, a1, a2 = (sp.Matrix(vector) for vector in root_covectors)
    beta = (
        (a1.T * root_blocks[(1, 2)] * a2)[0],
        (a0.T * root_blocks[(0, 2)] * a2)[0],
        (a0.T * root_blocks[(0, 1)] * a1)[0],
    )

    direct = 0
    for i, j, k in product(range(3), repeat=3):
        direct += (
            cross_vectors[0][i] * root_blocks[(1, 2)][j, k]
            + root_blocks[(0, 2)][i, k] * cross_vectors[1][j]
            + root_blocks[(0, 1)][i, j] * cross_vectors[2][k]
        ) * root_covectors[0][i] * root_covectors[1][j] * root_covectors[2][k]

    contracted_cross = [
        sum(root_covectors[mode][coordinate] * cross_vectors[mode][coordinate] for coordinate in range(3))
        for mode in range(3)
    ]
    factored = sum(beta[mode] * contracted_cross[mode] for mode in range(3))
    assert sp.expand(direct - factored) == 0
    print("physical singleton common-kernel identity: PASS")


def check_quotient_orbits():
    a, b = sp.symbols("A B")
    entries = quotient_entries(a, b)
    expected = {
        (0, 0, 0): 0,
        (0, 0, 1): -2 * a,
        (0, 1, 0): -2 * a,
        (0, 1, 1): -2 * b,
        (1, 0, 0): -2 * a,
        (1, 0, 1): -2 * b,
        (1, 1, 0): -2 * b,
        (1, 1, 1): 0,
    }
    assert all(sp.expand(entries[index] - expected[index]) == 0 for index in expected)

    hyperdet = cayley_hyperdet([entries[index] for index in product(range(2), repeat=3)])
    assert sp.factor(hyperdet) == -48 * a**2 * b**2

    for mode in range(3):
        matrix = flatten(entries, mode)
        minors = [sp.factor(matrix.extract((0, 1), columns).det()) for columns in combinations(range(4), 2)]
        assert any(minor.subs({a: 1, b: 0}) != 0 for minor in minors)
        assert any(minor.subs({a: 1, b: 1}) != 0 for minor in minors)

    support_one = {index: value.subs({a: 0, b: 0}) for index, value in entries.items()}
    support_two = {index: value.subs({a: 1, b: 0}) for index, value in entries.items()}
    support_three = {index: value.subs({a: 1, b: 1}) for index, value in entries.items()}
    assert all(value == 0 for value in support_one.values())
    assert sum(value != 0 for value in support_two.values()) == 3
    assert cayley_hyperdet([support_two[index] for index in product(range(2), repeat=3)]) == 0
    assert cayley_hyperdet([support_three[index] for index in product(range(2), repeat=3)]) != 0
    print("common binary quotient coefficients: PASS (8/8)")
    print("P3 quotient support orbits: PASS (zero / W / GHZ)")


def check_common_quotient_contraction():
    beta = sp.Matrix((1, 2, 3))
    quotient = sp.Matrix(((-2, 1, 0), (-3, 0, 1))).T
    assert (sp.Matrix((1, 2, 3)).T * quotient) == sp.zeros(1, 2)

    bars = (
        sp.Matrix(((1, 2), (3, 5), (7, 11))),
        sp.Matrix(((2, 1), (5, 3), (11, 7))),
        sp.Matrix(((1, 4), (2, 9), (3, 16))),
    )
    maps = tuple(bar * quotient.T for bar in bars)
    assert all(linear_map * beta == sp.zeros(3, 1) for linear_map in maps)

    direct = {}
    quotient_route = {}
    q_entries = quotient_entries(2, 3)
    for i, j, k in product(range(3), repeat=3):
        direct[(i, j, k)] = sp.expand(
            sum(
                maps[0][i, sigma[0]] * maps[1][j, sigma[1]] * maps[2][k, sigma[2]]
                for sigma in permutations(range(3))
            )
        )
        quotient_route[(i, j, k)] = sp.expand(
            sum(
                bars[0][i, p] * bars[1][j, q] * bars[2][k, r] * q_entries[(p, q, r)]
                for p, q, r in product(range(2), repeat=3)
            )
        )
    assert direct == quotient_route
    print("three-map common-quotient contraction: PASS (27 coefficients)")


def check_common_diagonal_lines():
    a = sp.Rational(2)
    b = sp.Rational(3)
    omega = (-1 + sp.sqrt(-3)) / 2
    assert sp.expand(omega**2 + omega + 1) == 0
    binary_lines = (sp.Matrix((1, a * omega / b)), sp.Matrix((1, a * omega**2 / b)))
    plane_basis = sp.Matrix(((-a, -b), (1, 0), (0, 1)))
    root_lines = tuple(sp.simplify(plane_basis * line) for line in binary_lines)
    beta = sp.Matrix((1, a, b))
    assert all(sp.simplify(beta.dot(line)) == 0 for line in root_lines)
    assert all(all(sp.simplify(entry) != 0 for entry in line) for line in root_lines)

    def q_value(left, middle, right):
        return sp.simplify(permanent_trilinear(left, middle, right))

    assert q_value(root_lines[0], root_lines[0], root_lines[1]) == 0
    assert q_value(root_lines[0], root_lines[1], root_lines[1]) == 0
    pure = (q_value(root_lines[0], root_lines[0], root_lines[0]), q_value(root_lines[1], root_lines[1], root_lines[1]))
    assert all(value != 0 for value in pure)

    scales = ((1, 2, 3), (5, 7, 11))
    matrices = tuple(line * sp.Matrix((scale,)) for line, scale in zip(root_lines, scales))
    assert all(matrix.rank() == 1 for matrix in matrices)
    assert all(all(entry != 0 for entry in matrix) for matrix in matrices)
    assert all(sp.simplify(matrix.per()) != 0 for matrix in matrices)
    print("binary-branch common diagonal lines: PASS")
    print("surviving-colour cross matrices: PASS (rank one, full support)")


def main():
    check_singleton_common_kernel()
    check_quotient_orbits()
    check_common_quotient_contraction()
    check_common_diagonal_lines()
    print("balanced m=3 boundary-annihilator common-quotient theorem: PASS")


if __name__ == "__main__":
    main()
