#!/usr/bin/env python3
"""Verify an exact finite-D23 factor cover for component twenty-five."""

from __future__ import annotations

import json
import time

import sympy as sp

from verify_p5_h22_unequal_endpoint_inward_star_component_partial import coordinates
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


def main():
    started = time.perf_counter()
    e, j, k, s, slope = sp.symbols("e j k s lambda")
    extensions = sp.symbols("z0:8")
    z0, _, z2, z3, z4, z5, _, _ = extensions
    pivot = e * j + k**2
    cross = e + j
    alpha, beta = pure_basis(e, j, k, s)
    tensor = coordinates(alpha, beta, extensions, "D23", "finite", slope)

    empty = tensor[(0, 0, 0, 0)]
    c0001 = tensor[(0, 0, 0, 1)]
    c0100 = tensor[(0, 1, 0, 0)]
    c0101 = tensor[(0, 1, 0, 1)]
    c1000 = tensor[(1, 0, 0, 0)]
    c1100 = tensor[(1, 1, 0, 0)]
    c1101 = tensor[(1, 1, 0, 1)]

    divisor_a = sp.expand((slope - 1) * z2)
    divisor_g = sp.expand((slope - 1) * (z0 - cross * z4) - pivot * (slope + 1) * z3)
    divisor_j = sp.expand(j * s * (k * z3 - z5) - z2)
    diagonal_gap = sp.expand(empty - cross * c1000)
    coordinate_gap = sp.expand(c0101 - cross * c1101)

    assert sp.factor(c0100 - cross * c1100) == 0
    assert sp.factor(c1100 - 2 * divisor_a) == 0
    assert sp.factor(c1000 - 2 * (slope - 1) * (pivot * s * z4 + cross * z2)) == 0
    assert sp.factor(diagonal_gap - 2 * pivot * s * divisor_g) == 0

    divisor_h = sp.expand(
        j * k * s * (slope - 1) * (z0 - cross * z4)
        - pivot * (slope + 1) * (j * s * z5 + z2)
    )
    assert sp.factor(coordinate_gap - 2 * divisor_h) == 0
    assert (
        sp.factor(divisor_h - pivot * (slope + 1) * divisor_j - j * k * s * divisor_g)
        == 0
    )

    # These are the normalized fixed-vertex Segre equations for subsets
    # {0,1}, {1,3}, and {0,1,3}, kept homogeneous in C_empty.
    segre_01 = sp.expand(c1100 * empty - c1000 * c0100)
    segre_13 = sp.expand(c0101 * empty - c0100 * c0001)
    segre_013 = sp.expand(c1101 * empty**2 - c1000 * c0100 * c0001)
    assert sp.factor(segre_01 - c1100 * diagonal_gap) == 0
    assert (
        sp.factor(
            empty * segre_13
            - cross * segre_013
            - empty**2 * coordinate_gap
            + diagonal_gap * c0100 * c0001
        )
        == 0
    )

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_factor_cover",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D23",
                "necessary_cover": [
                    {"branch": "A23", "equation": "(lambda-1)*z2=0"},
                    {
                        "branch": "G23_endpoint",
                        "equations": ["G23=0", "lambda+1=0"],
                    },
                    {
                        "branch": "G23_ordinary",
                        "equations": ["G23=0", "J23=0"],
                    },
                ],
                "G23": "(lambda-1)*(z0-Q*z4)-P*(lambda+1)*z3",
                "J23": "j*s*(k*z3-z5)-z2",
                "cover_branches_closed": False,
                "finite_D23_closed": False,
                "finite_D01_residual_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
