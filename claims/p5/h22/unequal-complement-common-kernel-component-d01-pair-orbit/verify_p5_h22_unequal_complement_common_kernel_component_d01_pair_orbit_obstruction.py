#!/usr/bin/env python3
"""Verify the component-22 finite-D01 weighted-H22 obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model, project

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from krenn_gu.p5_marked_basis import one_marked_map
from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)




def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def clear(expression):
    return sp.expand(sp.fraction(sp.together(expression))[0])


def f3_expression(A, R, D, h0, h3, rho):
    return sp.expand(
        8 * A**3 * D * h0 * rho - 8 * A**3 * D * h0 - 2 * A**3 * D * rho
        + 2 * A**3 * D + 6 * A**3 * rho - 6 * A**3
        + 4 * A**2 * D * R * h0 * rho - 20 * A**2 * D * R * h0
        - A**2 * D * R * rho + 5 * A**2 * D * R
        + 8 * A**2 * D * h0 * h3 * rho - 8 * A**2 * D * h0 * h3
        - 2 * A**2 * D * h3 * rho + 2 * A**2 * D * h3
        + 3 * A**2 * R * rho - 15 * A**2 * R + 6 * A**2 * h3 * rho
        - 6 * A**2 * h3 - 2 * A * D * R**2 * h0 * rho
        - 10 * A * D * R**2 * h0 + 2 * A * D * R**2
        + 8 * A * D * R * h0 * h3 * rho - 8 * A * D * R * h0 * h3
        - 2 * A * D * R * h3 * rho + 2 * A * D * R * h3
        - 2 * A * R**2 * rho - 8 * A * R**2 + 6 * A * R * h3 * rho
        - 6 * A * R * h3 - D * R**3 * h0 * rho - D * R**3 * h0
        + 2 * D * R**2 * h0 * h3 * rho - 2 * D * R**2 * h0 * h3
        - R**3 * rho - R**3 + 2 * R**2 * h3 * rho - 2 * R**2 * h3
    )


def model_data():
    A, R, D, rho = sp.symbols("A R D rho")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inverse = sp.Symbol("u")
    alpha, canonical = component_rows(A, R, D)
    beta = shifted(canonical, alpha, h)
    model = build_model(alpha, beta, z, "D01", "finite", rho)
    projected_alpha = tuple(
        project(alpha[i], z[i], "D01", "finite", rho) for i in range(4)
    )
    projected_beta = tuple(
        project(beta[i], z[4 + i], "D01", "finite", rho) for i in range(4)
    )
    base_equations = (*model["mixed"], model["A"] - 1, inverse * model["B"] - 1)
    return A, R, D, rho, h, z, inverse, projected_alpha, projected_beta, base_equations


def radical_decomposition(data):
    A, R, D, rho, h, z, inverse, _alpha, _beta, equations = data
    s = 2 * A + R
    f3 = f3_expression(A, R, D, h[0], h[3], rho)
    primes = (
        (
            2 * h[3] - s,
            h[2],
            D * h[0] + 1,
            2 * R * (A + R) * (rho - 1) * h[1]
            + (rho + 1) * (s * rho - (2 * A + 3 * R)),
        ),
        (
            2 * h[3] - s,
            h[1],
            D * h[0] + 1,
            R * (rho - 1) * (s * rho - R) * h[2]
            + (rho + 1) * (s * rho - (2 * A + 3 * R)),
        ),
        (h[2], h[1], f3),
    )
    eliminated = z + (inverse,)
    variables = eliminated + h + (rho,)
    lines = [
        'LIB "primdec.lib";',
        "ring RR=(0,A,R,D),(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
        "option(redSB);",
        "ideal I=" + ",".join(sg(clear(value)) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "list L=minAssGTZ(J);",
    ]
    for index, prime in enumerate(primes, 1):
        lines.extend(
            (
                f"ideal Q{index}=L[{index}]; Q{index}=std(Q{index});",
                f"ideal P{index}=" + ",".join(sg(clear(value)) for value in prime) + f"; P{index}=std(P{index});",
                f"ideal QP{index}=simplify(reduce(Q{index},P{index}),2);",
                f"ideal PQ{index}=simplify(reduce(P{index},Q{index}),2);",
            )
        )
    lines.extend(
        (
            "ideal H=intersect(P1,P2,P3); H=std(H);",
            (
                '"RESULT:"+string(size(L)==3)+":"'
                '+string((size(QP1)==0)&&(size(PQ1)==0)&&(size(QP2)==0)&&(size(PQ2)==0)&&(size(QP3)==0)&&(size(PQ3)==0))+":"'
                '+string(size(J))+":"+string(size(H));'
            ),
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), text=True, capture_output=True, timeout=180, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (completed.stdout, completed.stderr)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1:12:10"], completed.stdout
    return primes


def unit_branch(data, branch, generators, minors):
    _A, _R, _D, rho, h, z, inverse, alpha, beta, equations = data
    variables = z + (inverse,) + h + (rho,)
    lines = [
        "ring RR=(0,A,R,D),(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
    ]
    minor_names = []
    for index, (mode, rows) in enumerate(minors):
        submatrix = one_marked_map(mode, alpha, beta).extract(rows, range(4))
        entries = ",".join(sg(entry) for entry in submatrix)
        lines.extend(
            (
                f"matrix N{index}[4][4]=" + entries + ";",
                f"poly f{index}=det(N{index});",
            )
        )
        minor_names.append(f"f{index}")
    equation_text = [sg(clear(value)) for value in (*equations, *generators)]
    lines.extend(
        (
            "ideal I=" + ",".join((*equation_text, *minor_names)) + ";",
            "I=slimgb(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    program = "\n".join(lines)
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=60, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (branch, completed.stdout, completed.stderr)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1"], (branch, completed.stdout)
    return {"branch": branch, "generators_used": list(map(str, generators)), "minors": [(mode, list(rows)) for mode, rows in minors], "unit_ideal": True}


def main():
    data = model_data()
    _A, _R, _D, _rho, h, _z, _inverse, _alpha, _beta, _equations = data
    primes = radical_decomposition(data)
    units = (
        unit_branch(data, "P1", primes[0], ((0, (0, 1, 3, 7)), (3, (0, 1, 2, 7)))),
        unit_branch(data, "P2", primes[1], ((3, (0, 1, 2, 7)), (2, (0, 1, 5, 7)))),
        unit_branch(data, "P3_superset", (h[1], h[2]), ((0, (0, 1, 3, 7)), (3, (0, 1, 3, 7)))),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(A,R,D)",
                "component": 22,
                "pair_orbit": "finite D01 plus weight infinity",
                "projection_standard_basis_size": 12,
                "radical_prime_count": 3,
                "radical_intersection_basis_size": 10,
                "prime_generators": [[str(value) for value in prime] for prime in primes],
                "branch_unit_ideals": units,
                "finite_D01_pair_orbit_empty": True,
                "weight_infinity_reuses_H31_deletion": 1,
                "complementary_D23_pair_orbit_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
