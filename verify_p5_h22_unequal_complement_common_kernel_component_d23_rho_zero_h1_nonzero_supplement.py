#!/usr/bin/env python3
"""Replay the exact rho=0, h1!=0 supplement for component-22 D23 H22.

The verifier closes the h2=0 branch and leaves the displayed E=0 branch
explicitly unclassified.  No finite-field calculation is used.
"""

from __future__ import annotations

import json

import sympy as sp

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

t = sp.Symbol("t")
E = (
    (V.A * V.D - V.A + V.R * V.D) * V.h0
    + (V.A**2 * V.D + 3 * V.A**2 + V.A * V.R * V.D + 2 * V.A * V.R) * V.h1
    + V.s
)
kernel = sp.Matrix(
    (
        V.D - 1,
        2,
        2,
        0,
        (V.D - 1) * V.h0 + 2,
        2 * V.h1,
        2 * V.h2,
        -(V.D - 1),
    )
)


def cofactor_associate():
    """Certify det M[0,1,3,4,5,7,9 | 1,...,7] ~ h2*E over K."""

    rows = (0, 1, 3, 4, 5, 7, 9)
    columns = (1, 2, 3, 4, 5, 6, 7)
    matrix = V.mixed_matrix.extract(rows, columns).subs(V.rho, 0)
    entries = [
        V.sg(16 * matrix[row, column]) for row in range(7) for column in range(7)
    ]
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(h0,h1,h2,h3),dp;",
            "matrix M[7][7]=" + ",".join(entries) + ";",
            "poly a=det(M);",
            "poly b=" + V.sg(V.h2 * E) + ";",
            "ideal A0=a; ideal B0=b;",
            (
                '"RESULT:"+string(size(std(A0)))+":"'
                "+string((reduce(a,std(B0))==0)&&(reduce(b,std(A0))==0));"
            ),
            "quit;",
        )
    )
    return V.run_singular("rho_zero_selected_cofactor_h2_E", program, timeout=120)


def main():
    mixed_kernel = V.mixed_matrix.subs(V.rho, 0) * kernel
    assert all(sp.cancel(entry) == 0 for entry in mixed_kernel)

    kernel_substitution = {
        V.rho: 0,
        **{V.x[index]: t * kernel[index] for index in range(8)},
    }
    A_on_kernel = sp.cancel(V.model["A"].subs(kernel_substitution, simultaneous=True))
    B_on_kernel = sp.factor(V.model["B"].subs(kernel_substitution, simultaneous=True))
    assert A_on_kernel == 0
    assert sp.cancel(B_on_kernel - 2 * (V.D + 1) * t) == 0

    closed = [
        cofactor_associate(),
        V.unit_case(
            "rho_zero_h2_zero_h1_nonzero",
            {V.rho: 0, V.h2: 0},
            saturation=V.h1,
        ),
    ]

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "claim_label": "VERIFIED_PARTIAL_SUPPLEMENT",
                "kernel": [str(entry) for entry in kernel],
                "A_on_kernel": "0",
                "B_on_kernel": "2*(D+1)*t",
                "selected_cofactor_associate": "h2*E",
                "E": str(E),
                "closed_exact_cases": closed,
                "residual_unknown": "rho=0, E=0, h1*h2!=0",
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
