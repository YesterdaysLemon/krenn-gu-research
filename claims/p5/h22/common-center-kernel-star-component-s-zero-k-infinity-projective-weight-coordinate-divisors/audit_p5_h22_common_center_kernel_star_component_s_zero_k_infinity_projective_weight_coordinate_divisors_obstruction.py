#!/usr/bin/env python3
"""No-import audit of projective H22 emptiness on component 23's corner axes."""

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

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
TERNARY_WORDS = tuple(itertools.product((0, 1, 2), repeat=4))
PULLBACK = (0, 1, 3, 2)

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows(r, t):
    return (A, D, add(B, D, r), add(B, D, t)), (B, B, C, C)


def mark(alpha, beta, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def permanent_dp(matrix):
    states = {0: sp.Integer(1)}
    for row in matrix:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = following
    return sp.expand(states[(1 << len(matrix)) - 1])


def project(row, extension, direction):
    if direction == "D01":
        return (row[0], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def coefficient_tensor(alpha, marked, extensions, direction):
    alpha_rows = tuple(project(alpha[i], extensions[i], direction) for i in range(4))
    marked_rows = tuple(
        project(marked[i], extensions[4 + i], direction) for i in range(4)
    )
    return {
        word: permanent_dp(
            tuple(marked_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    assert shutil.which("wsl.exe")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def projection_audit():
    t = sp.symbols("t")
    h = sp.symbols("h0:4")
    x = sp.symbols("z0:8")
    w = sp.symbols("w")
    alpha, beta = rows(0, t)
    marked = mark(alpha, beta, h)
    tensors = tuple(
        coefficient_tensor(alpha, marked, x, direction) for direction in ("D01", "D23")
    )
    mixed = tuple(tensor[word] for tensor in tensors for word in MIXED_WORDS)
    diagonals = tuple(
        value for tensor in tensors for value in (tensor[WORDS[0]], tensor[WORDS[-1]])
    )
    assert diagonals[2] == 0
    product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])
    variables = (*x, w, *h, t)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed))
            + ","
            + singular_text(w * product - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,z0*z1*z2*z3*z4*z5*z6*z7*w); J=std(J);",
            "ideal E=h3,h0,h1*t-1; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=(size(JE)==0)&&(size(EJ)==0);",
            "int sourceUnit=reduce(1,I)==0;",
            'print("RESULT:"+string(same)+":"+string(size(J))+":"+string(sourceUnit));',
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
    assert markers == ["RESULT:1:3:0"], completed.stdout
    return markers[0]


def family_audit():
    t, H = sp.symbols("t H")
    h = (0, 1 / t, H, 0)
    x = sp.symbols("z0:8")
    alpha, beta = rows(0, t)
    marked = mark(alpha, beta, h)
    tensors = tuple(
        coefficient_tensor(alpha, marked, x, direction) for direction in ("D01", "D23")
    )
    mixed = tuple(tensor[word] for tensor in tensors for word in MIXED_WORDS)
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in mixed]
    )
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in matrix * kernel)
    selected_rows = (1, 3, 4, 8, 9, 12, 16)
    selected_columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(
        matrix.extract(selected_rows, selected_columns).det(method="domain-ge")
    )
    assert rank_minor == -128 * t**2

    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(value, variable) * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for tensor in tensors
        for value in (tensor[WORDS[0]], tensor[WORDS[-1]])
    )
    assert diagonals == (2 * t, 2 * H, 0, -2)

    alpha5 = tuple((*alpha[i], kernel[i]) for i in range(4))
    marked5 = tuple((*marked[i], kernel[4 + i]) for i in range(4))
    contractions = ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    gamma = sp.symbols("gamma0:5")
    gamma_equations = []
    for contraction in contractions:
        for word in itertools.product((0, 1), repeat=3):
            selected = (gamma,) + tuple(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            gamma_equations.append(permanent_dp(selected + (contraction,)))
    gamma_matrix = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in gamma]
            for equation in gamma_equations
        ]
    )
    gamma_rows = (0, 1, 2, 7, 9)
    gamma_minor = sp.factor(
        gamma_matrix.extract(gamma_rows, range(5)).det(method="domain-ge")
    )
    assert gamma_minor == 8 * H * t**2
    return (
        tuple(kernel),
        tuple(map(str, diagonals)),
        str(rank_minor),
        gamma_rows,
        str(gamma_minor),
    )


