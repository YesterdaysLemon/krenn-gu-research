#!/usr/bin/env python3
"""Close component 23's two r=0,t=+-1 weighted-H22 fibres."""

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
u = sp.Symbol("u")

COMMON_ORDINARY_ROWS = (
    (0, 1, 3, 7, 8, 9, 11, 12),
    (0, 1, 3, 4, 7, 8, 9, 11),
    (1, 3, 4, 5, 7, 8, 9, 11),
    (1, 3, 4, 7, 8, 9, 11, 12),
    (1, 3, 4, 7, 8, 9, 11, 13),
    (1, 3, 4, 7, 8, 9, 11, 14),
    (1, 3, 4, 7, 8, 9, 11, 16),
    (1, 3, 4, 7, 8, 9, 11, 17),
)
EXTRA_ORDINARY_ROW = {
    1: (1, 3, 4, 7, 8, 9, 11, 22),
    -1: (1, 3, 4, 7, 8, 9, 11, 21),
}
EXTRA_RESIDUAL_VALUE = {
    1: 2048 * lam * (lam - 1) ** 3 * (lam + 1) ** 3,
    -1: 4096 * lam * (lam - 1) ** 3 * (lam + 1) ** 3,
}


def singular_text(expression):
    return str(sp.factor(expression)).replace("**", "^")


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


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pure_special_fibre_certificate():
    zero_marking = dict(zip(h, (0, 0, 0, 0)))
    beta = tuple(
        tuple(sp.sympify(entry).subs(zero_marking) for entry in row) for row in marked
    )
    coordinate_pairs = tuple(itertools.combinations(range(4), 2))

    def symmetric_product(left, right):
        return sp.Matrix(
            [left[i] * right[j] + left[j] * right[i] for i, j in coordinate_pairs]
        )

    profiles = []
    pure_coefficients = []
    for t_value in (1, -1):
        substitutions = {r: 0, t: t_value}
        specialized_alpha = tuple(
            tuple(sp.cancel(sp.sympify(entry).subs(substitutions)) for entry in row)
            for row in alpha
        )
        specialized_beta = tuple(
            tuple(sp.cancel(sp.sympify(entry).subs(substitutions)) for entry in row)
            for row in beta
        )
        planes = tuple(
            (specialized_alpha[index], specialized_beta[index]) for index in range(4)
        )
        ranks = []
        for left, right in itertools.combinations(range(4), 2):
            matrix = sp.Matrix.hstack(
                *(
                    symmetric_product(planes[left][i], planes[right][j])
                    for i in range(2)
                    for j in range(2)
                )
            )
            ranks.append(matrix.rank())
        assert tuple(ranks) == (3, 3, 3, 4, 3, 4)
        coefficients = (
            permanent4(specialized_alpha),
            permanent4(specialized_beta),
        )
        assert coefficients == (0, -4)
        profiles.append(tuple(ranks))
        pure_coefficients.append(coefficients)
    return tuple(profiles), tuple(pure_coefficients)


def ordinary_unit_certificate(t_value):
    matrix = mixed.subs({r: 0, t: t_value}, simultaneous=True)
    row_sets = COMMON_ORDINARY_ROWS + (EXTRA_ORDINARY_ROW[t_value],)
    determinants = tuple(
        sp.factor(matrix.extract(rows, range(8)).det(method="domain-ge"))
        for rows in row_sets
    )

    residual = {
        h[0]: 2 / (lam + 1),
        h[1]: 1,
        h[2]: 1,
        h[3]: 0,
    }
    assert all(
        sp.cancel(determinant.subs(residual, simultaneous=True)) == 0
        for determinant in determinants[:-1]
    )
    actual_extra = sp.factor(determinants[-1].subs(residual, simultaneous=True))
    assert sp.cancel(actual_extra - EXTRA_RESIDUAL_VALUE[t_value]) == 0

    localizer = lam * (lam - 1) * (lam + 1)
    variables = (*h, lam, u)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, determinants))
            + ",u*"
            + singular_text(localizer)
            + "-1;",
            "I=std(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    label = f"t_{'plus' if t_value == 1 else 'minus'}_one_ordinary_unit_ideal"
    run_singular(label, program, "RESULT:1:1")
    return {
        "label": label,
        "minor_count": len(determinants),
        "extra_rows": EXTRA_ORDINARY_ROW[t_value],
        "extra_residual_value": str(actual_extra),
    }


