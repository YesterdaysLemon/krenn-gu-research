#!/usr/bin/env python3
"""Verify component 21 q=+/-p at both ell endpoints."""

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
    permanent4,
    pure_bases,
    shifted_beta,
    singular_command,
)
from verify_p5_h31_marked_basis_open_branch import one_marked_map



import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_Q_PLUS_MINUS_P_ELL_ENDPOINT_COMPLETE_OBSTRUCTION.md"


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def zero(expression, label):
    assert sp.factor(sp.cancel(expression)) == 0, label


def endpoint_projection(sign, side, chart, kappa_zero):
    p, kappa = sp.symbols("p kappa")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv_a, inv_b = sp.symbols("u v")
    lam = sp.Symbol("lambda")
    ell = sign if side == "same" else -sign
    active_kappa = 0 if kappa_zero else kappa
    alpha, beta = pure_bases(p, sign * p, active_kappa, ell)
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
    if side == "same" and not kappa_zero:
        expected = (h[3], 2 * h[1] + sign, 2 * p * h[0] + sign)
    elif side == "same":
        expected = (h[3], h[2], 2 * h[1] + sign, 2 * p * h[0] + sign)
    elif not kappa_zero:
        expected = (h[3], h[2] + sign * kappa, h[1], 2 * p * h[0] + sign)
    else:
        expected = (h[3], h[2], h[1])
    field = "p" if kappa_zero else "p,kappa"
    program = "\n".join(
        (
            f"ring R=(0,{field}),("
            + ",".join(map(str, variables))
            + f"),(dp(10),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(sg, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        sign,
        side,
        chart,
        kappa_zero,
        completed.stdout,
        completed.stderr,
    )
    expected_size = len(expected)
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [f"RESULT:1:{expected_size}"], (
        sign,
        side,
        chart,
        kappa_zero,
        completed.stdout,
    )
    return {
        "sign": sign,
        "endpoint": f"ell={'epsilon' if side == 'same' else '-epsilon'}",
        "chart": chart,
        "kappa": "0" if kappa_zero else "function-field",
        "projection_size": expected_size,
        "projection_equal": True,
    }


def common_matrix(d01, d23, z):
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        *tuple(d23["mixed"] * sp.Matrix(z)),
    )
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in z] for equation in equations]
    )


def check_kernel(matrix, vectors, rank_minors, label):
    for vector in vectors:
        assert all(sp.factor(value) == 0 for value in matrix * vector), label
    for rows, columns, expected in rank_minors:
        zero(matrix.extract(rows, columns).det() - expected, (label, rows, columns))
    assert sp.Matrix.hstack(*vectors).rank() == len(vectors)


