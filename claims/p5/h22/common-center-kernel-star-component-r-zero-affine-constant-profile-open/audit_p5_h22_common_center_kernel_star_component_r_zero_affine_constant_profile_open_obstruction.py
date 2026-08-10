#!/usr/bin/env python3
"""No-import audit of component 23's r=0 constant-profile affine theorem."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
t, lam = sp.symbols("t lam")

ORDINARY_ROWS = (
    (0, 1, 3, 7, 8, 9, 11, 12),
    (0, 1, 3, 4, 7, 8, 9, 11),
    (1, 3, 4, 5, 7, 8, 9, 11),
    (1, 3, 4, 7, 8, 9, 11, 12),
    (1, 3, 4, 7, 8, 9, 11, 13),
    (1, 3, 4, 7, 8, 9, 11, 14),
    (1, 3, 4, 7, 8, 9, 11, 16),
    (1, 3, 4, 7, 8, 9, 11, 17),
)


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def component_rows():
    """Rebuild the normalized component-23 r=0 rows without imports."""
    A = (1, 1, 0, 0)
    B = (0, 0, 1, 1)
    C = (1, -1, 0, 0)
    D = (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, 1 / t),
        add(add(A, C, -1), B),
        add(add(add(scale(-1, A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    marked = tuple(add(beta[index], alpha[index], h[index]) for index in range(4))
    return alpha, beta, marked


def project(row, extension, direction, chart, slope=None):
    if (direction, chart) == ("D01", "finite"):
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if (direction, chart) == ("D23", "finite"):
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if (direction, chart) == ("D01", "infinity"):
        return (row[0], row[2], row[3], extension)
    if (direction, chart) == ("D23", "infinity"):
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def build_model(direction, chart, slope=None):
    alpha, _, marked = component_rows()
    alpha_rows = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(marked[index], x[4 + index], direction, chart, slope)
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


def combined_matrix(slope):
    models = (
        build_model("D01", "finite", slope),
        build_model("D23", "finite", slope),
    )
    return sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(expression).replace("**", "^")


def run_singular(label, program, expected_marker, timeout=300):
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
    assert markers == [expected_marker], (label, completed.stdout, expected_marker)
    return label


def is_t_unit(expression):
    expression = sp.factor(expression)
    assert expression.free_symbols <= {t}, expression
    degree = sp.degree(expression, t)
    assert degree is not None and degree >= 0, expression
    quotient = sp.cancel(expression / t**degree)
    assert not quotient.free_symbols and quotient != 0, expression
    return True


def coefficient_vector(expression, substitutions):
    coefficients = tuple(
        sp.cancel(sp.diff(expression.subs(substitutions, simultaneous=True), var))
        for var in x
    )
    denominator = sp.Integer(1)
    for coefficient in coefficients:
        denominator = sp.lcm(denominator, sp.denom(coefficient))
    denominator = sp.factor(denominator)
    assert is_t_unit(denominator)
    cleared = tuple(
        sp.cancel(denominator * coefficient) for coefficient in coefficients
    )
    assert all(sp.denom(coefficient) == 1 for coefficient in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]", denominator


def pure_pair_certificate():
    alpha, beta, _ = component_rows()
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    coordinate_pairs = tuple(itertools.combinations(range(4), 2))

    def symmetric_product(left, right):
        return sp.Matrix(
            [left[i] * right[j] + left[j] * right[i] for i, j in coordinate_pairs]
        )

    matrices = []
    for left, right in itertools.combinations(range(4), 2):
        matrices.append(
            sp.Matrix.hstack(
                *(
                    symmetric_product(planes[left][i], planes[right][j])
                    for i in range(2)
                    for j in range(2)
                )
            )
        )
    ranks = tuple(matrix.rank() for matrix in matrices)
    assert ranks == (3, 3, 3, 4, 4, 4)

    variable_pair = matrices[4]
    cleared_minors = tuple(
        sp.factor(sp.together(variable_pair.extract(rows, range(4)).det()) * t**4)
        for rows in itertools.combinations(range(6), 4)
    )
    nonzero_minors = tuple(value for value in cleared_minors if value != 0)
    maximal_minor_gcd = sp.factor(sp.gcd_list(nonzero_minors))
    assert maximal_minor_gcd == 8 * t**2 * (t - 1) * (t + 1)
    special_profiles = tuple(
        tuple(matrix.subs(t, value).rank() for matrix in matrices) for value in (1, -1)
    )
    assert special_profiles == (
        (3, 3, 3, 4, 3, 4),
        (3, 3, 3, 4, 3, 4),
    )
    return ranks, maximal_minor_gcd, special_profiles


def ordinary_unit_certificate():
    matrix = combined_matrix(lam)
    numerators = []
    denominators = []
    for rows in ORDINARY_ROWS:
        determinant = sp.cancel(matrix.extract(rows, range(8)).det(method="domain-ge"))
        numerator, denominator = sp.fraction(determinant)
        assert is_t_unit(denominator)
        numerators.append(sp.factor(numerator))
        denominators.append(sp.factor(denominator))

    localizer = t * (t - 1) * (t + 1) * lam * (lam - 1) * (lam + 1)
    variables = (*h, t, lam, sp.Symbol("u"))
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, numerators))
            + ",u*"
            + singular_text(localizer)
            + "-1;",
            "I=std(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    run_singular("ordinary_localized_unit_ideal", program, "RESULT:1:1")
    return tuple(denominators)


def module_certificate(
    label,
    chart,
    slope,
    substitutions,
    quotient_relations,
    expected_indices,
    expected_membership,
):
    models = (
        build_model("D01", chart, slope),
        build_model("D23", chart, slope),
    )
    generators = []
    diagonals = []
    row_scales = []
    for model in models:
        for equation in model["mixed"]:
            vector, scale_factor = coefficient_vector(equation, substitutions)
            generators.append(vector)
            row_scales.append(scale_factor)
        for equation in (model["A"], model["B"]):
            vector, scale_factor = coefficient_vector(equation, substitutions)
            diagonals.append(vector)
            row_scales.append(scale_factor)

    variables = (t, sp.Symbol("u"), *h)
    relations = ["u*t*(t-1)*(t+1)-1", *map(singular_text, quotient_relations)]
    expected = ",".join(f"gen({index})" for index in expected_indices)
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=" + ",".join(relations) + "; Q=std(Q);",
            "qring R=Q;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
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
    assert all(is_t_unit(scale_factor) for scale_factor in row_scales)
    return label


def endpoint_certificates():
    lambda_zero = combined_matrix(0)
    H0 = 2 * h[3] * t**2 + 2 * h[3] * t - 4 * h[3] - t + 2
    dense_minor = sp.factor(
        lambda_zero.extract((0, 1, 3, 4, 7, 8, 9, 14), range(8)).det(method="domain-ge")
    )
    assert sp.cancel(dense_minor + 256 * h[3] * H0 / t) == 0

    labels = (
        module_certificate(
            "lambda_zero_h2_zero",
            "finite",
            sp.Integer(0),
            {h[2]: 0},
            (),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_certificate(
            "lambda_zero_h3_zero",
            "finite",
            sp.Integer(0),
            {h[3]: 0},
            (),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_certificate(
            "lambda_zero_H0_zero",
            "finite",
            sp.Integer(0),
            {},
            (H0,),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_certificate(
            "lambda_one",
            "finite",
            sp.Integer(1),
            {},
            (),
            (1, 2, 3, 4, 6, 7, 8),
            (True, True, True, False),
        ),
        module_certificate(
            "lambda_minus_one",
            "finite",
            sp.Integer(-1),
            {},
            (),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_certificate(
            "projective_weight",
            "infinity",
            None,
            {},
            (),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
    )
    return dense_minor, labels


def main():
    pair_ranks, pair_boundary_gcd, special_pair_profiles = pure_pair_certificate()
    ordinary_denominators = ordinary_unit_certificate()
    lambda_zero_dense_minor, endpoints = endpoint_certificates()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "independent_no_repository_imports": True,
                "component": 23,
                "component_divisor": "r=0",
                "base_ring": "Q[t,1/(t*(t-1)*(t+1))]",
                "pure_pair_profile": pair_ranks,
                "variable_pair_maximal_minor_gcd": str(pair_boundary_gcd),
                "localized_open_excludes_t": ["0", "1", "-1"],
                "t_plus_minus_one_special_all_pair_profiles": special_pair_profiles,
                "ordinary_raw_minor_count": len(ORDINARY_ROWS),
                "ordinary_denominators": tuple(map(str, ordinary_denominators)),
                "ordinary_localized_minor_ideal_is_unit": True,
                "lambda_zero_dense_minor": str(lambda_zero_dense_minor),
                "endpoint_and_projective_modules": endpoints,
                "H0_quotient_used_without_t_plus_2_division": True,
                "claim_label": "AUDITED_AFFINE_CONSTANT_PROFILE_OPEN_EMPTY",
                "weighted_H22_constant_profile_affine_open_closed": True,
                "t_plus_minus_one_special_all_pair_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
