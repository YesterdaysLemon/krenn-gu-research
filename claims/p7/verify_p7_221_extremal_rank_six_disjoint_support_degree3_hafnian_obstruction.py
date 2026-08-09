"""Verify the extremal rank-six disjoint-support hafnian obstruction.

This is a fixed exact symbolic replay, not a support or graph search.
"""

from itertools import combinations

import sympy as sp

import verify_p7_221_degree5_incidence_quotient_rectangle_flattening as binary


def edge(weights, left: int, right: int):
    return weights[tuple(sorted((left, right)))]


def four_hafnian(weights, vertices):
    first, second, third, fourth = vertices
    return sp.expand(
        edge(weights, first, second) * edge(weights, third, fourth)
        + edge(weights, first, third) * edge(weights, second, fourth)
        + edge(weights, first, fourth) * edge(weights, second, third)
    )


def permanent(matrix: sp.Matrix):
    size = matrix.rows
    if size == 0:
        return sp.Integer(1)
    first_row = matrix.row(0)
    return sp.expand(
        sum(
            first_row[column]
            * permanent(matrix.minor_submatrix(0, column))
            for column in range(size)
        )
    )


def main() -> None:
    rho = binary.RHO
    alpha = 1 + 43 * rho / 21
    beta = 2 * (1 + rho) / 7
    coefficient_matrix = sp.Matrix(
        ((alpha, -6, 0), (rho, 0, beta), (0, rho, beta))
    )
    assert sp.simplify(coefficient_matrix.det() - (124 - 76 * rho) / 7) == 0

    # Normalized six-vertex four-hafnian system.
    variables = sp.symbols("p q r s u v w z m n o t")
    p, q, r, s, u, v, w, z, m, n, o, t = variables
    weights = {
        (0, 1): sp.Integer(1),
        (2, 3): sp.Integer(1),
        (4, 5): sp.Integer(1),
        (0, 2): p,
        (0, 3): q,
        (1, 2): r,
        (1, 3): s,
        (0, 4): u,
        (0, 5): v,
        (1, 4): w,
        (1, 5): z,
        (2, 4): m,
        (2, 5): n,
        (3, 4): o,
        (3, 5): t,
    }
    equations = {
        vertices: four_hafnian(weights, vertices)
        for vertices in combinations(range(6), 4)
    }
    assert len(equations) == 15

    e_ab = equations[(0, 1, 2, 3)]
    substitutions_a = {
        m: -p * w - u * r,
        n: -p * z - v * r,
        o: -q * w - u * s,
        t: -q * z - v * s,
    }
    b_relations = (
        ((0, 2, 3, 4), 2 * (u - p * q * w) - u * e_ab),
        ((0, 2, 3, 5), 2 * (v - p * q * z) - v * e_ab),
        ((1, 2, 3, 4), 2 * (w - r * s * u) - w * e_ab),
        ((1, 2, 3, 5), 2 * (z - r * s * v) - z * e_ab),
    )
    for vertices, expected in b_relations:
        actual = sp.expand(equations[vertices].subs(substitutions_a))
        assert sp.expand(actual - expected) == 0

    x_value = p * s
    y_value = q * r
    u_value = p * q * w
    z_value = r * s * v
    m_value = substitutions_a[m].subs({u: u_value})
    n_value = substitutions_a[n].subs({z: z_value})
    c_equation = sp.expand(p + u_value * n_value + v * m_value)
    c_target = sp.expand(p * (1 + (y_value**2 + x_value) * v * w))
    expected_error = -p * v * w * (y_value + 1) * e_ab
    assert sp.expand(c_equation - c_target - expected_error) == 0

    # An exact normalized ideal check independently closes all possible
    # zero/nonzero subcases behind the hand derivation.
    groebner_basis = sp.groebner(tuple(equations.values()), *variables, order="grevlex")
    assert tuple(polynomial.as_expr() for polynomial in groebner_basis.polys) == (
        sp.Integer(1),
    )

    # Generic five-row permanent Laplace expansion along its first two rows.
    entries = sp.symbols("r0:25")
    generic = sp.Matrix(5, 5, entries)
    full_permanent = permanent(generic)
    laplace = sp.Integer(0)
    for columns in combinations(range(5), 2):
        complement = tuple(column for column in range(5) if column not in columns)
        left = generic.extract((0, 1), columns)
        right = generic.extract((2, 3, 4), complement)
        laplace += permanent(left) * permanent(right)
    assert sp.expand(full_permanent - laplace) == 0

    # Sharp surviving quotient shadow: a triangle of distinct support pairs.
    supports = ({0, 1}, {1, 2}, {0, 2})
    local_support_counts = tuple(
        sum(mode in support for support in supports) for mode in range(7)
    )
    assert local_support_counts == (2, 2, 2, 0, 0, 0, 0)
    assert sum(local_support_counts) == 6
    assert all(
        sum({left, right}.issubset(support) for support in supports) <= 1
        for left, right in combinations(range(7), 2)
    )
    assert all(len(support) == 2 for support in supports)
    assert len(set.union(*supports)) == 3

    print("PASS: exact degree-five coefficient antecedent is invertible")
    print("PASS: hand four-hafnian identities and normalized unit ideal")
    print("PASS: generic five-row-to-three-row permanent Laplace descent")
    print("PASS: disjoint extremal rank-six support is excluded")
    print("PASS: overlapping triangle rank-six quotient shadow survives")
    print("SCOPE: overlapping supports and rank below six remain unresolved")
    print("searches=0")


if __name__ == "__main__":
    main()
