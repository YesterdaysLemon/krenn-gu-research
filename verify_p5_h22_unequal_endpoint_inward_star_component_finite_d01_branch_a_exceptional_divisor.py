#!/usr/bin/env python3
"""Verify the rational survivor section on the finite-D01 A divisor."""

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
    divisor = sp.expand((j * s - 1) * slope - (j * s + 1))
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
    terminal = (
        tensor[(1, 0, 1, 0)],
        tensor[(1, 0, 1, 1)],
        tensor[(1, 1, 1, 0)],
        empty - 1,
        branch_a,
        linear_residual,
        tensor[(0, 0, 1, 1)] * empty - c2 * c3,
        tensor[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3,
    )
    section = (
        hypersurface,
        divisor,
        16 * s * (e - j) * cross**2 * k * w + (j * s - 1) ** 2 * leading,
        4 * (e**2 - k**2) * pivot * z3 + (j * s - 1),
        8 * k * cross**2 * (e - j) * z6 + j * (j * s - 1) * leading,
        z5 - z6 + k * z3,
        k * z1
        - k * cross * z6
        + k * pivot * s * (slope - 1) * w
        + j * (k**2 - e**2) * z3,
        (k**2 - e**2) * z7 - pivot * z6 + k**2 * cross * (slope - 1) * s * w + e * z1,
        2 * (slope - 1) * k * cross * z0
        - 2 * (slope - 1) * pivot**2 * z3
        + 2 * (slope - 1) * k * cross**2 * (slope + 1) * w
        + 1,
    )

    # A completely rational fibre witnesses that the proper generic ideal is
    # genuinely populated and also checks all ten normalized Segre equations.
    witness = {
        e: -5,
        j: 2,
        k: 3,
        s: -1,
        slope: sp.Rational(1, 3),
        w: sp.Rational(3, 112),
        z0: sp.Rational(13, 448),
        z1: sp.Rational(-33, 56),
        z3: sp.Rational(-3, 64),
        z5: sp.Rational(79, 448),
        z6: sp.Rational(1, 28),
        z7: sp.Rational(5, 32),
    }
    assert sp.expand(hypersurface.subs(witness)) == 0
    assert sp.expand(divisor.subs(witness)) == 0
    assert all(sp.expand(equation.subs(witness)) == 0 for equation in terminal)
    singletons = tuple(
        tensor[tuple(int(index == vertex) for index in range(4))] for vertex in range(4)
    )
    segre = []
    for size in (2, 3):
        for subset in itertools.combinations(range(4), size):
            word = tuple(int(index in subset) for index in range(4))
            segre.append(
                tensor[word] * empty ** (size - 1)
                - sp.prod(singletons[index] for index in subset)
            )
    assert len(segre) == 10
    assert all(sp.expand(equation.subs(witness)) == 0 for equation in segre)

    program = "\n".join(
        (
            "ring r=(0,e,j,s),(z0,z1,z3,z5,z6,z7,w,k,lambda),(dp(7),dp(2));",
            "option(redSB);",
            "ideal D=" + ",".join(map(sg, (hypersurface, divisor) + terminal)) + ";",
            "ideal H=" + ",".join(map(sg, section)) + ";",
            "ideal GD=std(D); ideal GH=std(H);",
            "int dh=1; int hd=1;",
            "for (int ii=1; ii<=size(D); ii++) { if (reduce(D[ii],GH)!=0) { dh=0; } }",
            "for (int jj=1; jj<=size(H); jj++) { if (reduce(H[jj],GD)!=0) { hd=0; } }",
            (
                '"RESULT:"+string(size(GD))+":"+string(size(GH))+":"'
                '+string(dh)+":"+string(hd)+":"+string(reduce(1,GD)==0);'
            ),
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
    assert markers == ["RESULT:9:9:1:1:0"], completed.stdout

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_generic_rational_survivor_section",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01",
                "input_branch": "ordinary A=0 exceptional divisor",
                "weight": "lambda=(js+1)/(js-1)",
                "w": "-(js-1)^2*R/(16*s*(e-j)*Q^2*k)",
                "z3": "-(js-1)/(4*(e^2-k^2)*P)",
                "z6": "-j*(js-1)*R/(8*k*Q^2*(e-j))",
                "terminal_ideal_equals_section_ideal_over_C(e,j,s)": True,
                "terminal_standard_basis_size": 9,
                "terminal_ideal_proper": True,
                "exact_rational_witness": {
                    "(e,j,k,s,lambda)": "(-5,2,3,-1,1/3)",
                    "(z0,z1,z2,z3,z4,z5,z6,z7)": "(13/448,-33/56,-1/56,-3/64,-1/28,79/448,1/28,5/32)",
                    "normalized_segre_equations_zero": "10/10",
                },
                "generic_A_exceptional_terminal_fibre_empty": False,
                "base_special_divisors_localized": True,
                "B_branch_tested": False,
                "special_component_divisors_tested": False,
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
