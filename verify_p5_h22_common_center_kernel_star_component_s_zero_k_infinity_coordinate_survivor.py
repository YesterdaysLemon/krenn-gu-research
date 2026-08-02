#!/usr/bin/env python3
"""Verify the exact H22 paired-incidence survivor on component 23's corner."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    WORDS,
    build_model,
    singular_command,
)

PAIRS = tuple(itertools.combinations(range(4), 2))

epsilon = sp.symbols("epsilon")
x = sp.symbols("x0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def arc_certificate():
    r = sp.Integer(0)
    t = sp.Integer(2)
    s = epsilon / 2
    k = 1 / epsilon
    assert sp.cancel(1 - r * t - k * s * (t - r)) == 0

    rescaled_alpha1 = add(scale(epsilon, A), D)
    planes = (
        (A, B),
        (rescaled_alpha1, add(B, scale(s, C))),
        (add(scale(s, add(A, scale(-1, C))), B), C),
        (add(scale(-s, add(A, C)), B, scale(t, D)), C),
    )
    limit = tuple(
        tuple(tuple(sp.limit(entry, epsilon, 0) for entry in row) for row in plane)
        for plane in planes
    )
    expected = (
        (A, B),
        (D, B),
        (B, C),
        (add(B, scale(2, D)), C),
    )
    assert limit == expected
    return expected


def pure_and_pair_certificate(planes):
    alpha = tuple(plane[0] for plane in planes)
    beta = tuple(plane[1] for plane in planes)
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )

    def symmetric_product(left, right):
        return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])

    matrices = []
    for left, right in PAIRS:
        matrices.append(
            sp.Matrix.hstack(
                *(
                    symmetric_product(planes[left][i], planes[right][j])
                    for i in range(2)
                    for j in range(2)
                )
            )
        )
    profile = tuple(matrix.rank() for matrix in matrices)
    assert profile == (3, 3, 3, 3, 3, 4)

    r, t = sp.symbols("r t")
    general_edge23 = sp.Matrix.hstack(
        *(
            symmetric_product(left, right)
            for left in (add(B, scale(r, D)), C)
            for right in (add(B, scale(t, D)), C)
        )
    )
    edge23_minors = [
        sp.factor(general_edge23.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]
    edge23_gcd = sp.factor(sp.gcd_list([value for value in edge23_minors if value]))
    assert sp.expand(edge23_gcd - 8 * (r - t) * (r * t - 1)) == 0
    return alpha, beta, coefficients, profile, edge23_gcd


def family_models():
    t, lam = sp.symbols("t lam")
    h = sp.symbols("h0:4")
    alpha = (A, D, B, add(B, scale(t, D)))
    beta = (B, B, C, C)
    marked = tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))
    models = tuple(
        build_model(alpha, marked, x, direction, "finite", lam)
        for direction in ("D01", "D23")
    )
    return t, lam, h, alpha, beta, models


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def projection_certificate():
    t, lam, h, _alpha, _beta, models = family_models()
    w, u = sp.symbols("w u")
    mixed = tuple(equation for model in models for equation in model["mixed"])
    diagonals = tuple(model[kind] for model in models for kind in ("A", "B"))
    assert diagonals[2] == 0
    product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])

    variables = (*x, w, u, *h, t, lam)
    origin_mixed = tuple(sp.expand(equation.subs(t, 0)) for equation in mixed)
    origin_product = sp.expand(product.subs(t, 0))
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(10),dp(6));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed))
            + ","
            + singular_text(w * product - 1)
            + ","
            + singular_text(u * t - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,x0*x1*x2*x3*x4*x5*x6*x7*w*u); J=std(J);",
            "ideal E=h3,h0,h1*t-1; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=(size(JE)==0)&&(size(EJ)==0);",
            "ideal I0="
            + ",".join(map(singular_text, origin_mixed))
            + ","
            + singular_text(w * origin_product - 1)
            + ";",
            "I0=slimgb(I0);",
            "int originUnit=reduce(1,I0)==0;",
            'print("RESULT:"+string(same)+":"+string(size(J))+":"+string(originUnit));',
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
    assert markers == ["RESULT:1:3:1"], completed.stdout
    return markers[0]


def family_certificate():
    t, lam, h, alpha, beta, models = family_models()
    H = sp.symbols("H")
    substitutions = {h[0]: 0, h[1]: 1 / t, h[2]: H, h[3]: 0}
    mixed = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    ).subs(substitutions, simultaneous=True)
    extension = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in mixed * extension)
    rows = (1, 3, 4, 8, 9, 12, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(mixed.extract(rows, columns).det(method="domain-ge"))
    assert sp.expand(rank_minor + 128 * t**2 * (lam - 1) ** 4 * (lam + 1) ** 3) == 0

    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable).subs(substitutions) * extension[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    expected_diagonals = (
        2 * t * (lam + 1),
        2 * H * (lam - 1),
        0,
        -2 * (lam + 1),
    )
    assert all(
        sp.expand(observed - expected) == 0
        for observed, expected in zip(diagonals, expected_diagonals, strict=True)
    )

    marked = tuple(add(beta[i], scale(substitutions[h[i]], alpha[i])) for i in range(4))
    alpha5 = tuple((*alpha[i], extension[i]) for i in range(4))
    marked5 = tuple((*marked[i], extension[4 + i]) for i in range(4))
    contractions = ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contractions:
        for word in itertools.product((0, 1), repeat=3):
            selected = [gamma]
            selected.extend(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            equations.append(permanent(tuple(selected) + (contraction,)))
    gamma_matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )
    gamma_rows = (0, 1, 2, 7, 9)
    gamma_minor = sp.factor(gamma_matrix.extract(gamma_rows, range(5)).det())
    assert sp.expand(gamma_minor - 8 * H * t**2 * (lam - 1) ** 4 * (lam + 1)) == 0
    return (
        tuple(map(str, expected_diagonals)),
        str(rank_minor),
        str(gamma_minor),
    )


def one_gamma_certificate(alpha5, marked5, contraction_rows):
    gamma = sp.symbols("gamma0:5")
    expected = (
        ((0, 1, 2, 7, 9), 288),
        ((0, 2, 4, 7, 8), 20736),
        ((0, 2, 7, 8, 15), -648),
        ((0, 2, 3, 7, 8), 1944),
    )
    observed = []
    for mode, (rows, determinant) in enumerate(expected):
        equations = []
        for contraction in contraction_rows:
            for word in itertools.product((0, 1), repeat=3):
                selected = []
                cursor = 0
                for index in range(4):
                    if index == mode:
                        selected.append(gamma)
                    else:
                        selected.append(
                            marked5[index] if word[cursor] else alpha5[index]
                        )
                        cursor += 1
                equations.append(permanent(tuple(selected) + (contraction,)))
        matrix = sp.Matrix(
            [
                [sp.diff(equation, variable) for variable in gamma]
                for equation in equations
            ]
        )
        assert matrix.shape == (16, 5)
        assert matrix.rank() == 5
        assert matrix.extract(rows, range(5)).det() == determinant
        assert matrix.nullspace() == []
        observed.append((rows, determinant))
    return tuple(observed)


def survivor_certificate(alpha, beta):
    marking = (sp.Integer(0), sp.Rational(1, 2), sp.Integer(3), sp.Integer(0))
    marked = tuple(add(beta[i], scale(marking[i], alpha[i])) for i in range(4))
    assert all(
        sp.Matrix.vstack(sp.Matrix(alpha[i]).T, sp.Matrix(marked[i]).T).rank() == 2
        for i in range(4)
    )

    weight = sp.Integer(2)
    extension = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    models = tuple(
        build_model(alpha, marked, x, direction, "finite", weight)
        for direction in ("D01", "D23")
    )
    mixed = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )
    assert mixed.shape == (28, 8)
    assert mixed.rank() == 7
    assert mixed * extension == sp.zeros(28, 1)
    kernel = mixed.nullspace()
    assert len(kernel) == 1
    assert kernel[0] == extension

    diagonals = tuple(
        sp.expand(
            sum(
                sp.diff(model[kind], variable) * extension[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    assert diagonals == (12, 6, 0, -6)
    assert diagonals[1] * diagonals[3] != 0 and diagonals[0] != 0

    alpha5 = tuple((*alpha[i], extension[i]) for i in range(4))
    marked5 = tuple((*marked[i], extension[4 + i]) for i in range(4))
    contraction_rows = ((1, 2, 0, 0, 0), (0, 0, 1, 2, 0))
    direct = []
    for contraction in contraction_rows:
        values = {
            word: permanent(
                tuple(
                    marked5[index] if word[index] else alpha5[index]
                    for index in range(4)
                )
                + (contraction,)
            )
            for word in WORDS
        }
        assert all(values[word] == 0 for word in WORDS[1:-1])
        direct.append((values[WORDS[0]], values[WORDS[-1]]))
    assert tuple(direct) == ((12, 6), (0, -6))
    gamma_witnesses = one_gamma_certificate(alpha5, marked5, contraction_rows)
    return (
        marking,
        weight,
        tuple(extension),
        diagonals,
        tuple(direct),
        mixed.rank(),
        gamma_witnesses,
    )


def main():
    projection = projection_certificate()
    family_diagonals, family_rank_minor, family_gamma_minor = family_certificate()
    planes = arc_certificate()
    alpha, beta, coefficients, profile, edge23_gcd = pure_and_pair_certificate(planes)
    marking, weight, extension, diagonals, direct, rank, gamma_witnesses = (
        survivor_certificate(alpha, beta)
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "boundary": "s=0,k=infinity",
                "point": {"r": 0, "t": 2},
                "finite_r_zero_projection": "<h3,h0,t*h1-1>",
                "projection_certificate": projection,
                "t_zero_genuine_paired_incidence": "empty",
                "family_diagonals": family_diagonals,
                "family_rank_minor": family_rank_minor,
                "family_mode0_one_gamma_minor": family_gamma_minor,
                "valuative_arc": "r=0,t=2,k=1/epsilon,s=epsilon/2",
                "pure_support": {"1111": str(coefficients[(1, 1, 1, 1)])},
                "pair_profile": profile,
                "general_edge23_maximal_minor_gcd": str(edge23_gcd),
                "marking": tuple(map(str, marking)),
                "finite_weight": f"[{weight}:1]",
                "extension": tuple(map(str, extension)),
                "mixed_matrix_rank": rank,
                "mixed_equations_zero": 28,
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "diagonals": tuple(map(str, diagonals)),
                "direct_five_coordinate_diagonals": tuple(
                    tuple(map(str, values)) for values in direct
                ),
                "one_gamma_rank_witnesses": gamma_witnesses,
                "genuine_shared_incidence": True,
                "full_P5_to_Delta3": "obstructed_at_one_gamma_stage",
                "finite_r_zero_ternary_H22": "empty",
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
