#!/usr/bin/env python3
"""Close component 22's finite-D23 rho=E=0 residual chart."""

from __future__ import annotations

import functools
import json

import sympy as sp

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V
from verify_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_h1_nonzero_supplement import (
    E,
    kernel,
)

ROWS = (
    (0, 1, 2, 3, 4, 5, 7),
    (0, 1, 2, 3, 4, 6, 7),
    (0, 1, 2, 3, 5, 6, 7),
    (0, 1, 2, 4, 5, 6, 7),
    (0, 1, 2, 3, 4, 7, 8),
    (0, 1, 2, 3, 4, 7, 10),
    (0, 1, 2, 3, 4, 7, 11),
)
COLUMNS = (0, 1, 2, 3, 4, 5, 6)


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def cleared_row(entries):
    denominators = [sp.factor(sp.fraction(sp.together(entry))[1]) for entry in entries]
    multiplier = functools.reduce(sp.lcm, denominators, sp.Integer(1))
    result = [sp.cancel(multiplier * entry) for entry in entries]
    assert all(sp.fraction(entry)[1] == 1 for entry in result)
    return result


def selected_minor_unit_ideal(matrix):
    rows = [cleared_row(list(matrix.row(index))) for index in range(14)]
    declarations = []
    for index, row_indices in enumerate(ROWS):
        entries = [
            sg(rows[row_index][column])
            for row_index in row_indices
            for column in range(7)
        ]
        declarations.append(f"matrix N{index}[7][7]=" + ",".join(entries) + ";")
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(h1,h2,h3,z),dp;",
            "option(redSB);",
            *declarations,
            "ideal I="
            + ",".join(f"det(N{index})" for index in range(len(ROWS)))
            + ",z*h1*h2-1;",
            "I=slimgb(I); ideal J=std(I);",
            '"RESULT:"+string(size(J))+":"+string(reduce(1,J)==0);',
            "quit;",
        )
    )
    return V.run_singular(
        "rho_zero_E_zero_selected_minor_unit_ideal", program, timeout=120
    )


def main():
    coefficient = sp.factor(sp.diff(E, V.h0))
    expected_coefficient = V.A * V.D - V.A + V.R * V.D
    assert sp.expand(coefficient - expected_coefficient) == 0
    h0_solution = sp.cancel(-E.subs(V.h0, 0) / coefficient)
    assert sp.cancel(E.subs(V.h0, h0_solution)) == 0

    substitutions = {V.rho: 0, V.h0: h0_solution}
    specialized_matrix = V.mixed_matrix.subs(substitutions, simultaneous=True)
    specialized_kernel = kernel.subs(V.h0, h0_solution)
    assert all(
        sp.cancel(entry) == 0 for entry in specialized_matrix * specialized_kernel
    )

    parameter = sp.Symbol("tau")
    extension_substitution = {
        **substitutions,
        **{V.x[index]: parameter * specialized_kernel[index] for index in range(8)},
    }
    A_on_kernel = sp.cancel(
        V.model["A"].subs(extension_substitution, simultaneous=True)
    )
    B_on_kernel = sp.factor(
        V.model["B"].subs(extension_substitution, simultaneous=True)
    )
    assert A_on_kernel == 0
    assert sp.cancel(B_on_kernel - 2 * (V.D + 1) * parameter) == 0

    seven_column_matrix = specialized_matrix.extract(range(14), COLUMNS)
    certificate = selected_minor_unit_ideal(seven_column_matrix)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23 rho=0, E=0, h1*h2!=0",
                "claim_label": "VERIFIED_EMPTY",
                "E_h0_coefficient": str(coefficient),
                "h0_solution": str(h0_solution),
                "mixed_minor_rows": ROWS,
                "mixed_minor_columns": COLUMNS,
                "minor_unit_ideal_certificate": certificate,
                "mixed_rank": 7,
                "kernel_line": [str(entry) for entry in specialized_kernel],
                "A_on_kernel": "0",
                "B_on_kernel": "2*(D+1)*tau",
                "residual_chart_closed": True,
                "rho_zero_h1_nonzero_closed_with_prior_results": True,
                "rho_zero_all_markings_closed_with_prior_h1_zero_result": True,
                "generic_weighted_H22_fibre_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
