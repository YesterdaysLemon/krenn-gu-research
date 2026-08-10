#!/usr/bin/env python3
"""Verify generic marked-H31 exclusion on common-singleton component 18."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p4/classifications")
ROOT = REPO_ROOT

from analyze_p4_common_singleton_local_dimension import common_singleton_family
from verify_p4_directed_zero_divisor_triangle_components import coefficients
from krenn_gu.p5_marked_basis import mixed_matrix

ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_SINGLETON_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
SAMPLE = (-3, -2, -1, -1, -1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(matrix: sp.Matrix, index: int) -> tuple[sp.Expr, ...]:
    return tuple(matrix.row(index))


def main() -> None:
    L, M, a, b, c = sp.symbols("L M a b c")
    parameters = (L, M, a, b, c)
    shifts = sp.symbols("h0:4")
    planes, v2_3, v3 = common_singleton_family(*parameters)

    # The component chart stores every plane as (e,vector).  At mode zero
    # the pure row is e and the kernel row is ell; at the other modes the
    # pure row is vi and the kernel row is e.
    alpha = (
        row(planes[0], 1),
        row(planes[1], 0),
        row(planes[2], 0),
        row(planes[3], 0),
    )
    canonical_beta = (
        row(planes[0], 0),
        row(planes[1], 1),
        row(planes[2], 1),
        row(planes[3], 1),
    )
    beta = tuple(
        tuple(
            sp.expand(
                canonical_beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    marked_planes = tuple(sp.Matrix((alpha[mode], beta[mode])) for mode in range(4))
    pure = coefficients(marked_planes)
    kappa = sp.factor(pure[(1, 1, 1, 1)])
    assert kappa != 0
    assert all(
        sp.factor(value) == 0 for word, value in pure.items() if word != (1, 1, 1, 1)
    )
    sample = dict(zip(parameters, SAMPLE, strict=True))
    assert sp.factor(kappa.subs(sample)) == 4
    assert sp.factor(v2_3.subs(sample)) == 2
    assert tuple(sp.factor(entry.subs(sample)) for entry in v3) == (1, 3, -1)

    deletion_results = []
    for distinguished in range(4):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
        assert mixed.shape == (14, 8)
        assert diagonal_alpha == sp.zeros(1, 8)
        assert diagonal_beta.shape == (1, 8)
        deletion_results.append(
            {
                "distinguished_coordinate": distinguished,
                "mixed_matrix_shape": list(mixed.shape),
                "all_kernel_diagonal": [0] * 8,
            }
        )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "component_function_field": "C(L,M,a,b,c)",
                "marking_ring": "C(L,M,a,b,c)[h0,h1,h2,h3]",
                "pure_support": {"1111": str(kappa)},
                "sample_pure_coefficient": 4,
                "deletions": deletion_results,
                "binary_neighbour_excluded": True,
                "generic_marked_H31_fibre_empty": True,
                "projective_boundary_closed": False,
                "weighted_H22_closed_by_this_theorem": False,
                "weighted_H22_companion_theorem": (
                    "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"
                ),
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
