#!/usr/bin/env python3
"""Close component 23's s=0, rt=1 normalized all-pair H22 face."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_partial import (
    singular_command,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

r, k, lam = sp.symbols("r k lam")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


alpha = (
    A,
    add(A, scale(k, D)),
    add(B, scale(r, D)),
    add(B, scale(1 / r, D)),
)
beta = (B, B, C, C)
marked = tuple(add(beta[index], scale(h[index], alpha[index])) for index in range(4))


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def symmetric_product(left, right):
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def pure_and_pair_certificate():
    pure = {
        word: sp.factor(
            permanent4(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == -4
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    matrices = []
    for left, right in PAIRS:
        matrices.append(
            sp.Matrix.hstack(
                *(
                    symmetric_product(
                        alpha[left] if i == 0 else beta[left],
                        alpha[right] if j == 0 else beta[right],
                    )
                    for i in range(2)
                    for j in range(2)
                )
            )
        )
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 4, 4, 3)

    for matrix in matrices[:5]:
        three_minors = {
            sp.factor(matrix.extract(rows, columns).det())
            for rows in itertools.combinations(range(6), 3)
            for columns in itertools.combinations(range(4), 3)
        }
        assert 4 in three_minors or -4 in three_minors

    pair23_three = {
        sp.factor(sp.cancel(matrices[5].extract(rows, columns).det()))
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
    }
    pair23_three.discard(sp.Integer(0))
    assert pair23_three == {
        sp.factor(4 * (r - 1) * (r + 1) / r),
        sp.factor(-4 * (r - 1) * (r + 1) / r),
    }
    assert all(
        sp.cancel(matrices[5].extract(rows, range(4)).det()) == 0
        for rows in itertools.combinations(range(6), 4)
    )

    expected_maximal = (
        {sp.factor(-8 * k * (r + 1)), sp.factor(8 * k * (r - 1))},
        {
            sp.factor(-8 * k * (r + 1) / r),
            sp.factor(-8 * k * (r - 1) / r),
        },
    )
    for matrix, expected in zip(matrices[3:5], expected_maximal, strict=True):
        maximal = {
            sp.factor(sp.cancel(matrix.extract(rows, range(4)).det()))
            for rows in itertools.combinations(range(6), 4)
        }
        maximal.discard(sp.Integer(0))
        assert maximal == expected

    assert tuple(matrix.subs(k, 0).rank() for matrix in matrices) == (3,) * 6
    assert tuple(matrix.subs(r, 1).rank() for matrix in matrices) == (3, 3, 3, 4, 4, 2)
    assert tuple(matrix.subs(r, -1).rank() for matrix in matrices) == (3, 3, 3, 4, 4, 2)
    return pure[(1, 1, 1, 1)]


finite_models = (
    build_model(alpha, marked, x, "D01", "finite", lam),
    build_model(alpha, marked, x, "D23", "finite", lam),
)
finite_mixed = sp.Matrix(
    [
        [sp.diff(equation, variable) for variable in x]
        for model in finite_models
        for equation in model["mixed"]
    ]
)


def determinant_pair(label, substitutions, base_rows, expected_14, expected_15):
    matrix = finite_mixed.subs(substitutions, simultaneous=True)
    observed = tuple(
        sp.factor(
            sp.cancel(
                matrix.extract((*base_rows, final), range(8)).det(method="domain-ge")
            )
        )
        for final in (14, 15)
    )
    assert all(
        sp.cancel(left - right) == 0
        for left, right in zip(observed, (expected_14, expected_15), strict=True)
    )
    return label


def ordinary_minor_certificate():
    q_minus = lam * (r + 1) - (r - 1)
    q_plus = lam * (r + 1) + (r - 1)
    assert sp.expand(q_plus - q_minus - 2 * (r - 1)) == 0
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2

    labels = (
        determinant_pair(
            "h2_h3_pair",
            {},
            (0, 1, 2, 3, 8, 9, 12),
            common * h[2] * h[3] * k**4 * q_minus / r**2,
            common * h[2] * h[3] * k**4 * q_plus / r**3,
        ),
        determinant_pair(
            "h2_r_minus_kh1_pair",
            {},
            (0, 1, 3, 5, 8, 9, 12),
            common * h[2] * k**3 * (r - k * h[1]) * q_minus / r**2,
            common * h[2] * k**3 * (r - k * h[1]) * q_plus / r**3,
        ),
        determinant_pair(
            "h0_minus_h1_pair_on_h2_zero",
            {h[2]: 0},
            (0, 1, 3, 7, 8, 9, 12),
            common * k**4 * (h[0] - h[1]) * q_minus / r**2,
            common * k**4 * (h[0] - h[1]) * q_plus / r**3,
        ),
        determinant_pair(
            "h1_pair_on_h2_zero_h0_equal_h1",
            {h[2]: 0, h[0]: h[1]},
            (0, 1, 3, 8, 9, 11, 12),
            -common * h[1] ** 2 * k**4 * q_minus / r**2,
            -common * h[1] ** 2 * k**4 * q_plus / r**3,
        ),
        determinant_pair(
            "r_minus_kh1_h3_zero_pair",
            {h[3]: 0, h[1]: r / k},
            (0, 1, 3, 8, 9, 11, 12),
            -common * k**2 * q_minus,
            -common * k**2 * q_plus / r,
        ),
        determinant_pair(
            "deep_marking_pair",
            {h[0]: 0, h[1]: 0, h[2]: 0},
            (0, 1, 3, 8, 9, 12, 13),
            512
            * k**3
            * (lam - 1) ** 5
            * (lam + 1) ** 2
            * (r - 1)
            * (r + 1)
            * q_minus
            / r,
            512
            * k**3
            * (lam - 1) ** 5
            * (lam + 1) ** 2
            * (r - 1)
            * (r + 1)
            * q_plus
            / r**2,
        ),
    )
    return labels


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def is_r_unit(expression):
    expression = sp.factor(expression)
    assert expression.free_symbols <= {r}, expression
    polynomial = sp.Poly(expression, r)
    assert len(polynomial.terms()) == 1 and polynomial.LC() != 0, expression
    return True


def coefficient_vector(expression, substitutions):
    entries = tuple(
        sp.cancel(sp.diff(expression.subs(substitutions, simultaneous=True), variable))
        for variable in x
    )
    denominator = sp.factor(sp.lcm([sp.denom(entry) for entry in entries]))
    assert is_r_unit(denominator)
    cleared = tuple(sp.cancel(denominator * entry) for entry in entries)
    assert all(sp.denom(entry) == 1 for entry in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]"


def run_module_certificate(
    label, chart, slope, substitutions, variables, localizer, expected, expected_size
):
    models = (
        build_model(alpha, marked, x, "D01", chart, slope),
        build_model(alpha, marked, x, "D23", chart, slope),
    )
    generators = [
        coefficient_vector(equation, substitutions)
        for model in models
        for equation in model["mixed"]
    ]
    diagonals = [
        coefficient_vector(model[key], substitutions)
        for model in models
        for key in ("A", "B")
    ]
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
                '"RESULT:'
                + label
                + ':"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M));'
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
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    marker = (
        "RESULT:"
        + label
        + ":"
        + ":".join("1" if value else "0" for value in expected)
        + f":{expected_size}"
    )
    assert markers == [marker], (label, completed.stdout, marker)
    return label


def special_module_certificates():
    u = sp.Symbol("u")
    all_pair = r * (r - 1) * (r + 1)
    return (
        run_module_certificate(
            "k_zero_ordinary",
            "finite",
            lam,
            {k: 0},
            (r, *h, lam, u),
            all_pair * (lam - 1) * (lam + 1),
            (True, True, True, True),
            7,
        ),
        run_module_certificate(
            "lambda_one",
            "finite",
            sp.Integer(1),
            {},
            (r, k, *h, u),
            all_pair,
            (False, True, False, False),
            15,
        ),
        run_module_certificate(
            "lambda_minus_one",
            "finite",
            sp.Integer(-1),
            {},
            (r, k, *h, u),
            all_pair,
            (True, False, False, True),
            30,
        ),
        run_module_certificate(
            "projective_weight",
            "infinity",
            None,
            {},
            (r, k, *h, u),
            all_pair,
            (True, True, True, True),
            8,
        ),
    )


def main():
    pure_beta = pure_and_pair_certificate()
    ordinary = ordinary_minor_certificate()
    special = special_module_certificates()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "face": "s=0, rt=1, t=1/r",
                "all_pair_base": "Q[r,k,1/(r*(r-1)*(r+1))]",
                "pure_support": {"1111": str(pure_beta)},
                "generic_pair_profile": [3, 3, 3, 4, 4, 3],
                "k_zero_pair_profile": [3, 3, 3, 3, 3, 3],
                "excluded_pair_drop": "r=+-1 gives r23=2; r=0 is outside t=1/r",
                "ordinary_k_nonzero_minor_certificates": ordinary,
                "special_module_certificates": special,
                "normalized_affine_all_pair_weighted_H22_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
