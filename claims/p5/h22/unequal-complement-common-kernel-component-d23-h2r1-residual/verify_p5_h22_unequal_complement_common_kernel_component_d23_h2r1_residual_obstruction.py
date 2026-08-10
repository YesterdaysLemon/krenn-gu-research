#!/usr/bin/env python3
"""Verify the R*h2=1 slice of component 22's finite-D23 residual."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/unequal-complement-common-kernel-component-d23-pair-orbit-partial")

from verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction import (
    G2,
    G,
    L,
    R,
    T,
    f2,
    f6,
    f7,
    h1,
    h2,
    h3,
    mixed_matrix,
    rho,
    s,
)



import json
import subprocess

import sympy as sp


ROWS = (
    (0, 1, 2, 5, 6, 8, 9, 10),
    (0, 1, 3, 4, 7, 10, 11, 12),
)


def sg(expression: sp.Expr) -> str:
    numerator = sp.fraction(sp.together(expression))[0]
    return str(sp.factor(numerator)).replace("**", "^")


def main() -> None:
    substitutions = {h1: 0, h2: 1 / R, h3: s / 2}
    matrix = mixed_matrix.subs(substitutions, simultaneous=True)
    declarations = []
    for index, rows in enumerate(ROWS):
        entries = [sg(16 * matrix[row, column]) for row in rows for column in range(8)]
        declarations.append(f"matrix N{index}[8][8]=" + ",".join(entries) + ";")

    saturation = (f2 * rho * (rho - 1) * f6 * f7 * (rho + 1) * L * T).subs(
        substitutions, simultaneous=True
    )
    equations = [
        "det(N0)",
        "det(N1)",
        sg(G.subs(substitutions, simultaneous=True)),
        sg(G2.subs(substitutions, simultaneous=True)),
        f"z*({sg(saturation)})-1",
    ]
    program = "\n".join(
        [
            "ring K=(0,A,R,D),(h0,rho,z),dp;",
            "option(redSB);",
            *declarations,
            "ideal I=" + ",".join(equations) + ";",
            "I=slimgb(I);",
            "ideal J=std(I);",
            '"RESULT:"+string(size(J))+":"+string(reduce(1,J)==0);',
            "quit;",
        ]
    )
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
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
    assert markers == ["RESULT:1:1"], completed.stdout

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "residual_slice": "h1=0, 2*h3=2*A+R, G=G2=0, R*h2=1",
                "mixed_minor_rows": ROWS,
                "unit_ideal": True,
                "complementary_residual_closed": False,
                "h1_nonzero_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
