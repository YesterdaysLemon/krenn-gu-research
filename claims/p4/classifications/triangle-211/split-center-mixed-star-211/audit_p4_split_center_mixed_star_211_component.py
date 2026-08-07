#!/usr/bin/env python3
"""Independent no-import audit for the split-center mixed star component."""

from __future__ import annotations

import itertools
import json

import sympy as sp

PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[i].row(bits[i]) for i in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def transform(row, permutation, scales):
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def main():
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    k, s, tau = sp.Rational(2), sp.Rational(3), sp.Rational(2)
    c = (tau - k * s) / (1 - k * s * tau)
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((A + c * C + k * B - k * D).T, C.T),
        sp.Matrix.vstack(D.T, (tau * A + C - k * tau * B).T),
    )
    permutation = (2, 0, 3, 1)
    scales = (sp.Rational(2), sp.Rational(3), sp.Rational(5), sp.Rational(7))
    moved = tuple(
        sp.Matrix.vstack(
            transform(plane.row(0), permutation, scales).T,
            transform(plane.row(1), permutation, scales).T,
        )
        for plane in planes
    )
    tensor = coefficients(moved)
    pure_support = {"".join(map(str, bits)): str(value) for bits, value in tensor.items() if value}
    assert pure_support == {"1111": "9240"}
    pair_matrices = {
        edge: pair_matrix(moved[edge[0]], moved[edge[1]]) for edge in PAIRS
    }
    profile = tuple(pair_matrices[edge].rank() for edge in PAIRS)
    assert profile == (3, 3, 3, 4, 4, 4)
    relation_ranks = []
    for edge in ((0, 1), (0, 2), (0, 3)):
        kernel = pair_matrices[edge].nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    # Independent projective endpoint h=0, followed by the same source move.
    endpoint = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + 2 * D).T, (B + 3 * C).T),
        sp.Matrix.vstack((A - sp.Rational(1, 6) * C + 2 * B - 2 * D).T, C.T),
        sp.Matrix.vstack(D.T, (A - 2 * B).T),
    )
    endpoint_tensor = coefficients(endpoint)
    assert {bits: value for bits, value in endpoint_tensor.items() if value} == {
        (1, 1, 1, 1): 24
    }

    # X2<->X3 changes epsilon=+1,k=2 into epsilon=-1,k=-2.
    swap = (0, 1, 3, 2)
    sign_moved = tuple(
        sp.Matrix.vstack(
            sp.Matrix([plane.row(0)[swap[index]] for index in range(4)]).T,
            sp.Matrix([plane.row(1)[swap[index]] for index in range(4)]).T,
        )
        for plane in planes
    )
    assert coefficients(sign_moved)[(1, 1, 1, 1)] == 44
    minus_k = -k
    minus_epsilon = -1
    minus_sheet = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + minus_k * D).T, (B + s * C).T),
        sp.Matrix.vstack(
            (
                A
                + c * C
                + minus_epsilon * minus_k * B
                - minus_k * D
            ).T,
            C.T,
        ),
        sp.Matrix.vstack(
            D.T,
            (tau * A + C - minus_epsilon * minus_k * tau * B).T,
        ),
    )
    assert all(
        sp.Matrix.vstack(sign_moved[index], minus_sheet[index]).rank() == 2
        for index in range(4)
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import audit",
                "field": "Q",
                "source_permutation": permutation,
                "source_scales": [str(value) for value in scales],
                "pure_support": pure_support,
                "pair_profile": profile,
                "relation_ranks": relation_ranks,
                "projective_h_zero_endpoint": True,
                "sign_sheet_source_swap": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
