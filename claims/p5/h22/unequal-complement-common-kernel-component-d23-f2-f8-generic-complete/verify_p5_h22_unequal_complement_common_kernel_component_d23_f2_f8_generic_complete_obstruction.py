#!/usr/bin/env python3
"""Verify component 22's generic finite-D23 H=f2=f8 closure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

for parent in Path(__file__).resolve().parents:
    if (parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(
    REPO_ROOT,
    "claims/p5/h22/unequal-complement-common-kernel-component-d23-pair-orbit-partial",
)

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

THEOREM = HERE / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_"
    "F2_F8_GENERIC_COMPLETE_OBSTRUCTION.md"
)
H0_ROWS = (0, 1, 2, 3, 4, 7, 8, 11)
H3_ROWS_A = (0, 1, 2, 3, 4, 7, 8, 9)
H3_ROWS_B = (0, 1, 2, 3, 4, 7, 8, 13)


def determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    data = [
        [field.from_sympy(sp.cancel(matrix[rows[i], column])) for column in range(8)]
        for i in range(8)
    ]
    return sp.cancel(DomainMatrix(data, (8, 8), field).det().as_expr())


def exact_equal(left, right):
    assert sp.cancel(left - right) == 0


def main() -> None:
    denominator = V.A * V.D + V.A + V.D * V.R
    numerator = V.A * V.D - V.A + V.D * V.R
    rho8 = -numerator / denominator
    exact_equal(rho8 + 1, 2 * V.A / denominator)
    assert sp.Poly(numerator, V.A, V.R, V.D) != 0

    base = V.mixed_matrix.subs(
        {
            V.h1: -1 / (2 * V.A),
            V.h2: -1 / V.s,
            V.rho: rho8,
        },
        simultaneous=True,
    )

    q11 = (
        4 * V.A**2 * V.D * V.h0
        - 3 * V.A**2 * V.D
        + V.A**2
        + 4 * V.A * V.D * V.R * V.h0
        - 3 * V.A * V.D * V.R
        + V.A * V.R
        + V.D * V.R**2 * V.h0
        - V.D * V.R**2
    )
    unit11 = (
        512
        * V.A**4
        * V.D**4
        * V.R**2
        * (V.A + V.R) ** 3
        * V.s**4
        * (4 * V.A + V.R)
        * (V.D - 1) ** 2
        * (V.D + 1) ** 3
        * numerator
        / denominator**7
    )
    det11 = determinant(base, H0_ROWS, (V.A, V.R, V.D, V.h0, V.h3))
    exact_equal(det11, unit11 * q11)

    h0_value = (V.D * (3 * V.A**2 + 3 * V.A * V.R + V.R**2) - V.A * (V.A + V.R)) / (
        V.D * V.s**2
    )
    exact_equal(q11.subs(V.h0, h0_value), 0)
    reduced = base.subs(V.h0, h0_value)

    cap_c = 8 * V.A**3 + 16 * V.A**2 * V.R + 11 * V.A * V.R**2 + 2 * V.R**3
    cap_b9 = (
        32 * V.A**5
        - 4 * V.A**4 * V.D**2 * V.R
        + 100 * V.A**4 * V.R
        - 8 * V.A**3 * V.D**2 * V.R**2
        + 116 * V.A**3 * V.R**2
        - 6 * V.A**2 * V.D**2 * V.R**3
        + 66 * V.A**2 * V.R**3
        - 2 * V.A * V.D**2 * V.R**4
        + 19 * V.A * V.R**4
        + 2 * V.R**5
    )
    cap_b13 = (
        16 * V.A**4
        + 2 * V.A**3 * V.D**2 * V.R
        + 38 * V.A**3 * V.R
        + 34 * V.A**2 * V.R**2
        - 2 * V.A * V.D**2 * V.R**3
        + 15 * V.A * V.R**3
        + 2 * V.R**4
    )
    cap_l9 = 2 * V.s * cap_c * V.h3 + cap_b9
    cap_l13 = 2 * cap_c * V.h3 + cap_b13

    unit9 = (
        -512
        * V.A**5
        * V.D**4
        * V.R
        * (V.A + V.R) ** 2
        * V.s**3
        * (V.D - 1)
        * (V.D + 1) ** 3
        * numerator
        / denominator**7
    )
    unit13 = (
        256
        * V.A**4
        * V.D**4
        * V.R
        * (V.A + V.R) ** 2
        * V.s**4
        * (V.D - 1)
        * (V.D + 1) ** 3
        * numerator
        / denominator**7
    )
    det9 = determinant(reduced, H3_ROWS_A, (V.A, V.R, V.D, V.h3))
    det13 = determinant(reduced, H3_ROWS_B, (V.A, V.R, V.D, V.h3))
    exact_equal(det9, unit9 * cap_l9)
    exact_equal(det13, unit13 * cap_l13)

    incompatibility = (
        -2 * V.A**2 * V.R * (V.A + V.R) * (4 * V.A + V.R) * (V.D - 1) * (V.D + 1)
    )
    exact_equal(cap_b9 - V.s * cap_b13, incompatibility)
    resultant = sp.factor(sp.resultant(cap_l9, cap_l13, V.h3))
    expected_resultant = (
        4 * V.A**2 * V.R * (V.A + V.R) * (4 * V.A + V.R) * (V.D - 1) * (V.D + 1) * cap_c
    )
    exact_equal(resultant, expected_resultant)
    assert sp.Poly(expected_resultant, V.A, V.R, V.D) != 0

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero generic-component branch closure",
        "whole geometric generic intersection (1) is empty",
        "after every field extension `E/K`",
        "isolated complement `2*h3+s!=0`",
        "function-field theorem",
        "rest of the `f2=0` residual",
        "global conjecture remains **UNRESOLVED**",
        "No finite-field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "closed_branch": "H=f2=f8=0",
                "rho_and_rho_plus_one_nonzero_generically": True,
                "h0_rows": H0_ROWS,
                "h3_rows": [H3_ROWS_A, H3_ROWS_B],
                "h3_resultant": str(sp.factor(expected_resultant)),
                "slope_intersection_included": True,
                "isolated_complement_closed": True,
                "pointwise_special_fibres_closed": False,
                "remaining_f2_residual_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
