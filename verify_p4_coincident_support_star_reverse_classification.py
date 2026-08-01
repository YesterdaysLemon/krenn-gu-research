#!/usr/bin/env python3
"""Verify the projective reverse classification of the component-21 star."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_rank(left: sp.Matrix, right: sp.Matrix) -> int:
    return sp.Matrix.hstack(
        *(
            product(left.row(i).T, right.row(j).T)
            for i in range(2)
            for j in range(2)
        )
    ).rank()


def plucker(plane: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [plane[:, columns].det() for columns in itertools.combinations(range(4), 2)]
    )


def proportional(left: sp.Matrix, right: sp.Matrix) -> bool:
    return sp.Matrix.hstack(left, right).rank() == 1


def main() -> None:
    alpha, ell, aa, b, d, e, f, g, h, j, k, n = sp.symbols(
        "alpha ell aa b d e f g h j k n"
    )
    beta, phi = sp.symbols("beta phi", nonzero=True)
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))

    planes = (
        sp.Matrix.vstack((A - alpha * C).T, (aa * A + b * B + d * D).T),
        sp.Matrix.vstack((ell * A + C).T, A.T),
        sp.Matrix.vstack(C.T, (e * A + f * B + g * D).T),
        sp.Matrix.vstack((h * A + j * C + k * B + n * D).T, (A + ell * C).T),
    )
    coefficients = {
        bits: sp.factor(
            permanent([planes[mode].row(bits[mode]) for mode in range(4)])
        )
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    expected = {
        (0, 0, 1, 0): 4 * (alpha + ell) * (f * k - g * n),
        (0, 1, 1, 0): 4 * (f * k - g * n),
        (1, 0, 0, 0): -4 * (b * k - d * n),
        (1, 0, 1, 0): 4
        * (
            aa * ell * f * k
            - aa * ell * g * n
            + b * e * ell * k
            + b * ell * f * h
            - b * f * j
            - d * e * ell * n
            - d * ell * g * h
            + d * g * j
        ),
        (1, 1, 1, 0): 4
        * (aa * f * k - aa * g * n + b * e * k + b * f * h - d * e * n - d * g * h),
        (1, 1, 1, 1): 4 * (b * f - d * g),
    }
    assert set(support) == set(expected)
    assert all(sp.factor(support[bits] - value) == 0 for bits, value in expected.items())

    parallel = {b: beta * n, d: beta * k, f: phi * n, g: phi * k}
    T1111 = sp.factor(coefficients[(1, 1, 1, 1)].subs(parallel, simultaneous=True))
    T1110 = sp.factor(coefficients[(1, 1, 1, 0)].subs(parallel, simultaneous=True))
    T1010 = sp.factor(coefficients[(1, 0, 1, 0)].subs(parallel, simultaneous=True))
    assert sp.factor(T1111 - 4 * beta * phi * (n**2 - k**2)) == 0
    assert sp.factor(T1110 - h * T1111) == 0
    assert sp.factor(T1010 - ell * T1110 + j * T1111) == 0

    source_diagonal = sp.diag(1, 1, 1 / (n + k), 1 / (n - k))
    assert sp.simplify((n * B + k * D).T * source_diagonal) == B.T
    assert sp.simplify((k * B + n * D).T * source_diagonal) == D.T

    # Finite placement in the component-21 mode-zero plane.
    p = beta / aa
    q = beta / (alpha * aa)
    target0 = sp.Matrix.vstack((A - alpha * C).T, (aa * A + beta * B).T)
    component0 = sp.Matrix.vstack((A + p * B).T, (C + q * B).T)
    assert proportional(plucker(target0), plucker(component0))

    # Vertical projective point and its three endpoint analogues in the
    # intrinsic (A^C,A^B,C^B) coordinates.
    t = sp.symbols("t", nonzero=True)
    vertical_limit = sp.Matrix((0, 1, -alpha))
    generic_arc = sp.Matrix((1, 1 / t, -alpha / t))
    assert sp.simplify(t * generic_arc).subs(t, 0) == vertical_limit
    assert sp.simplify(t * sp.Matrix((1, 1 / t, 0))).subs(t, 0) == sp.Matrix((0, 1, 0))
    assert sp.simplify(t * sp.Matrix((1, 0, -1 / t))).subs(t, 0) == sp.Matrix((0, 0, -1))

    # Profiles in the original homogeneous component family.  The endpoint
    # p=0 remains all-pair; the displayed sample is the advertised boundary.
    kappa = sp.symbols("kappa")

    def component_planes(p0: sp.Expr, q0: sp.Expr) -> tuple[sp.Matrix, ...]:
        return (
            sp.Matrix.vstack((A + p0 * B).T, (C + q0 * B).T),
            sp.Matrix.vstack(A.T, C.T),
            sp.Matrix.vstack(C.T, (B + kappa * A).T),
            sp.Matrix.vstack((A + ell * C).T, D.T),
        )

    generic = tuple(
        plane.subs({kappa: 1, ell: 2}) for plane in component_planes(2, 3)
    )
    endpoint = tuple(
        plane.subs({kappa: 1, ell: 2}) for plane in component_planes(0, 3)
    )
    generic_profile = tuple(pair_rank(generic[i], generic[j]) for i, j in PAIRS)
    endpoint_profile = tuple(pair_rank(endpoint[i], endpoint[j]) for i, j in PAIRS)
    assert generic_profile == (3, 4, 4, 3, 3, 4)
    assert endpoint_profile == (3, 3, 4, 3, 3, 4)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "coincident-support rank-one star with signature (1,1,1,0)",
                "nonzero_purity_forces": [
                    "(b,d)=beta(n,k)",
                    "(f,g)=phi(n,k)",
                    "h=j=0",
                    "beta*phi*(n^2-k^2)!=0",
                ],
                "finite_component21_placement": True,
                "vertical_projective_placement": True,
                "kernel_line_endpoints_placed": True,
                "generic_pair_profile": generic_profile,
                "endpoint_pair_profile": endpoint_profile,
                "other_star_orientations_classified": False,
                "special_projective_P5_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
