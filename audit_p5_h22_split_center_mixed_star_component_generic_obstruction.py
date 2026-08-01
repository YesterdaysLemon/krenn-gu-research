#!/usr/bin/env python3
"""Independent rational audit for component twenty-four weighted H22."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def permanent_dp(square):
    size = len(square)
    states = {0: sp.Integer(1)}
    for row in square:
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + coefficient * row[column]
                )
        states = next_states
    return sp.expand(states[(1 << size) - 1])


def add(*vectors):
    return tuple(
        sp.expand(sum(vector[index] for vector in vectors)) for index in range(4)
    )


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def component_rows(k, s, t):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    c = (t - k * s) / (1 - k * s * t)
    alpha = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(cap_a, scale(c, cap_c), scale(k, cap_b), scale(-k, cap_d)),
        cap_d,
    )
    beta = (
        cap_b,
        add(cap_b, scale(s, cap_c)),
        cap_c,
        add(scale(t, cap_a), cap_c, scale(-k * t, cap_b)),
    )
    return alpha, beta


def marked(alpha, beta, h):
    return tuple(add(beta[index], scale(h[index], alpha[index])) for index in range(4))


def project(row, extension, direction, chart, slope):
    if (direction, chart) == ("D01", "finite"):
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if (direction, chart) == ("D01", "infinity"):
        return (row[0], row[2], row[3], extension)
    if (direction, chart) == ("D23", "finite"):
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if (direction, chart) == ("D23", "infinity"):
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction(alpha, beta, z, direction, chart, slope):
    alpha_rows = tuple(
        project(alpha[index], z[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], z[4 + index], direction, chart, slope)
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
                * permanent_dp(
                    tuple(selected[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    mixed = sp.Matrix(
        [[sp.diff(coefficients[word], variable) for variable in z] for word in MIXED]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[WORDS[0]], variable) for variable in z]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[WORDS[-1]], variable) for variable in z]]
    )
    return alpha_rows, beta_rows, mixed, diagonal_alpha, diagonal_beta


def one_marked_zero(alpha_rows, beta_rows):
    output = []
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[index + 1] if word[index] else alpha_rows[index + 1]
            for index in range(3)
        )
        output.append(
            tuple(
                permanent_dp(
                    tuple(
                        tuple(row[column] for column in range(4) if column != omitted)
                        for row in selected
                    )
                )
                for omitted in range(4)
            )
        )
    return sp.Matrix(output)


def quadratic_markings(k, s, t, slope):
    h3 = sp.solve(
        2 * s * (k**2 * s**2 - 1) * sp.Symbol("h3")
        + (k**4 * s**4 * t**2 - k**2 * s**2 * t**2 - k**2 * s**2 + 1) * slope
        - 3 * k**4 * s**4 * t**2
        - 2 * k**3 * s**3 * t**3
        + 4 * k**3 * s**3 * t
        + k**2 * s**2 * t**2
        + k**2 * s**2
        - 2 * k * s * t
        + 1,
        sp.Symbol("h3"),
    )[0]
    h2 = -((k * s * t - 1) * h3 + k * t * (1 - k * s * t)) / (
        k * (t**2 - 1) * (k * s * t + 1)
    )
    h1 = -(
        (1 - k**2 * s**2) * h3 * slope
        + (k**2 * s**2 + 2 * k * s * t + 1) * h3
        + k * (k**2 * s**2 * t - t) * slope
        + k * (-(k**2) * s**2 * t - 2 * k * s - t)
    ) / (2 * k**3 * s * (t**2 - 1))
    return (sp.Integer(0), sp.factor(h1), sp.factor(h2), sp.factor(h3))


def witness(label, k, s, t, direction, chart, slope, h):
    z = sp.symbols("z0:8")
    alpha, beta = component_rows(k, s, t)
    beta = marked(alpha, beta, h)
    alpha_rows, beta_rows, mixed, diagonal_alpha, diagonal_beta = contraction(
        alpha, beta, z, direction, chart, slope
    )
    mixed_rank = mixed.rank()
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - mixed_rank
    determinant = sp.Integer(0)
    a_value = sp.Integer(0)
    b_value = sp.Integer(0)
    for coefficients in itertools.product((1, 2, 3), repeat=len(kernel)):
        vector = sum(
            (coefficient * basis for coefficient, basis in zip(coefficients, kernel, strict=True)),
            sp.zeros(8, 1),
        )
        a_value = sp.factor((diagonal_alpha * vector)[0])
        b_value = sp.factor((diagonal_beta * vector)[0])
        if a_value == 0 or b_value == 0:
            continue
        values = dict(zip(z, vector, strict=True))
        determinant = sp.factor(
            one_marked_zero(alpha_rows, beta_rows)
            .subs(values)
            .extract((0, 1, 3, 7), range(4))
            .det()
        )
        if determinant != 0:
            break
    assert a_value != 0 and b_value != 0 and determinant != 0
    return {
        "branch": label,
        "parameters": [str(k), str(s), str(t)],
        "weight": "infinity" if slope is None else str(slope),
        "mixed_rank": mixed_rank,
        "diagonals_nonzero": True,
        "N0_0137_nonzero": True,
    }


def main():
    started = time.perf_counter()
    k, s, t = map(sp.Integer, (2, 3, 2))
    alpha, beta = component_rows(k, s, t)
    pure = {
        word: permanent_dp(
            tuple(beta[index] if word[index] else alpha[index] for index in range(4))
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4 * (k * s * t - 1)
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    q3b_h2 = -(k**2 * s**2 * t**2 - 1) / (2 * t * (k**2 * s**2 - 1))
    results = [
        witness(
            "D01_finite", k, s, t, "D01", "finite", sp.Integer(3), (0, 5, 0, k * t)
        ),
        witness(
            "D01_infinity_q1",
            k,
            s,
            t,
            "D01",
            "infinity",
            None,
            (0, (t + 1 - 2 * k * s * t) / (k * (t - 1)), 0, k * t),
        ),
        witness(
            "D23_finite_linear",
            k,
            s,
            t,
            "D23",
            "finite",
            sp.Integer(3),
            (0, -1 / k, 0, k * t),
        ),
        witness(
            "D23_infinity_q3a", k, s, t, "D23", "infinity", None, (0, -1 / k, 0, k * t)
        ),
        witness(
            "D23_infinity_q3b",
            k,
            s,
            t,
            "D23",
            "infinity",
            None,
            (0, s * t, q3b_h2, k * t),
        ),
    ]
    kq, sq, tq = map(sp.Integer, (2, 2, 3))
    for root in (sp.Rational(71, 65), sp.Rational(13, 3)):
        results.append(
            witness(
                "D23_finite_quadratic",
                kq,
                sq,
                tq,
                "D23",
                "finite",
                root,
                quadratic_markings(kq, sq, tq, root),
            )
        )
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import exact-rational audit",
                "pure_support": {"1111": str(pure[WORDS[-1]])},
                "branch_witnesses": results,
                "quadratic_branch_both_rational_roots_checked": True,
                "generic_function_field_proof_replaced": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
