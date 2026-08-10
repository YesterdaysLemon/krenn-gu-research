#!/usr/bin/env python3
"""No-import audit of component 23's r=0,t=+-1 weighted-H22 fibres."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import functools
import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
COORDINATE_PAIRS = tuple(itertools.combinations(range(4), 2))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
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


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


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


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def component_rows(t_value):
    t_value = sp.Integer(t_value)
    k = 1 / t_value
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    d = (0, 0, 1, -1)
    alpha = (
        a,
        add(a, d, k),
        add(add(a, c, -1), b),
        add(add(add(scale(-1, a), c, -1), b), d, t_value),
    )
    beta = (b, add(b, c), c, c)
    return alpha, beta


def marked_rows(alpha, beta):
    return tuple(add(beta[index], alpha[index], h[index]) for index in range(4))


def project(row, extension, direction, chart, slope=None):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def build_model(alpha, beta, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != index))
                for index in range(4)
            )
        )
    return {
        "mixed": tuple(coefficients[word] for word in MIXED_WORDS),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


@functools.cache
def fibre_models(t_value, chart, slope):
    alpha, beta = component_rows(t_value)
    marked = marked_rows(alpha, beta)
    return (
        build_model(alpha, marked, "D01", chart, slope),
        build_model(alpha, marked, "D23", chart, slope),
    )


def coefficient_vector(expression, substitutions):
    coefficients = tuple(
        sp.expand(sp.diff(expression.subs(substitutions, simultaneous=True), variable))
        for variable in x
    )
    multiplier = functools.reduce(
        sp.lcm,
        (sp.denom(coefficient) for coefficient in coefficients),
        sp.Integer(1),
    )
    assert multiplier != 0 and not multiplier.free_symbols
    cleared = tuple(sp.expand(multiplier * coefficient) for coefficient in coefficients)
    assert all(sp.denom(coefficient) == 1 for coefficient in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]"


def mixed_matrix(t_value):
    models = fibre_models(t_value, "finite", lam)
    return sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )


def pure_special_fibre_certificate():
    profiles = []
    pure_coefficients = []
    for t_value in (1, -1):
        alpha, beta = component_rows(t_value)
        planes = tuple((alpha[index], beta[index]) for index in range(4))
        ranks = []
        for left, right in itertools.combinations(range(4), 2):
            columns = []
            for i in range(2):
                for j in range(2):
                    left_row = planes[left][i]
                    right_row = planes[right][j]
                    columns.append(
                        sp.Matrix(
                            [
                                left_row[a] * right_row[b] + left_row[b] * right_row[a]
                                for a, b in COORDINATE_PAIRS
                            ]
                        )
                    )
            ranks.append(sp.Matrix.hstack(*columns).rank())
        assert tuple(ranks) == (3, 3, 3, 4, 3, 4)
        coefficients = (permanent4(alpha), permanent4(beta))
        assert coefficients == (0, -4)
        profiles.append(tuple(ranks))
        pure_coefficients.append(coefficients)
    return tuple(profiles), tuple(pure_coefficients)


def ordinary_unit_certificate(t_value):
    matrix = mixed_matrix(t_value)
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

    variables = (*h, lam, u)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, determinants))
            + ",u*lam*(lam-1)*(lam+1)-1;",
            "I=std(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    label = f"audit_t_{'plus' if t_value == 1 else 'minus'}_one_ordinary"
    run_singular(label, program, "RESULT:1:1")
    return label, str(actual_extra)


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
    models = fibre_models(t_value, chart, slope)
    generators = ",".join(
        coefficient_vector(equation, substitutions)
        for model in models
        for equation in model["mixed"]
    )
    diagonals = tuple(
        coefficient_vector(equation, substitutions)
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
    matrix = mixed_matrix(t_value).subs(lam, 0)
    dense_minor = sp.factor(
        matrix.extract((0, 1, 3, 4, 7, 8, 9, 14), range(8)).det(method="domain-ge")
    )
    expected_dense = -256 * h[3] if t_value == 1 else 256 * h[3] * (3 - 4 * h[3])
    assert sp.expand(dense_minor - expected_dense) == 0

    prefix = f"audit_t_{'plus' if t_value == 1 else 'minus'}_one"
    lambda_zero = [
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
        lambda_zero.append(
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

    others = (
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
    return str(dense_minor), tuple(lambda_zero), others


def main():
    pair_profiles, pure_coefficients = pure_special_fibre_certificate()
    ordinary = tuple(ordinary_unit_certificate(value) for value in (1, -1))
    endpoints = tuple(endpoint_certificates(value) for value in (1, -1))
    print(
        json.dumps(
            {
                "status": "pass",
                "audit_type": "no_repository_imports",
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
                "claim_label": "AUDITED_SPECIAL_ALL_PAIR_FIBRES_EMPTY",
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
