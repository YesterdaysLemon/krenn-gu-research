#!/usr/bin/env python3
"""Verify the component-21 q=+/-p shared-branch ternary obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/coincident-support")

from derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate import (
    WORDS,
    build_model,
    pure_bases,
    shifted_beta,
    singular_command,
)
from krenn_gu.p5_marked_basis import one_marked_map



import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_Q_PLUS_MINUS_P_SHARED_BRANCH_TERNARY_OBSTRUCTION.md"


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def zero(expression, label):
    assert sp.factor(sp.cancel(expression)) == 0, label


def projection_certificate(sign, chart):
    p, kappa, ell = sp.symbols("p kappa ell")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv_a, inv_b = sp.symbols("u v")
    lam = sp.Symbol("lambda")
    alpha, beta = pure_bases(p, sign * p, kappa, ell)
    marked = shifted_beta(alpha, beta, h)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, z, "D01", chart, slope)
    d23 = build_model(alpha, marked, z, "D23", chart, slope)
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        d01["B"] - 1,
        *tuple(d23["mixed"] * sp.Matrix(z)),
        inv_a * d23["A"] - 1,
        inv_b * d23["B"] - 1,
    )
    eliminated = z + (inv_a, inv_b)
    retained = h + ((lam,) if chart == "finite" else ())
    variables = eliminated + retained
    expected = (
        h[3],
        h[2] - sign * kappa,
        (ell + sign) * h[1] + 1,
        p * (ell + sign) * h[0] + sign * ell,
    )
    program = "\n".join(
        (
            "ring R=(0,p,kappa,ell),("
            + ",".join(map(str, variables))
            + f"),(dp(10),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(sg, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            (
                'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"'
                '+string(size(I))+":"+string(size(J)));'
            ),
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        sign,
        chart,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        sign,
        chart,
        completed.stdout,
    )
    _, _, ideal_size, projection_size = markers[0].split(":")
    return {
        "sign": sign,
        "chart": chart,
        "ideal_size": int(ideal_size),
        "projection_size": int(projection_size),
        "projection_equal": True,
    }


def shared_matrix(d01, d23, extensions):
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        *tuple(d23["mixed"] * sp.Matrix(extensions)),
    )
    return sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in extensions]
            for equation in equations
        ]
    )


def branch_certificate(sign, chart):
    p, kappa, ell, lam, cap_c = sp.symbols("p kappa ell lambda C0")
    z = sp.symbols("z0:8")
    alpha, beta = pure_bases(p, sign * p, kappa, ell)
    marking = (
        -sign * ell / (p * (ell + sign)),
        -1 / (ell + sign),
        sign * kappa,
        0,
    )
    marked = shifted_beta(alpha, beta, marking)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, z, "D01", chart, slope)
    d23 = build_model(alpha, marked, z, "D23", chart, slope)
    zero(d01["A"], (sign, chart, "D01 all-alpha Hall diagonal"))
    matrix = shared_matrix(d01, d23, z)
    vector = sp.Matrix(
        (
            -sign * p * (ell + sign),
            0,
            sign * ell,
            0,
            0,
            sign,
            kappa * (ell - sign),
            0,
        )
    )
    assert all(sp.factor(value) == 0 for value in matrix * vector)

    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minors = []
    if chart == "finite" and sign == 1:
        rows = (11, 14, 16, 17, 18, 22, 26)
        determinant = sp.factor(matrix.extract(rows, columns).det())
        expected = 512 * p**4 * (lam - 1) ** 4 * (lam + 1) * (ell - 1) / (ell + 1)
        zero(determinant - expected, "finite sign-plus rank minor")
        rank_minors.append((rows, determinant))
    elif chart == "finite":
        rows_a = (11, 14, 16, 17, 18, 22, 26)
        rows_b = (10, 11, 16, 18, 22, 23, 26)
        determinant_a = sp.factor(matrix.extract(rows_a, columns).det())
        determinant_b = sp.factor(matrix.extract(rows_b, columns).det())
        expected_a = (
            -512 * lam**2 * p**4 * (lam - 1) ** 4 * (lam + 1) * (ell + 1) / (ell - 1)
        )
        cap_h = lam * ell + lam + ell - 1
        expected_b = 128 * p**4 * (lam - 1) ** 4 * (lam + 1) ** 2 * (ell + 1) * cap_h
        zero(determinant_a - expected_a, "finite sign-minus rank minor A")
        zero(determinant_b - expected_b, "finite sign-minus rank minor B")
        zero(cap_h.subs(lam, 0) - (ell - 1), "finite sign-minus cover")
        rank_minors.extend(((rows_a, determinant_a), (rows_b, determinant_b)))
    elif sign == 1:
        rows = (10, 11, 16, 18, 22, 23, 26)
        determinant = sp.factor(matrix.extract(rows, columns).det())
        expected = 128 * p**4 * (ell - 1) * (ell + 1)
        zero(determinant - expected, "infinity sign-plus rank minor")
        rank_minors.append((rows, determinant))
    else:
        rows = (10, 11, 16, 17, 18, 22, 26)
        determinant = sp.factor(matrix.extract(rows, columns).det())
        expected = -256 * p**4 * (ell + 1) ** 2
        zero(determinant - expected, "infinity sign-minus rank minor")
        rank_minors.append((rows, determinant))

    substitution = dict(zip(z, cap_c * vector, strict=True))
    diagonals = tuple(
        sp.factor(expression.subs(substitution))
        for expression in (d01["B"], d23["A"], d23["B"])
    )
    cap_f = lam * ell + lam - ell + 1
    if chart == "finite":
        expected_diagonals = (
            2 * sign * cap_c * p * cap_f,
            2 * cap_c * p * (ell + sign) ** 2 * (lam - 1),
            -2 * cap_c * (ell - sign) * (lam + 1),
        )
        weight_factor = (lam + 1) ** 3
    else:
        expected_diagonals = (
            2 * sign * cap_c * p * (ell + 1),
            2 * cap_c * p * (ell + sign) ** 2,
            -2 * cap_c * (ell - sign),
        )
        weight_factor = 1
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected, (sign, chart, "diagonal"))

    one_marked = one_marked_map(3, d23["alpha_rows"], d23["beta_rows"]).subs(
        substitution
    )
    ternary_rows = (0, 1, 4, 7)
    ternary_minor = sp.factor(one_marked.extract(ternary_rows, range(4)).det())
    expected_ternary = (
        8 * cap_c**3 * p**3 * (ell + sign) ** 3 * (ell - sign) ** 2 * weight_factor
    )
    zero(ternary_minor - expected_ternary, (sign, chart, "ternary minor"))
    return {
        "sign": sign,
        "chart": chart,
        "kernel_vector": [str(sp.factor(value)) for value in vector],
        "rank_minor_rows": [list(rows) for rows, _ in rank_minors],
        "rank_minor_values": [str(value) for _, value in rank_minors],
        "diagonals": [str(value) for value in diagonals],
        "ternary_minor_rows": list(ternary_rows),
        "ternary_minor": str(ternary_minor),
        "common_kernel_complete": True,
        "ternary_rank_four_on_genuine_open": True,
    }


def main():
    p, kappa, ell = sp.symbols("p kappa ell")
    pure_supports = {}
    for sign in (1, -1):
        alpha, beta = pure_bases(p, sign * p, kappa, ell)
        support = {
            word: sp.factor(
                permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            )
            for word in WORDS
        }
        assert support[WORDS[-1]] == 4 * p
        assert all(value == 0 for word, value in support.items() if word != WORDS[-1])
        pure_supports[str(sign)] = "T_1111=4*p only"

    projection_jobs = [
        (sign, chart) for sign in (1, -1) for chart in ("finite", "infinity")
    ]
    projections = [projection_certificate(*job) for job in projection_jobs]
    branches = [branch_certificate(sign, chart) for sign, chart in projection_jobs]
    theorem_hash = hashlib.sha256(THEOREM.read_bytes()).hexdigest()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic-zero function fields and exact specialization identities",
                "component": 21,
                "divisors": ["q=+p", "q=-p"],
                "pure_supports": pure_supports,
                "shared_incidence_projections": projections,
                "branch_certificates": branches,
                "homogeneous_weight_cover": ["finite [lambda:1]", "infinity [1:0]"],
                "generic_q_sign_divisor_H22_empty": True,
                "displayed_branch_obstructed_at_kappa_zero": True,
                "ell_plus_minus_one_intersections_closed": False,
                "all_kappa_zero_specialization_branches_classified": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": theorem_hash,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
