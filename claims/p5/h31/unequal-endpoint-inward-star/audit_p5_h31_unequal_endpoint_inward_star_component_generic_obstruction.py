#!/usr/bin/env python3
"""Independent no-import audit of component twenty-five generic H31."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def permanent_dp(square):
    size = len(square)
    states = {0: sp.Integer(1)}
    for row in square:
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + coefficient * row[column]
                )
        states = next_states
    return sp.expand(states[(1 << size) - 1])


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
    return (
        (
            add(scale(cross, cap_a), scale(-pivot, cap_b)),
            add(
                scale(cross, add(cap_a, scale(k, cap_d))),
                scale(-pivot, add(cap_b, scale(s, cap_c))),
            ),
            cap_c,
            cap_d,
        ),
        (
            cap_a,
            add(cap_a, scale(k, cap_d)),
            add(cap_a, scale(e, cap_b), scale(-k, cap_d)),
            add(cap_a, scale(-s * j, cap_c), scale(j, cap_b)),
        ),
    )


def marked(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def extension_coefficients(distinguished, alpha, beta, extension):
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_rows = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
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


def matrices(distinguished, alpha, beta):
    extension = sp.symbols("z0:8")
    coefficients = extension_coefficients(distinguished, alpha, beta, extension)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in extension]
            for word in MIXED
        ]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[WORDS[0]], variable) for variable in extension]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[WORDS[-1]], variable) for variable in extension]]
    )
    return mixed, diagonal_alpha, diagonal_beta


def command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def module_check(distinguished, alpha, beta, hypersurface):
    mixed, diagonal_alpha, diagonal_beta = matrices(distinguished, alpha, beta)
    generators = ",".join(
        "[" + ",".join(sg(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_text = "[" + ",".join(sg(value) for value in diagonal_alpha) + "]"
    beta_text = "[" + ",".join(sg(value) for value in diagonal_beta) + "]"
    program = "\n".join(
        (
            "ring r=(0,e,j,s),(k,h0,h1,h2,h3),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "module M=" + generators + "; M=std(M);",
            "vector a=" + alpha_text + "; vector b=" + beta_text + ";",
            "vector ar=reduce(a,M); vector br=reduce(b,M);",
            (
                '"RESULT:"+string(reduce(ar,std(0))==0)+":"'
                '+string(reduce(br,std(0))==0)+":"+string(size(M));'
            ),
            "quit;",
        )
    )
    completed = subprocess.run(
        command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1
    _, alpha_zero, beta_zero, size = markers[0].split(":")
    assert (alpha_zero, beta_zero) == ("1", "0")
    return {"distinguished": distinguished, "module_basis_size": int(size)}


def main():
    started = time.perf_counter()
    e, j, k, s = sp.symbols("e j k s")
    shifts = sp.symbols("h0:4")
    pivot = e * j + k**2
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - (e + j) ** 2)
    alpha, beta = bases(e, j, k, s)
    pure = {
        word: sp.factor(
            permanent_dp(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(0, 0, 1, 1)] - 4 * pivot * hypersurface) == 0
    assert sp.factor(pure[WORDS[-1]] - 4 * pivot) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word not in ((0, 0, 1, 1), WORDS[-1])
    )
    active = marked(alpha, beta, shifts)
    modules = [
        module_check(distinguished, alpha, active, hypersurface)
        for distinguished in range(4)
    ]
    assert [result["module_basis_size"] for result in modules] == [10, 10, 12, 12]
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import subset-DP quotient-ring audit",
                "field": "C(e,j,s)[k]/(F)",
                "pure_support_mod_F": {"1111": str(4 * pivot)},
                "row_module_obstructions": modules,
                "generic_marked_H31_fibre_empty": True,
                "pivot_zero_boundary_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
