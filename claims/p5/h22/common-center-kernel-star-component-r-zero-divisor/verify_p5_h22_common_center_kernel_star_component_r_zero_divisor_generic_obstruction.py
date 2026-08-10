#!/usr/bin/env python3
"""Close the divisor-generic r=0 weighted-H22 fibre of component 23."""

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
from krenn_gu.p5_weighted_h22_contraction import build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement")

from verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement import (
    F,
    H,
    alpha,
    h,
    marked,
    mixed,
    r,
    t,
    x,
)
from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)



lam = sp.Symbol("lam")


def pure_pair_profile():
    zero_marking = dict(zip(h, (0, 0, 0, 0)))
    beta = tuple(tuple(entry.subs(zero_marking) for entry in row) for row in marked)
    coordinate_pairs = tuple(itertools.combinations(range(4), 2))

    def symmetric_product(left, right):
        return sp.Matrix(
            [left[i] * right[j] + left[j] * right[i] for i, j in coordinate_pairs]
        )

    planes = tuple((alpha[index], beta[index]) for index in range(4))
    ranks = []
    for left, right in itertools.combinations(range(4), 2):
        matrix = sp.Matrix.hstack(
            *(
                symmetric_product(planes[left][i], planes[right][j]).subs(r, 0)
                for i in range(2)
                for j in range(2)
            )
        )
        ranks.append(matrix.rank())
    assert tuple(ranks) == (3, 3, 3, 4, 4, 4)
    return tuple(ranks)


def exact_minor(label, selected_rows, substitutions, expected):
    matrix = mixed.subs({r: 0, **substitutions}, simultaneous=True).extract(
        selected_rows, range(8)
    )
    actual = sp.factor(matrix.det(method="domain-ge"))
    assert sp.cancel(actual - expected) == 0, (label, actual, expected)
    return label


def module_certificate(
    label,
    chart,
    slope,
    substitutions,
    variables,
    expected_indices,
    expected_membership,
):
    models = (
        build_model(alpha, marked, x, "D01", chart, slope),
        build_model(alpha, marked, x, "D23", chart, slope),
    )
    all_substitutions = {r: 0, **substitutions}
    generators = ",".join(
        coefficient_row(equation.subs(all_substitutions, simultaneous=True), x)
        for model in models
        for equation in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(equation.subs(all_substitutions, simultaneous=True), x)
        for model in models
        for equation in (model["A"], model["B"])
    )
    expected = ",".join(f"gen({index})" for index in expected_indices)
    program = "\n".join(
        (
            "ring R=(0,t),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            "vector A01=" + diagonals[0] + ";",
            "vector B01=" + diagonals[1] + ";",
            "vector A23=" + diagonals[2] + ";",
            "vector B23=" + diagonals[3] + ";",
            (
                '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"'
                '+string(reduce(A01,M)==0)+":"+string(reduce(A23,M)==0)+":"'
                '+string(reduce(B01,M)==0)+":"+string(reduce(B23,M)==0)+":"'
                "+string(size(M));"
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
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in expected_membership)
        + f":{len(expected_indices)}"
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [marker], (label, completed.stdout)
    return label


def ordinary_certificates():
    ordinary = lam * (lam - 1) * (lam + 1)
    certificates = [
        exact_minor(
            "ordinary_dense_minor",
            (0, 1, 3, 7, 8, 9, 11, 12),
            {},
            -2048
            * h[3]
            * lam
            * (lam - 1) ** 2
            * (lam + 1) ** 3
            * (h[0] * (lam + 1) - 2),
        )
    ]

    # F|_(r=0)=h3*t^2*(h0*(lam+1)-2).  The h3!=0 factor branch is empty.
    certificates.append(
        exact_minor(
            "ordinary_h3_nonzero_F_zero",
            (0, 1, 3, 4, 7, 8, 9, 11),
            {h[0]: 2 / (lam + 1)},
            -2048 * h[3] * lam * (lam - 1) ** 2 * (lam + 1) ** 4,
        )
    )

    # On h3=0 the first minor leaves h2=0 or h1=1.
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_primary_split",
            (1, 3, 4, 5, 7, 8, 9, 11),
            {h[3]: 0},
            -2048 * h[2] * lam * (h[1] - 1) * (lam - 1) ** 2 * (lam + 1) ** 4,
        )
    )

    # First residual: h3=h2=0.
    certificates.append(
        exact_minor(
            "ordinary_h3_h2_zero_h0_split",
            (1, 3, 4, 7, 8, 9, 11, 12),
            {h[2]: 0, h[3]: 0},
            2048 * lam * (lam - 1) ** 3 * (lam + 1) ** 3 * (h[0] - h[1] - 1),
        )
    )
    certificates.append(
        exact_minor(
            "ordinary_h3_h2_zero_h0_relation",
            (1, 3, 4, 7, 8, 9, 11, 13),
            {h[0]: h[1] + 1, h[2]: 0, h[3]: 0},
            -2048 * lam * (h[1] - 1) * (lam - 1) ** 3 * (lam + 1) ** 3,
        )
    )
    certificates.append(
        exact_minor(
            "ordinary_h3_h2_zero_terminal_weight_split",
            (1, 3, 4, 7, 8, 9, 11, 14),
            {h[0]: 2, h[1]: 1, h[2]: 0, h[3]: 0},
            1024 * lam * (lam - 1) ** 3 * (lam + 1) ** 3 * ((lam + 1) * t - 2) / t,
        )
    )
    terminal_weight = 2 / t - 1
    certificates.append(
        exact_minor(
            "ordinary_h3_h2_zero_terminal",
            (1, 3, 4, 7, 8, 9, 11, 16),
            {
                h[0]: 2,
                h[1]: 1,
                h[2]: 0,
                h[3]: 0,
                lam: terminal_weight,
            },
            131072 * (t - 2) * (t - 1) ** 3 / t**9,
        )
    )

    # Second residual: h3=0,h1=1, with h2 arbitrary.
    G = 2 * h[0] * h[2] * lam - h[0] * lam + h[0] - 2 * h[2] * lam + 2 * lam - 2
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_h1_one_G_split",
            (1, 3, 4, 7, 8, 9, 11, 12),
            {h[1]: 1, h[3]: 0},
            -2048 * lam * (lam - 1) ** 2 * (lam + 1) ** 3 * G,
        )
    )
    h2_solution = (lam - 1) * (h[0] - 2) / (2 * lam * (h[0] - 1))
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_h1_one_G_zero",
            (1, 3, 4, 7, 8, 9, 11, 14),
            {h[1]: 1, h[2]: h2_solution, h[3]: 0},
            512
            * (lam - 1) ** 3
            * (lam + 1) ** 3
            * (h[0] * (lam + 1) - 2)
            * ((lam + 1) * t - 2)
            / t,
        )
    )
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_h1_one_G_J0",
            (1, 3, 4, 7, 8, 9, 11, 17),
            {
                h[0]: 2 / (lam + 1),
                h[1]: 1,
                h[2]: 1,
                h[3]: 0,
            },
            -2048 * lam * (lam - 1) ** 3 * (lam + 1) ** 3 * (t - 1) * (t + 1) / t,
        )
    )
    L = h[0] * t - 4 * h[0] + 2 * t
    h2_weight_solution = sp.cancel(h2_solution.subs(lam, terminal_weight))
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_h1_one_G_Jt_split",
            (1, 3, 4, 7, 8, 9, 11, 17),
            {
                h[1]: 1,
                h[2]: h2_weight_solution,
                h[3]: 0,
                lam: terminal_weight,
            },
            -131072 * (t - 1) ** 4 * (t + 1) * L / t**9,
        )
    )
    terminal_h0 = -2 * t / (t - 4)
    terminal_h2 = 4 * (t - 1) / (3 * t - 4)
    assert sp.cancel(h2_weight_solution.subs(h[0], terminal_h0) - terminal_h2) == 0
    certificates.append(
        exact_minor(
            "ordinary_h3_zero_h1_one_G_Jt_terminal",
            (1, 3, 4, 7, 8, 9, 11, 16),
            {
                h[0]: terminal_h0,
                h[1]: 1,
                h[2]: terminal_h2,
                h[3]: 0,
                lam: terminal_weight,
            },
            131072 * (t - 2) * (t - 1) ** 3 / (t**8 * (t - 4)),
        )
    )

    assert ordinary != 0
    return tuple(certificates)


