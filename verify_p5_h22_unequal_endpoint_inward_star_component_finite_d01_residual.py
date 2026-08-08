#!/usr/bin/env python3
"""Verify the finite-D01 residual factor cover on component twenty-five."""

from __future__ import annotations

import itertools
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

WORDS = tuple(itertools.product((0, 1), repeat=4))


def main():
    started = time.perf_counter()
    e, j, k, s, slope, w = sp.symbols("e j k s lambda w")
    z0, z1, _, z3, _, z5, z6, z7 = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = pure_basis(e, j, k, s)
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", slope)

    # The previous residual equation is identically satisfied, and all
    # non-full canonical coordinates containing only mode zero vanish.
    residual = sp.expand((slope + 1) * extensions[2] + (slope - 1) * extensions[4])
    assert residual == 0
    assert all(
        sp.factor(tensor[word]) == 0
        for word in ((1, 0, 0, 0), (1, 0, 0, 1), (1, 1, 0, 0), (1, 1, 0, 1))
    )

    empty = tensor[(0, 0, 0, 0)]
    assert sp.factor(empty.subs(slope, 1)) == 0

    # Away from lambda=-1, the fixed-vertex equations force the other three
    # non-full coordinates containing mode zero to vanish.  Together with
    # C_empty=1, these four linear equations have the following solution.
    solution = {
        z5: z6 - k * z3,
        z1: cross * z6 - pivot * s * (slope - 1) * w - j * (k**2 - e**2) * z3 / k,
    }
    solution[z7] = (
        pivot * z6 - k**2 * cross * (slope - 1) * s * w - e * solution[z1]
    ) / (k**2 - e**2)
    solution[z0] = (
        pivot**2 * z3 - k * cross**2 * (slope + 1) * w - 1 / (2 * (slope - 1))
    ) / (k * cross)
    forced = (
        tensor[(1, 0, 1, 0)],
        tensor[(1, 0, 1, 1)],
        tensor[(1, 1, 1, 0)],
        empty - 1,
    )
    assert all(sp.factor(sp.cancel(value.subs(solution))) == 0 for value in forced)

    # The first remaining three-mode Segre equation splits into two linear
    # z3 branches.  This is an exact identity before imposing F=0.
    c1 = tensor[(0, 1, 0, 0)]
    c2 = tensor[(0, 0, 1, 0)]
    first_toric = sp.cancel((tensor[(0, 1, 1, 0)] * empty - c1 * c2).subs(solution))
    branch_a = sp.expand(1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3)
    branch_b = sp.expand(
        2 * pivot * ((slope - 1) * s * pivot - (slope + 1) * cross) * z3 - s
    )
    expected = sp.cancel(pivot * branch_a * branch_b / cross**2)
    assert sp.factor(sp.cancel(first_toric - expected)) == 0

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_factor_cover",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01",
                "input_residual": "L01=0",
                "denominator_free_parameterization": {
                    "z2": "(lambda-1)*w",
                    "z4": "-(lambda+1)*w",
                },
                "lambda_one_binary_incidence_empty": True,
                "ordinary_weight_open": "lambda^2 != 1",
                "ordinary_weight_factor_cover": {
                    "A": "1+2*(lambda-1)*(e^2-k^2)*P*z3",
                    "B": "2*P*((lambda-1)*s*P-(lambda+1)*Q)*z3-s",
                    "equation": "A*B=0",
                },
                "ordinary_factor_branches_closed": False,
                "lambda_minus_one_closed": False,
                "finite_D01_residual_closed": False,
                "finite_D23_closed": False,
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
