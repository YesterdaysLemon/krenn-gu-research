#!/usr/bin/env python3
"""Verify the remaining ordinary component-23 finite H22 residual."""

from __future__ import annotations

import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement")
expose_claim_package(REPO_ROOT, "claims/p5/h31/common-center-kernel-star")

import verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement as D
from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)
from verify_p5_h31_common_center_kernel_star_component_generic_obstruction import (
    rows,
    shifted,
)




def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def h3_zero_module(h1_solution):
    r, t, lam = D.r, D.t, D.lam
    h, x = D.h, D.x
    alpha, canonical = rows(r, t)
    marked = shifted(canonical, alpha, h)
    models = (
        build_model(alpha, marked, x, "D01", "finite", lam),
        build_model(alpha, marked, x, "D23", "finite", lam),
    )
    substitutions = {h[3]: 0, h[1]: h1_solution}
    generators = [
        coefficient_row(equation.subs(substitutions, simultaneous=True), x)
        for model in models
        for equation in model["mixed"]
    ]
    relation = "u*h2*lam*(lam-1)*(lam+1)-1"
    generators.extend(
        "[" + ",".join(relation if column == row else "0" for column in range(8)) + "]"
        for row in range(8)
    )
    expected = ",".join(f"gen({index})" for index in range(1, 9))
    program = "\n".join(
        (
            "ring R=(0,r,t),(h0,h2,lam,u),dp;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:8"], completed.stdout
    return "F_zero_h3_zero_h2_nonzero_ordinary_full_module"


def H_zero_minor(L, C):
    r, t, lam = D.r, D.t, D.lam
    h = D.h
    selected_rows = (0, 1, 2, 3, 7, 8, 9, 11)
    selected = D.mixed.extract(selected_rows, range(8))
    entries = ",".join(sg(entry) for entry in list(selected))
    expected = (
        -1024
        * r
        * t
        * (r + 1)
        * (r * t - 1) ** 5
        * h[2]
        * lam
        * (lam - 1) ** 2
        * (lam + 1) ** 4
        * C
        / ((r - t) ** 2 * L)
    )
    program = "\n".join(
        (
            "ring R=(0,r,t,lam,h0,h2),(h1,h3),dp;",
            "matrix M[8][8]=" + entries + ";",
            "poly F=" + sg(D.F) + ";",
            "poly H=" + sg(D.H) + ";",
            "ideal I=F,H; I=std(I);",
            "poly q=reduce(det(M),I);",
            "number expected=" + sg(expected) + ";",
            '"RESULT:"+string(q-expected==0)+":"+string(size(I));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:2"], completed.stdout
    return "F_H_zero_selected_minor_normal_form"


def main():
    r, t, lam = D.r, D.t, D.lam
    h = D.h

    h1_coefficient = sp.factor(sp.diff(D.F, h[1]))
    expected_coefficient = -r * (lam - 1) * (r - t) * (r * t - 1)
    assert sp.factor(h1_coefficient - expected_coefficient) == 0
    h1_solution = sp.cancel(-D.F.subs({h[1]: 0, h[3]: 0}) / h1_coefficient)
    assert sp.cancel(D.F.subs({h[3]: 0, h[1]: h1_solution}, simultaneous=True)) == 0

    L = sp.factor(sp.diff(D.H, h[3]) / 2)
    C = sp.factor(D.H.subs(h[3], 0) / (r + 1))
    assert sp.expand(D.H - (2 * L * h[3] + (r + 1) * C)) == 0
    resultant = sp.factor(sp.resultant(L, C, lam))
    expected_resultant = (
        -3 * r**3
        + 3 * r**2 * t
        + 4 * r**2
        - 3 * r * t**2
        - 4 * r * t
        + 2 * r
        - t**3
        + 4 * t**2
        + 2 * t
        - 4
    )
    assert sp.expand(resultant - expected_resultant) == 0
    coefficient_field = sp.QQ.frac_field(r, t)
    assert sp.Poly(L, lam, domain=coefficient_field).gcd(
        sp.Poly(C, lam, domain=coefficient_field)
    ) == sp.Poly(1, lam, domain=coefficient_field)

    certificates = (
        h3_zero_module(h1_solution),
        H_zero_minor(L, C),
        "L_C_coprime_so_H_zero_C_zero_implies_h3_zero",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(r,t)",
                "component": 23,
                "direction": "remaining finite ordinary F-zero residual",
                "claim_label": "VERIFIED_EMPTY_WITH_PRIOR_FACTOR_COVER",
                "F_h1_coefficient": str(h1_coefficient),
                "H_decomposition": "H=2*L*h3+(r+1)*C",
                "L": str(L),
                "C": str(C),
                "resultant_L_C": str(resultant),
                "certificates": certificates,
                "ordinary_residual_closed": True,
                "generic_finite_all_markings_closed_with_prior_results": True,
                "generic_weighted_H22_component_closed_with_prior_infinity_result": True,
                "special_projective_component_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
