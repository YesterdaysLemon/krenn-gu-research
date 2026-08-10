#!/usr/bin/env python3
"""No-import audit of the component-23 corner H22 paired survivor."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

epsilon = sp.symbols("epsilon")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(
        sp.expand(sum(row[index] for row in rows)) for index in range(len(rows[0]))
    )


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = following
    return sp.expand(states[(1 << len(rows)) - 1])


def valuative_rebuild():
    r, t, k, s = 0, 2, 1 / epsilon, epsilon / 2
    assert sp.cancel(1 - r * t - k * s * (t - r)) == 0
    rescaled_planes = (
        (A, B),
        (add(scale(epsilon, A), D), add(B, scale(s, C))),
        (add(scale(s, add(A, scale(-1, C))), B, scale(r, D)), C),
        (add(scale(-s, add(A, C)), B, scale(t, D)), C),
    )
    return tuple(
        tuple(tuple(sp.limit(entry, epsilon, 0) for entry in row) for row in plane)
        for plane in rescaled_planes
    )


def pair_profile(planes):
    def product(left, right):
        return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])

    matrices = tuple(
        sp.Matrix.hstack(
            *(
                product(planes[left][i], planes[right][j])
                for i in range(2)
                for j in range(2)
            )
        )
        for left, right in PAIRS
    )
    return tuple(matrix.rank() for matrix in matrices)


def general_edge23_gcd():
    r, t = sp.symbols("r t")

    def product(left, right):
        return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])

    matrix = sp.Matrix.hstack(
        *(
            product(left, right)
            for left in (add(B, scale(r, D)), C)
            for right in (add(B, scale(t, D)), C)
        )
    )
    minors = [
        sp.factor(matrix.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]
    result = sp.factor(sp.gcd_list([value for value in minors if value]))
    assert sp.expand(result - 8 * (r - t) * (r * t - 1)) == 0
    return result


def contraction_coefficients(alpha5, marked5, contraction):
    return {
        word: permanent_dp(
            tuple(
                marked5[index] if word[index] else alpha5[index] for index in range(4)
            )
            + (contraction,)
        )
        for word in WORDS
    }


def one_gamma_audit(alpha5, marked5, contractions):
    gamma = sp.symbols("gamma0:5")
    expected = (
        ((0, 1, 2, 7, 9), 288),
        ((0, 2, 4, 7, 8), 20736),
        ((0, 2, 7, 8, 15), -648),
        ((0, 2, 3, 7, 8), 1944),
    )
    for mode, (rows, determinant) in enumerate(expected):
        equations = []
        for contraction in contractions:
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
                equations.append(permanent_dp(tuple(selected) + (contraction,)))
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
    return expected


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    assert shutil.which("wsl.exe")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def symbolic_family_rebuild():
    t, lam, H = sp.symbols("t lam H")
    h = sp.symbols("h0:4")
    variables = sp.symbols("z0:8")
    alpha = (A, D, B, add(B, scale(t, D)))
    beta = (B, B, C, C)
    marked_general = tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))
    contractions = ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
    general_alpha5 = tuple((*alpha[i], variables[i]) for i in range(4))
    general_marked5 = tuple((*marked_general[i], variables[4 + i]) for i in range(4))
    coefficient_sets = tuple(
        contraction_coefficients(general_alpha5, general_marked5, contraction)
        for contraction in contractions
    )
    mixed_equations = tuple(
        coefficients[word] for coefficients in coefficient_sets for word in WORDS[1:-1]
    )
    diagonals = tuple(
        value
        for coefficients in coefficient_sets
        for value in (coefficients[WORDS[0]], coefficients[WORDS[-1]])
    )
    assert diagonals[2] == 0

    w, u = sp.symbols("w u")
    product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])
    ring_variables = (*variables, w, u, *h, t, lam)
    origin_mixed = tuple(sp.expand(equation.subs(t, 0)) for equation in mixed_equations)
    origin_product = sp.expand(product.subs(t, 0))
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, ring_variables)) + "),(dp(10),dp(6));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed_equations))
            + ","
            + singular_text(w * product - 1)
            + ","
            + singular_text(u * t - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,z0*z1*z2*z3*z4*z5*z6*z7*w*u); J=std(J);",
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

    substitutions = {h[0]: 0, h[1]: 1 / t, h[2]: H, h[3]: 0}
    family_matrix = sp.Matrix(
        [
            [sp.diff(equation.subs(substitutions), variable) for variable in variables]
            for equation in mixed_equations
        ]
    )
    witness = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in family_matrix * witness)
    rows = (1, 3, 4, 8, 9, 12, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(family_matrix.extract(rows, columns).det(method="domain-ge"))
    assert sp.expand(rank_minor + 128 * t**2 * (lam - 1) ** 4 * (lam + 1) ** 3) == 0
    family_diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(diagonal.subs(substitutions), variable) * witness[index]
                for index, variable in enumerate(variables)
            )
        )
        for diagonal in diagonals
    )
    expected_diagonals = (
        2 * t * (lam + 1),
        2 * H * (lam - 1),
        0,
        -2 * (lam + 1),
    )
    assert all(
        sp.expand(observed - expected) == 0
        for observed, expected in zip(family_diagonals, expected_diagonals, strict=True)
    )

    marked_family = tuple(
        add(beta[i], scale(substitutions[h[i]], alpha[i])) for i in range(4)
    )
    alpha5 = tuple((*alpha[i], witness[i]) for i in range(4))
    marked5 = tuple((*marked_family[i], witness[4 + i]) for i in range(4))
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contractions:
        for word in itertools.product((0, 1), repeat=3):
            selected = [gamma]
            selected.extend(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            equations.append(permanent_dp(tuple(selected) + (contraction,)))
    gamma_matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )
    gamma_minor = sp.factor(gamma_matrix.extract((0, 1, 2, 7, 9), range(5)).det())
    assert sp.expand(gamma_minor - 8 * H * t**2 * (lam - 1) ** 4 * (lam + 1)) == 0
    return (
        markers[0],
        tuple(map(str, expected_diagonals)),
        str(rank_minor),
        str(gamma_minor),
    )


def main():
    projection, family_diagonals, family_rank_minor, family_gamma_minor = (
        symbolic_family_rebuild()
    )
    planes = valuative_rebuild()
    expected = (
        (A, B),
        (D, B),
        (B, C),
        (add(B, scale(2, D)), C),
    )
    assert planes == expected

    pure = {
        word: permanent_dp(tuple(planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == -4
    assert sum(value != 0 for value in pure.values()) == 1
    profile = pair_profile(planes)
    assert profile == (3, 3, 3, 3, 3, 4)
    edge23_gcd = general_edge23_gcd()

    alpha = tuple(plane[0] for plane in planes)
    beta = tuple(plane[1] for plane in planes)
    marking = (0, sp.Rational(1, 2), 3, 0)
    marked = tuple(add(beta[i], scale(marking[i], alpha[i])) for i in range(4))
    assert all(sp.Matrix((alpha[i], marked[i])).rank() == 2 for i in range(4))

    extension = (0, 0, -1, -1, 0, 1, 0, 0)
    alpha5 = tuple((*alpha[i], extension[i]) for i in range(4))
    marked5 = tuple((*marked[i], extension[4 + i]) for i in range(4))
    contractions = ((1, 2, 0, 0, 0), (0, 0, 1, 2, 0))
    coefficient_sets = tuple(
        contraction_coefficients(alpha5, marked5, contraction)
        for contraction in contractions
    )
    for coefficients in coefficient_sets:
        assert all(coefficients[word] == 0 for word in WORDS[1:-1])
    diagonals = tuple(
        value
        for coefficients in coefficient_sets
        for value in (coefficients[WORDS[0]], coefficients[WORDS[-1]])
    )
    assert diagonals == (12, 6, 0, -6)

    variables = sp.symbols("z0:8")
    generic_alpha5 = tuple((*alpha[i], variables[i]) for i in range(4))
    generic_marked5 = tuple((*marked[i], variables[4 + i]) for i in range(4))
    generic_sets = tuple(
        contraction_coefficients(generic_alpha5, generic_marked5, contraction)
        for contraction in contractions
    )
    mixed_matrix = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in variables]
            for coefficients in generic_sets
            for word in WORDS[1:-1]
        ]
    )
    witness = sp.Matrix(extension)
    assert mixed_matrix.shape == (28, 8)
    assert mixed_matrix.rank() == 7
    assert mixed_matrix * witness == sp.zeros(28, 1)
    assert mixed_matrix.nullspace() == [witness]
    assert diagonals[1] * diagonals[3] == -36
    assert diagonals[0] != 0
    gamma_witnesses = one_gamma_audit(alpha5, marked5, contractions)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP permanent rebuild",
                "field": "Q",
                "arc_exact": True,
                "finite_r_zero_projection": "<h3,h0,t*h1-1>",
                "projection_certificate": projection,
                "t_zero_genuine_paired_incidence": "empty",
                "family_diagonals": family_diagonals,
                "family_rank_minor": family_rank_minor,
                "family_mode0_one_gamma_minor": family_gamma_minor,
                "pair_profile": profile,
                "general_edge23_maximal_minor_gcd": str(edge23_gcd),
                "mixed_matrix": [28, 8, 7],
                "extension": extension,
                "diagonals": tuple(map(str, diagonals)),
                "genuine_shared_incidence": True,
                "one_gamma_rank_witnesses": gamma_witnesses,
                "full_ternary_compatibility": "obstructed",
                "finite_r_zero_ternary_H22": "empty",
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
