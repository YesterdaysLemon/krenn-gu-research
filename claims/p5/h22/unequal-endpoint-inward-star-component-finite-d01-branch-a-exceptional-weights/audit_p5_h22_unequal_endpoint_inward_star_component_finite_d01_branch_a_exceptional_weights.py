#!/usr/bin/env python3
"""No-import audit of the retained-weight projection on the D01 A branch."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent_dp(square):
    states = {0: sp.Integer(1)}
    for row in square:
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + coefficient * row[column]
                )
        states = next_states
    return sp.expand(states[15])


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def bases(e, j, k, s):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    pivot = e * j + k**2
    cross = e + j
    alpha = (
        add(scale(cross, cap_a), scale(-pivot, cap_b)),
        add(
            scale(cross, add(cap_a, scale(k, cap_d))),
            scale(-pivot, add(cap_b, scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(cap_a, scale(e, cap_b), scale(-k, cap_d)),
        add(cap_a, scale(-s * j, cap_c), scale(j, cap_b)),
    )
    return alpha, beta


def projected(row, extension, slope):
    return (slope * row[0] + row[1], row[2], row[3], extension)


def tensor(alpha, beta, extensions, slope):
    alpha_rows = tuple(
        projected(alpha[index], extensions[index], slope) for index in range(4)
    )
    beta_rows = tuple(
        projected(beta[index], extensions[4 + index], slope) for index in range(4)
    )
    return {
        word: permanent_dp(
            tuple(
                beta_rows[index] if word[index] else alpha_rows[index]
                for index in range(4)
            )
        )
        for word in WORDS
    }


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
    alpha, beta = bases(e, j, k, s)
    coefficients = tensor(alpha, beta, extensions, slope)

    empty = coefficients[WORDS[0]]
    c1 = coefficients[(0, 1, 0, 0)]
    c2 = coefficients[(0, 0, 1, 0)]
    c3 = coefficients[(0, 0, 0, 1)]
    branch_a = 1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3
    linear_residual = (
        2 * k * cross**2 * (e - j) * (slope - 1) * ((slope + 1) * w + z6) + j * leading
    )
    equations = (
        hypersurface,
        coefficients[(1, 0, 1, 0)],
        coefficients[(1, 0, 1, 1)],
        coefficients[(1, 1, 1, 0)],
        empty - 1,
        branch_a,
        linear_residual,
        coefficients[(0, 0, 1, 1)] * empty - c2 * c3,
        coefficients[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3,
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
                "role": "independent no-import subset-DP elimination audit",
                "field": "C(e,j,s)",
                "input_branch": "ordinary finite-D01 A=0",
                "projection_generator_verified": "(lambda+1)*((js-1)*lambda-(js+1))",
                "remaining_exceptional_weight_divisor": "(js-1)*lambda-(js+1)=0",
                "exceptional_divisor_tested": False,
                "A_branch_closed": False,
                "B_branch_closed": False,
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
