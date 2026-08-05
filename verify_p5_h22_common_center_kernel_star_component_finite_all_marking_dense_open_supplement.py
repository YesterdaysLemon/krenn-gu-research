#!/usr/bin/env python3
"""Verify a finite all-marking dense-open H22 supplement for component 23."""

from __future__ import annotations

import functools
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

r, t, lam = sp.symbols("r t lam")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
alpha, canonical = rows(r, t)
marked = shifted(canonical, alpha, h)
d01 = build_model(alpha, marked, x, "D01", "finite", lam)
d23 = build_model(alpha, marked, x, "D23", "finite", lam)
mixed = sp.Matrix(
    [
        [sp.diff(equation, variable) for variable in x]
        for equation in (*d01["mixed"], *d23["mixed"])
    ]
)

F = (
    (-2 * r**4 * t**2 + 2 * r**3 * t + 2 * r**2 * t**2 - 2 * r * t) * h[0] * h[2] * lam
    + (-(r**4) * t**2 + r**3 * t**3 + r**3 * t - r * t**3 - r * t + t**2)
    * h[0]
    * h[3]
    * lam
    + (r**4 * t**2 + r**3 * t**3 - r**3 * t - 2 * r**2 * t**2 - r * t**3 + r * t + t**2)
    * h[0]
    * h[3]
    + (r**4 * t**2 - r**3 * t - r**2 * t**2 + r * t) * h[0] * lam
    + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * h[1] * lam
    + (2 * r**4 - 2 * r**3 * t - 2 * r**2 + 2 * r * t) * h[2] * lam
    + (-(r**4) * t**2 + r**3 * t + r**2 * t**2 - r * t) * h[0]
    + (r**3 * t - r**2 * t**2 - r**2 + r * t) * h[1]
    + (-2 * r**3 * t + 2 * r**2 * t**2 + 2 * r * t - 2 * t**2) * h[3]
    + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * lam
    + (r**3 * t - r**2 * t**2 - r**2 + r * t)
)

H = (
    (2 * r**2 - 2 * r * t - 2 * r + 4 * t**2 + 2 * t - 4) * h[3] * lam
    + (4 * r**2 - 2 * r * t - 2 * r + 2 * t**2 + 2 * t - 4) * h[3]
    + (r**2 - r * t + r - t) * lam
    + (-(r**2) - r * t + r - t + 2)
)


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def cleared_row_entries(entries):
    denominators = [sp.factor(sp.fraction(sp.together(entry))[1]) for entry in entries]
    multiplier = functools.reduce(sp.lcm, denominators, sp.Integer(1))
    result = [sp.cancel(multiplier * entry) for entry in entries]
    assert all(sp.fraction(entry)[1] == 1 for entry in result)
    return result


def determinant_associate(label, selected_rows, expected):
    matrix = mixed.extract(selected_rows, range(8))
    entries = []
    for row_index in range(8):
        entries.extend(cleared_row_entries(list(matrix.row(row_index))))
    program = "\n".join(
        (
            "ring K=(0,r,t),(h0,h1,h2,h3,lam),dp;",
            "matrix M[8][8]=" + ",".join(map(sg, entries)) + ";",
            "poly a=det(M);",
            "poly b=" + sg(expected) + ";",
            "ideal A0=a; ideal B0=b;",
            (
                '"RESULT:"+string(size(std(A0)))+":"'
                "+string((reduce(a,std(B0))==0)&&(reduce(b,std(A0))==0));"
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
    assert markers == ["RESULT:1:1"], (label, completed.stdout)
    return label


def lambda_minus_one_module():
    minus_one_models = (
        build_model(alpha, marked, x, "D01", "finite", sp.Integer(-1)),
        build_model(alpha, marked, x, "D23", "finite", sp.Integer(-1)),
    )
    generators = ",".join(
        coefficient_row(equation, x)
        for model in minus_one_models
        for equation in model["mixed"]
    )
    program = "\n".join(
        (
            "ring R=(0,r,t),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "module E=" + ",".join(f"gen({index})" for index in range(1, 9)) + ";",
            "E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
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
    return "lambda_minus_one_all_markings_full_module"


def main():
    certificates = [
        determinant_associate(
            "D01_dense_open_minor",
            (0, 1, 3, 7, 8, 9, 11, 12),
            lam * (lam - 1) ** 2 * (lam + 1) ** 3 * F,
        ),
        determinant_associate(
            "cross_contraction_lambda_zero_minor",
            (0, 1, 2, 3, 7, 8, 9, 14),
            h[2] * h[3] * H * (lam - 1) ** 3 * (lam + 1) ** 4,
        ),
        lambda_minus_one_module(),
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(r,t)",
                "component": 23,
                "direction": "generic finite all markings",
                "claim_label": "VERIFIED_PARTIAL_SUPPLEMENT",
                "certificates": certificates,
                "F": str(F),
                "H": str(H),
                "lambda_minus_one_all_markings_closed": True,
                "residual_unknown": [
                    "lambda=1",
                    "lambda=0 and h2*h3*H=0",
                    "lambda not in {0,1,-1}, F=0 and h2*h3*H=0",
                ],
                "generic_finite_all_markings_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
