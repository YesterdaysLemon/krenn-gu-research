#!/usr/bin/env python3
"""Close component 22's generic finite-D23 rho=-1 weighted-H22 slice."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_RHO_MINUS_ONE_OBSTRUCTION.md"
)

ROWS = (
    (0, 1, 2, 3, 4, 5, 8),
    (0, 1, 3, 4, 5, 6, 8),
    (0, 1, 3, 4, 5, 7, 8),
    (0, 1, 3, 4, 5, 8, 10),
    (0, 1, 3, 4, 5, 8, 12),
)
COLUMNS = (0, 1, 2, 3, 4, 5, 6)


def polynomial_string(expression):
    value = sp.cancel(expression)
    numerator, denominator = sp.fraction(value)
    assert denominator == 1
    return str(sp.expand(numerator)).replace("**", "^")


def rank_drop_certificate(matrix, expected, q3, q4):
    cleared = sp.Matrix(
        [[sp.cancel(16 * entry) for entry in matrix.row(i)] for i in range(14)]
    )
    assert all(sp.fraction(entry)[1] == 1 for entry in cleared)
    declarations = []
    for index, row_indices in enumerate(ROWS):
        entries = [
            polynomial_string(cleared[row, column])
            for row in row_indices
            for column in COLUMNS
        ]
        declarations.append(f"matrix M{index}[7][7]=" + ",".join(entries) + ";")

    def ideal_string(values):
        return ",".join(V.sg(value) for value in values)

    program = "\n".join(
        (
            "ring K=(0,A,R,D),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            *declarations,
            "ideal I=" + ",".join(f"det(M{i})" for i in range(len(ROWS))) + ";",
            "I=slimgb(I); ideal J=std(I);",
            "ideal E=" + ideal_string(expected) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            "ideal P3=" + ideal_string(q3) + "; P3=std(P3);",
            "ideal P4=" + ideal_string(q4) + "; P4=std(P4);",
            "ideal U=intersect(P3,P4); U=std(U);",
            "ideal EU=simplify(reduce(E,U),2); ideal UE=simplify(reduce(U,E),2);",
            (
                '"RESULT:"+string((size(E)==4)&&(size(JE)==0)&&(size(EJ)==0)'
                '&&(size(EU)==0)&&(size(UE)==0))+":1";'
            ),
            "quit;",
        )
    )
    marker = V.run_singular(
        "rho_minus_one_five_minor_rank_drop_ideal", program, timeout=120
    )
    assert marker == "rho_minus_one_five_minor_rank_drop_ideal"
    return marker


def main():
    tau = sp.Symbol("tau")
    kernel = sp.Matrix((-1 / V.D, 0, 0, 0, (1 - V.h0) / V.D, 0, 0, 1))
    matrix = V.mixed_matrix.subs(V.rho, -1)
    assert all(sp.cancel(entry) == 0 for entry in matrix * kernel)

    extension = {
        V.rho: -1,
        **{V.x[index]: tau * kernel[index] for index in range(8)},
    }
    A_on_kernel = sp.cancel(V.model["A"].subs(extension, simultaneous=True))
    B_on_kernel = sp.cancel(V.model["B"].subs(extension, simultaneous=True))
    assert A_on_kernel == B_on_kernel == 0

    linear = (
        2 * V.A**2 * V.R * (V.D**2 - 1) * V.h1
        - 2 * (V.A + V.R) * V.h3
        - 2 * V.A**2 * V.D**2
        + 4 * V.A**2
        + 3 * V.A * V.R
        + V.R**2
    )
    second_factor = (
        2 * (V.A + V.R) * V.h3
        + 2 * V.A**2 * V.D**2
        - 4 * V.A**2
        + V.A * V.R * V.D**2
        - 4 * V.A * V.R
        - V.R**2
    )
    quadratic = (2 * V.h3 - V.s) * second_factor
    expected = (V.R * V.h2 - 1, linear, V.h0 - 1, quadratic)

    h3_q4 = sp.cancel(
        (
            -2 * V.A**2 * V.D**2
            + 4 * V.A**2
            - V.A * V.R * V.D**2
            + 4 * V.A * V.R
            + V.R**2
        )
        / (2 * (V.A + V.R))
    )
    q3_substitutions = {
        V.h0: 1,
        V.h1: 1 / V.R,
        V.h2: 1 / V.R,
        V.h3: V.s / 2,
        V.rho: -1,
    }
    q4_substitutions = {
        V.h0: 1,
        V.h1: -1 / (2 * V.A),
        V.h2: 1 / V.R,
        V.h3: h3_q4,
        V.rho: -1,
    }
    q3_ideal = (
        V.h0 - 1,
        V.R * V.h1 - 1,
        V.R * V.h2 - 1,
        2 * V.h3 - V.s,
    )
    q4_ideal = (
        V.h0 - 1,
        2 * V.A * V.h1 + 1,
        V.R * V.h2 - 1,
        2 * (V.A + V.R) * V.h3
        + 2 * V.A**2 * V.D**2
        - 4 * V.A**2
        + V.A * V.R * V.D**2
        - 4 * V.A * V.R
        - V.R**2,
    )
    for substitutions in (q3_substitutions, q4_substitutions):
        assert all(sp.cancel(value.subs(substitutions)) == 0 for value in expected)

    rank_drop = rank_drop_certificate(matrix, expected, q3_ideal, q4_ideal)
    closed_points = (
        V.unit_case("rho_minus_one_Q3_rank_obstruction", q3_substitutions),
        V.unit_case("rho_minus_one_Q4_rank_obstruction", q4_substitutions),
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23 rho=-1",
                "claim_label": "VERIFIED_EMPTY",
                "universal_kernel": [str(entry) for entry in kernel],
                "A_on_kernel": "0",
                "B_on_kernel": "0",
                "mixed_minor_rows": ROWS,
                "mixed_minor_columns": COLUMNS,
                "rank_drop_ideal_certificate": rank_drop,
                "rank_drop_points": {
                    "Q3": {
                        str(key): str(value) for key, value in q3_substitutions.items()
                    },
                    "Q4": {
                        str(key): str(value) for key, value in q4_substitutions.items()
                    },
                },
                "closed_exact_points": closed_points,
                "rho_minus_one_slice_closed": True,
                "generic_weighted_H22_fibre_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
