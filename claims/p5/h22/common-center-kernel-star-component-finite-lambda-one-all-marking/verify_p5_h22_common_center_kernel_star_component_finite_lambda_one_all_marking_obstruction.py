#!/usr/bin/env python3
"""Verify the finite lambda=1 all-marking H22 obstruction on component 23."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, _ = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/common-center-kernel-star")

from verify_p5_h31_common_center_kernel_star_component_generic_obstruction import (  # noqa: E402
    rows,
    shifted,
)

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (  # noqa: E402
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_partial import (  # noqa: E402
    coefficient_row,
    singular_command,
)


def main():
    r, t = sp.symbols("r t")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    alpha, canonical = rows(r, t)
    marked = shifted(canonical, alpha, h)
    models = (
        build_model(alpha, marked, x, "D01", "finite", sp.Integer(1)),
        build_model(alpha, marked, x, "D23", "finite", sp.Integer(1)),
    )
    generators = ",".join(
        coefficient_row(equation, x) for model in models for equation in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(equation, x)
        for model in models
        for equation in (model["A"], model["B"])
    )
    expected = ",".join(f"gen({index})" for index in (1, 2, 3, 4, 6, 7, 8))
    program = "\n".join(
        (
            "ring R=(0,r,t),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            "vector A01=" + diagonals[0] + ";",
            "vector B01=" + diagonals[1] + ";",
            "vector A23=" + diagonals[2] + ";",
            "vector B23=" + diagonals[3] + ";",
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
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:1:1:1:0:7"], completed.stdout

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(r,t)",
                "component": 23,
                "direction": "finite lambda=1 all markings",
                "claim_label": "VERIFIED_EMPTY",
                "mixed_module": ["e1", "e2", "e3", "e4", "e6", "e7", "e8"],
                "module_equality_bidirectional": True,
                "diagonal_membership_A01_A23_B01_B23": [True, True, True, False],
                "lambda_one_all_markings_closed": True,
                "generic_finite_all_markings_closed": False,
                "remaining_residual_from_dense_open_supplement": [
                    "lambda=0 and h2*h3*H=0",
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