def main():
    pair_profile = pure_pair_profile()
    r0_F = sp.factor(F.subs(r, 0))
    r0_H = sp.factor(H.subs(r, 0))
    assert sp.expand(r0_F - h[3] * t**2 * (h[0] * (lam + 1) - 2)) == 0
    assert (
        sp.expand(
            r0_H
            - (
                4 * h[3] * lam * t**2
                + 2 * h[3] * lam * t
                - 4 * h[3] * lam
                + 2 * h[3] * t**2
                + 2 * h[3] * t
                - 4 * h[3]
                - lam * t
                - t
                + 2
            )
        )
        == 0
    )

    ordinary = ordinary_certificates()

    H0 = sp.factor(r0_H.subs(lam, 0))
    H0_solution = sp.cancel((t - 2) / (2 * (t - 1) * (t + 2)))
    assert sp.cancel(H0.subs(h[3], H0_solution)) == 0
    endpoint_certificates = (
        exact_minor(
            "lambda_zero_dense_minor",
            (0, 1, 3, 4, 7, 8, 9, 14),
            {lam: 0},
            -256 * h[3] * H0 / t,
        ),
        module_certificate(
            "lambda_zero_h2_zero",
            "finite",
            sp.Integer(0),
            {h[2]: 0},
            (h[0], h[1], h[3]),
            tuple(range(1, 9)),
            (True, True, True, True),
        ),
        module_certificate(
            "lambda_zero_h3_zero",
            "finite",
            sp.Integer(0),
            {h[3]: 0},
            (h[0], h[1], h[2]),
            tuple(range(1, 9)),
            (True, True, True, True),
        ),
        module_certificate(
            "lambda_zero_H_zero",
            "finite",
            sp.Integer(0),
            {h[3]: H0_solution},
            (h[0], h[1], h[2]),
            tuple(range(1, 9)),
            (True, True, True, True),
        ),
        module_certificate(
            "lambda_one",
            "finite",
            sp.Integer(1),
            {},
            h,
            (1, 2, 3, 4, 6, 7, 8),
            (True, True, True, False),
        ),
        module_certificate(
            "lambda_minus_one",
            "finite",
            sp.Integer(-1),
            {},
            h,
            tuple(range(1, 9)),
            (True, True, True, True),
        ),
        module_certificate(
            "projective_weight",
            "infinity",
            None,
            {},
            h,
            tuple(range(1, 9)),
            (True, True, True, True),
        ),
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(t)",
                "component": 23,
                "component_divisor": "r=0",
                "pure_pair_profile": pair_profile,
                "claim_label": "VERIFIED_DIVISOR_GENERIC_EMPTY",
                "ordinary_minor_tree": ordinary,
                "finite_endpoint_and_projective_certificates": endpoint_certificates,
                "finite_weight_chart_closed": True,
                "projective_weight_chart_closed": True,
                "weighted_H22_divisor_generic_fibre_closed": True,
                "exceptional_t_points_individually_classified": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
