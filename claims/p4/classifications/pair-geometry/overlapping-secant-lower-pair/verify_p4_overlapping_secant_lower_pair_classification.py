#!/usr/bin/env python3
"""Verify the overlapping-secant classification and sixfold identification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def main() -> None:
    s, t, lam, u, n, v = sp.symbols("s t lambda u n v")
    a = sp.Matrix([1, s, 0, 0])
    a_bar = sp.Matrix([1, -s, 0, 0])
    b = sp.Matrix([1, 0, t, 0])
    b_bar = sp.Matrix([1, 0, -t, 0])
    c_vec = sp.Matrix([0, s, t, 0])
    z_vec = sp.Matrix([0, 0, 0, 1])
    planes_matrix = [
        sp.Matrix.vstack(a.T, b.T),
        sp.Matrix.vstack(a_bar.T, b_bar.T),
        sp.Matrix.vstack(c_vec.T, (a + lam * z_vec + u * a_bar).T),
        sp.Matrix.vstack((c_vec + n * a_bar).T, (a - lam * z_vec + v * a_bar).T),
    ]
    planes = tuple(tuple(tuple(row) for row in matrix.tolist()) for matrix in planes_matrix)

    coefficients = {
        bits: permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    expected = {
        (1, 0, 1, 0): -2 * lam * n * s * t,
        (1, 0, 1, 1): 2 * lam * s * t * (u - v),
    }
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    # The abstract R determinant in the adapted flag bases.
    m_symbol = sp.symbols("m")
    flag_r = sp.Matrix([[0, -m_symbol * lam], [n * lam, lam * (v - u)]])
    assert sp.factor(flag_r.det()) == m_symbol * n * lam**2

    reduced = [sp.simplify(matrix[:, [0, 1]].inv() * matrix) for matrix in planes_matrix]
    chart_coordinates = sp.Matrix(
        [entry for matrix in reduced for entry in (matrix[0, 2], matrix[0, 3], matrix[1, 2], matrix[1, 3])]
    )
    parameters = (s, t, lam, u, n, v)
    common_parameters = dict(zip(parameters, (1, 1, -2, 7, -1, 3)))
    family_jacobian = chart_coordinates.jacobian(parameters).subs(common_parameters)
    family_rows = [0, 2, 8, 9, 12, 14]
    family_minor = family_jacobian.extract(family_rows, range(6)).det()
    assert family_minor == sp.Rational(-1, 13824)
    assert family_jacobian.rank() == 6

    x = sp.symbols("x0:16")
    target = sp.symbols("z0:4")
    universal_planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        universal_planes.append(((1, 0, x0, x1), (0, 1, x2, x3)))
    universal_coefficients = {
        bits: permanent(tuple(universal_planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    anchor = (0, 1, 0, 0)
    equations = sp.Matrix(
        [
            universal_coefficients[bits]
            - universal_coefficients[anchor]
            * sp.prod(target[i] for i in range(4) if bits[i] != anchor[i])
            for bits in BITS
            if bits != anchor
        ]
    )
    variables = list(x + target)
    sample = [
        1, 0, -1, 0,
        -1, 0, -1, 0,
        sp.Rational(3, 4), sp.Rational(-1, 4), 1, 0,
        sp.Rational(1, 3), sp.Rational(2, 3),
        sp.Rational(2, 3), sp.Rational(1, 3),
        -1, 0, 0, sp.Rational(4, 5),
    ]
    substitution = dict(zip(variables, sample))
    assert equations.subs(substitution) == sp.zeros(15, 1)
    incidence_jacobian = equations.jacobian(variables).subs(substitution)
    incidence_rows = list(range(14))
    incidence_columns = list(range(12)) + [17, 18]
    incidence_minor = incidence_jacobian.extract(incidence_rows, incidence_columns).det()
    assert incidence_minor == sp.Rational(280, 729)
    assert incidence_jacobian.rank() == 14

    # Match the older sixfold certificate by source and mode symmetries.
    old_planes = [
        sp.Matrix([[1, 0, 0, -1], [0, 0, 1, 1]]),
        sp.Matrix([[1, 1, 0, 2], [0, 2, 1, 3]]),
        sp.Matrix([[1, 0, -1, 0], [0, 1, -3, -4]]),
        sp.Matrix([[1, 0, 0, 1], [0, 0, 1, -1]]),
    ]

    def transform(matrix: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([[row[3], -row[0], row[2], row[1]] for row in matrix.tolist()])

    transformed = [transform(old_planes[index]) for index in (0, 3, 2, 1)]
    common_planes = [matrix.subs(common_parameters) for matrix in planes_matrix]
    for left, right in zip(transformed, common_planes):
        assert left.rref()[0] == right.rref()[0]

    generic_parameters = dict(zip(parameters, (1, 2, 3, 4, 5, 6)))
    generic_planes = tuple(
        tuple(
            tuple(sp.sympify(entry).subs(generic_parameters) for entry in row)
            for row in plane
        )
        for plane in planes
    )
    pair_profile = [
        pair_matrix(generic_planes[i], generic_planes[j]).rank()
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert pair_profile == [2, 3, 4, 3, 4, 4]
    rank_two_kernel = pair_matrix(generic_planes[0], generic_planes[1]).nullspace()
    assert [sp.Matrix(2, 2, vector).rank() for vector in rank_two_kernel] == [1, 1]

    print(
        json.dumps(
            {
                "status": "pass",
                "flag_determinant": str(sp.factor(flag_r.det())),
                "family_tangent_minor": str(family_minor),
                "incidence_rank": int(incidence_jacobian.rank()),
                "incidence_minor": str(incidence_minor),
                "pair_profile": [int(value) for value in pair_profile],
                "kernel_support_intersection": 1,
                "identified_component": "known six-dimensional lower-pair component",
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
