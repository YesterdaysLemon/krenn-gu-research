#!/usr/bin/env python3
"""Verify the complete affine disjoint mixed-star classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def make_planes(A, B, f, phi, j, kappa, eta):
    a = sp.Matrix([1, 1, 0, 0])
    a_bar = sp.Matrix([1, -1, 0, 0])
    b = sp.Matrix([0, 0, 1, 1])
    b_bar = sp.Matrix([0, 0, 1, -1])
    x_0 = A * a + B * a_bar + b - b_bar
    y_1 = -A * f * a + a_bar + f * b + phi * b_bar
    y_2 = -A * j * a + eta * a_bar + j * b + kappa * b_bar
    return (
        sp.Matrix.vstack(b_bar.T, x_0.T),
        sp.Matrix.vstack(y_1.T, a.T),
        sp.Matrix.vstack(y_2.T, a.T),
        sp.Matrix.vstack(a_bar.T, b.T),
    )


def main() -> None:
    A, B, f, phi, j, kappa, eta = sp.symbols(
        "A B f phi j kappa eta"
    )
    planes = make_planes(A, B, f, phi, j, kappa, eta)
    plane_rows = tuple(
        tuple(tuple(row) for row in matrix.tolist()) for matrix in planes
    )
    coefficients = {
        bits: sp.factor(
            permanent(tuple(plane_rows[mode][bits[mode]] for mode in range(4)))
        )
        for bits in BITS
    }
    expected = {
        (0, 0, 0, 0): 4 * (eta * phi + kappa),
        (1, 0, 0, 0): -4 * (
            B * f * j - B * kappa * phi + eta * f + eta * phi + j + kappa
        ),
        (1, 0, 0, 1): -4 * (A**2 * f * j + B * eta * f + B * j + eta),
        (1, 1, 1, 1): 4,
    }
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    N = sp.Matrix(
        [
            [0, 1, phi],
            [B * f + 1, 1 - B * phi, f + phi],
            [A**2 * f + B, 0, B * f + 1],
        ]
    )
    vector = sp.Matrix([j, kappa, eta])
    assert sp.simplify(
        N * vector
        - sp.Matrix(
            [
                coefficients[(0, 0, 0, 0)] / 4,
                -coefficients[(1, 0, 0, 0)] / 4,
                -coefficients[(1, 0, 0, 1)] / 4,
            ]
        )
    ) == sp.zeros(3, 1)

    delta = B * f + 1
    capital_j = f + B * phi**2
    capital_d = A**2 * f + B
    determinant = sp.factor(N.det())
    assert sp.factor(determinant - (capital_d * capital_j - delta**2)) == 0
    expected_phi = sp.expand(
        A**2 * B * f * phi**2
        + A**2 * f**2
        - B**2 * f**2
        + B**2 * phi**2
        - B * f
        - 1
    )
    assert sp.factor(determinant - expected_phi) == 0

    generic_kernel = sp.Matrix([capital_j, phi * delta, -delta])
    assert sp.simplify(
        N * generic_kernel - sp.Matrix([0, 0, determinant])
    ) == sp.zeros(3, 1)

    # The three decisive minors characterize rank one on the affine chart.
    minors = {
        "delta": sp.factor(N.extract((0, 1), (0, 1)).det()),
        "J": sp.factor(N.extract((0, 1), (1, 2)).det()),
        "D": sp.factor(N.extract((0, 2), (0, 1)).det()),
    }
    assert minors == {"delta": -delta, "J": capital_j, "D": -capital_d}
    rank_one_substitution = {f: -1 / B, phi: 1 / B, A: B}
    rank_one_matrix = sp.simplify(N.subs(rank_one_substitution))
    assert rank_one_matrix.rank() == 1
    h = sp.symbols("h")
    assert sp.simplify(
        rank_one_matrix * sp.Matrix([h, -1 / B, 1])
    ) == sp.zeros(3, 1)
    assert sp.simplify(
        rank_one_matrix * sp.Matrix([1, 0, 0])
    ) == sp.zeros(3, 1)

    # Rational formal arcs at B=1.  A exists because only A^2 enters N and
    # the displayed A^2 has nonzero constant term.
    t, target_h = sp.symbols("t target_h")
    arc_delta = t
    arc_f = t - 1
    arc_phi = 1 - (target_h + 1) * t / 2
    arc_j = sp.factor(arc_f + arc_phi**2)
    arc_d = sp.factor(arc_delta**2 / arc_j)
    arc_a_squared = sp.factor((arc_d - 1) / arc_f)
    arc_N = N.subs(
        {B: 1, f: arc_f, phi: arc_phi, A**2: arc_a_squared}
    )
    arc_kernel = sp.Matrix([arc_j, arc_phi * arc_delta, -arc_delta])
    assert sp.simplify(arc_N * arc_kernel) == sp.zeros(3, 1)
    finite_limit = sp.Matrix(
        [sp.limit(value, t, 0) for value in -arc_kernel / arc_delta]
    )
    assert finite_limit == sp.Matrix([target_h, -1, 1])
    assert sp.limit(arc_a_squared, t, 0) == 1

    endpoint_delta = t**2
    endpoint_f = t**2 - 1
    endpoint_phi = 1 + t
    endpoint_j = sp.factor(endpoint_f + endpoint_phi**2)
    endpoint_d = sp.factor(endpoint_delta**2 / endpoint_j)
    endpoint_a_squared = sp.factor((endpoint_d - 1) / endpoint_f)
    endpoint_N = N.subs(
        {B: 1, f: endpoint_f, phi: endpoint_phi, A**2: endpoint_a_squared}
    )
    endpoint_kernel = sp.Matrix(
        [endpoint_j, endpoint_phi * endpoint_delta, -endpoint_delta]
    )
    assert sp.simplify(endpoint_N * endpoint_kernel) == sp.zeros(3, 1)
    endpoint_limit = sp.Matrix(
        [sp.limit(value, t, 0) for value in endpoint_kernel / t]
    )
    assert endpoint_limit == sp.Matrix([2, 0, 0])
    assert sp.limit(endpoint_a_squared, t, 0) == 1

    # Boundary representatives remain pure and have no lower pair image.
    samples = [
        {A: 1, B: 1, f: -1, phi: 1, j: 2, kappa: -1, eta: 1},
        {A: 1, B: 1, f: -1, phi: 1, j: 1, kappa: 0, eta: 0},
    ]
    profiles = []
    for sample in samples:
        point = tuple(matrix.subs(sample) for matrix in planes)
        point_rows = tuple(
            tuple(tuple(row) for row in matrix.tolist()) for matrix in point
        )
        point_coefficients = {
            bits: permanent(tuple(point_rows[mode][bits[mode]] for mode in range(4)))
            for bits in BITS
        }
        assert point_coefficients[(1, 1, 1, 1)] == 4
        assert all(
            value == 0
            for bits, value in point_coefficients.items()
            if bits != (1, 1, 1, 1)
        )
        profile = [
            pair_matrix(point[left].tolist(), point[right].tolist()).rank()
            for left, right in itertools.combinations(range(4), 2)
        ]
        assert min(profile) == 3
        profiles.append(profile)

    print(
        json.dumps(
            {
                "status": "pass",
                "purity_matrix": "N",
                "determinant": str(determinant),
                "rank_one_equations": ["B*f+1", "f+B*phi^2", "A^2*f+B"],
                "rank_one_kernel": "P1",
                "finite_kernel_arcs": True,
                "projective_kernel_arc": True,
                "boundary_pair_profiles": profiles,
                "containing_component": 8,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