def module_certificate(
    label,
    t_value,
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
    all_substitutions = {r: 0, t: t_value, **substitutions}
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
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            "int sameModule=(size(ME)==0)&&(size(EM)==0);",
            *(f"int diagonal{index}=reduce(d{index},M)==0;" for index in range(4)),
            (
                '"RESULT:"+string(sameModule)+":"+'
                + '+":"+'.join(f"string(diagonal{index})" for index in range(4))
                + '+":"+string(size(M));'
            ),
            "quit;",
        )
    )
    marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in expected_membership)
        + f":{len(expected_indices)}"
    )
    run_singular(label, program, marker)
    return label


def endpoint_certificates(t_value):
    lambda_zero = mixed.subs({r: 0, t: t_value, lam: 0}, simultaneous=True)
    dense_minor = sp.factor(
        lambda_zero.extract((0, 1, 3, 4, 7, 8, 9, 14), range(8)).det(method="domain-ge")
    )
    expected_dense = -256 * h[3] if t_value == 1 else 256 * h[3] * (3 - 4 * h[3])
    assert sp.expand(dense_minor - expected_dense) == 0

    prefix = f"t_{'plus' if t_value == 1 else 'minus'}_one"
    lambda_zero_modules = [
        module_certificate(
            f"{prefix}_lambda_zero_h3_zero",
            t_value,
            "finite",
            sp.Integer(0),
            {h[3]: 0},
            h[:3],
            tuple(range(1, 9)),
            (True,) * 4,
        )
    ]
    if t_value == -1:
        lambda_zero_modules.append(
            module_certificate(
                f"{prefix}_lambda_zero_h3_three_quarters",
                t_value,
                "finite",
                sp.Integer(0),
                {h[3]: sp.Rational(3, 4)},
                h[:3],
                tuple(range(1, 9)),
                (True,) * 4,
            )
        )

    endpoint_modules = (
        module_certificate(
            f"{prefix}_lambda_one",
            t_value,
            "finite",
            sp.Integer(1),
            {},
            h,
            (1, 2, 3, 4, 6, 7, 8),
            (True, True, True, False),
        ),
        module_certificate(
            f"{prefix}_lambda_minus_one",
            t_value,
            "finite",
            sp.Integer(-1),
            {},
            h,
            (1, 2, 3, 4, 5, 6, 8),
            (True, False, True, True),
        ),
        module_certificate(
            f"{prefix}_projective_weight",
            t_value,
            "infinity",
            None,
            {},
            h,
            tuple(range(1, 9)),
            (True,) * 4,
        ),
    )
    return str(dense_minor), tuple(lambda_zero_modules), endpoint_modules


def main():
    pair_profiles, pure_coefficients = pure_special_fibre_certificate()
    ordinary = tuple(ordinary_unit_certificate(value) for value in (1, -1))
    endpoints = tuple(endpoint_certificates(value) for value in (1, -1))
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "parameter_points": ((0, 1), (0, -1)),
                "pure_pair_profiles": pair_profiles,
                "pure_coefficients_alpha_beta": tuple(
                    tuple(map(str, coefficients)) for coefficients in pure_coefficients
                ),
                "ordinary_certificates": ordinary,
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "endpoint_and_projective_certificates": endpoints,
                "claim_label": "VERIFIED_SPECIAL_ALL_PAIR_FIBRES_EMPTY",
                "weighted_H22_special_fibres_closed": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