def same_endpoint_generic(sign, chart):
    p, kappa, t, lam, cap_c = sp.symbols("p kappa t lambda C")
    z = sp.symbols("z0:8")
    marking = (-sign / (2 * p), -sp.Rational(sign, 2), t, 0)
    alpha, canonical = pure_bases(p, sign * p, kappa, sign)
    beta = shifted_beta(alpha, canonical, marking)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, beta, z, "D01", chart, slope)
    d23 = build_model(alpha, beta, z, "D23", chart, slope)
    matrix = common_matrix(d01, d23, z)
    d = t - sign * kappa
    vector = sp.Matrix(
        (
            -2 * sign * p * (t + sign * kappa),
            -2 * sign * d,
            2 * kappa,
            0,
            d,
            t + sign * kappa,
            0,
            2 * d,
        )
    )
    columns = (0, 1, 2, 3, 4, 5, 6)
    if chart == "finite" and sign == 1:
        minors = (
            (
                (10, 11, 16, 18, 22, 26, 28),
                columns,
                -256 * lam**2 * p**3 * d * (lam - 1) ** 5,
            ),
            (
                (14, 16, 17, 18, 22, 26, 28),
                columns,
                128 * p**3 * d * (lam - 1) ** 5 * (lam + 1),
            ),
        )
    elif chart == "finite":
        minors = (
            (
                (10, 11, 16, 18, 22, 26, 28),
                columns,
                256 * p**3 * d * (lam - 1) ** 5,
            ),
        )
    elif sign == 1:
        minors = (((10, 11, 16, 18, 22, 26, 28), columns, -256 * p**3 * d),)
    else:
        minors = (((14, 16, 17, 18, 22, 26, 28), columns, -128 * p**3 * d),)
    check_kernel(matrix, (vector,), minors, (sign, "same generic", chart))
    substitution = dict(zip(z, cap_c * vector, strict=True))
    diagonals = tuple(
        sp.factor(value.subs(substitution)) for value in (d01["B"], d23["A"], d23["B"])
    )
    cap_n = kappa * (lam - 1) + t * (lam + 1)
    if chart == "finite":
        expected_diagonals = (
            4 * cap_c * p * cap_n,
            16 * cap_c * kappa * p * (lam - 1),
            4 * cap_c * d * (lam + 1),
        )
        weight = (lam + 1) ** 3
    else:
        expected_diagonals = (
            4 * cap_c * p * (t + kappa),
            16 * cap_c * kappa * p,
            4 * cap_c * d,
        )
        weight = 1
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected, (sign, "same generic diagonal", chart))
    marked = one_marked_map(3, d23["alpha_rows"], d23["beta_rows"]).subs(substitution)
    determinant = sp.factor(marked.extract((0, 1, 4, 7), range(4)).det())
    expected_det = sign * 512 * cap_c**3 * kappa * p**3 * d**2 * weight
    zero(determinant - expected_det, (sign, "same generic ternary", chart))

    special_beta = shifted_beta(
        alpha, canonical, (-sign / (2 * p), -sp.Rational(sign, 2), sign * kappa, 0)
    )
    special_d01 = build_model(alpha, special_beta, z, "D01", chart, slope)
    special_d23 = build_model(alpha, special_beta, z, "D23", chart, slope)
    special_matrix = common_matrix(special_d01, special_d23, z)
    special_vector = sp.Matrix((-2 * p, 0, 1, 0, 0, sign, 0, 0))
    special_columns = (0, 1, 2, 3, 4, 6, 7)
    if chart == "finite" and sign == 1:
        special_minors = (
            (
                (10, 11, 16, 18, 22, 26, 28),
                special_columns,
                -256 * kappa * lam**2 * p**3 * (lam - 1) ** 5,
            ),
            (
                (14, 16, 17, 18, 22, 26, 28),
                special_columns,
                128 * kappa * p**3 * (lam - 1) ** 5 * (lam + 1),
            ),
        )
    elif chart == "finite":
        special_minors = (
            (
                (10, 11, 16, 18, 22, 26, 28),
                special_columns,
                -256 * kappa * p**3 * (lam - 1) ** 5,
            ),
        )
    elif sign == 1:
        special_minors = (
            ((10, 11, 16, 18, 22, 26, 28), special_columns, -256 * kappa * p**3),
        )
    else:
        special_minors = (
            ((14, 16, 17, 18, 22, 26, 28), special_columns, 128 * kappa * p**3),
        )
    check_kernel(
        special_matrix,
        (special_vector,),
        special_minors,
        (sign, "same d=0", chart),
    )
    special_substitution = dict(zip(z, cap_c * special_vector, strict=True))
    zero(special_d23["B"].subs(special_substitution), (sign, "same d=0 B23", chart))
    return {
        "sign": sign,
        "chart": chart,
        "generic_kernel_complete": True,
        "generic_diagonals": [str(value) for value in diagonals],
        "generic_ternary_minor": str(determinant),
        "d_zero_kernel_complete": True,
        "d_zero_B23": "0",
    }


