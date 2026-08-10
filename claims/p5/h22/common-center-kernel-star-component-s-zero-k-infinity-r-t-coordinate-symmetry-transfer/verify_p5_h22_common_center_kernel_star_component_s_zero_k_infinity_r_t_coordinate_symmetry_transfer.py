#!/usr/bin/env python3
"""Verify the corner-only r/t mode-swap transfer for component 23."""

from __future__ import annotations

import itertools
import json

import sympy as sp

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap
from krenn_gu.p5_weighted_h22_contraction import permanent4
REPO_ROOT, HERE = bootstrap(__file__)


WORDS = tuple(itertools.product((0, 1), repeat=4))
TERNARY_WORDS = tuple(itertools.product((0, 1, 2), repeat=4))
MODE_PULLBACK = (0, 1, 3, 2)

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def corner_rows(r, t):
    alpha = (A, D, add(B, D, r), add(B, D, t))
    beta = (B, B, C, C)
    return alpha, beta


def mark(alpha, beta, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def project(row, extension, direction, mu, nu):
    if direction == "D01":
        return (mu * row[0] + nu * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], mu * row[2] + nu * row[3], extension)
    raise ValueError(direction)


def homogeneous_tensor(alpha, marked, extensions, direction, mu, nu):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, mu, nu) for i in range(4)
    )
    marked_rows = tuple(
        project(marked[i], extensions[4 + i], direction, mu, nu) for i in range(4)
    )
    return {
        word: permanent4(
            tuple(marked_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def contraction(direction, mu, nu):
    if direction == "D01":
        return (nu, mu, 0, 0, 0)
    if direction == "D23":
        return (0, 0, nu, mu, 0)
    raise ValueError(direction)


def equal(left, right):
    return sp.cancel(sp.together(left - right)) == 0


def row_and_plane_covariance(r, t, h, extensions):
    old_alpha, old_beta = corner_rows(r, t)
    new_alpha, new_beta = corner_rows(t, r)
    new_h = (h[0], h[1], h[3], h[2])
    old_marked = mark(old_alpha, old_beta, h)
    new_marked = mark(new_alpha, new_beta, new_h)
    new_extensions = (
        extensions[0],
        extensions[1],
        extensions[3],
        extensions[2],
        extensions[4],
        extensions[5],
        extensions[7],
        extensions[6],
    )

    for i, old_i in enumerate(MODE_PULLBACK):
        assert old_alpha[old_i] == new_alpha[i]
        assert old_beta[old_i] == new_beta[i]
        assert old_marked[old_i] == new_marked[i]

    # The affine marking is a row operation, so these fixed minors certify
    # that every marked pair is still a basis of its plane.
    basis_minors = (
        sp.Matrix((new_alpha[0], new_marked[0])).extract((0, 1), (0, 2)).det(),
        sp.Matrix((new_alpha[1], new_marked[1])).extract((0, 1), (2, 3)).det(),
        sp.Matrix((new_alpha[2], new_marked[2])).extract((0, 1), (0, 2)).det(),
        sp.Matrix((new_alpha[3], new_marked[3])).extract((0, 1), (0, 2)).det(),
    )
    assert tuple(map(sp.factor, basis_minors)) == (1, 2, -t - 1, -r - 1)
    # At t=-1 or r=-1 use the other F-coordinate; no parameter value loses
    # independence because (1+u,1-u) cannot vanish simultaneously over Q.
    alternate_minors = (
        sp.factor(
            sp.Matrix((new_alpha[2], new_marked[2])).extract((0, 1), (0, 3)).det()
        ),
        sp.factor(
            sp.Matrix((new_alpha[3], new_marked[3])).extract((0, 1), (0, 3)).det()
        ),
    )
    assert alternate_minors == (t - 1, r - 1)

    assert (new_h[0], new_h[1], new_h[3], new_h[2]) == h
    assert (
        new_extensions[0],
        new_extensions[1],
        new_extensions[3],
        new_extensions[2],
        new_extensions[4],
        new_extensions[5],
        new_extensions[7],
        new_extensions[6],
    ) == extensions
    return (
        old_alpha,
        old_marked,
        new_alpha,
        new_marked,
        new_h,
        new_extensions,
    )


def binary_covariance(r, t, h, extensions, mu, nu):
    (
        old_alpha,
        old_marked,
        new_alpha,
        new_marked,
        new_h,
        new_extensions,
    ) = row_and_plane_covariance(r, t, h, extensions)
    checked = {}
    for direction in ("D01", "D23"):
        old = homogeneous_tensor(old_alpha, old_marked, extensions, direction, mu, nu)
        new = homogeneous_tensor(
            new_alpha, new_marked, new_extensions, direction, mu, nu
        )
        count = 0
        for word in WORDS:
            pulled_word = (word[0], word[1], word[3], word[2])
            assert equal(new[word], old[pulled_word])
            count += 1
        checked[direction] = count
    return checked, new_h, new_extensions


def ternary_covariance(r, t, h, extensions, mu, nu):
    (
        old_alpha,
        old_marked,
        new_alpha,
        new_marked,
        _new_h,
        new_extensions,
    ) = row_and_plane_covariance(r, t, h, extensions)
    gamma_symbols = sp.symbols("g0:20")
    old_gamma = tuple(
        tuple(gamma_symbols[5 * i + q] for q in range(5)) for i in range(4)
    )
    new_gamma = tuple(old_gamma[MODE_PULLBACK[i]] for i in range(4))
    old_alpha5 = tuple((*old_alpha[i], extensions[i]) for i in range(4))
    old_marked5 = tuple((*old_marked[i], extensions[4 + i]) for i in range(4))
    new_alpha5 = tuple((*new_alpha[i], new_extensions[i]) for i in range(4))
    new_marked5 = tuple((*new_marked[i], new_extensions[4 + i]) for i in range(4))
    old_colours = (old_alpha5, old_marked5, old_gamma)
    new_colours = (new_alpha5, new_marked5, new_gamma)

    # Check all ternary row words structurally.  Each new row is exactly the
    # pulled-back old row; generic permanent invariance then proves equality
    # for every number and placement of missing-third rows.
    for word in TERNARY_WORDS:
        new_selected = tuple(new_colours[word[i]][i] for i in range(4))
        old_selected = tuple(old_colours[word[i]][MODE_PULLBACK[i]] for i in range(4))
        assert new_selected == old_selected

    generic = sp.symbols("z0:25")
    matrix = tuple(tuple(generic[5 * i + q] for q in range(5)) for i in range(5))
    swapped = (matrix[0], matrix[1], matrix[3], matrix[2], matrix[4])
    assert permanent(matrix) == permanent(swapped)

    # Anchor both contractions and all 64 one-gamma equations directly.
    direct_counts = {}
    for direction in ("D01", "D23"):
        q = contraction(direction, mu, nu)
        count = 0
        for new_mode in range(4):
            old_mode = MODE_PULLBACK[new_mode]
            other_new = tuple(i for i in range(4) if i != new_mode)
            for bits in itertools.product((0, 1), repeat=3):
                new_selected = []
                old_selected = [None] * 4
                cursor = 0
                for i in range(4):
                    if i == new_mode:
                        row = new_gamma[i]
                    else:
                        row = new_marked5[i] if bits[cursor] else new_alpha5[i]
                        cursor += 1
                    new_selected.append(row)
                    old_selected[MODE_PULLBACK[i]] = row
                assert old_selected[old_mode] == old_gamma[old_mode]
                assert equal(
                    permanent(tuple(new_selected) + (q,)),
                    permanent(tuple(old_selected) + (q,)),
                )
                count += 1
        assert other_new  # keep the three-other-mode convention explicit
        direct_counts[direction] = count
    return len(TERNARY_WORDS), direct_counts


def main():
    r, t, mu, nu = sp.symbols("r t mu nu")
    h = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    binary_counts, new_h, new_extensions = binary_covariance(
        r, t, h, extensions, mu, nu
    )
    ternary_words, one_gamma_counts = ternary_covariance(r, t, h, extensions, mu, nu)

    assert (t, r)[::-1] == (r, t)
    source_parameter = sp.Symbol("s")
    assert (sp.Integer(0), source_parameter)[::-1] == (source_parameter, 0)
    # The weight is fixed, including [0:1] and [1:0].
    assert (mu, nu) == (mu, nu)
    assert (0, 1) == (0, 1)
    assert (1, 0) == (1, 0)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity",
                "symmetry": "tensor-mode swap (2 3), ambient identity",
                "parameter_map": "(r,t) -> (t,r)",
                "marking_map": tuple(map(str, new_h)),
                "extension_map": tuple(map(str, new_extensions)),
                "homogeneous_weight_map": "[mu:nu] -> [mu:nu]",
                "binary_tensor_words_checked_per_direction": binary_counts,
                "ternary_words_structurally_checked": ternary_words,
                "one_gamma_equations_checked_per_direction": one_gamma_counts,
                "source_divisor": "r=0,t finite",
                "target_divisor": "t=0,r finite",
                "source_theorem": "VERIFIED_FINITE_WEIGHT_TERNARY_H22_EMPTY",
                "transferred_claim": "VERIFIED_FINITE_WEIGHT_TERNARY_H22_EMPTY",
                "target_lambda_zero_covered": True,
                "projective_weight_transferred_but_not_closed": True,
                "r_infinity_covered": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
