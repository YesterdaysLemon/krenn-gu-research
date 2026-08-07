#!/usr/bin/env python3
"""Verify the disjoint-secant lower-pair P4 component."""

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
    s, t, lam, m, n, rho = sp.symbols("s t lambda m n rho")
    a = sp.Matrix([1, s, 0, 0])
    a_bar = sp.Matrix([1, -s, 0, 0])
    b = sp.Matrix([0, 0, 1, t])
    b_bar = sp.Matrix([0, 0, 1, -t])
    ell = a + lam * b_bar
    ell_bar = a - lam * b_bar
    k = a_bar + m * b
    k_bar = b + n * a_bar
    other = ell_bar + rho * a_bar
    planes_matrix = [
        sp.Matrix.vstack(a.T, b.T),
        sp.Matrix.vstack(a_bar.T, b_bar.T),
        sp.Matrix.vstack(k.T, ell.T),
        sp.Matrix.vstack(k_bar.T, other.T),
    ]
    planes = tuple(tuple(tuple(row) for row in matrix.tolist()) for matrix in planes_matrix)

    coefficients = {
        bits: permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    expected = {
        (1, 0, 0, 0): -4 * s * t * (m * n + 1),
        (1, 0, 0, 1): -4 * m * rho * s * t,
    }
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    reduced = [sp.simplify(matrix[:, [0, 2]].inv() * matrix) for matrix in planes_matrix]
    chart_coordinates = sp.Matrix(
        [entry for matrix in reduced for entry in (matrix[0, 1], matrix[0, 3], matrix[1, 1], matrix[1, 3])]
    )
    parameters = (s, t, lam, m, n, rho)
    sample_parameters = dict(zip(parameters, (1, 2, 3, 4, 5, 6)))
    family_jacobian = chart_coordinates.jacobian(parameters).subs(sample_parameters)
    family_rows = [0, 3, 8, 9, 12, 14]
    family_minor = family_jacobian.extract(family_rows, range(6)).det()
    assert family_minor == sp.Rational(48, 1331)
    assert family_jacobian.rank() == 6

    # Universal pivot-02 Segre incidence.
    x = sp.symbols("x0:16")
    z = sp.symbols("z0:4")
    universal_planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        universal_planes.append(((1, x0, 0, x1), (0, x2, 1, x3)))
    universal_coefficients = {
        bits: permanent(tuple(universal_planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    anchor = (1, 0, 0, 0)
    equations = sp.Matrix(
        [
            universal_coefficients[bits]
            - universal_coefficients[anchor]
            * sp.prod(z[i] for i in range(4) if bits[i] != anchor[i])
            for bits in BITS
            if bits != anchor
        ]
    )
    variables = list(x + z)
    sample = [
        1, 0, 0, 2,
        -1, 0, 0, -2,
        7, -48, -2, 14,
        sp.Rational(-10, 11), sp.Rational(6, 11),
        sp.Rational(-5, 11), sp.Rational(-8, 11),
        0, 0, sp.Rational(-1, 3), sp.Rational(9, 29),
    ]
    substitution = dict(zip(variables, sample))
    assert equations.subs(substitution) == sp.zeros(15, 1)
    incidence_jacobian = equations.jacobian(variables).subs(substitution)
    incidence_rows = list(range(14))
    incidence_columns = list(range(12)) + [16, 17]
    incidence_minor = incidence_jacobian.extract(incidence_rows, incidence_columns).det()
    assert incidence_minor == sp.Rational(136141760102400, 19487171)
    assert incidence_jacobian.rank() == 14

    rational_planes = tuple(
        tuple(
            tuple(sp.sympify(entry).subs(sample_parameters) for entry in row)
            for row in plane
        )
        for plane in planes
    )
    pair_profile = [
        pair_matrix(rational_planes[i], rational_planes[j]).rank()
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert pair_profile == [2, 3, 4, 3, 4, 4]
    rank_two_kernel = pair_matrix(rational_planes[0], rational_planes[1]).nullspace()
    assert [sp.Matrix(2, 2, vector).rank() for vector in rank_two_kernel] == [1, 1]
    support_pairs = []
    for vector in rank_two_kernel:
        matrix = sp.Matrix(2, 2, vector)
        left = next(column for column in matrix.columnspace())
        right = next(column for column in matrix.T.columnspace())
        left_form = sp.zeros(1, 4)
        right_form = sp.zeros(1, 4)
        for index in range(2):
            left_form += left[index] * sp.Matrix(rational_planes[0])[index, :]
            right_form += right[index] * sp.Matrix(rational_planes[1])[index, :]
        support = tuple(index for index in range(4) if left_form[index] or right_form[index])
        support_pairs.append(support)
    assert support_pairs == [(0, 1), (2, 3)]

    print(
        json.dumps(
            {
                "status": "pass",
                "family_tangent_minor": str(family_minor),
                "incidence_rank": int(incidence_jacobian.rank()),
                "incidence_minor": str(incidence_minor),
                "component_dimension": 6,
                "pair_profile": [int(value) for value in pair_profile],
                "rank_two_kernel_type": "reduced secant",
                "kernel_support_pairs": [list(pair) for pair in support_pairs],
                "component_number": 15,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