def same_endpoint_kappa_zero(sign, chart):
    p, lam, cap_x, cap_y = sp.symbols("p lambda X Y")
    z = sp.symbols("z0:8")
    alpha, canonical = pure_bases(p, sign * p, 0, sign)
    beta = shifted_beta(
        alpha, canonical, (-sign / (2 * p), -sp.Rational(sign, 2), 0, 0)
    )
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, beta, z, "D01", chart, slope)
    d23 = build_model(alpha, beta, z, "D23", chart, slope)
    matrix = common_matrix(d01, d23, z)
    vector_x = sp.Matrix((-2 * sign * p, 0, sign, 0, 0, 1, 0, 0))
    vector_y = sp.Matrix(
        (0, -sign, -sp.Rational(sign, 2), 0, sp.Rational(1, 2), 0, 0, 1)
    )
    columns = (0, 1, 2, 3, 4, 6)
    if chart == "finite" and sign == 1:
        minors = (
            (
                (10, 11, 16, 18, 22, 26),
                columns,
                -128 * lam**2 * p**3 * (lam - 1) ** 4,
            ),
            (
                (14, 16, 17, 18, 22, 26),
                columns,
                64 * p**3 * (lam - 1) ** 4 * (lam + 1),
            ),
        )
    elif chart == "finite":
        minors = (((10, 11, 16, 18, 22, 26), columns, -128 * p**3 * (lam - 1) ** 4),)
    elif sign == 1:
        minors = (((10, 11, 16, 18, 22, 26), columns, -128 * p**3),)
    else:
        minors = (((14, 16, 17, 18, 22, 26), columns, 64 * p**3),)
    check_kernel(matrix, (vector_x, vector_y), minors, (sign, "same kappa=0", chart))
    vector = cap_x * vector_x + cap_y * vector_y
    substitution = dict(zip(z, vector, strict=True))
    diagonals = tuple(
        sp.factor(value.subs(substitution)) for value in (d01["B"], d23["A"], d23["B"])
    )
    if chart == "finite" and sign == 1:
        expected_diagonals = (
            2 * p * (2 * cap_x * lam + cap_y),
            4 * p * (2 * cap_x - cap_y) * (lam - 1),
            2 * cap_y * (lam + 1),
        )
    elif chart == "finite":
        expected_diagonals = (
            2 * p * (2 * cap_x + cap_y * lam),
            -4 * p * (2 * cap_x - cap_y) * (lam - 1),
            2 * cap_y * (lam + 1),
        )
    elif sign == 1:
        expected_diagonals = (
            4 * cap_x * p,
            4 * p * (2 * cap_x - cap_y),
            2 * cap_y,
        )
    else:
        expected_diagonals = (
            2 * cap_y * p,
            -4 * p * (2 * cap_x - cap_y),
            2 * cap_y,
        )
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected, (sign, "same kappa=0 diagonal", chart))
    marked = one_marked_map(3, d23["alpha_rows"], d23["beta_rows"]).subs(substitution)
    determinant = sp.factor(marked.extract((0, 1, 4, 7), range(4)).det())
    weight = (lam + 1) ** 3 if chart == "finite" else 1
    expected_det = 32 * cap_y**2 * p**3 * (2 * cap_x - cap_y) * weight
    zero(determinant - expected_det, (sign, "same kappa=0 ternary", chart))
    return {
        "sign": sign,
        "chart": chart,
        "kernel_dimension": 2,
        "kernel_complete": True,
        "diagonals": [str(value) for value in diagonals],
        "ternary_minor": str(determinant),
    }


