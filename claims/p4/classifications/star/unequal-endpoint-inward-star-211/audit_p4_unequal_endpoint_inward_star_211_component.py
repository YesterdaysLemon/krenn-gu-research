#!/usr/bin/env python3
"""Independent no-import audit for the unequal-endpoint inward component."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[index].row(bits[index]) for index in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def transform(row, permutation, scales):
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def flattening(tensor, mode):
    other_modes = tuple(index for index in range(4) if index != mode)
    columns = tuple(itertools.product((0, 1), repeat=3))
    matrix = sp.zeros(2, 8)
    for row in (0, 1):
        for column, other_bits in enumerate(columns):
            bits = [0, 0, 0, 0]
            bits[mode] = row
            for index, bit in zip(other_modes, other_bits):
                bits[index] = bit
            matrix[row, column] = tensor[tuple(bits)]
    return matrix


def main():
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    e, j, k, s = map(sp.Rational, (-2, 5, 3, -1))
    assert (e * j + k**2) * (1 + e * j * s**2) == (e + j) ** 2
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack(C.T, (A + e * B - k * D).T),
        sp.Matrix.vstack(D.T, (A - s * j * C + j * B).T),
    )
    permutation = (2, 0, 3, 1)
    scales = tuple(map(sp.Rational, (2, 3, 5, 7)))
    moved = tuple(
        sp.Matrix.vstack(
            transform(plane.row(0), permutation, scales).T,
            transform(plane.row(1), permutation, scales).T,
        )
        for plane in planes
    )
    tensor = coefficients(moved)
    pure_support = {
        "".join(map(str, bits)): str(value) for bits, value in tensor.items() if value
    }
    assert pure_support == {
        "0011": "-840",
        "0111": "2520",
        "1011": "2520",
        "1111": "-7560",
    }
    flattening_ranks = [flattening(tensor, mode).rank() for mode in range(4)]
    assert flattening_ranks == [1, 1, 1, 1]

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

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import rational audit",
                "field": "Q",
                "source_permutation": permutation,
                "source_scales": [str(value) for value in scales],
                "pure_support": pure_support,
                "flattening_ranks": flattening_ranks,
                "pair_profile": profile,
                "relation_ranks": relation_ranks,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
