#!/usr/bin/env python3
"""No-import audit of generic projective-D23 closure on component 25."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = WORDS[1:-1]


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + coefficient * row[column]
                )
        states = next_states
    return sp.factor(states[15])


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def plus_basis(s, k):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    return (
        (
            add(cap_a, scale(-1 / s, cap_b)),
            add(cap_a, scale(k, cap_d), scale(-1 / s, cap_b), scale(-1, cap_c)),
            cap_c,
            cap_d,
        ),
        (
            cap_a,
            add(cap_a, scale(k, cap_d)),
            add(cap_a, scale(1 / s, cap_b), scale(-k, cap_d)),
            add(cap_b, scale(-s, cap_c)),
        ),
    )


def project(row, extension, direction, slope):
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    return (slope * row[0] + row[1], row[2], row[3], extension)


def projected(alpha, beta, extension, direction, slope):
    return (
        tuple(project(alpha[i], extension[i], direction, slope) for i in range(4)),
        tuple(project(beta[i], extension[4 + i], direction, slope) for i in range(4)),
    )


def coordinates(alpha, beta):
    return {
        word: permanent_dp(
            tuple(beta[index] if word[index] else alpha[index] for index in range(4))
        )
        for word in WORDS
    }


def one_marked(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent_dp(
                    tuple(basis if other == mode else selected[other] for other in range(4))
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def main():
    started = time.perf_counter()
    s, k, slope, parameter = sp.symbols("s k lambda u")
    z = sp.symbols("y0:8")
    alpha, beta = plus_basis(s, k)
    alpha_23, beta_23 = projected(alpha, beta, z, "D23", slope)
    canonical = coordinates(alpha_23, beta_23)
    empty = canonical[WORDS[0]]
    singletons = tuple(
        canonical[tuple(int(index == mode) for index in range(4))]
        for mode in range(4)
    )
    equations = [empty - 1]
    for word in WORDS:
        weight = sum(word)
        if 2 <= weight <= 3:
            equations.append(
                canonical[word] * empty ** (weight - 1)
                - sp.prod(singletons[index] for index in range(4) if word[index])
            )
    numerators = tuple(sp.together(value).as_numer_denom()[0] for value in equations)

    x = s + 2 * (1 - slope) * parameter
    line = {
        z[0]: x / (2 * s * (slope - 1)),
        z[1]: x
        * (k * s * (slope - 1) + slope + 1)
        / (2 * s * (slope - 1) * (slope + 1)),
        z[2]: 1 / (2 * (slope - 1)),
        z[3]: x / (2 * (slope + 1)),
        z[4]: 0,
        z[5]: k * x / (2 * (slope + 1)),
        z[6]: parameter / s - k * x / (2 * (slope + 1)),
        z[7]: parameter,
    }
    assert all(sp.factor(sp.cancel(value.subs(line))) == 0 for value in equations)

    field = sp.QQ.frac_field(s, k, slope)
    reverse_variables = tuple(reversed(z))
    actual = sp.groebner(
        numerators, *reverse_variables, domain=field, order="grevlex"
    )
    expected_numerators = tuple(
        sp.together(z[index] - line[z[index]])
        .as_numer_denom()[0]
        .subs(parameter, z[7])
        for index in range(7)
    )
    expected = sp.groebner(
        expected_numerators, *reverse_variables, domain=field, order="grevlex"
    )
    assert all(actual.reduce(value)[1] == 0 for value in expected_numerators)
    assert all(
        expected.reduce(polynomial.as_expr())[1] == 0 for polynomial in actual.polys
    )

    extension = tuple(line[value] for value in z)
    alpha_23, beta_23 = projected(alpha, beta, extension, "D23", slope)
    canonical_line = coordinates(alpha_23, beta_23)
    marking = tuple(
        -canonical_line[tuple(int(index == mode) for index in range(4))]
        for mode in range(4)
    )
    expected_marking = (
        -1,
        -1,
        -1,
        -(slope + 1) / (slope - 1),
    )
    assert all(
        sp.factor(sp.cancel(left - right)) == 0
        for left, right in zip(marking, expected_marking, strict=True)
    )
    beta_23_marked = tuple(
        add(beta_23[index], scale(marking[index], alpha_23[index]))
        for index in range(4)
    )
    marked_23 = coordinates(alpha_23, beta_23_marked)
    assert marked_23[WORDS[0]] == 1
    assert all(marked_23[word] == 0 for word in MIXED)

    alpha_01, beta_01 = projected(alpha, beta, extension, "D01", slope)
    beta_01_marked = tuple(
        add(beta_01[index], scale(marking[index], alpha_01[index]))
        for index in range(4)
    )
    mode_two = one_marked(2, alpha_01, beta_01_marked)
    first_minor = sp.factor(
        mode_two.extract((2, 3, 6, 7), range(4)).det(method="domain-ge")
    )
    expected_first = -(slope + 1) * x**2 / (s**4 * (slope - 1))
    assert sp.factor(sp.cancel(first_minor - expected_first)) == 0

    residual = {parameter: s / (2 * (slope - 1))}
    mode_zero = one_marked(0, alpha_01, beta_01_marked)
    second_minor = sp.factor(
        mode_zero.extract((0, 4, 5, 6), range(4))
        .det(method="domain-ge")
        .subs(residual)
    )
    assert second_minor == k**2

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "no-import subset-DP, reverse-grevlex, alternate-minor audit",
                "component": 25,
                "sheet": "a=1,g=0,es=1; opposite sign by certified symmetry",
                "normalized_incidence_ideal_equals_affine_line": True,
                "affine_line_parameter": "u=y7",
                "forced_marking": ["-1", "-1", "-1", "-(lambda+1)/(lambda-1)"],
                "paired_rank_cover": {
                    "X_nonzero_mode_2_minor": str(expected_first),
                    "X_zero_mode_0_minor": "k^2",
                },
                "generic_finite_D23_closed": True,
                "special_finite_weights_closed": False,
                "component_parameter_divisors_closed": False,
                "weight_infinity_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
