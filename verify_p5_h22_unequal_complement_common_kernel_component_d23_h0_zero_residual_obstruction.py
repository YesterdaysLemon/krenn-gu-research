#!/usr/bin/env python3
"""Close component 22's finite-D23 h0=0 residual at binary level."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_partial import singular_command
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_"
    "H0_ZERO_RESIDUAL_OBSTRUCTION.md"
)

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
w, z = sp.symbols("w z")
s = 2 * A + R


def residual_polynomials():
    f2 = s * h2 + 1
    f6 = (D - 1) * rho + D + 1
    f7 = (A * D + A + R) * rho + A * D - A - R
    f8 = (A * D + A + R * D) * rho + A * D - A + R * D
    L = (A * D + A + R * D) * h0 * rho + (A * D - A + R * D) * h0 + R * rho + s
    T = (
        (A**2 * D - 3 * A**2 - 3 * A * R - R**2) * rho
        + A**2 * D
        + 3 * A**2
        + 3 * A * R
        + R**2
    )
    G = (
        (
            4 * A**2 * D**2
            - 4 * A**2 * D
            + 4 * A * R * D**2
            - 4 * A * R * D
            + R**2 * D**2
            - R**2 * D
        )
        * h0
        * rho
        + (
            2 * A**3 * D**2
            + 2 * A**3 * D
            + 4 * A**2 * R * D**2
            + 2 * A**2 * R
            + A * R**2 * D**2
            + A * R**2
        )
        * h2
        * rho
        + (
            -4 * A**2 * D**2
            + 4 * A**2 * D
            - 4 * A * R * D**2
            + 4 * A * R * D
            - R**2 * D**2
            + R**2 * D
        )
        * h0
        + (
            -2 * A**3 * D**2
            + 2 * A**3 * D
            - 4 * A**2 * R * D**2
            - 2 * A**2 * R
            - A * R**2 * D**2
            - A * R**2
        )
        * h2
        + (-(A**2) * D**2 + 5 * A**2 * D - 2 * A**2 + 4 * A * R * D - A * R + R**2 * D)
        * rho
        + A**2 * D**2
        - 3 * A**2 * D
        + 2 * A**2
        - 4 * A * R * D
        + A * R
        - R**2 * D
    )
    G2 = (
        (-8 * A**2 * D + A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2 * rho
        + (-8 * A**2 * D - A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2
        + (-A * D**2 - A * D - R * D) * h0 * rho
        + (2 * A**2 * D - 6 * A**2 - A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        * rho
        + (A * D**2 - A * D - R * D) * h0
        + (2 * A**2 * D - 6 * A**2 + A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        + (A * D**2 - A * D - 2 * A - R) * rho
        - A * D**2
        - A * D
        - 2 * A
        - R
    )
    return f2, f6, f7, f8, L, T, G, G2


def clear(expression):
    return sp.factor(sp.fraction(sp.together(expression))[0])


def singular_text(expression):
    return str(clear(expression)).replace("**", "^")


def run_singular(label, program, expected, timeout=300):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
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
    assert markers == [expected], (label, completed.stdout, expected)
    return label


def build_residual():
    f2, f6, f7, f8, L, T, G, G2 = residual_polynomials()
    substitutions = {h0: 0, h1: 0, h3: s / 2}
    restricted = tuple(
        sp.factor(polynomial.subs(substitutions, simultaneous=True))
        for polynomial in (f2, f6, f7, f8, L, T, G, G2)
    )
    f2_0, f6_0, f7_0, f8_0, L0, T0, _G0, _G20 = restricted
    assert sp.factor(L0 - (R * rho + s)) == 0
    multiplier = sp.factor(
        h2
        * f2_0
        * rho
        * (rho - 1)
        * (rho + 1)
        * f6_0
        * f7_0
        * f8_0
        * L0
        * T0
        * (R * h2 - 1)
    )
    return substitutions, restricted, multiplier


def parameter_residual_nonempty(G0, G20, multiplier):
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(h2,rho,z),dp;",
            "option(redSB);",
            "ideal P="
            + ",".join(map(singular_text, (G0, G20, z * multiplier - 1)))
            + ";",
            "P=std(P);",
            'print("RESULT:"+string(reduce(1,P)!=0)+":"+string(dim(P)));',
            "quit;",
        )
    )
    return run_singular("parameter residual", program, "RESULT:1:0")


def binary_incidence_unit(substitutions, G0, G20, multiplier):
    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    mixed = tuple(
        expression.subs(substitutions, simultaneous=True)
        for expression in model["mixed"]
    )
    diagonal_a = model["A"].subs(substitutions, simultaneous=True)
    diagonal_b = model["B"].subs(substitutions, simultaneous=True)
    equations = (
        *mixed,
        diagonal_a - 1,
        w * diagonal_b - 1,
        G0,
        G20,
        z * multiplier - 1,
    )
    variables = x + (h2, rho, w, z)
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + ";",
            "I=slimgb(I); ideal J=std(I);",
            'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
            "quit;",
        )
    )
    return run_singular("binary incidence", program, "RESULT:1:1")


def main():
    substitutions, restricted, multiplier = build_residual()
    f2_0, f6_0, f7_0, f8_0, L0, T0, G0, G20 = restricted
    parameter = parameter_residual_nonempty(G0, G20, multiplier)
    incidence = binary_incidence_unit(substitutions, G0, G20, multiplier)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "chart": "h0=h1=0, 2*h3=2*A+R, G=G2=0",
                "open_factors": tuple(
                    map(
                        str,
                        (
                            h2,
                            f2_0,
                            rho,
                            rho - 1,
                            rho + 1,
                            f6_0,
                            f7_0,
                            f8_0,
                            L0,
                            T0,
                            R * h2 - 1,
                        ),
                    )
                ),
                "parameter_residual_certificate": parameter,
                "parameter_residual_dimension": 0,
                "binary_incidence_certificate": incidence,
                "refined_residual_binary_empty": True,
                "complete_h0_zero_residual_empty_with_prior_factor_theorems": True,
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
