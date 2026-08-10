#!/usr/bin/env python3
"""No-import audit of component 25's g=0, es=1 generic-D01 obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


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


def polynomially_rescaled_basis(s, k):
    """An independent denominator-free source basis for the same face."""
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    alpha = (
        add(scale(s, cap_a), scale(-1, cap_b)),
        add(
            scale(s, cap_a),
            scale(s * k, cap_d),
            scale(-1, cap_b),
            scale(-s, cap_c),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(scale(s, cap_a), cap_b, scale(-s * k, cap_d)),
        add(cap_b, scale(-s, cap_c)),
    )
    return alpha, beta


def marked(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def contracted_rows(alpha, beta, extensions, slope=None):
    def project(row, extension):
        if slope is None:
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


def independent_module_check(rows, parameters, shifts):
    field = QQ.frac_field(*parameters)
    ring = field.old_poly_ring(*shifts)
    free = ring.free_module(8)
    # Reverse the generators and use position-over-term, unlike the primary.
    module = free.submodule(
        *(free.convert(rows[word]) for word in reversed(MIXED)),
        order="lex",
        TOP=False,
    )
    target = free.convert(rows[WORDS[0]])
    return target in module, len(module._groebner())


def main():
    started = time.perf_counter()
    s, k, slope = sp.symbols("s k lambda")
    shifts = sp.symbols("u0:4")
    extensions = sp.symbols("y0:8")
    alpha, beta = polynomially_rescaled_basis(s, k)

    pure = {
        word: sp.factor(
            permanent_dp(
                tuple(beta[index] if word[index] else alpha[index] for index in range(4))
            )
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    active = marked(alpha, beta, shifts)
    finite = contracted_rows(alpha, active, extensions, slope)
    finite_contained, finite_size = independent_module_check(
        finite, (s, k, slope), shifts
    )
    assert finite_contained

    infinity = contracted_rows(alpha, active, extensions)
    infinity_contained, infinity_size = independent_module_check(
        infinity, (s, k), shifts
    )
    assert infinity_contained

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "no-import subset-DP, rescaled-basis, POT-module audit",
                "component": 25,
                "projective_leaf_face": "g=0, a=1, es=1",
                "pure_support_in_rescaled_basis": {"1111": "4"},
                "finite_D01_all_alpha_in_mixed_module": finite_contained,
                "finite_D01_module_basis_size": finite_size,
                "D01_weight_infinity_all_alpha_in_mixed_module": infinity_contained,
                "D01_weight_infinity_module_basis_size": infinity_size,
                "finite_special_weights_closed": False,
                "finite_D23_closed": False,
                "opposite_es_sign_closed": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
