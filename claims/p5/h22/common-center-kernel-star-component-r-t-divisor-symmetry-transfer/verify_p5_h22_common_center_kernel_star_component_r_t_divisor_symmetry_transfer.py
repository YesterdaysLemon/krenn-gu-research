#!/usr/bin/env python3
"""Verify component 23's exact r=0 to t=0 weighted-H22 symmetry transfer."""

from __future__ import annotations

import itertools
import json

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model, permanent4

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/common-center-kernel-star")

from verify_p5_h31_common_center_kernel_star_component_generic_obstruction import (
    rows,
    shifted,
)



WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
ROW_PULLBACK = (0, 1, 3, 2)
ALPHA_SCALES = (-1, -1, 1, 1)


def source_u(row):
    return (-row[1], -row[0], row[2], row[3])


def source_v(row):
    return (row[0], row[1], row[3], row[2])


def source_j(row):
    return source_v(source_u(row))


def project_homogeneous(row, extension, direction, mu, nu):
    if direction == "D01":
        return (mu * row[0] + nu * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], mu * row[2] + nu * row[3], extension)
    raise ValueError(direction)


def homogeneous_tensor(alpha, beta, extensions, direction, mu, nu):
    alpha_rows = tuple(
        project_homogeneous(alpha[i], extensions[i], direction, mu, nu)
        for i in range(4)
    )
    beta_rows = tuple(
        project_homogeneous(beta[i], extensions[4 + i], direction, mu, nu)
        for i in range(4)
    )
    return {
        word: permanent4(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }


def equal(left, right):
    return sp.cancel(sp.together(left - right)) == 0


def family_covariance(r, t, h):
    alpha, beta = rows(r, t)
    target_alpha, target_beta = rows(-t, -r)
    for i, old_i in enumerate(ROW_PULLBACK):
        assert all(
            equal(source_j(alpha[old_i])[q], ALPHA_SCALES[i] * target_alpha[i][q])
            for q in range(4)
        )
        assert all(equal(source_j(beta[old_i])[q], target_beta[i][q]) for q in range(4))

    marked = shifted(beta, alpha, h)
    target_h = (-h[0], -h[1], h[3], h[2])
    target_marked = shifted(target_beta, target_alpha, target_h)
    for i, old_i in enumerate(ROW_PULLBACK):
        assert all(
            equal(source_j(marked[old_i])[q], target_marked[i][q]) for q in range(4)
        )

    # The two generators record the relevant normalized-family Klein four.
    u_alpha, u_beta = rows(t, r)
    v_alpha, v_beta = rows(-r, -t)
    for i, old_i in enumerate(ROW_PULLBACK):
        assert all(
            equal(source_u(alpha[old_i])[q], ALPHA_SCALES[i] * u_alpha[i][q])
            for q in range(4)
        )
        assert all(equal(source_u(beta[old_i])[q], u_beta[i][q]) for q in range(4))
    for i in range(4):
        assert all(equal(source_v(alpha[i])[q], v_alpha[i][q]) for q in range(4))
        assert all(equal(source_v(beta[i])[q], v_beta[i][q]) for q in range(4))

    return alpha, marked, target_alpha, target_marked, target_h


def projected_covariance(mu, nu):
    row = sp.symbols("v0:4")
    extension = sp.Symbol("e")
    old_01 = project_homogeneous(row, extension, "D01", mu, nu)
    old_23 = project_homogeneous(row, extension, "D23", mu, nu)
    new_01 = project_homogeneous(source_j(row), extension, "D01", nu, mu)
    new_23 = project_homogeneous(source_j(row), extension, "D23", nu, mu)
    assert new_01 == (-old_01[0], old_01[2], old_01[1], extension)
    assert new_23 == (-old_23[1], -old_23[0], old_23[2], extension)

    # U exchanges only D01's weight; V exchanges only D23's weight.
    assert project_homogeneous(source_u(row), extension, "D01", nu, mu) == (
        -old_01[0],
        old_01[1],
        old_01[2],
        extension,
    )
    assert project_homogeneous(source_u(row), extension, "D23", mu, nu) == (
        -old_23[1],
        -old_23[0],
        old_23[2],
        extension,
    )
    assert project_homogeneous(source_v(row), extension, "D01", mu, nu) == (
        old_01[0],
        old_01[2],
        old_01[1],
        extension,
    )
    assert project_homogeneous(source_v(row), extension, "D23", nu, mu) == old_23


def permanent_invariance():
    entries = sp.symbols("z0:16")
    matrix = tuple(tuple(entries[4 * i + j] for j in range(4)) for i in range(4))
    transformed = tuple(source_j(row) for row in matrix)
    assert sp.expand(permanent4(transformed) - permanent4(matrix)) == 0


def tensor_covariance(r, t, h, x, mu, nu):
    alpha, marked, target_alpha, target_marked, target_h = family_covariance(r, t, h)
    target_x = (-x[0], -x[1], x[3], x[2], x[4], x[5], x[7], x[6])
    old = {
        direction: homogeneous_tensor(alpha, marked, x, direction, mu, nu)
        for direction in ("D01", "D23")
    }
    target = {
        direction: homogeneous_tensor(
            target_alpha, target_marked, target_x, direction, nu, mu
        )
        for direction in ("D01", "D23")
    }
    checked = {}
    for direction, projected_scale in (("D01", -1), ("D23", 1)):
        count = 0
        for word in WORDS:
            old_word = (word[0], word[1], word[3], word[2])
            row_scale = sp.prod(ALPHA_SCALES[i] for i in range(4) if word[i] == 0)
            assert equal(
                target[direction][word],
                projected_scale * row_scale * old[direction][old_word],
            )
            count += 1
        checked[direction] = count

    # Anchor the homogeneous convention to both repository weight charts.
    for direction in ("D01", "D23"):
        finite = build_model(alpha, marked, x, direction, "finite", mu)
        infinity = build_model(alpha, marked, x, direction, "infinity", None)
        homogeneous_finite = homogeneous_tensor(alpha, marked, x, direction, mu, 1)
        homogeneous_infinity = homogeneous_tensor(alpha, marked, x, direction, 1, 0)
        for word in WORDS:
            assert equal(homogeneous_finite[word], finite["coefficients"][word])
            assert equal(homogeneous_infinity[word], infinity["coefficients"][word])

    return checked, target_h, target_x


def main():
    r, t, mu, nu = sp.symbols("r t mu nu")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")

    projected_covariance(mu, nu)
    permanent_invariance()
    tensor_counts, target_h, target_x = tensor_covariance(r, t, h, x, mu, nu)

    source_localizer = t * (t - 1) * (t + 1)
    target_parameter = -t
    target_localizer = sp.factor(
        target_parameter * (target_parameter - 1) * (target_parameter + 1)
    )
    assert sp.expand(target_localizer + source_localizer) == 0
    assert source_j(source_j(sp.symbols("v0:4"))) == sp.symbols("v0:4")
    parameter_image = (-t, -r)
    parameter_twice = (-parameter_image[1], -parameter_image[0])
    assert parameter_twice == (r, t)
    assert (-target_h[0], -target_h[1], target_h[3], target_h[2]) == h
    assert (
        -target_x[0],
        -target_x[1],
        target_x[3],
        target_x[2],
        *target_x[4:6],
        target_x[7],
        target_x[6],
    ) == x

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "source_mode_map": "(-v1,-v0,v3,v2)",
                "row_permutation": [0, 1, 3, 2],
                "parameter_map": ["-t", "-r"],
                "marking_map": ["-h0", "-h1", "h3", "h2"],
                "extension_map": ["-x0", "-x1", "x3", "x2", "x4", "x5", "x7", "x6"],
                "homogeneous_weight_map": "[mu:nu] -> [nu:mu]",
                "tensor_words_checked_per_direction": tensor_counts,
                "mixed_words_checked_per_direction": len(MIXED_WORDS),
                "pure_words_checked_per_direction": 2,
                "permanent_preserved_exactly": True,
                "source_localizer": str(source_localizer),
                "target_localizer_pullback": str(target_localizer),
                "target_constant_profile_open_boundaries": {
                    "chart_boundary": ["r=0"],
                    "special_all_pair_transferred_separately": ["r=1", "r=-1"],
                },
                "source_theorem": "VERIFIED_CONSTANT_PROFILE_OPEN_EMPTY_ON_r_ZERO",
                "source_special_theorem": "VERIFIED_SPECIAL_ALL_PAIR_FIBRES_EMPTY",
                "transferred_claim": "VERIFIED_AFFINE_NONZERO_EMPTY_ON_t_ZERO",
                "direct_twenty_one_minor_route_used": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
