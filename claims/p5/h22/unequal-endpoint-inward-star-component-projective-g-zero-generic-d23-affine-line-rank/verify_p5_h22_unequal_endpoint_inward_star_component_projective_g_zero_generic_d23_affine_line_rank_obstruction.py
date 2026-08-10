#!/usr/bin/env python3
"""Verify generic projective-D23 closure on component 25's g=0 sign sheets."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from krenn_gu.p5_marked_basis import one_marked_map, permanent



import itertools
import json
import time

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def boundary_basis(s, k, sign):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    e = sp.Rational(sign, 1) / s
    alpha = (
        add(cap_a, scale(-e, cap_b)),
        add(
            cap_a,
            scale(k, cap_d),
            scale(-e, cap_b),
            scale(-sign, cap_c),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(cap_a, scale(e, cap_b), scale(-k, cap_d)),
        add(cap_b, scale(-s, cap_c)),
    )
    return alpha, beta


def marked(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def project(row, extension, direction, slope):
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    raise ValueError(direction)


def tensor(alpha, beta, extensions, direction, slope):
    alpha_p = tuple(
        project(alpha[index], extensions[index], direction, slope)
        for index in range(4)
    )
    beta_p = tuple(
        project(beta[index], extensions[4 + index], direction, slope)
        for index in range(4)
    )
    values = {
        word: sp.factor(
            permanent(
                tuple(
                    beta_p[index] if word[index] else alpha_p[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    return alpha_p, beta_p, values


def fixed_vertex_equations(values):
    empty = values[WORDS[0]]
    singletons = tuple(
        values[tuple(int(index == mode) for index in range(4))]
        for mode in range(4)
    )
    equations = [empty - 1]
    for word in WORDS:
        weight = sum(word)
        if 2 <= weight <= 3:
            equations.append(
                values[word] * empty ** (weight - 1)
                - sp.prod(singletons[index] for index in range(4) if word[index])
            )
    return tuple(equations), singletons


def normalized_line(s, k, slope, parameter, extensions):
    x = s + 2 * (1 - slope) * parameter
    return {
        extensions[0]: x / (2 * s * (slope - 1)),
        extensions[1]: x
        * (k * s * (slope - 1) + slope + 1)
        / (2 * s * (slope - 1) * (slope + 1)),
        extensions[2]: 1 / (2 * (slope - 1)),
        extensions[3]: x / (2 * (slope + 1)),
        extensions[4]: 0,
        extensions[5]: k * x / (2 * (slope + 1)),
        extensions[6]: parameter / s - k * x / (2 * (slope + 1)),
        extensions[7]: parameter,
    }


def main():
    started = time.perf_counter()
    s, k, slope, parameter = sp.symbols("s k lambda t")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    alpha, beta = boundary_basis(s, k, 1)

    # The two sign sheets are related by simultaneous swaps in both ambient
    # coordinate pairs, s,k -> -s,-k, and homogeneous weight inversion.
    alpha_minus, beta_minus = boundary_basis(s, k, -1)
    alpha_plus_transfer, beta_plus_transfer = boundary_basis(-s, -k, 1)
    row_signs = (1, 1, -1, -1)
    plus_shifts = tuple(row_signs[index] * shifts[index] for index in range(4))
    plus_extensions = tuple(
        row_signs[index] * extensions[index] for index in range(4)
    ) + extensions[4:]
    _, _, minus_transfer = tensor(
        alpha_minus,
        marked(alpha_minus, beta_minus, shifts),
        extensions,
        "D23",
        slope,
    )
    _, _, plus_transfer = tensor(
        alpha_plus_transfer,
        marked(alpha_plus_transfer, beta_plus_transfer, plus_shifts),
        plus_extensions,
        "D23",
        1 / slope,
    )
    for word in WORDS:
        source_scale = sp.prod(
            row_signs[index] for index in range(4) if word[index] == 0
        )
        assert (
            sp.factor(
                sp.cancel(source_scale * minus_transfer[word] - slope * plus_transfer[word])
            )
            == 0
        )

    _, _, canonical = tensor(alpha, beta, extensions, "D23", slope)
    equations, singletons = fixed_vertex_equations(canonical)
    numerators = tuple(sp.together(value).as_numer_denom()[0] for value in equations)
    field = sp.QQ.frac_field(s, k, slope)
    actual = sp.groebner(numerators, *extensions, domain=field, order="grevlex")

    line = normalized_line(s, k, slope, parameter, extensions)
    expected_equations = tuple(
        sp.together(extensions[index] - line[extensions[index]])
        .as_numer_denom()[0]
        .subs(parameter, extensions[7])
        for index in range(7)
    )
    expected = sp.groebner(
        expected_equations, *extensions, domain=field, order="grevlex"
    )
    assert all(actual.reduce(value)[1] == 0 for value in expected_equations)
    assert all(
        expected.reduce(polynomial.as_expr())[1] == 0 for polynomial in actual.polys
    )
    assert len(actual) == len(expected) == 7

    assert all(
        sp.factor(sp.cancel(value.subs(line))) == 0 for value in equations
    )
    marking = tuple(sp.factor(-value.subs(line)) for value in singletons)
    expected_marking = (-1, -1, -1, -(slope + 1) / (slope - 1))
    assert all(
        sp.factor(sp.cancel(left - right)) == 0
        for left, right in zip(marking, expected_marking, strict=True)
    )

    alpha_23, beta_23, _ = tensor(alpha, beta, tuple(line[z] for z in extensions), "D23", slope)
    beta_23_marked = marked(alpha_23, beta_23, marking)
    marked_23 = {
        word: sp.factor(
            permanent(
                tuple(
                    beta_23_marked[index] if word[index] else alpha_23[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert marked_23[WORDS[0]] == 1
    assert all(marked_23[word] == 0 for word in MIXED)
    opposite_diagonal = sp.factor(marked_23[WORDS[-1]])
    expected_diagonal = -(
        (slope + 1) * (s + 4 * (1 - slope) * parameter)
    ) / (s * (slope - 1))
    assert sp.factor(sp.cancel(opposite_diagonal - expected_diagonal)) == 0

    alpha_01, beta_01, _ = tensor(alpha, beta, tuple(line[z] for z in extensions), "D01", slope)
    beta_01_marked = marked(alpha_01, beta_01, marking)
    x = s + 2 * (1 - slope) * parameter
    mode_three = one_marked_map(3, alpha_01, beta_01_marked)
    first_minor = sp.factor(
        mode_three.extract((0, 3, 4, 7), range(4)).det(method="domain-ge")
    )
    expected_first = 8 * k * (slope + 1) ** 2 * x / (
        s**6 * (slope - 1) ** 3
    )
    assert sp.factor(sp.cancel(first_minor - expected_first)) == 0

    residual_parameter = s / (2 * (slope - 1))
    mode_zero = one_marked_map(0, alpha_01, beta_01_marked)
    second_minor = sp.factor(
        mode_zero.extract((0, 4, 5, 6), range(4))
        .det(method="domain-ge")
        .subs(parameter, residual_parameter)
    )
    assert second_minor == k**2

    print(
        json.dumps(
            {
                "status": "pass_with_generic_projective_D23_closure",
                "component": 25,
                "projective_leaf_sheets": ["a=1,g=0,es=1", "a=1,g=0,es=-1"],
                "field": "Q(s,k,lambda)",
                "sign_sheet_transfer": "swap 0<->1 and 2<->3, s,k->-s,-k, lambda->1/lambda",
                "normalized_binary_incidence_ideal": "affine line with parameter t",
                "forced_marking": ["-1", "-1", "-1", "-(lambda+1)/(lambda-1)"],
                "opposite_diagonal": str(expected_diagonal),
                "paired_D01_rank_cover": {
                    "open_factor": "X=s+2*(1-lambda)*t",
                    "X_nonzero_mode_3_minor": str(expected_first),
                    "X_zero_parameter": "t=s/(2*(lambda-1))",
                    "X_zero_mode_0_minor": "k^2",
                },
                "generic_finite_D23_closed": True,
                "special_finite_weights_closed": False,
                "component_parameter_divisors_closed": False,
                "D23_weight_infinity_closed": False,
                "other_projective_charts_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
