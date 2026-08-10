#!/usr/bin/env python3
"""Close component 23's two s=1 parameter-infinity curves for H31/H22."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

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
from krenn_gu.p5_weighted_h22_contraction import build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")

from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)



ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P5_COMPONENT23_S_ONE_PARAMETER_INFINITY_CURVES_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

k, lam, inverse = sp.symbols("k lam u")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
w = sp.Symbol("w")
z = sp.Symbol("z")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def curve_rows(curve):
    beta = (B, add(B, C), C, C)
    if curve == "Dr":
        alpha = (
            A,
            add(A, scale(k, D)),
            D,
            add(scale(-1, A), scale(-1, C), B, scale(k, D)),
        )
    elif curve == "Dt":
        alpha = (
            A,
            add(A, scale(k, D)),
            add(A, scale(-1, C), B, scale(-k, D)),
            D,
        )
    else:
        raise ValueError(curve)
    return alpha, beta


def shifted(alpha, beta, marking=h):
    return tuple(
        add(beta[index], scale(marking[index], alpha[index])) for index in range(4)
    )


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def geometry_certificate(curve):
    alpha, beta = curve_rows(curve)
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(alpha[i] if bit == 0 else beta[i] for i, bit in enumerate(word))
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))

    planes = tuple((alpha[i], beta[i]) for i in range(4))
    matrices = tuple(pair_matrix(planes[i], planes[j]) for i, j in PAIRS)
    expected = (3, 2, 3, 3, 4, 4) if curve == "Dr" else (3, 3, 2, 4, 3, 4)
    special = (3, 2, 3, 3, 3, 4) if curve == "Dr" else (3, 3, 2, 3, 3, 4)
    assert tuple(matrix.rank() for matrix in matrices) == expected
    assert all(
        tuple(matrix.subs(k, value).rank() for matrix in matrices) == special
        for value in (0, 1, -1)
    )
    rank_four_edge = 4 if curve == "Dr" else 3
    maximal = [
        sp.factor(matrices[rank_four_edge].extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]
    maximal = [value for value in maximal if value != 0]
    assert sp.factor(sp.gcd_list(maximal) - 8 * k * (k - 1) * (k + 1)) == 0

    rank_two_edge = 1 if curve == "Dr" else 2
    kernel = matrices[rank_two_edge].nullspace()
    assert kernel == [sp.Matrix((0, 1, 0, 0)), sp.Matrix((0, 0, 1, 0))]
    support_pair = ((0, 1), (2, 3))
    return {
        "curve": curve,
        "pair_profile": expected,
        "special_profiles": {str(value): special for value in (0, 1, -1)},
        "rank_two_edge": "02" if curve == "Dr" else "03",
        "rank_four_minor_gcd": str(sp.factor(sp.gcd_list(maximal))),
        "zero_product_supports": support_pair,
        "pure_coefficient": "T1111=-4",
    }


def involution_certificate():
    dr_alpha, dr_beta = curve_rows("Dr")
    dt_alpha, dt_beta = curve_rows("Dt")

    def involution(row):
        return (-row[1], -row[0], row[3], row[2])

    mode_order = (0, 1, 3, 2)
    alpha_scales = (-1, -1, 1, -1)
    assert all(
        involution(dr_alpha[mode_order[i]]) == scale(alpha_scales[i], dt_alpha[i])
        for i in range(4)
    )
    assert all(involution(dr_beta[mode_order[i]]) == dt_beta[i] for i in range(4))

    old = sp.symbols("v0:4")
    moved = involution(old)
    mu = sp.Symbol("mu")
    assert (
        sp.expand(
            (mu * moved[0] + moved[1]).subs(mu, 1 / lam) + (lam * old[0] + old[1]) / lam
        )
        == 0
    )
    assert (
        sp.expand(
            (mu * moved[2] + moved[3]).subs(mu, 1 / lam) - (lam * old[2] + old[3]) / lam
        )
        == 0
    )
    return {
        "source_involution": "(-v1,-v0,v3,v2)",
        "mode_order": mode_order,
        "alpha_row_scales": alpha_scales,
        "marking_map": "(h0,h1,h2,h3)->(-h0,-h1,h3,-h2)",
        "deletion_map": "(0,1,2,3)->(1,0,3,2)",
        "weight_map": "[lambda:1]->[1:lambda] on both D01 and D23",
    }


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(label, program, expected, timeout=300):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [expected], (label, completed.stdout, expected)
    return label


EXPECTED_PROJECTIONS = {
    0: (h[3], h[1] - 1, h[0], (k**2 - 1) * h[2]),
    1: (h[3], h[1] - 1, h[0], (k**2 - 1) * h[2]),
    2: (h[2] - h[3], h[1] - 1, h[0], h[3] ** 2 - h[3], k * h[3] - h[3]),
    3: (h[2] + h[3], h[1] - 1, h[0], h[3] ** 2 - h[3], k * h[3] + h[3]),
}


def h31_projection(deletion):
    alpha, beta = curve_rows("Dr")
    marked = shifted(alpha, beta)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    vector = sp.Matrix(x)
    equations = (
        *tuple(mixed * vector),
        (diagonal_a * vector)[0] - 1,
        w * (diagonal_b * vector)[0] - 1,
    )
    eliminated = x + (w,)
    variables = eliminated + (k,) + h
    expected = EXPECTED_PROJECTIONS[deletion]
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
            "quit;",
        )
    )
    run_singular(f"Dr deletion {deletion}", program, f"RESULT:1:{len(expected)}")
    return {"deletion": deletion, "projected_ideal": tuple(map(str, expected))}


def h31_k_zero_nonextensions():
    alpha, beta = curve_rows("Dr")
    marked = shifted(alpha, beta)
    output = []
    for deletion in (0, 1):
        mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
        vector = sp.Matrix(x)
        equations = tuple(
            value.subs(k, 0)
            for value in (
                *tuple(mixed * vector),
                (diagonal_a * vector)[0] - 1,
                w * (diagonal_b * vector)[0] - 1,
            )
        )
        eliminated = x + (w,)
        variables = eliminated + h
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
                "option(redSB);",
                "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
                'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
                "quit;",
            )
        )
        run_singular(f"Dr k=0 deletion {deletion}", program, "RESULT:1:1")
        output.append(deletion)
    return tuple(output)


def global_one_marked(deletion, extension, alpha, marked, mode=1):
    pure = one_marked_map(mode, alpha, marked).row_join(sp.zeros(8, 1))
    neighbour = marked_extension(deletion, extension, alpha, marked, mode)
    common = tuple(index for index in range(4) if index != deletion)
    embedded = sp.zeros(8, 5)
    for column, coordinate in enumerate(common):
        embedded[:, coordinate] = neighbour[:, column]
    embedded[:, 4] = neighbour[:, 3]
    return pure.col_join(embedded)


def branch_certificate(label, deletion, marking, substitutions, require_nonzero=()):
    alpha, beta = curve_rows("Dr")
    alpha = tuple(
        tuple(sp.sympify(value).subs(substitutions) for value in row) for row in alpha
    )
    marked = shifted(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    frame = mixed.nullspace()
    assert len(frame) == 2 and mixed.rank() == 6
    c0, c1 = sp.symbols("c0 c1")
    extension = frame[0] * c0 + frame[1] * c1
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    stacked = global_one_marked(deletion, extension, alpha, marked)
    rows = (0, 6, 7, 8, 14)
    determinant = sp.factor(stacked.extract(rows, range(5)).det(method="domain-ge"))
    expected_sign = 1 if deletion == 0 else -1
    if deletion in (2, 3):
        expected_sign = -1
    assert sp.factor(determinant - expected_sign * 32 * actual_a) == 0
    return {
        "branch": label,
        "deletion": deletion,
        "marking": tuple(map(str, marking)),
        "substitutions": {str(key): str(value) for key, value in substitutions.items()},
        "localized_nonzero": tuple(map(str, require_nonzero)),
        "mixed_rank": 6,
        "kernel_frame": tuple(tuple(map(str, vector)) for vector in frame),
        "diagonals": (str(actual_a), str(actual_b)),
        "stacked_mode": 1,
        "stacked_rows": rows,
        "stacked_determinant": str(determinant),
        "determinant_over_A": str(expected_sign * 32),
    }


def h31_branches():
    branches = []
    for deletion in range(4):
        nonzero = (k,) if deletion in (0, 1) else ()
        branches.append(
            branch_certificate(
                f"generic_d{deletion}", deletion, (0, 1, 0, 0), {}, nonzero
            )
        )
    for sign in (1, -1):
        for deletion in (0, 1):
            branches.append(
                branch_certificate(
                    f"k_{sign}_h2_nonzero_d{deletion}",
                    deletion,
                    (0, 1, z, 0),
                    {k: sign},
                    (z,),
                )
            )
    branches.append(branch_certificate("k_1_extra_d2", 2, (0, 1, 1, 1), {k: 1}))
    branches.append(branch_certificate("k_minus_1_extra_d3", 3, (0, 1, -1, 1), {k: -1}))
    return tuple(branches)


H22_EXPECTED = {
    "Dr": {
        "lambda_one_nonzero_k": (
            "gen(1)",
            "gen(2)",
            "gen(3)",
            "gen(6)-gen(4)",
            "gen(7)",
            "gen(8)",
            "h3*gen(4)",
            "h2*gen(4)",
            "(h1+1)*gen(4)",
            "h0*gen(4)",
        ),
        "lambda_one_k_zero": ("gen(1)", "gen(2)", "gen(3)", "gen(6)-gen(4)", "gen(7)"),
        "lambda_minus_one": (
            "gen(1)",
            "gen(2)",
            "gen(3)",
            "gen(5)",
            "gen(6)+gen(4)",
            "gen(8)",
            "h3*gen(4)",
            "h2*gen(4)",
            "(h1+1)*gen(4)",
            "h0*gen(4)",
        ),
    },
    "Dt": {
        "lambda_one_nonzero_k": (
            "gen(1)",
            "gen(2)",
            "gen(4)",
            "gen(6)-gen(3)",
            "gen(7)",
            "gen(8)",
            "h3*gen(3)",
            "h2*gen(3)",
            "(h1-1)*gen(3)",
            "h0*gen(3)",
        ),
        "lambda_one_k_zero": ("gen(1)", "gen(2)", "gen(4)", "gen(6)-gen(3)", "gen(8)"),
        "lambda_minus_one": (
            "gen(1)",
            "gen(2)",
            "gen(4)",
            "gen(5)",
            "gen(6)+gen(3)",
            "gen(7)",
            "h3*gen(3)",
            "h2*gen(3)",
            "(h1-1)*gen(3)",
            "h0*gen(3)",
        ),
    },
}


def h22_module(curve, case):
    alpha, beta = curve_rows(curve)
    marked = shifted(alpha, beta)
    if case == "generic_weight":
        chart, slope, substitutions, localizer = (
            "finite",
            lam,
            {},
            (lam - 1) * (lam + 1),
        )
        expected_module = tuple(f"gen({index})" for index in range(1, 9))
        expected_membership = (True,) * 4
    elif case == "lambda_one_nonzero_k":
        chart, slope, substitutions, localizer = "finite", sp.Integer(1), {}, k
        expected_module = H22_EXPECTED[curve][case]
        expected_membership = (False, True, True, False)
    elif case == "lambda_one_k_zero":
        chart, slope, substitutions, localizer = (
            "finite",
            sp.Integer(1),
            {k: 0},
            sp.Integer(1),
        )
        expected_module = H22_EXPECTED[curve][case]
        expected_membership = (True, True, True, False)
    elif case == "lambda_minus_one":
        chart, slope, substitutions, localizer = (
            "finite",
            sp.Integer(-1),
            {},
            sp.Integer(1),
        )
        expected_module = H22_EXPECTED[curve][case]
        expected_membership = (True, False, False, True)
    elif case == "projective_weight":
        chart, slope, substitutions, localizer = "infinity", None, {}, sp.Integer(1)
        expected_module = tuple(f"gen({index})" for index in range(1, 9))
        expected_membership = (True,) * 4
    else:
        raise ValueError(case)

    models = tuple(
        build_model(alpha, marked, x, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = ",".join(
        coefficient_row(expression.subs(substitutions, simultaneous=True), x)
        for model in models
        for expression in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(model[key].subs(substitutions, simultaneous=True), x)
        for model in models
        for key in ("A", "B")
    )
    variables = (
        (() if k in substitutions else (k,))
        + h
        + ((lam,) if slope == lam else ())
        + (inverse,)
    )
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(" + singular_text(localizer) + ")-1; Q=std(Q); qring R=Q;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + ",".join(expected_module) + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            *(f"int z{index}=reduce(d{index},M)==0;" for index in range(4)),
            'print("RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M)));',
            "quit;",
        )
    )
    marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in expected_membership)
        + f":{len(expected_module)}"
    )
    run_singular(f"{curve} {case}", program, marker)
    return {
        "curve": curve,
        "case": case,
        "diagonal_order": ("A01", "B01", "A23", "B23"),
        "diagonal_membership": expected_membership,
        "module_generators": expected_module,
    }


def main():
    geometry = tuple(geometry_certificate(curve) for curve in ("Dr", "Dt"))
    involution = involution_certificate()
    projections = tuple(h31_projection(deletion) for deletion in range(4))
    k_zero_empty = h31_k_zero_nonextensions()
    branches = h31_branches()
    h22 = tuple(
        h22_module(curve, case)
        for curve in ("Dr", "Dt")
        for case in (
            "generic_weight",
            "lambda_one_nonzero_k",
            "lambda_one_k_zero",
            "lambda_minus_one",
            "projective_weight",
        )
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "boundary": "s=1, r=infinity and t=infinity replacement curves",
                "geometry": geometry,
                "involution": involution,
                "Dr_h31_projections": projections,
                "Dr_k_zero_false_projection_insertions": k_zero_empty,
                "Dr_h31_branches": branches,
                "h22_modules": h22,
                "fixed_order_marked_H31_empty": True,
                "fixed_order_weighted_H22_empty": True,
                "triple_parameter_infinity_included": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
