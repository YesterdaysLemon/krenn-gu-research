#!/usr/bin/env python3
"""Extract the retained-weight projection of the finite-D01 A branch."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

from verify_p5_h22_unequal_endpoint_inward_star_component_partial import coordinates
from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    pure_basis,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def main():
    started = time.perf_counter()
    e, j, k, s, slope, w = sp.symbols("e j k s lambda w")
    z0, z1, _, z3, _, z5, z6, z7 = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    leading = 1 + e * j * s**2
    hypersurface = sp.expand(pivot * leading - cross**2)
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = pure_basis(e, j, k, s)
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", slope)

    empty = tensor[WORDS[0]]
    c1 = tensor[(0, 1, 0, 0)]
    c2 = tensor[(0, 0, 1, 0)]
    c3 = tensor[(0, 0, 0, 1)]
    branch_a = 1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3
    linear_residual = (
        2 * k * cross**2 * (e - j) * (slope - 1) * ((slope + 1) * w + z6) + j * leading
    )
    equations = (
        hypersurface,
        tensor[(1, 0, 1, 0)],
        tensor[(1, 0, 1, 1)],
        tensor[(1, 1, 1, 0)],
        empty - 1,
        branch_a,
        linear_residual,
        tensor[(0, 0, 1, 1)] * empty - c2 * c3,
        tensor[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3,
    )
    expected = sp.expand((slope + 1) * ((j * s - 1) * slope - (j * s + 1)))
    program = "\n".join(
        (
            "ring r=(0,e,j,s),(z0,z1,z3,z5,z6,z7,w,k,lambda),(dp(7),dp(2));",
            "option(redSB);",
            "ideal J=" + ",".join(map(sg, equations)) + ";",
            "ideal G=std(J);",
            "ideal E=eliminate(G,z0*z1*z3*z5*z6*z7*w); E=std(E);",
            "poly target=" + sg(expected) + ";",
            '"RESULT:"+string(size(E))+":"+string(reduce(target,E)==0)+":"+string(reduce(1,E)==0);',
            '"BEGIN_PROJECTION";',
            "E;",
            '"END_PROJECTION";',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
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
    assert markers == ["RESULT:2:1:0"], completed.stdout

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_single_exceptional_weight_divisor",
                "field": "C(e,j,s)",
                "component": 25,
                "pair_orbit": "finite D01",
                "input_branch": "ordinary A=0",
                "retained_variables": ["k", "lambda"],
                "projection_generators": [
                    "F=(ej+k^2)(1+ejs^2)-(e+j)^2",
                    "(lambda+1)*((js-1)*lambda-(js+1))",
                ],
                "ordinary_weight_open": "lambda^2 != 1",
                "remaining_exceptional_weight_divisor": "(js-1)*lambda-(js+1)=0",
                "exceptional_divisor_tested": False,
                "A_branch_closed": False,
                "B_branch_closed": False,
                "finite_D01_residual_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
