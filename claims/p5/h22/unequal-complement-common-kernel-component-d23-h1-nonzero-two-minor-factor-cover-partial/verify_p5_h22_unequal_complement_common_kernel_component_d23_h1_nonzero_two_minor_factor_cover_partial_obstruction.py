#!/usr/bin/env python3
"""Verify the exact second-cofactor cover on component 22's h1 chart."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/unequal-complement-common-kernel-component-d23-pair-orbit-partial")

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V



import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_"
    "TWO_MINOR_FACTOR_COVER_PARTIAL_OBSTRUCTION.md"
)
FIRST_ROWS = tuple(range(8))
SECOND_ROWS = (1, 2, 3, 5, 6, 7, 9, 12)


def native_associate(matrix, clearing_factor, expected):
    cleared = matrix.applyfunc(lambda entry: sp.expand(clearing_factor * entry))
    assert all(sp.denom(entry) == 1 for entry in cleared)
    determinant = DomainMatrix.from_Matrix(cleared).det().as_expr()
    quotient = sp.cancel(determinant / expected)
    numerator, denominator = sp.fraction(quotient)
    assert quotient != 0
    assert quotient.free_symbols <= {V.A, V.R, V.D}
    assert sp.factor(determinant - quotient * expected) == 0
    return sp.factor(numerator), sp.factor(denominator)


def factors():
    cap_h = 2 * V.A * V.h1 + 1
    cap_u = 2 * V.h0 * V.f6 + (3 - V.D) * V.rho - (V.D + 1)
    cap_v = (
        (
            2 * V.A**2 * V.D**2
            + 2 * V.A**2 * V.D
            + 5 * V.A * V.R * V.D**2
            - 2 * V.A * V.R * V.D
            - V.A * V.R
            + V.D**2 * V.R**2
            - V.R**2
        )
        * V.h2
        * V.rho
        + (
            -2 * V.A**2 * V.D**2
            + 2 * V.A**2 * V.D
            - 5 * V.A * V.R * V.D**2
            - 2 * V.A * V.R * V.D
            + V.A * V.R
            - V.D**2 * V.R**2
            + V.R**2
        )
        * V.h2
        + (V.A * V.D + V.A + V.D**2 * V.R - V.D * V.R + V.R) * V.rho
        + V.A * V.D
        - V.A
        - V.D**2 * V.R
        - V.D * V.R
        - V.R
    )
    return cap_h, cap_u, cap_v


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero second-cofactor partial obstruction",
        "divisors in (2) remain **UNKNOWN**",
        "No finite field",
        "conjecture remain **UNRESOLVED**",
    ):
        assert phrase in theorem

    _cap_h, cap_u, cap_v = factors()

    second_matrix = V.mixed_matrix.extract(SECOND_ROWS, range(8)).subs(
        V.h1, -1 / (2 * V.A), simultaneous=True
    )
    second_expected = (
        V.h2 * V.f2 * V.rho * (V.rho + 1) ** 2 * V.f7 * V.f8 * cap_u * cap_v
    )
    second = native_associate(second_matrix, 16 * V.A, second_expected)
    expected_second = -(2**33) * V.A**8 * V.D * V.s**3 * (V.D + 1)
    assert sp.factor(second[0] - expected_second) == 0
    assert second[1] == 1

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23 h1!=0, rho!=0,-1",
                "context_first_minor_rows": FIRST_ROWS,
                "context_first_minor_replayed_here": False,
                "second_minor_rows": SECOND_ROWS,
                "second_minor_quotient": [str(value) for value in second],
                "rank_drop_cover": "on 2*A*h1+1=0: h2*f2*f7*f8*U*V=0",
                "displayed_residual_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
