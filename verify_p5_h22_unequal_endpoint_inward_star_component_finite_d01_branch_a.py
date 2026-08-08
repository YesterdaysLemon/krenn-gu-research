#!/usr/bin/env python3
"""Verify the ordinary finite-D01 A-branch linear reduction."""

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


def reduce_mod_f(numerator, hypersurface, k, parameters):
    domain = sp.QQ.frac_field(*parameters)
    polynomial = sp.Poly(sp.expand(numerator), k, domain=domain)
    modulus = sp.Poly(hypersurface, k, domain=domain)
    return polynomial.rem(modulus).as_expr()


def main():
    started = time.perf_counter()
    e, j, k, s, slope, w = sp.symbols("e j k s lambda w")
    z0, z1, _, z3, _, z5, z6, z7 = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    leading = 1 + e * j * s**2
    hypersurface = sp.expand(pivot * leading - cross**2)
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = pure_basis(e, j, k, s)
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", slope)

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
    branch_z3 = -1 / (2 * (slope - 1) * (e**2 - k**2) * pivot)

    empty = tensor[(0, 0, 0, 0)]
    c1 = tensor[(0, 1, 0, 0)]
    c3 = tensor[(0, 0, 0, 1)]
    segre_13 = tensor[(0, 1, 0, 1)] * empty - c1 * c3
    substituted = sp.cancel(segre_13.subs(solution).subs(z3, branch_z3))
    numerator = sp.fraction(substituted)[0]
    reduced = reduce_mod_f(
        numerator,
        hypersurface,
        k,
        (e, j, s, slope, w, z6),
    )
    linear_residual = sp.expand(
        2 * k * cross**2 * (e - j) * (slope - 1) * ((slope + 1) * w + z6) + j * leading
    )
    assert sp.factor(sp.cancel(reduced + cross**2 * linear_residual / leading**2)) == 0
    z6_solution = sp.factor(
        -(slope + 1) * w - j * leading / (2 * k * cross**2 * (e - j) * (slope - 1))
    )
    assert sp.factor(linear_residual.subs(z6, z6_solution)) == 0

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_linear_residual",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01",
                "weight_open": "lambda^2 != 1",
                "input_branch": "A=0",
                "A_branch_z3": "-1/(2*(lambda-1)*(e^2-k^2)*P)",
                "linear_residual": ("2*k*Q^2*(e-j)*(lambda-1)*((lambda+1)*w+z6)+j*R=0"),
                "z6_solution": "-(lambda+1)*w-j*R/(2*k*Q^2*(e-j)*(lambda-1))",
                "remaining_free_extension_parameter": "w",
                "A_branch_closed": False,
                "B_branch_closed": False,
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
