#!/usr/bin/env python3
"""Independent no-import audit of component twenty-five partial H22 closure."""

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


def project(row, extension, direction, chart, slope=None):
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def tensor(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[index], extensions[index], direction, chart, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], extensions[4 + index], direction, chart, slope)
        for index in range(4)
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


def module_check(direction, distinguished, alpha, beta, extensions, hypersurface):
    weighted = tensor(alpha, beta, extensions, direction, "infinity")
    deleted_alpha = tuple(
        tuple(
            alpha[mode][coordinate]
            for coordinate in range(4)
            if coordinate != distinguished
        )
        + (extensions[mode],)
        for mode in range(4)
    )
    deleted_beta = tuple(
        tuple(
            beta[mode][coordinate]
            for coordinate in range(4)
            if coordinate != distinguished
        )
        + (extensions[4 + mode],)
        for mode in range(4)
    )
    deleted = {
        word: permanent_dp(
            tuple(
                deleted_beta[mode] if word[mode] else deleted_alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert all(sp.expand(weighted[word] - deleted[word]) == 0 for word in WORDS)

    rows = {
        word: tuple(sp.diff(weighted[word], extension) for extension in extensions)
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
    _, alpha_zero, beta_zero, size = markers[0].split(":")
    assert (alpha_zero, beta_zero) == ("1", "0")
    return {
        "direction": direction,
        "identified_H31_deleted_coordinate": distinguished,
        "module_basis_size": int(size),
        "binary_incidence_empty": True,
    }


def main():
    started = time.perf_counter()
    e, j, k, s, slope = sp.symbols("e j k s lambda")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - cross**2)
    alpha, beta = bases(e, j, k, s)

    finite = tensor(alpha, beta, extensions, "D01", "finite", slope)
    linear_factor = sp.expand((slope + 1) * extensions[2] + (slope - 1) * extensions[4])
    identities = (
        finite[(1, 1, 0, 1)],
        finite[(1, 0, 0, 0)] - cross * finite[(1, 1, 0, 0)],
        k * finite[(1, 0, 0, 1)] - j * pivot * finite[(1, 1, 0, 0)],
        finite[(1, 1, 0, 0)] + 2 * k * linear_factor,
    )
    assert all(sp.factor(value) == 0 for value in identities)
    t, c1, c3, inverse = sp.symbols("t c1 c3 inverse")
    dense_ideal = (
        t - cross * t * c1,
        j * pivot * t - k * cross * t * c3,
        cross * t * c1 * c3,
        inverse * t - 1,
    )
    dense_basis = sp.groebner(
        dense_ideal,
        inverse,
        t,
        c1,
        c3,
        domain=sp.QQ.frac_field(e, j, k),
    )
    assert list(dense_basis) == [1]

    active = marked(alpha, beta, shifts)
    infinity = (
        module_check("D01", 1, alpha, active, extensions, hypersurface),
        module_check("D23", 3, alpha, active, extensions, hypersurface),
    )
    assert [entry["module_basis_size"] for entry in infinity] == [10, 12]
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_residual",
                "role": "independent no-import subset-DP quotient-ring audit",
                "field": "C(e,j,s)[k]/(F)",
                "finite_D01_L01_nonzero_empty": True,
                "weight_infinity_obstructions": infinity,
                "finite_D01_L01_zero_closed": False,
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