def opposite_endpoint(sign, chart, kappa_zero):
    p, kappa, r, lam, cap_c = sp.symbols("p kappa r lambda C")
    z = sp.symbols("z0:8")
    active_kappa = 0 if kappa_zero else kappa
    marking = (r, 0, 0, 0) if kappa_zero else (-sign / (2 * p), 0, -sign * kappa, 0)
    alpha, canonical = pure_bases(p, sign * p, active_kappa, -sign)
    beta = shifted_beta(alpha, canonical, marking)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, beta, z, "D01", chart, slope)
    d23 = build_model(alpha, beta, z, "D23", chart, slope)
    matrix = common_matrix(d01, d23, z)
    if kappa_zero:
        vector = sp.Matrix((-sign * p, sign, 0, 0, sign * p * r, 0, 0, 1))
    else:
        vector = sp.Matrix((-sign * p, sign, 0, 0, -sp.Rational(1, 2), 0, kappa, 1))
    columns = (0, 1, 2, 3, 4, 5, 6)
    if chart == "finite" and sign == 1:
        minors = (
            (
                (10, 11, 18, 20, 21, 22, 26),
                columns,
                -512 * p**4 * (lam - 1) ** 4 * (lam + 1),
            ),
        )
    elif chart == "finite":
        minors = (
            (
                (10, 11, 18, 20, 21, 22, 26),
                columns,
                -512 * lam**2 * p**4 * (lam - 1) ** 4 * (lam + 1),
            ),
            (
                (14, 18, 20, 21, 22, 23, 26),
                columns,
                128 * p**4 * (lam - 1) ** 4 * (lam + 1) ** 3,
            ),
        )
    elif sign == 1:
        minors = (((14, 18, 20, 21, 22, 23, 26), columns, 128 * p**4),)
    else:
        minors = (((10, 11, 18, 20, 21, 22, 26), columns, -512 * p**4),)
    check_kernel(matrix, (vector,), minors, (sign, "opposite", chart, kappa_zero))
    substitution = dict(zip(z, cap_c * vector, strict=True))
    diagonals = tuple(
        sp.factor(value.subs(substitution)) for value in (d01["B"], d23["A"], d23["B"])
    )
    weight = lam + 1 if chart == "finite" else 1
    if not kappa_zero:
        expected_diagonals = (
            2 * cap_c * p * weight,
            4 * sign * cap_c * p * ((lam - 1) if chart == "finite" else 1),
            4 * cap_c * kappa * p * weight,
        )
        expected_det = -sign * 64 * cap_c**3 * kappa * p**4 * weight**3
    else:
        extra = 2 * p * r + sign
        expected_diagonals = (
            2 * cap_c * p * weight,
            4 * sign * cap_c * p * ((lam - 1) if chart == "finite" else 1),
            2 * sign * cap_c * weight * extra,
        )
        expected_det = -32 * cap_c**3 * p**3 * weight**3 * extra
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected, (sign, "opposite diagonal", chart, kappa_zero))
    marked = one_marked_map(3, d23["alpha_rows"], d23["beta_rows"]).subs(substitution)
    determinant = sp.factor(marked.extract((0, 1, 3, 7), range(4)).det())
    zero(determinant - expected_det, (sign, "opposite ternary", chart, kappa_zero))
    return {
        "sign": sign,
        "chart": chart,
        "kappa": "0" if kappa_zero else "nonzero function-field",
        "kernel_complete": True,
        "diagonals": [str(value) for value in diagonals],
        "ternary_minor": str(determinant),
    }


def main():
    kappa, ell = sp.symbols("kappa ell")
    zero_alpha, zero_beta = pure_bases(0, 0, kappa, ell)
    assert zero_alpha[0] == (0, 0, 0, 0)
    assert all(
        permanent4(
            tuple(
                zero_beta[index] if word[index] else zero_alpha[index]
                for index in range(4)
            )
        )
        == 0
        for word in WORDS
    )
    projection_jobs = [
        (sign, side, chart, kappa_zero)
        for sign in (1, -1)
        for side in ("same", "opposite")
        for chart in ("finite", "infinity")
        for kappa_zero in (False, True)
    ]
    projections = [endpoint_projection(*job) for job in projection_jobs]
    same_generic = [
        same_endpoint_generic(sign, chart)
        for sign in (1, -1)
        for chart in ("finite", "infinity")
    ]
    same_zero = [
        same_endpoint_kappa_zero(sign, chart)
        for sign in (1, -1)
        for chart in ("finite", "infinity")
    ]
    opposite = [
        opposite_endpoint(sign, chart, kappa_zero)
        for sign in (1, -1)
        for chart in ("finite", "infinity")
        for kappa_zero in (False, True)
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic-zero function fields",
                "component": 21,
                "projection_certificates": projections,
                "ell_equals_epsilon": {
                    "kappa_nonzero": same_generic,
                    "kappa_zero": same_zero,
                    "complete": True,
                },
                "ell_equals_minus_epsilon": {
                    "certificates": opposite,
                    "complete": True,
                },
                "homogeneous_weight_cover": ["finite [lambda:1]", "infinity [1:0]"],
                "ell_endpoint_H22_fibres_empty_for_p_nonzero": True,
                "raw_p_equals_q_equals_zero_chart_pure_coefficients": "all zero",
                "p_equals_q_equals_zero_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
