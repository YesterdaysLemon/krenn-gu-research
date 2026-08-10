#!/usr/bin/env python3
"""No-import audit of the rational survivor on the finite-D01 A divisor."""

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
    divisor = sp.expand((j * s - 1) * slope - (j * s + 1))
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = bases(e, j, k, s)
    coefficients = tensor(alpha, beta, extensions, slope)

    empty = coefficients[WORDS[0]]
    c1 = coefficients[(0, 1, 0, 0)]
    c2 = coefficients[(0, 0, 1, 0)]
    c3 = coefficients[(0, 0, 0, 1)]
    terminal = (
        coefficients[(1, 0, 1, 0)],
        coefficients[(1, 0, 1, 1)],
        coefficients[(1, 1, 1, 0)],
        empty - 1,
        1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3,
        2 * k * cross**2 * (e - j) * (slope - 1) * ((slope + 1) * w + z6) + j * leading,
        coefficients[(0, 0, 1, 1)] * empty - c2 * c3,
        coefficients[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3,
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
                "role": "independent no-import subset-DP ideal-equivalence audit",
                "field": "C(e,j,s)[k]/(F)",
                "input_branch": "ordinary finite-D01 A exceptional divisor",
                "terminal_and_section_basis_sizes": [9, 9],
                "mutual_generatorwise_remainders_zero": True,
                "terminal_ideal_proper": True,
                "base_special_divisors_localized": True,
                "B_branch_tested": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
