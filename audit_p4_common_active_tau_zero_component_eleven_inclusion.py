#!/usr/bin/env python3
"""Independent audit of the common-active component-eleven degeneration."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def add(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    keys = set(left) | set(right)
    return {
        key: sp.expand(left.get(key, 0) + right.get(key, 0))
        for key in keys
        if sp.expand(left.get(key, 0) + right.get(key, 0)) != 0
    }


def multiply(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def linear_form(entries: tuple[sp.Expr, ...]) -> dict[int, sp.Expr]:
    return {1 << index: value for index, value in enumerate(entries) if value != 0}


def top_product(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    value = {0: sp.Integer(1)}
    for row in rows:
        value = multiply(value, linear_form(row))
    return sp.expand(value.get(15, 0))


def wedge(rows: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(rows[0][left] * rows[1][right] - rows[0][right] * rows[1][left])
        for left, right in itertools.combinations(range(4), 2)
    )


def scale_row(
    row: tuple[sp.Expr, ...], diagonal: tuple[sp.Expr, ...]
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(value * weight) for value, weight in zip(row, diagonal, strict=True)
    )


def main() -> None:
    alpha, beta, s, t, epsilon = sp.symbols("alpha beta s t epsilon")
    e = (1, 0, 0, 0)
    h = (0, 1, -1, 0)
    w = (0, 1, 1, 0)
    c = (0, 0, 0, 1)

    def combine(*terms: tuple[sp.Expr, tuple[sp.Expr, ...]]) -> tuple[sp.Expr, ...]:
        result = {1 << index: sp.Integer(0) for index in range(4)}
        for scalar, row in terms:
            result = add(
                result,
                {
                    1 << index: sp.expand(scalar * value)
                    for index, value in enumerate(row)
                },
            )
        return tuple(result.get(1 << index, 0) for index in range(4))

    target = (
        (combine((1, h), (alpha, e)), combine((1, c), (beta, e))),
        (e, combine((t, h), (1, c))),
        (e, combine((s, h), (1, c))),
        (w, e),
    )
    tensor = {}
    for word in itertools.product((0, 1), repeat=4):
        tensor[word] = sp.factor(
            top_product(tuple(target[i][word[i]] for i in range(4)))
        )
    expected_tensor = {
        (0, 1, 1, 1): -2 * (s + t),
        (1, 1, 1, 1): -2 * s * t,
    }
    assert {word for word, value in tensor.items() if value != 0} == set(
        expected_tensor
    )
    for word, expected_value in expected_tensor.items():
        assert sp.expand(tensor[word] - expected_value) == 0

    a = combine((1, e), (1, c))
    a_bar = combine((1, e), (-1, c))
    b = h
    b_bar = w
    assert multiply(linear_form(a), linear_form(a_bar)) == {}
    assert multiply(linear_form(b), linear_form(b_bar)) == {}

    p_value = -1 / (2 * t * alpha * epsilon)
    q_value = p_value - beta / (t * alpha)
    r_value = t / s
    raw = (
        (combine((1, a), (p_value, b)), combine((1, a_bar), (q_value, b))),
        (a, combine((1, a_bar), (1, b))),
        (a, combine((r_value, a_bar), (1, b))),
        (b_bar, a_bar),
    )
    diagonal = (1, -2 * t * epsilon, -2 * t * epsilon, epsilon)
    moving = tuple(tuple(scale_row(row, diagonal) for row in plane) for plane in raw)
    expected = (
        (-beta, beta, alpha, 0, 1 + epsilon * beta, -1 - epsilon * beta),
        (t, -t, 1, 0, -epsilon * t, epsilon * t),
        (s, -s, 1, 0, -epsilon * s, epsilon * s),
        (-1, -1, 0, 0, -epsilon, -epsilon),
    )
    scales = (
        -2 * epsilon / alpha,
        -2 * epsilon,
        -2 * epsilon * t / s,
        -2 * epsilon * t,
    )
    for plane, scale, expected_vector, target_plane in zip(
        moving, scales, expected, target, strict=True
    ):
        normalized = tuple(sp.factor(entry / scale) for entry in wedge(plane))
        assert normalized == expected_vector
        assert tuple(entry.subs(epsilon, 0) for entry in normalized) == wedge(
            target_plane
        )

    # A second exact specialization guards against accidental symbolic naming
    # agreement with the primary verifier.
    specialization = {alpha: 5, beta: -2, s: 7, t: 3}
    specialized_target = tuple(
        tuple(
            tuple(sp.expand(sp.sympify(entry).subs(specialization)) for entry in row)
            for row in plane
        )
        for plane in target
    )
    specialized_tensor = {
        word: top_product(tuple(specialized_target[i][word[i]] for i in range(4)))
        for word in itertools.product((0, 1), repeat=4)
    }
    assert specialized_tensor[(0, 1, 1, 1)] == -20
    assert specialized_tensor[(1, 1, 1, 1)] == -42
    assert sum(value != 0 for value in specialized_tensor.values()) == 2

    print(
        json.dumps(
            {
                "status": "pass",
                "implementation": "subset_dictionary_and_exterior_audit",
                "symbolic_limits": 4,
                "independent_exact_specialization": {
                    str(key): value for key, value in specialization.items()
                },
                "search_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
