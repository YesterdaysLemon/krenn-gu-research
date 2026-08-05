#!/usr/bin/env python3
"""Verify projective-weight H22 emptiness on component 23's corner axes."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    WORDS,
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_coordinate_survivor import (
    A,
    B,
    C,
    D,
    add,
    permanent,
    scale,
    singular_command,
    singular_text,
)

PULLBACK = (0, 1, 3, 2)


def corner_rows(r, t):
    return (A, D, add(B, scale(r, D)), add(B, scale(t, D))), (B, B, C, C)


def projective_models(t, h, x):
    alpha, beta = corner_rows(sp.Integer(0), t)
    marked = tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))
    models = tuple(
        build_model(alpha, marked, x, direction, "infinity", None)
        for direction in ("D01", "D23")
    )
    return alpha, beta, marked, models


def projection_certificate():
    t = sp.symbols("t")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    w = sp.symbols("w")
    _alpha, _beta, _marked, models = projective_models(t, h, x)
    mixed = tuple(equation for model in models for equation in model["mixed"])
    diagonals = tuple(model[kind] for model in models for kind in ("A", "B"))
    assert diagonals[2] == 0
    genuine_product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])

    variables = (*x, w, *h, t)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed))
            + ","
            + singular_text(w * genuine_product - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,x0*x1*x2*x3*x4*x5*x6*x7*w); J=std(J);",
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


def family_certificate():
    t, H = sp.symbols("t H")
    h = (sp.Integer(0), 1 / t, H, sp.Integer(0))
    x = sp.symbols("x0:8")
    alpha, _beta, marked, models = projective_models(t, h, x)
    mixed_matrix = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in mixed_matrix * kernel)
    rows = (1, 3, 4, 8, 9, 12, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(mixed_matrix.extract(rows, columns).det(method="domain-ge"))
    assert sp.expand(rank_minor + 128 * t**2) == 0
    assert mixed_matrix.rank() == 7
    assert mixed_matrix.nullspace() == [kernel]

    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable) * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    assert diagonals == (2 * t, 2 * H, 0, -2)

    alpha5 = tuple((*alpha[i], kernel[i]) for i in range(4))
    marked5 = tuple((*marked[i], kernel[4 + i]) for i in range(4))
    contractions = ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contractions:
        for word in itertools.product((0, 1), repeat=3):
            selected = (gamma,) + tuple(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            equations.append(permanent(selected + (contraction,)))
    gamma_matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )
    gamma_rows = (0, 1, 2, 7, 9)
    gamma_minor = sp.factor(
        gamma_matrix.extract(gamma_rows, range(5)).det(method="domain-ge")
    )
    assert sp.expand(gamma_minor - 8 * H * t**2) == 0
    return (
        tuple(kernel),
        tuple(map(str, diagonals)),
        str(rank_minor),
        gamma_rows,
        str(gamma_minor),
    )


def transfer_certificate():
    r, t = sp.symbols("r t")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    old_alpha, old_beta = corner_rows(r, t)
    new_alpha, new_beta = corner_rows(t, r)
    old_marked = tuple(add(old_beta[i], scale(h[i], old_alpha[i])) for i in range(4))
    new_h = (h[0], h[1], h[3], h[2])
    new_marked = tuple(
        add(new_beta[i], scale(new_h[i], new_alpha[i])) for i in range(4)
    )
    new_x = (x[0], x[1], x[3], x[2], x[4], x[5], x[7], x[6])
    for i, old_i in enumerate(PULLBACK):
        assert new_alpha[i] == old_alpha[old_i]
        assert new_beta[i] == old_beta[old_i]
        assert new_marked[i] == old_marked[old_i]

    counts = {}
    for direction in ("D01", "D23"):
        old_model = build_model(old_alpha, old_marked, x, direction, "infinity", None)
        new_model = build_model(
            new_alpha, new_marked, new_x, direction, "infinity", None
        )
        count = 0
        for word in WORDS:
            pulled = (word[0], word[1], word[3], word[2])
            assert (
                sp.expand(
                    new_model["coefficients"][word] - old_model["coefficients"][pulled]
                )
                == 0
            )
            count += 1
        counts[direction] = count
    assert (new_h[0], new_h[1], new_h[3], new_h[2]) == h
    assert (
        new_x[0],
        new_x[1],
        new_x[3],
        new_x[2],
        new_x[4],
        new_x[5],
        new_x[7],
        new_x[6],
    ) == x
    return counts, tuple(map(str, new_h)), tuple(map(str, new_x))


def main():
    projection = projection_certificate()
    kernel, diagonals, rank_minor, gamma_rows, gamma_minor = family_certificate()
    transfer_counts, marking_map, extension_map = transfer_certificate()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity",
                "weight": "[1:0]",
                "r_zero_projection": "<h3,h0,t*h1-1>",
                "projection_certificate": projection,
                "binary_survivor_kernel": tuple(map(str, kernel)),
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "survivor_diagonals": diagonals,
                "rank_seven_minor": rank_minor,
                "mode_zero_one_gamma_rows": gamma_rows,
                "mode_zero_one_gamma_minor": gamma_minor,
                "genuine_open": "t*H != 0",
                "r_zero_projective_weight_ternary_H22": "empty",
                "mode_swap": "(2 3)",
                "parameter_map": "(r,t) -> (t,r)",
                "marking_map": marking_map,
                "extension_map": extension_map,
                "projective_tensor_words_checked_per_direction": transfer_counts,
                "t_zero_projective_weight_ternary_H22": "empty",
                "parameter_infinity_covered": False,
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
