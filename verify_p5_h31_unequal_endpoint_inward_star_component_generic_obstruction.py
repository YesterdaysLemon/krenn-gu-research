#!/usr/bin/env python3
"""Exact generic marked-H31 obstruction for component twenty-five."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix, permanent

WORDS = tuple(itertools.product((0, 1), repeat=4))


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def pure_basis(e, j, k, s):
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


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def quotient_row_module(distinguished, alpha, beta, hypersurface):
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
    generators = ",".join(
        "[" + ",".join(sg(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_text = (
        "[" + ",".join(sg(diagonal_alpha[0, column]) for column in range(8)) + "]"
    )
    beta_text = (
        "[" + ",".join(sg(diagonal_beta[0, column]) for column in range(8)) + "]"
    )
    program = "\n".join(
        (
            "ring r=(0,e,j,s),(k,h0,h1,h2,h3),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "vector a=" + alpha_text + ";",
            "vector b=" + beta_text + ";",
            "vector ar=reduce(a,M); vector br=reduce(b,M);",
            (
                '"RESULT:"+string(reduce(ar,std(0))==0)+":"'
                '+string(reduce(br,std(0))==0)+":"+string(size(M));'
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
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, alpha_zero, beta_zero, basis_size = markers[0].split(":")
    assert alpha_zero == "1" and beta_zero == "0", markers[0]
    return {
        "distinguished": distinguished,
        "all_alpha_in_mixed_module": True,
        "all_beta_in_mixed_module": False,
        "module_basis_size": int(basis_size),
    }


def main():
    started = time.perf_counter()
    e, j, k, s = sp.symbols("e j k s")
    shifts = sp.symbols("h0:4")
    pivot = e * j + k**2
    cross = e + j
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - cross**2)
    alpha, beta = pure_basis(e, j, k, s)

    assert sp.factor(sp.Matrix(((cross, -pivot), (1, 0))).det() - pivot) == 0
    pure = {
        word: sp.factor(
            permanent(
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
        quotient_row_module(distinguished, alpha, active, hypersurface)
        for distinguished in range(4)
    ]
    assert [result["module_basis_size"] for result in modules] == [10, 10, 12, 12]
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "hypersurface": str(hypersurface),
                "pure_basis_pivot": str(pivot),
                "pure_support_mod_F": {"1111": str(4 * pivot)},
                "row_module_obstructions": modules,
                "generic_marked_H31_fibre_empty": True,
                "pivot_zero_boundary_closed": False,
                "special_component_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
