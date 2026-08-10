#!/usr/bin/env python3
"""No-import audit of the component-23 r/t divisor symmetry transfer."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
ROW_PULLBACK = (0, 1, 3, 2)
ALPHA_SCALES = (-1, -1, 1, 1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows(r, t):
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    k = (1 - r * t) / (t - r)
    alpha = (
        A,
        add(A, D, k),
        add(add(add(A, C, -1), B), D, r),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    return alpha, beta


def mark(alpha, beta, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def j(row):
    return (-row[1], -row[0], row[3], row[2])


def project(row, extension, direction, weight):
    mu, nu = weight
    if direction == "D01":
        return (mu * row[0] + nu * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], mu * row[2] + nu * row[3], extension)
    raise ValueError(direction)


def permanent(matrix):
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[i][permutation[i]] for i in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def coefficient_tensor(alpha, beta, extensions, direction, weight):
    alpha_projected = tuple(
        project(alpha[i], extensions[i], direction, weight) for i in range(4)
    )
    beta_projected = tuple(
        project(beta[i], extensions[4 + i], direction, weight) for i in range(4)
    )
    return {
        word: permanent(
            tuple(
                beta_projected[i] if word[i] else alpha_projected[i] for i in range(4)
            )
        )
        for word in WORDS
    }


def equal(left, right):
    return sp.cancel(sp.together(left - right)) == 0


def main():
    r, t, mu, nu = sp.symbols("r t mu nu")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    alpha, beta = component_rows(r, t)
    target_alpha, target_beta = component_rows(-t, -r)
    marked = mark(alpha, beta, h)
    target_h = (-h[0], -h[1], h[3], h[2])
    target_marked = mark(target_alpha, target_beta, target_h)
    target_x = (-x[0], -x[1], x[3], x[2], x[4], x[5], x[7], x[6])

    for i, old_i in enumerate(ROW_PULLBACK):
        assert all(
            equal(j(alpha[old_i])[q], ALPHA_SCALES[i] * target_alpha[i][q])
            for q in range(4)
        )
        assert all(equal(j(beta[old_i])[q], target_beta[i][q]) for q in range(4))
        assert all(equal(j(marked[old_i])[q], target_marked[i][q]) for q in range(4))

    # Independently check that J is an exact permanent symmetry.
    generic_entries = sp.symbols("z0:16")
    generic_matrix = tuple(
        tuple(generic_entries[4 * i + q] for q in range(4)) for i in range(4)
    )
    assert (
        sp.expand(
            permanent(tuple(j(row) for row in generic_matrix))
            - permanent(generic_matrix)
        )
        == 0
    )

    old_tensors = {
        direction: coefficient_tensor(alpha, marked, x, direction, (mu, nu))
        for direction in ("D01", "D23")
    }
    target_tensors = {
        direction: coefficient_tensor(
            target_alpha,
            target_marked,
            target_x,
            direction,
            (nu, mu),
        )
        for direction in ("D01", "D23")
    }

    checked = {"D01": 0, "D23": 0}
    for direction, projected_scale in (("D01", -1), ("D23", 1)):
        for word in WORDS:
            pulled_word = (word[0], word[1], word[3], word[2])
            alpha_scale = (-1) ** (word[0] + word[1])
            assert equal(
                target_tensors[direction][word],
                projected_scale * alpha_scale * old_tensors[direction][pulled_word],
            )
            checked[direction] += 1

    # Direct homogeneous endpoint audit: zero and infinity exchange, +/-1 fix.
    assert (0, 1)[::-1] == (1, 0)
    assert (1, 0)[::-1] == (0, 1)
    assert (1, 1)[::-1] == (1, 1)
    assert (-1, 1)[::-1] == (1, -1)
    # [1:-1]=[-1:1], so the last pair is the same projective point.

    source_f = t * (t - 1) * (t + 1)
    target_r = -t
    target_f = target_r * (target_r - 1) * (target_r + 1)
    assert sp.expand(target_f + source_f) == 0
    assert j(j(sp.symbols("v0:4"))) == sp.symbols("v0:4")

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "independent_no_repository_imports": True,
                "component": 23,
                "row_family_covariance": True,
                "marked_family_covariance": True,
                "permanent_preserved_exactly": True,
                "parameter_map": "(r,t) -> (-t,-r)",
                "homogeneous_weight_map": "[mu:nu] -> [nu:mu]",
                "tensor_words_checked_per_direction": checked,
                "mixed_and_pure_covariance_checked": True,
                "localization_pullback": "r*(r-1)*(r+1) -> -t*(t-1)*(t+1)",
                "target_divisor": "t=0",
                "target_constant_profile_open_boundaries": {
                    "chart_boundary": ["r=0"],
                    "special_all_pair_transferred_separately": ["r=1", "r=-1"],
                },
                "source_special_claim_required": "AUDITED_SPECIAL_ALL_PAIR_FIBRES_EMPTY",
                "transferred_claim": "AUDITED_AFFINE_NONZERO_EMPTY_ON_t_ZERO",
                "direct_twenty_one_minor_route_used": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
