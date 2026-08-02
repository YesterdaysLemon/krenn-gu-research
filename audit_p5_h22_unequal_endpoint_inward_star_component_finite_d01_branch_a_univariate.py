#!/usr/bin/env python3
"""No-import audit of generic-weight emptiness on the D01 A branch."""

from __future__ import annotations

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
    linear_ideal = (
        coefficients[(1, 0, 1, 0)],
        coefficients[(1, 0, 1, 1)],
        coefficients[(1, 1, 1, 0)],
        empty - 1,
        branch_a,
        linear_residual,
    )
    segre_23 = coefficients[(0, 0, 1, 1)] * empty - c2 * c3
    segre_123 = coefficients[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3
    program = "\n".join(
        (
            "ring r=(0,e,j,s,lambda),(k,z0,z1,z3,z5,z6,z7,w),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "option(redSB);",
            "ideal L=" + ",".join(map(sg, linear_ideal)) + "; L=std(L);",
            "poly r23=reduce(" + sg(segre_23) + ",L);",
            "poly r123=reduce(" + sg(segre_123) + ",L);",
            "ideal J=L,r23,r123; J=std(J);",
            '"RESULT:"+string(reduce(1,J)==0)+":"+string(size(J));',
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
    assert markers == ["RESULT:1:1"], completed.stdout
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_exceptional_weight_residual",
                "role": "independent no-import subset-DP quotient-ring audit",
                "field": "C(e,j,s,lambda)[k]/(F)",
                "input_branch": "ordinary finite-D01 A=0",
                "reduced_standard_basis": ["1"],
                "A_branch_generic_weight_empty": True,
                "exceptional_weight_divisor_extracted": False,
                "A_branch_all_weights_closed": False,
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