def transfer_audit():
    r, t = sp.symbols("r t")
    h = sp.symbols("h0:4")
    x = sp.symbols("z0:8")
    old_alpha, old_beta = rows(r, t)
    new_alpha, new_beta = rows(t, r)
    old_marked = mark(old_alpha, old_beta, h)
    new_h = (h[0], h[1], h[3], h[2])
    new_marked = mark(new_alpha, new_beta, new_h)
    new_x = (x[0], x[1], x[3], x[2], x[4], x[5], x[7], x[6])
    for i, old_i in enumerate(PULLBACK):
        assert new_alpha[i] == old_alpha[old_i]
        assert new_beta[i] == old_beta[old_i]
        assert new_marked[i] == old_marked[old_i]

    binary_counts = {}
    for direction in ("D01", "D23"):
        old_tensor = coefficient_tensor(old_alpha, old_marked, x, direction)
        new_tensor = coefficient_tensor(new_alpha, new_marked, new_x, direction)
        count = 0
        for word in WORDS:
            pulled = (word[0], word[1], word[3], word[2])
            assert sp.expand(new_tensor[word] - old_tensor[pulled]) == 0
            count += 1
        binary_counts[direction] = count

    gamma_symbols = sp.symbols("g0:20")
    old_gamma = tuple(
        tuple(gamma_symbols[5 * i + column] for column in range(5)) for i in range(4)
    )
    new_gamma = tuple(old_gamma[PULLBACK[i]] for i in range(4))
    old_alpha5 = tuple((*old_alpha[i], x[i]) for i in range(4))
    old_marked5 = tuple((*old_marked[i], x[4 + i]) for i in range(4))
    new_alpha5 = tuple((*new_alpha[i], new_x[i]) for i in range(4))
    new_marked5 = tuple((*new_marked[i], new_x[4 + i]) for i in range(4))
    old_colours = (old_alpha5, old_marked5, old_gamma)
    new_colours = (new_alpha5, new_marked5, new_gamma)
    contraction_rows = {
        "D01": (0, 1, 0, 0, 0),
        "D23": (0, 0, 0, 1, 0),
    }
    ternary_counts = {}
    for direction, contraction in contraction_rows.items():
        count = 0
        for word in TERNARY_WORDS:
            pulled = (word[0], word[1], word[3], word[2])
            new_selected = tuple(new_colours[word[i]][i] for i in range(4))
            old_selected = tuple(old_colours[pulled[i]][i] for i in range(4))
            assert (
                sp.expand(
                    permanent_dp(new_selected + (contraction,))
                    - permanent_dp(old_selected + (contraction,))
                )
                == 0
            )
            count += 1
        ternary_counts[direction] = count
    return binary_counts, ternary_counts


def main():
    projection = projection_audit()
    kernel, diagonals, rank_minor, gamma_rows, gamma_minor = family_audit()
    binary_counts, ternary_counts = transfer_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP permanent rebuild",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity",
                "weight": "[1:0]",
                "r_zero_projection": "<h3,h0,t*h1-1>",
                "projection_certificate": projection,
                "kernel": tuple(map(str, kernel)),
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "diagonals": diagonals,
                "rank_seven_minor": rank_minor,
                "one_gamma_rows": gamma_rows,
                "one_gamma_minor": gamma_minor,
                "genuine_open": "t*H != 0",
                "r_zero_projective_weight_H22": "empty",
                "mode_swap_binary_words_per_direction": binary_counts,
                "mode_swap_ternary_words_per_direction": ternary_counts,
                "t_zero_projective_weight_H22": "empty",
                "parameter_infinity_covered": False,
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
