#!/usr/bin/env python3
"""Replay the exact partial D23 weighted-H22 cover on component twenty-two.

This is deliberately a partial obstruction.  The residual resultant branch
recorded in the companion note is not certified empty here.
"""

from __future__ import annotations

import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
    project,
)
from verify_p5_h31_marked_basis_open_branch import one_marked_map
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

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
w, v = sp.symbols("w v")
s = 2 * A + R

alpha, canonical = component_rows(A, R, D)
marked = shifted(canonical, alpha, (h0, h1, h2, h3))
model = build_model(alpha, marked, x, "D23", "finite", rho)
projected_alpha = tuple(
    project(alpha[i], x[i], "D23", "finite", rho) for i in range(4)
)
projected_beta = tuple(
    project(marked[i], x[4 + i], "D23", "finite", rho) for i in range(4)
)
mixed_matrix = sp.Matrix(
    [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
)

N0_0137 = one_marked_map(0, projected_alpha, projected_beta).extract(
    (0, 1, 3, 7), range(4)
)
N1_0127 = one_marked_map(1, projected_alpha, projected_beta).extract(
    (0, 1, 2, 7), range(4)
)
N1_0147 = one_marked_map(1, projected_alpha, projected_beta).extract(
    (0, 1, 4, 7), range(4)
)
MINORS = (N0_0137, N1_0127, N1_0147)

f2 = s * h2 + 1
f3 = 2 * h3 - s
f6 = (D - 1) * rho + D + 1
f7 = (A * D + A + R) * rho + A * D - A - R
f8 = (A * D + A + R * D) * rho + A * D - A + R * D
L = (
    (A * D + A + R * D) * h0 * rho
    + (A * D - A + R * D) * h0
    + R * rho
    + s
)
T = (
    (A**2 * D - 3 * A**2 - 3 * A * R - R**2) * rho
    + A**2 * D
    + 3 * A**2
    + 3 * A * R
    + R**2
)
G = (
    (4*A**2*D**2 - 4*A**2*D + 4*A*R*D**2 - 4*A*R*D + R**2*D**2 - R**2*D) * h0 * rho
    + (2*A**3*D**2 + 2*A**3*D + 4*A**2*R*D**2 + 2*A**2*R + A*R**2*D**2 + A*R**2) * h2 * rho
    + (-4*A**2*D**2 + 4*A**2*D - 4*A*R*D**2 + 4*A*R*D - R**2*D**2 + R**2*D) * h0
    + (-2*A**3*D**2 + 2*A**3*D - 4*A**2*R*D**2 - 2*A**2*R - A*R**2*D**2 - A*R**2) * h2
    + (-A**2*D**2 + 5*A**2*D - 2*A**2 + 4*A*R*D - A*R + R**2*D) * rho
    + A**2*D**2 - 3*A**2*D + 2*A**2 - 4*A*R*D + A*R - R**2*D
)
G2 = (
    (-8*A**2*D + A*R*D**2 - 7*A*R*D - R**2*D) * h0*h2*rho
    + (-8*A**2*D - A*R*D**2 - 7*A*R*D - R**2*D) * h0*h2
    + (-A*D**2 - A*D - R*D) * h0*rho
    + (2*A**2*D - 6*A**2 - A*R*D**2 + 2*A*R*D - 5*A*R - R**2) * h2*rho
    + (A*D**2 - A*D - R*D) * h0
    + (2*A**2*D - 6*A**2 + A*R*D**2 + 2*A*R*D - 5*A*R - R**2) * h2
    + (A*D**2 - A*D - 2*A - R) * rho
    - A*D**2 - A*D - 2*A - R
)


def sg(expression):
    return str(sp.factor(sp.fraction(sp.together(expression))[0])).replace("**", "^")


def matrix_declaration(name, matrix, substitutions):
    entries = [
        sg(16 * matrix[row, column].subs(substitutions, simultaneous=True))
        for row in range(4)
        for column in range(4)
    ]
    return f"matrix {name}[4][4]=" + ",".join(entries) + ";"


def run_singular(label, program, timeout=300):
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
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
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1"], (label, completed.stdout)
    return label


def unit_case(label, substitutions, minor_indices=(0, 1, 2), extra=(), saturation=None):
    substitutions = dict(substitutions)
    remaining = [z for z in (h0, h1, h2, h3, rho) if z not in substitutions]
    variables = [*x, *remaining, w]
    equations = [*model["mixed"], model["A"] - 1, w * model["B"] - 1, *extra]
    if saturation is not None:
        variables.append(v)
        equations.append(v * saturation - 1)
    equations = [e.subs(substitutions, simultaneous=True) for e in equations]
    declarations = [
        matrix_declaration(f"N{index}", MINORS[minor_index], substitutions)
        for index, minor_index in enumerate(minor_indices)
    ]
    program = "\n".join(
        [
            "ring K=(0,A,R,D),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            *declarations,
            "ideal I=" + ",".join(map(sg, equations))
            + "," + ",".join(f"det(N{i})" for i in range(len(declarations))) + ";",
            "I=slimgb(I);",
            "ideal J=std(I);",
            '"RESULT:"+string(size(J))+":"+string(reduce(1,J)==0);',
            "quit;",
        ]
    )
    return run_singular(label, program)


def determinant_associate(label, rows, substitutions, expected):
    matrix = mixed_matrix.extract(rows, range(8)).subs(substitutions, simultaneous=True)
    remaining = sorted(
        (set().union(*(entry.free_symbols for entry in matrix)) | expected.free_symbols)
        - {A, R, D},
        key=str,
    )
    entries = [sg(16 * matrix[row, column]) for row in range(8) for column in range(8)]
    program = "\n".join(
        [
            "ring K=(0,A,R,D),(" + ",".join(map(str, remaining)) + "),dp;",
            "matrix M[8][8]=" + ",".join(entries) + ";",
            "poly a=det(M);",
            "poly b=" + sg(expected) + ";",
            "ideal A0=a; ideal B0=b;",
            '"RESULT:"+string(size(std(A0)))+":"+string((reduce(a,std(B0))==0)&&(reduce(b,std(A0))==0));',
            "quit;",
        ]
    )
    return run_singular(label, program, timeout=120)


def main():
    closed = []

    cover0 = f2 * f3 * rho * (rho - 1) * f6 * f7 * f8 * (rho + 1) ** 2
    closed.append(determinant_associate("h1_zero_primary_factor_cover", tuple(range(8)), {h1: 0}, cover0))

    cover1 = h2 * f2 * rho * f6 * f7 * L * G * (rho + 1) ** 2
    closed.append(determinant_associate(
        "f3_secondary_factor_cover", (1, 2, 3, 5, 6, 7, 9, 12), {h1: 0, h3: s/2}, cover1
    ))
    cover2 = f2 * rho * (rho - 1) * T * L * G2 * (rho + 1) ** 2
    closed.append(determinant_associate(
        "G_tertiary_factor_cover", (0, 2, 3, 6, 7, 9, 10, 11), {h1: 0, h3: s/2}, cover2
    ))

    q1 = {
        h1: 0, h2: 0, h3: s/2,
        rho: (3*A*D + 5*A + 2*R*D + 3*R)/(3*A*D - 5*A + 2*R*D - 3*R),
        h0: (A*D - 3*A - 2*R)/(2*D*s),
    }
    q2 = {
        h1: 0, h2: -1/s, h3: -s/2,
        rho: (A*D - A - R)/(A*D + A + R), h0: -1/(D - 1),
    }
    q3 = {h0: 1, h1: 1/R, h2: 1/R, h3: s/2, rho: -1}
    closed.extend((
        unit_case("Q1_rank_obstruction", q1, (0,)),
        unit_case("Q2_rank_obstruction", q2, (1,)),
        unit_case("Q3_rank_obstruction", q3, (2,)),
    ))

    for label, substitutions in (
        ("h1_zero_f2", {h1: 0, h2: -1/s}),
        ("h1_zero_rho", {h1: 0, rho: 0}),
        ("h1_zero_rho_minus_1", {h1: 0, rho: 1}),
        ("h1_zero_f6", {h1: 0, rho: -(D+1)/(D-1)}),
        ("h1_zero_f7", {h1: 0, rho: -(A*D-A-R)/(A*D+A+R)}),
        ("h1_zero_f8", {h1: 0, rho: -(A*D-A+R*D)/(A*D+A+R*D)}),
        ("h1_zero_rho_plus_1", {h1: 0, rho: -1}),
    ):
        closed.append(unit_case(label, substitutions))

    closed.append(unit_case(
        "f3_h2_zero", {h1: 0, h2: 0, h3: s/2}, (0,)
    ))
    sat_L = h2 * f2 * rho * f6 * f7 * (rho + 1)
    closed.append(unit_case(
        "f3_L_branch", {h1: 0, h3: s/2}, extra=(L,), saturation=sat_L
    ))
    rho_T = -(A**2*D + 3*A**2 + 3*A*R + R**2)/(A**2*D - 3*A**2 - 3*A*R - R**2)
    sat_T = h2 * f2 * rho * (rho - 1) * f6 * f7 * (rho + 1) * L
    closed.append(unit_case(
        "f3_G_T_branch", {h1: 0, h3: s/2, rho: rho_T},
        extra=(G,), saturation=sat_T,
    ))

    print(json.dumps({
        "status": "pass",
        "field": "Q(A,R,D)",
        "component": 22,
        "direction": "finite D23",
        "claim_label": "VERIFIED_PARTIAL",
        "closed_exact_cases": closed,
        "residual_unknown": "h1=0, 2*h3=s, G=G2=0 away from h2*f2*rho*(rho-1)*f6*f7*(rho+1)*L=0; all h1!=0 cases not already covered by the displayed primary factors also remain unclassified",
        "generic_weighted_H22_fibre_closed": False,
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
