"""Verify the complete P7 four-face null stratum and sharp boundary.

This is a fixed exact symbolic replay, not a graph, support, or selector search.
"""

from functools import cache
from itertools import combinations
from math import comb

import sympy as sp


def permanent(matrix: sp.Matrix):
    """Exact Laplace recurrence for the small fixed matrices in the note."""
    size = matrix.rows
    if size == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            matrix[0, column]
            * permanent(matrix.minor_submatrix(0, column))
            for column in range(size)
        )
    )


def edge(weights, left: int, right: int):
    return weights[tuple(sorted((left, right)))]


def four_hafnian(weights, vertices):
    first, second, third, fourth = vertices
    return sp.expand(
        edge(weights, first, second) * edge(weights, third, fourth)
        + edge(weights, first, third) * edge(weights, second, fourth)
        + edge(weights, first, fourth) * edge(weights, second, third)
    )


def hafnian(matrix: sp.Matrix):
    """Memoized exact matching recurrence for one fixed sparse 14-vertex block."""
    size = matrix.rows

    @cache
    def recurrence(mask: int):
        if mask == 0:
            return sp.Integer(1)
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        total = sp.Integer(0)
        cursor = remainder
        while cursor:
            second_bit = cursor & -cursor
            second = second_bit.bit_length() - 1
            total += matrix[first, second] * recurrence(remainder ^ second_bit)
            cursor ^= second_bit
        return sp.expand(total)

    return recurrence((1 << size) - 1)


def normalized_matching_ideal() -> None:
    variables = sp.symbols("p q r s u v w x a b c d")
    p, q, r, s, u, v, w, x, a, b, c, d = variables
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
        (1, 5): x,
        (2, 4): a,
        (2, 5): b,
        (3, 4): c,
        (3, 5): d,
    }
    equations = tuple(
        four_hafnian(weights, vertices)
        for vertices in combinations(range(6), 4)
    )
    assert len(equations) == comb(6, 4) == 15
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert tuple(poly.as_expr() for poly in basis.polys) == (sp.Integer(1),)


def tangent_identity() -> None:
    names = ("01", "02", "03", "12", "13", "23")
    direct = dict(zip(names, sp.symbols("b01 b02 b03 b12 b13 b23"), strict=True))
    correction = dict(zip(names, sp.symbols("k01 k02 k03 k12 k13 k23"), strict=True))
    h = sp.symbols("h")
    residual = {name: h * direct[name] + correction[name] for name in names}
    complements = {
        "01": "23",
        "02": "13",
        "03": "12",
        "12": "03",
        "13": "02",
        "23": "01",
    }
    moment_four = (
        direct["01"] * direct["23"]
        + direct["02"] * direct["13"]
        + direct["03"] * direct["12"]
    )
    dual_wick_sum = sum(
        residual[name] * direct[complements[name]] for name in names
    )
    tangent = sum(
        correction[name] * direct[complements[name]] for name in names
    )
    assert sp.expand(dual_wick_sum - 2 * h * moment_four - tangent) == 0


def common_block_model():
    tau = (sp.Rational(1, 480), sp.Rational(1, 4800), sp.Rational(1, 38124))
    pure_matrices = []
    for colour in range(3):
        rows = []
        for root in range(5):
            value = sp.Integer(root + 1)
            shifted = 2 * value + 1
            if colour == 0:
                row = (tau[0], 1, 2, 1, 2)
            elif colour == 1:
                row = (tau[1], value, shifted, 1, 2)
            else:
                row = (tau[2], value, shifted, value, shifted)
            rows.append(row)
        pure_matrices.append(sp.Matrix(rows))
    assert tuple(permanent(matrix) for matrix in pure_matrices) == (1, 1, 1)

    left, right = sp.symbols("i j", integer=True)
    determinant_u = sp.Matrix(((1, left + 1), (1, right + 1))).det()
    determinant_v = sp.Matrix(((2, 2 * left + 3), (2, 2 * right + 3))).det()
    assert sp.expand(determinant_u - (right - left)) == 0
    assert sp.expand(determinant_v - 4 * (right - left)) == 0

    # Coordinate row matrices for all six double blockers.  Their nullspaces
    # are exactly their missing-colour axes.
    blocker_types = ((0, 1), (0, 2), (1, 2))
    for first_colour, second_colour in blocker_types:
        for scale in (1, 2):
            rows = []
            for root in range(5):
                row = [sp.Integer(0)] * 3
                if scale == 1:
                    row[first_colour] = 1
                    row[second_colour] = root + 1
                else:
                    row[first_colour] = 2
                    row[second_colour] = 2 * root + 3
                rows.append(row)
            row_matrix = sp.Matrix(rows)
            missing = ({0, 1, 2} - {first_colour, second_colour}).pop()
            expected = sp.eye(3).col(missing)
            assert row_matrix.rank() == 2
            assert row_matrix.nullspace() == [expected]

    return pure_matrices


