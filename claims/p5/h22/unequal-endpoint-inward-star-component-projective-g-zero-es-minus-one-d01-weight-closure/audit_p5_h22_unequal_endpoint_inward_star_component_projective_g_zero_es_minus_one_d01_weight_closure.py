#!/usr/bin/env python3
"""No-import audit of D01 closure on component 25's g=0, es=-1 sheet."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp
from sympy.polys.domains import QQ

WORDS = tuple(itertools.product((0, 1), repeat=4))
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
    return states[15]


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def rescaled_minus_basis(s, k):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    alpha = (
        add(scale(s, cap_a), cap_b),
        add(scale(s, cap_a), scale(s * k, cap_d), cap_b, scale(s, cap_c)),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(scale(s, cap_a), scale(-1, cap_b), scale(-s * k, cap_d)),
        add(cap_b, scale(-s, cap_c)),
    )
    return alpha, beta


def marked(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def rows(alpha, beta, extensions, slope):
    def project(row, extension):
        if slope == "infinity":
            return (row[0], row[2], row[3], extension)
        return (slope * row[0] + row[1], row[2], row[3], extension)

    result = {}
    for word in WORDS:
        value = permanent_dp(
            tuple(
                project(
                    beta[index] if word[index] else alpha[index],
                    extensions[4 + index] if word[index] else extensions[index],
                )
                for index in range(4)
            )
        )
        result[word] = tuple(sp.diff(value, z) for z in extensions)
    return result


def module_check(values, parameters, shifts, diagonal):
    field = QQ.frac_field(*parameters)
    ring = field.old_poly_ring(*shifts)
    free = ring.free_module(8)
    module = free.submodule(
        *(free.convert(values[word]) for word in reversed(MIXED)),
        order="lex",
        TOP=False,
    )
    contained = free.convert(values[diagonal]) in module
    return contained, len(module._groebner())


def main():
    started = time.perf_counter()
    s, k, slope = sp.symbols("s k lambda")
    shifts = sp.symbols("u0:4")
    extensions = sp.symbols("y0:8")
    alpha, beta = rescaled_minus_basis(s, k)

    pure = {
        word: sp.factor(
            permanent_dp(
                tuple(beta[index] if word[index] else alpha[index] for index in range(4))
            )
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == -4
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    active = marked(alpha, beta, shifts)
    generic_rows = rows(alpha, active, extensions, slope)
    generic_contained, generic_size = module_check(
        generic_rows, (s, k, slope), shifts, WORDS[0]
    )
    assert generic_contained

    endpoints = {}
    for label, weight, diagonal in (
        ("lambda=0", sp.Integer(0), WORDS[0]),
        ("lambda=1", sp.Integer(1), WORDS[0]),
        ("lambda=-1", sp.Integer(-1), WORDS[-1]),
        ("lambda=infinity", "infinity", WORDS[0]),
    ):
        contained, size = module_check(
            rows(alpha, active, extensions, weight), (s, k), shifts, diagonal
        )
        assert contained
        endpoints[label] = {
            "forced_diagonal": "all-alpha" if diagonal == WORDS[0] else "all-beta",
            "module_basis_size": size,
        }

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "no-import subset-DP, rescaled-basis, POT-module audit",
                "component": 25,
                "projective_leaf_sheet": "a=1, g=0, es=-1",
                "pure_support_in_rescaled_basis": {"1111": "-4"},
                "fresh_generic_finite_D01_module_check": generic_contained,
                "generic_module_basis_size": generic_size,
                "endpoint_results": endpoints,
                "all_finite_special_weights_closed": False,
                "finite_D23_closed": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
