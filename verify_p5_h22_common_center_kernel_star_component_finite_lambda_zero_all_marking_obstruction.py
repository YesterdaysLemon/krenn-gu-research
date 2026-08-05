#!/usr/bin/env python3
"""Verify the three lambda=0 residual branches for component-23 finite H22."""

from __future__ import annotations

import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)
from verify_p5_h31_common_center_kernel_star_component_generic_obstruction import (
    rows,
    shifted,
)

r, t = sp.symbols("r t")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
alpha, canonical = rows(r, t)
marked = shifted(canonical, alpha, h)
models = (
    build_model(alpha, marked, x, "D01", "finite", sp.Integer(0)),
    build_model(alpha, marked, x, "D23", "finite", sp.Integer(0)),
)

H0_COEFFICIENT = 4 * r**2 - 2 * r * t - 2 * r + 2 * t**2 + 2 * t - 4
H0_CONSTANT = -(r**2) - r * t + r - t + 2
H0 = H0_COEFFICIENT * h[3] + H0_CONSTANT
H0_SOLUTION = -H0_CONSTANT / H0_COEFFICIENT


def module_branch(label, substitutions, variables):
    generators = ",".join(
        coefficient_row(equation.subs(substitutions, simultaneous=True), x)
        for model in models
        for equation in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(equation.subs(substitutions, simultaneous=True), x)
        for model in models
        for equation in (model["A"], model["B"])
    )
    expected = ",".join(f"gen({index})" for index in range(1, 9))
    program = "\n".join(
        (
            "ring R=(0,r,t),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            "vector A01=" + diagonals[0] + "; vector B01=" + diagonals[1] + ";",
            "vector A23=" + diagonals[2] + "; vector B23=" + diagonals[3] + ";",
            (
                '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"'
                '+string(reduce(A01,M)==0)+":"+string(reduce(A23,M)==0)+":"'
                '+string(reduce(B01,M)==0)+":"+string(reduce(B23,M)==0)+":"'
                "+string(size(M));"
            ),
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:1:1:1:1:8"], (label, completed.stdout)
    return label


def main():
    assert sp.cancel(H0.subs(h[3], H0_SOLUTION)) == 0
    certificates = (
        module_branch("lambda_zero_h2_zero", {h[2]: 0}, (h[0], h[1], h[3])),
        module_branch("lambda_zero_h3_zero", {h[3]: 0}, (h[0], h[1], h[2])),
        module_branch(
            "lambda_zero_H_zero",
            {h[3]: H0_SOLUTION},
            (h[0], h[1], h[2]),
        ),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(r,t)",
                "component": 23,
                "direction": "finite lambda=0 all markings",
                "claim_label": "VERIFIED_EMPTY_WITH_PRIOR_FACTOR_COVER",
                "prior_cover_required": "h2*h3*H0=0",
                "H0": str(H0),
                "H0_solution_for_h3": str(H0_SOLUTION),
                "branch_certificates": certificates,
                "each_branch_mixed_module_full": True,
                "lambda_zero_all_markings_closed": True,
                "generic_finite_all_markings_closed": False,
                "remaining_residual_from_dense_open_supplement": [
                    "lambda not in {0,1,-1}, F=0 and h2*h3*H=0",
                ],
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
