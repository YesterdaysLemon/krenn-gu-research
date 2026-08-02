#!/usr/bin/env python3
"""Verify weighted-H22 emptiness on component 23's s=0,k=inf,rt=1 locus."""

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
    PAIRS,
    A,
    B,
    C,
    D,
    add,
    permanent,
    scale,
    singular_command,
)

r, lam = sp.symbols("r lam")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")

alpha = (A, D, add(B, scale(r, D)), add(B, scale(1 / r, D)))
beta = (B, B, C, C)
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
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 3, 3, 3)
    edge23 = matrices[-1]
    three_minors = [
        sp.factor(edge23.extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
    ]
    gcd = sp.factor(sp.gcd_list([value for value in three_minors if value]))
    assert sp.expand(gcd - 4 * (r - 1) * (r + 1) / r) == 0
    return coefficients[WORDS[-1]], gcd


def mixed_matrix(chart, slope=None, substitutions=None):
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
    _models, matrix = mixed_matrix("finite", lam)
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 4 * (r - 1) ** 2 * (r + 1) ** 2

    def determinant(rows, substitutions, expected):
        observed = sp.factor(
            matrix.subs(substitutions, simultaneous=True)
            .extract(rows, range(8))
            .det(method="domain-ge")
        )
        assert sp.expand(observed - expected) == 0, (rows, observed, expected)
        return rows

    labels = (
        determinant(
            (0, 1, 2, 3, 8, 9, 12, 16),
            {},
            common * h[2] * h[3] / r**2,
        ),
        determinant(
            (0, 1, 3, 5, 8, 9, 12, 16),
            {},
            common * h[2] * (r - h[1]) / r**2,
        ),
        determinant(
            (0, 1, 3, 4, 8, 9, 12, 16),
            {},
            -common * h[3] * (r * h[1] - 1) / r**3,
        ),
        determinant(
            (0, 1, 3, 7, 8, 9, 12, 16),
            {},
            common * h[0] / r**2,
        ),
        determinant(
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[3]: 0, h[1]: r},
            -256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2 / r,
        ),
        determinant(
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[1]: 1 / r},
            256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2 / r**3,
        ),
        determinant(
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[3]: 0},
            -256
            * (lam - 1) ** 5
            * (lam + 1) ** 3
            * (r - 1)
            * (r + 1)
            * (h[1] * (r**2 + 1) - 2 * r)
            / r**2,
        ),
    )
    return labels


def residual_certificate():
    residual_h = {
        h[0]: 0,
        h[1]: 2 * r / (r**2 + 1),
        h[2]: 0,
        h[3]: 0,
    }
    models, matrix = mixed_matrix("finite", lam, residual_h)
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in matrix * kernel)
    selected_rows = (0, 1, 3, 8, 9, 12, 16)
    selected_columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(
        matrix.extract(selected_rows, selected_columns).det(method="domain-ge")
    )
    expected_minor = (
        128
        * (lam - 1) ** 4
        * (lam + 1) ** 3
        * (r - 1) ** 2
        * (r + 1) ** 2
        / (r * (r**2 + 1))
    )
    assert sp.expand(rank_minor - expected_minor) == 0
    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind].subs(residual_h, simultaneous=True), variable)
                * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    expected_diagonals = (
        2 * (lam + 1) * (r**2 + 1) / r,
        0,
        0,
        -2 * (lam + 1),
    )
    assert all(
        sp.cancel(observed - expected) == 0
        for observed, expected in zip(diagonals, expected_diagonals, strict=True)
    )
    return tuple(kernel), str(rank_minor), tuple(map(str, diagonals))


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def coefficient_vector(expression, substitutions):
    entries = tuple(
        sp.cancel(sp.diff(expression.subs(substitutions, simultaneous=True), variable))
        for variable in x
    )
    denominator = sp.factor(sp.lcm([sp.denom(entry) for entry in entries]))
    polynomial = sp.Poly(denominator, r)
    assert len(polynomial.terms()) == 1 and polynomial.LC() != 0
    cleared = tuple(sp.cancel(denominator * entry) for entry in entries)
    assert all(sp.denom(entry) == 1 for entry in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]"


def module_certificate(label, chart, slope, expected, expected_size):
    models = tuple(
        build_model(alpha, marked, x, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = [
        coefficient_vector(equation, {})
        for model in models
        for equation in model["mixed"]
    ]
    diagonals = [
        coefficient_vector(model[kind], {}) for model in models for kind in ("A", "B")
    ]
    u = sp.symbols("u")
    variables = (r, *h, u)
    localizer = r * (r - 1) * (r + 1)
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(" + singular_text(localizer) + ")-1; Q=std(Q);",
            "qring R=Q;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            *(f"int z{index}=reduce(d{index},M)==0;" for index in range(4)),
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
    return label, expected


def special_weight_certificates():
    return (
        module_certificate(
            "lambda_one", "finite", sp.Integer(1), (False, True, True, False), 16
        ),
        module_certificate(
            "lambda_minus_one",
            "finite",
            sp.Integer(-1),
            (True, False, True, True),
            5,
        ),
        module_certificate(
            "projective_weight", "infinity", None, (False, True, True, False), 13
        ),
    )


def main():
    pure_beta, edge23_gcd = pure_and_pair_certificate()
    ordinary_minors = ordinary_minor_certificate()
    residual_kernel, residual_rank_minor, residual_diagonals = residual_certificate()
    special_weights = special_weight_certificates()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity,rt=1,t=1/r",
                "base": "Q[r,1/(r*(r-1)*(r+1))]",
                "pure_support": {"1111": str(pure_beta)},
                "pair_profile": (3, 3, 3, 3, 3, 3),
                "edge23_three_minor_gcd": str(edge23_gcd),
                "ordinary_weight_open": "(lambda-1)*(lambda+1) != 0",
                "ordinary_rank_eight_minors": ordinary_minors,
                "ordinary_residual_marking": "h0=h2=h3=0; h1*(r^2+1)=2*r",
                "ordinary_residual_kernel": tuple(map(str, residual_kernel)),
                "ordinary_residual_rank_minor": residual_rank_minor,
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "ordinary_residual_diagonals": residual_diagonals,
                "ordinary_residual_genuine": False,
                "special_weight_modules": tuple(label for label, _ in special_weights),
                "normalized_rt_one_weighted_H22": "empty",
                "parameter_endpoints_covered": False,
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
