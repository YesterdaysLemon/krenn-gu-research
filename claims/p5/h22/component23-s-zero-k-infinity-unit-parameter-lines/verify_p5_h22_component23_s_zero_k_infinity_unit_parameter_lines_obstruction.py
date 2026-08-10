#!/usr/bin/env python3
"""Verify weighted-H22 emptiness on component 23's r,t=+/-1 corner lines."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import WORDS, build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-coordinate-survivor")

from verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_coordinate_survivor import (
    PAIRS,
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



u, lam, H = sp.symbols("u lam H")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")


def corner_rows(r, t):
    return (A, D, add(B, scale(r, D)), add(B, scale(t, D))), (B, B, C, C)


alpha, beta = corner_rows(sp.Integer(1), u)
marked = tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pure_and_pair_certificate():
    coefficients = {
        word: sp.factor(
            permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        )
        for word in WORDS
    }
    assert coefficients[WORDS[-1]] == -4
    assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
    planes = tuple(zip(alpha, beta))
    matrices = tuple(
        sp.Matrix.hstack(
            *(
                symmetric_product(planes[left][i], planes[right][j])
                for i in range(2)
                for j in range(2)
            )
        )
        for left, right in PAIRS
    )
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 3, 3, 4)
    edge23 = matrices[-1]
    minors = [
        sp.factor(edge23.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]
    gcd = sp.factor(sp.gcd_list([value for value in minors if value]))
    assert sp.expand(gcd - 8 * (u - 1) ** 2) == 0
    return coefficients[WORDS[-1]], gcd


def models_and_matrix(chart, slope=None, substitutions=None):
    substitutions = substitutions or {}
    models = tuple(
        build_model(alpha, marked, x, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    matrix = sp.Matrix(
        [
            [
                sp.diff(equation.subs(substitutions, simultaneous=True), variable)
                for variable in x
            ]
            for model in models
            for equation in model["mixed"]
        ]
    )
    return models, matrix


def ordinary_minor_certificate():
    _models, matrix = models_and_matrix("finite", lam)
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 4 * (u - 1) ** 2 * (u + 1)

    def determinant(rows, substitutions, expected):
        observed = sp.factor(
            matrix.subs(substitutions, simultaneous=True)
            .extract(rows, range(8))
            .det(method="domain-ge")
        )
        assert sp.expand(observed - expected) == 0, (rows, observed, expected)
        return rows

    return (
        determinant(
            (0, 1, 2, 3, 8, 9, 13, 16),
            {},
            common * h[2] * h[3] * u,
        ),
        determinant(
            (0, 1, 3, 5, 8, 9, 13, 16),
            {},
            -common * h[2] * (h[1] * u - 1),
        ),
        determinant(
            (0, 1, 3, 4, 8, 9, 13, 16),
            {},
            -common * h[3] * u * (h[1] - 1),
        ),
        determinant(
            (0, 1, 3, 7, 8, 9, 13, 16),
            {},
            common * h[0] * u,
        ),
        determinant(
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[3]: 0, h[1]: 1 / u},
            -256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (u - 1) ** 2 * (u + 1),
        ),
        determinant(
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[3]: 0},
            256 * u * (lam - 1) ** 5 * (lam + 1) ** 3 * (h[1] - 1) * (u - 1) * (u + 1),
        ),
    )


def contraction_rows(chart, slope=None):
    if chart == "finite":
        return ((1, slope, 0, 0, 0), (0, 0, 1, slope, 0))
    assert chart == "infinity"
    return ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))


def one_gamma_matrix(alpha5, marked5, chart, slope=None):
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contraction_rows(chart, slope):
        for word in itertools.product((0, 1), repeat=3):
            selected = (gamma,) + tuple(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            equations.append(permanent(selected + (contraction,)))
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )


def residual_family_certificate(chart, slope=None):
    substitutions = {h[0]: 0, h[1]: 1, h[2]: 0, h[3]: H}
    models, matrix = models_and_matrix(chart, slope, substitutions)
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, H * u))
    assert all(sp.expand(value) == 0 for value in matrix * kernel)
    rows = (0, 1, 3, 8, 9, 13, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(matrix.extract(rows, columns).det(method="domain-ge"))
    if chart == "finite":
        expected_rank_minor = (
            128 * u * (slope - 1) ** 4 * (slope + 1) ** 3 * (u - 1) ** 2
        )
        expected_diagonals = (
            2 * (slope + 1) * (u + 1),
            2 * H * (slope - 1) * (u + 1),
            0,
            -2 * (slope + 1),
        )
        expected_gamma_minor = (
            8 * H * (slope - 1) ** 4 * (slope + 1) * (u - 1) * (u + 1) ** 2
        )
    else:
        expected_rank_minor = 128 * u * (u - 1) ** 2
        expected_diagonals = (2 * (u + 1), 2 * H * (u + 1), 0, -2)
        expected_gamma_minor = 8 * H * (u - 1) * (u + 1) ** 2
    assert sp.expand(rank_minor - expected_rank_minor) == 0
    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind].subs(substitutions, simultaneous=True), variable)
                * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    assert all(
        sp.expand(observed - expected) == 0
        for observed, expected in zip(diagonals, expected_diagonals, strict=True)
    )
    alpha5 = tuple((*alpha[i], kernel[i]) for i in range(4))
    marked_rows = tuple(
        add(beta[i], scale(substitutions[h[i]], alpha[i])) for i in range(4)
    )
    marked5 = tuple((*marked_rows[i], kernel[4 + i]) for i in range(4))
    gamma_matrix = one_gamma_matrix(alpha5, marked5, chart, slope)
    gamma_rows = (0, 1, 2, 7, 9)
    gamma_minor = sp.factor(
        gamma_matrix.extract(gamma_rows, range(5)).det(method="domain-ge")
    )
    assert sp.expand(gamma_minor - expected_gamma_minor) == 0
    return str(rank_minor), tuple(map(str, diagonals)), str(gamma_minor)


def coefficient_vector(expression):
    return (
        "["
        + ",".join(singular_text(sp.diff(expression, variable)) for variable in x)
        + "]"
    )


def module_certificate(label, slope, expected, expected_size):
    models = tuple(
        build_model(alpha, marked, x, direction, "finite", slope)
        for direction in ("D01", "D23")
    )
    generators = [
        coefficient_vector(equation) for model in models for equation in model["mixed"]
    ]
    diagonals = [
        coefficient_vector(model[kind]) for model in models for kind in ("A", "B")
    ]
    program = "\n".join(
        (
            "ring R=(0,u),(" + ",".join(map(str, h)) + "),dp;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            *(f"vector d{i}={value};" for i, value in enumerate(diagonals)),
            *(f"int z{i}=reduce(d{i},M)==0;" for i in range(4)),
            (
                'print("RESULT:'
                + label
                + ':"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M)));'
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
    expected_marker = (
        "RESULT:"
        + label
        + ":"
        + ":".join("1" if value else "0" for value in expected)
        + f":{expected_size}"
    )
    assert markers == [expected_marker], (completed.stdout, expected_marker)
    return label


def projective_projection_certificate():
    models = tuple(
        build_model(alpha, marked, x, direction, "infinity", None)
        for direction in ("D01", "D23")
    )
    mixed = tuple(equation for model in models for equation in model["mixed"])
    diagonals = tuple(model[kind] for model in models for kind in ("A", "B"))
    w = sp.symbols("w")
    product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])
    variables = (*x, w, *h)
    program = "\n".join(
        (
            "ring R=(0,u),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed))
            + ","
            + singular_text(w * product - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,x0*x1*x2*x3*x4*x5*x6*x7*w); J=std(J);",
            "ideal E=h2,h1-1,h0; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=(size(JE)==0)&&(size(EJ)==0);",
            'print("RESULT:"+string(same)+":"+string(size(J))+":"+string(reduce(1,I)==0));',
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


def project(row, extension, direction, mu, nu):
    if direction == "D01":
        return (mu * row[0] + nu * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], mu * row[2] + nu * row[3], extension)
    raise ValueError(direction)


def homogeneous_tensor(alpha_rows, marked_rows, extensions, direction, mu, nu):
    projected_alpha = tuple(
        project(alpha_rows[i], extensions[i], direction, mu, nu) for i in range(4)
    )
    projected_marked = tuple(
        project(marked_rows[i], extensions[4 + i], direction, mu, nu) for i in range(4)
    )
    return {
        word: permanent(
            tuple(
                projected_marked[i] if word[i] else projected_alpha[i] for i in range(4)
            )
        )
        for word in WORDS
    }


def source_j(row):
    return (-row[1], -row[0], row[3], row[2])


def symmetry_certificate():
    r0, t0, mu, nu = sp.symbols("r0 t0 mu nu")
    h0 = sp.symbols("q0:4")
    e = sp.symbols("e0:8")
    old_alpha, old_beta = corner_rows(r0, t0)
    old_marked = tuple(add(old_beta[i], scale(h0[i], old_alpha[i])) for i in range(4))

    # Mode swap (2 3): parameter and marking coordinates swap, weight fixed.
    pullback = (0, 1, 3, 2)
    swapped_alpha, swapped_beta = corner_rows(t0, r0)
    swapped_h = (h0[0], h0[1], h0[3], h0[2])
    swapped_marked = tuple(
        add(swapped_beta[i], scale(swapped_h[i], swapped_alpha[i])) for i in range(4)
    )
    swapped_e = (e[0], e[1], e[3], e[2], e[4], e[5], e[7], e[6])
    for i, old_i in enumerate(pullback):
        assert swapped_alpha[i] == old_alpha[old_i]
        assert swapped_beta[i] == old_beta[old_i]
        assert swapped_marked[i] == old_marked[old_i]

    # Signed ambient involution J: parameters negate and weight reciprocates.
    signs = (-1, -1, 1, 1)
    signed_alpha, signed_beta = corner_rows(-r0, -t0)
    signed_h = (-h0[0], -h0[1], h0[2], h0[3])
    signed_marked = tuple(
        add(signed_beta[i], scale(signed_h[i], signed_alpha[i])) for i in range(4)
    )
    signed_e = (-e[0], -e[1], e[2], e[3], e[4], e[5], e[6], e[7])
    for i in range(4):
        assert source_j(old_alpha[i]) == scale(signs[i], signed_alpha[i])
        assert source_j(old_beta[i]) == signed_beta[i]
        assert source_j(old_marked[i]) == signed_marked[i]

    old_tensors = {
        direction: homogeneous_tensor(old_alpha, old_marked, e, direction, mu, nu)
        for direction in ("D01", "D23")
    }
    swapped_tensors = {
        direction: homogeneous_tensor(
            swapped_alpha, swapped_marked, swapped_e, direction, mu, nu
        )
        for direction in ("D01", "D23")
    }
    signed_tensors = {
        direction: homogeneous_tensor(
            signed_alpha, signed_marked, signed_e, direction, nu, mu
        )
        for direction in ("D01", "D23")
    }
    counts = {"mode_swap": 0, "signed_weight_reciprocity": 0}
    for direction, projected_sign in (("D01", -1), ("D23", 1)):
        for word in WORDS:
            pulled = (word[0], word[1], word[3], word[2])
            assert (
                sp.expand(
                    swapped_tensors[direction][word] - old_tensors[direction][pulled]
                )
                == 0
            )
            row_sign = sp.prod(signs[i] for i in range(4) if word[i] == 0)
            assert (
                sp.expand(
                    signed_tensors[direction][word]
                    - projected_sign * row_sign * old_tensors[direction][word]
                )
                == 0
            )
            counts["mode_swap"] += 1
            counts["signed_weight_reciprocity"] += 1
    return counts


def main():
    pure_beta, edge23_gcd = pure_and_pair_certificate()
    ordinary_minors = ordinary_minor_certificate()
    finite_rank_minor, finite_diagonals, finite_gamma_minor = (
        residual_family_certificate("finite", lam)
    )
    lambda_one = module_certificate(
        "lambda_one", sp.Integer(1), (False, True, True, False), 12
    )
    lambda_minus_one = module_certificate(
        "lambda_minus_one", sp.Integer(-1), (True, False, True, True), 5
    )
    projective_projection = projective_projection_certificate()
    projective_rank_minor, projective_diagonals, projective_gamma_minor = (
        residual_family_certificate("infinity", None)
    )
    symmetry_counts = symmetry_certificate()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(u)",
                "component": 23,
                "corner": "s=0,k=infinity",
                "base_line": "r=1; u=t; u*(u-1)*(u+1) != 0",
                "pure_support": {"1111": str(pure_beta)},
                "pair_profile": (3, 3, 3, 3, 3, 4),
                "edge23_maximal_minor_gcd": str(edge23_gcd),
                "ordinary_minor_rows": ordinary_minors,
                "ordinary_complete_residual": "h0=h2=0,h1=1,h3=H",
                "ordinary_rank_minor": finite_rank_minor,
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "ordinary_diagonals": finite_diagonals,
                "ordinary_one_gamma_minor": finite_gamma_minor,
                "finite_endpoints": (lambda_one, lambda_minus_one),
                "projective_projection": "<h2,h1-1,h0>",
                "projective_projection_certificate": projective_projection,
                "projective_rank_minor": projective_rank_minor,
                "projective_diagonals": projective_diagonals,
                "projective_one_gamma_minor": projective_gamma_minor,
                "symmetry_tensor_words_checked": symmetry_counts,
                "four_unit_parameter_lines_weighted_H22": "empty",
                "excluded_intersections": "u=0,+1,-1,infinity",
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
