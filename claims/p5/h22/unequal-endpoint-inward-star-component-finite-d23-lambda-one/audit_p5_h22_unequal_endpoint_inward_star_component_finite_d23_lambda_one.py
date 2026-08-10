#!/usr/bin/env python3
"""No-import audit of the finite-D23 lambda=1 obstruction."""

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
MIXED = WORDS[1:-1]


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


def marked(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def projected(row, extension):
    return (row[0], row[1], row[2] + row[3], extension)


def tensor(alpha, beta, extensions):
    alpha_rows = tuple(projected(alpha[index], extensions[index]) for index in range(4))
    beta_rows = tuple(
        projected(beta[index], extensions[4 + index]) for index in range(4)
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
    e, j, k, s = sp.symbols("e j k s")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    pivot = e * j + k**2
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - (e + j) ** 2)
    alpha, beta = bases(e, j, k, s)
    canonical = tensor(alpha, beta, extensions)
    assert all(
        sp.factor(canonical[word]) == 0
        for word in ((1, 0, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0))
    )

    active = marked(alpha, beta, shifts)
    coefficients = tensor(alpha, active, extensions)
    rows = {
        word: tuple(sp.diff(coefficients[word], extension) for extension in extensions)
        for word in WORDS
    }
    generators = ",".join("[" + ",".join(map(sg, rows[word])) + "]" for word in MIXED)
    alpha_text = "[" + ",".join(map(sg, rows[WORDS[0]])) + "]"
    beta_text = "[" + ",".join(map(sg, rows[WORDS[-1]])) + "]"
    program = "\n".join(
        (
            "ring r=(0,e,j,s),(k,h0,h1,h2,h3),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "vector a=" + alpha_text + "; vector b=" + beta_text + ";",
            "vector ar=reduce(a,M); vector br=reduce(b,M);",
            '"RESULT:"+string(ar==0)+":"+string(br==0)+":"+string(size(M));',
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
    assert markers == ["RESULT:1:0:7"], completed.stdout
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import subset-DP quotient-ring audit",
                "field": "C(e,j,s)[k]/(F)",
                "pair_orbit": "finite D23",
                "weight": "lambda=1",
                "all_alpha_in_mixed_module": True,
                "all_beta_in_mixed_module": False,
                "module_basis_size": 7,
                "all_markings_covered": True,
                "lambda_one_binary_incidence_empty": True,
                "finite_D23_closed": False,
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
