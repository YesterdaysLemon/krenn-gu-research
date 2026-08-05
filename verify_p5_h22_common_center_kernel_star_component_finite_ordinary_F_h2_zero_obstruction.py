#!/usr/bin/env python3
"""Verify the ordinary-weight F=0, h2=0 component-23 H22 obstruction."""

from __future__ import annotations

import json
import subprocess

import sympy as sp

import verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement as D
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


def main():
    r, t, lam = D.r, D.t, D.lam
    h, x = D.h, D.x

    F0 = sp.factor(D.F.subs(h[2], 0))
    h1_coefficient = sp.factor(sp.diff(F0, h[1]))
    expected_coefficient = -r * (lam - 1) * (r - t) * (r * t - 1)
    assert sp.factor(h1_coefficient - expected_coefficient) == 0
    h1_solution = sp.cancel(-F0.subs(h[1], 0) / h1_coefficient)
    assert sp.cancel(F0.subs(h[1], h1_solution)) == 0

    alpha, canonical = rows(r, t)
    marked = shifted(canonical, alpha, h)
    models = (
        build_model(alpha, marked, x, "D01", "finite", lam),
        build_model(alpha, marked, x, "D23", "finite", lam),
    )
    substitutions = {h[2]: 0, h[1]: h1_solution}
    generators = [
        coefficient_row(equation.subs(substitutions, simultaneous=True), x)
        for model in models
        for equation in model["mixed"]
    ]
    relation = "u*lam*(lam-1)*(lam+1)-1"
    generators.extend(
        "[" + ",".join(relation if column == row else "0" for column in range(8)) + "]"
        for row in range(8)
    )
    expected = ",".join(f"gen({index})" for index in range(1, 9))
    program = "\n".join(
        (
            "ring R=(0,r,t),(h0,h3,lam,u),dp;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(size(M));',
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
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:8"], completed.stdout

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(r,t)",
                "component": 23,
                "direction": "finite ordinary weight, F=0 and h2=0",
                "claim_label": "VERIFIED_EMPTY",
                "F_h1_coefficient": str(h1_coefficient),
                "h1_solution": str(h1_solution),
                "localization": "u*lambda*(lambda-1)*(lambda+1)=1",
                "localized_mixed_module_full": True,
                "branch_closed_for_all_ordinary_weights": True,
                "remaining_ordinary_residual": "F=0, h2!=0, and (h3=0 or H=0)",
                "generic_finite_all_markings_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
