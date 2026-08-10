#!/usr/bin/env python3
"""Verify that the component-25 rational terminal survivor is a false positive."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    project,
)
from verify_p5_h22_unequal_endpoint_inward_star_component_partial import coordinates
from verify_p5_h31_marked_basis_open_branch import one_marked_map
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-endpoint-inward-star")

from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    pure_basis,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def projected_marked_rows(alpha, beta, extension, marking, direction, slope):
    alpha_p = tuple(
        project(alpha[index], extension[index], direction, "finite", slope)
        for index in range(4)
    )
    canonical_beta_p = tuple(
        project(beta[index], extension[4 + index], direction, "finite", slope)
        for index in range(4)
    )
    beta_p = tuple(
        tuple(
            canonical_beta_p[index][coordinate]
            + marking[index] * alpha_p[index][coordinate]
            for coordinate in range(4)
        )
        for index in range(4)
    )
    return alpha_p, beta_p


def main():
    started = time.perf_counter()
    e, j, k, s = map(sp.Rational, (-5, 2, 3, -1))
    slope = sp.Rational(1, 3)
    extension = tuple(
        map(
            sp.Rational,
            (
                sp.Rational(13, 448),
                sp.Rational(-33, 56),
                sp.Rational(-1, 56),
                sp.Rational(-3, 64),
                sp.Rational(-1, 28),
                sp.Rational(79, 448),
                sp.Rational(1, 28),
                sp.Rational(5, 32),
            ),
        )
    )
    alpha, beta = pure_basis(e, j, k, s)
    canonical = coordinates(alpha, beta, extension, "D01", "finite", slope)
    assert canonical[WORDS[0]] == 1
    singletons = tuple(
        canonical[tuple(int(index == mode) for index in range(4))] for mode in range(4)
    )
    marking = tuple(-value for value in singletons)
    assert marking == (0, sp.Rational(5, 16), 2, sp.Rational(-38, 21))

    rank_table = {}
    minor_0123 = {}
    projected = {}
    for direction in ("D01", "D23"):
        alpha_p, beta_p = projected_marked_rows(
            alpha, beta, extension, marking, direction, slope
        )
        projected[direction] = (alpha_p, beta_p)
        matrices = tuple(one_marked_map(mode, alpha_p, beta_p) for mode in range(4))
        rank_table[direction] = tuple(matrix.rank() for matrix in matrices)
        minor_0123[direction] = tuple(
            sp.factor(matrix.extract((0, 1, 2, 3), range(4)).det())
            for matrix in matrices
        )

    assert rank_table == {"D01": (3, 3, 3, 3), "D23": (4, 4, 4, 4)}
    assert minor_0123["D01"] == (0, 0, 0, 0)
    assert minor_0123["D23"] == (
        sp.Rational(-380369, 9261),
        sp.Rational(-97669, 903168),
        sp.Rational(-505, 451584),
        sp.Rational(-6829, 8232),
    )

    alpha_01, beta_01 = projected["D01"]
    marked_d01 = {
        word: permanent(
            tuple(
                beta_01[index] if word[index] else alpha_01[index] for index in range(4)
            )
        )
        for word in WORDS
    }
    assert marked_d01[WORDS[0]] == 1
    assert marked_d01[WORDS[-1]] == 0
    assert all(marked_d01[word] == 0 for word in WORDS[1:-1])

    obstruction = one_marked_map(1, *projected["D23"]).extract((0, 4, 5, 6), range(4))
    expected_obstruction = sp.Matrix(
        (
            (sp.Rational(31, 672), sp.Rational(-79, 672), 0, 0),
            (sp.Rational(-1, 84), sp.Rational(1, 28), 0, 0),
            (sp.Rational(61, 882), sp.Rational(-61, 294), sp.Rational(3, 28), 0),
            (
                sp.Rational(131, 672),
                sp.Rational(65, 224),
                sp.Rational(-3, 32),
                sp.Rational(-4, 3),
            ),
        )
    )
    assert obstruction == expected_obstruction
    assert obstruction.det() == sp.Rational(-1, 28224)

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_false_positive_excluded",
                "field": "Q",
                "component": 25,
                "binary_witness": {
                    "(e,j,k,s,lambda)": "(-5,2,3,-1,1/3)",
                    "marking": ["0", "5/16", "2", "-38/21"],
                    "marking_unique_on_C0000_equals_1": True,
                },
                "D01_one_marked_ranks": [3, 3, 3, 3],
                "D01_marked_diagonals": ["1", "0"],
                "D23_one_marked_ranks": [4, 4, 4, 4],
                "fixed_obstruction": {
                    "direction": "D23",
                    "mode": 1,
                    "rows": [0, 4, 5, 6],
                    "determinant": "-1/28224",
                },
                "witness_is_full_H22_lift": False,
                "entire_exceptional_divisor_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
