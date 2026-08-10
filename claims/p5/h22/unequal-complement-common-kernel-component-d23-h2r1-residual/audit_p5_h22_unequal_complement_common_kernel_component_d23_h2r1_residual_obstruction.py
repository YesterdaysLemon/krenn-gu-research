#!/usr/bin/env python3
"""No-import rational audit of the component-22 R*h2=1 residual slice."""

from __future__ import annotations

import json

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)




def main() -> None:
    A, R, D = sp.symbols("A R D")
    h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
    x = sp.symbols("x0:8")

    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
    )

    parameter_point = {A: 2, R: 1, D: 3, h1: 0, h2: 1, h3: sp.Rational(5, 2)}
    # At this point G=0 and G2=0 away from rho=-1 give this unique solution.
    residual_point = {h0: sp.Rational(-1, 15), rho: sp.Rational(55, 79)}
    substitutions = {**parameter_point, **residual_point}
    specialized = matrix.subs(substitutions, simultaneous=True)
    rows0 = (0, 1, 2, 5, 6, 8, 9, 10)
    rows1 = (0, 1, 3, 4, 7, 10, 11, 12)
    determinant0 = specialized.extract(rows0, range(8)).det(method="domain-ge")
    determinant1 = specialized.extract(rows1, range(8)).det(method="domain-ge")
    assert determinant0 == 0
    assert determinant1 == sp.Rational(-28153111608840683520000, 19203908986159)

    # Reconstruct the specialized residual equations independently.
    G = 15 * (10 * h0 * rho - 10 * h0 + 27 * rho - 19)
    G2 = -10 * (15 * h0 + 1) * (rho + 1)
    assert G.subs(residual_point) == 0
    assert G2.subs(residual_point) == 0
    assert residual_point[rho] not in (0, 1, -1)

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent exact-rational audit",
                "parameter_point": [2, 1, 3],
                "residual_point": [str(residual_point[h0]), str(residual_point[rho])],
                "first_minor": str(determinant0),
                "second_minor": str(determinant1),
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