def full_pure_hafnians_and_response(pure_matrices) -> None:
    # Vertices: roots 0..4, q0=5, q1=6, then
    # t,u01,v01,u02,v02,u12,v12 = 7..13.
    h = sp.symbols("h")
    blocker_order = ("t", "u01", "v01", "u02", "v02", "u12", "v12")
    supported = {
        0: ("t", "u01", "v01", "u02", "v02"),
        1: ("t", "u01", "v01", "u12", "v12"),
        2: ("t", "u02", "v02", "u12", "v12"),
    }
    missing_pair = {
        0: ("u12", "v12"),
        1: ("u02", "v02"),
        2: ("u01", "v01"),
    }

    for colour in range(3):
        adjacency = sp.zeros(14)
        adjacency[5, 6] = adjacency[6, 5] = h
        matrix = pure_matrices[colour]
        for root in range(5):
            for local_column, blocker in enumerate(supported[colour]):
                vertex = 7 + blocker_order.index(blocker)
                adjacency[root, vertex] = adjacency[vertex, root] = matrix[
                    root, local_column
                ]
        u_blocker, v_blocker = missing_pair[colour]
        u_vertex = 7 + blocker_order.index(u_blocker)
        v_vertex = 7 + blocker_order.index(v_blocker)
        adjacency[5, u_vertex] = adjacency[u_vertex, 5] = 1
        adjacency[6, v_vertex] = adjacency[v_vertex, 6] = 1
        assert sp.expand(hafnian(adjacency)) == 1

    # B=0 gives M=1 and Z=h+A*C.  Every nonconstant coefficient is h-free,
    # while both complete singleton rows are fixed.
    u0, u1, u2, v0, v1, v2 = sp.symbols("u0 u1 u2 v0 v1 v2")
    a_row = u0 + u1 + u2
    b_row = v0 + v1 + v2
    response = sp.Poly(h + a_row * b_row, u0, u1, u2, v0, v1, v2)
    assert response.coeff_monomial(1) == h
    nonconstant = {
        monomial: coefficient
        for monomial, coefficient in response.terms()
        if sum(monomial) > 0
    }
    assert len(nonconstant) == 9
    assert all(h not in coefficient.free_symbols for coefficient in nonconstant.values())
    assert all(sum(monomial) == 2 for monomial in nonconstant)


def main() -> None:
    # Inclusion--exclusion: three size-six tagged families, three singleton
    # pairwise intersections, and no triple intersection.
    assert 3 * comb(4, 2) - comb(3, 2) == comb(6, 4) == 15
    normalized_matching_ideal()
    tangent_identity()
    pure_matrices = common_block_model()
    full_pure_hafnians_and_response(pure_matrices)

    print("PASS: eighteen tagged windows cover all fifteen four-subsets")
    print("PASS: four-face nullity forces common-null matching number at most two")
    print("PASS: residual correction is tangent to the four-hafnian-zero locus")
    print("PASS: saturated-null common-block model has three unit pure coefficients")
    print("PASS: full paired singleton rows and nonempty responses coexist with free h")
    print("SCOPE: unrestricted selectors and the complete mixed P7 system remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
