#!/usr/bin/env python3
"""Verify generic and endpoint D01 closure on component 25's g=0, es=-1 face."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp
from sympy.polys.domains import QQ

from verify_p5_h31_marked_basis_open_branch import permanent

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))


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


def contract(row, extension, slope):
    if slope == "infinity":
        return (row[0], row[2], row[3], extension)
    return (slope * row[0] + row[1], row[2], row[3], extension)


def tensor(alpha, beta, extensions, slope):
    return {
        word: permanent(
            tuple(
                contract(
                    beta[index] if word[index] else alpha[index],
                    extensions[4 + index] if word[index] else extensions[index],
                    slope,
                )
                for index in range(4)
            )
        )
        for word in WORDS
    }


def coefficient_rows(values, extensions):
    return {
        word: tuple(sp.cancel(sp.diff(values[word], z)) for z in extensions)
        for word in WORDS
    }


def membership(rows, parameters, shifts, diagonal):
    field = QQ.frac_field(*parameters)
    ring = field.old_poly_ring(*shifts)
    free = ring.free_module(8)
    module = free.submodule(
        *(free.convert(rows[word]) for word in MIXED), order="lex", TOP=True
    )
    contained = free.convert(rows[diagonal]) in module
    return contained, len(module._groebner())


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def main():
    started = time.perf_counter()
    s, k, slope = sp.symbols("s k lambda")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    alpha_minus, beta_minus = boundary_basis(s, k, -1)

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    beta_minus[index] if word[index] else alpha_minus[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == -4 / s
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    sample_planes = tuple(
        sp.Matrix.vstack(
            sp.Matrix(alpha_minus[index]).T, sp.Matrix(beta_minus[index]).T
        ).subs({s: 1, k: 2})
        for index in range(4)
    )
    sample_profile = tuple(
        pair_matrix(sample_planes[left], sample_planes[right]).rank()
        for left, right in itertools.combinations(range(4), 2)
    )
    assert sample_profile == (3, 3, 3, 4, 4, 4)

    # Legal transfer from es=1: swap X0,X1 (so C -> -C), send s -> -s,
    # rescale the mode-two alpha row, and invert the D01 weight.
    alpha_plus, beta_plus = boundary_basis(-s, k, 1)
    row_signs = (1, 1, -1, 1)
    plus_shifts = tuple(row_signs[index] * shifts[index] for index in range(4))
    plus_extensions = tuple(
        row_signs[index] * extensions[index] for index in range(4)
    ) + extensions[4:]
    minus_values = tensor(
        alpha_minus, marked(alpha_minus, beta_minus, shifts), extensions, slope
    )
    plus_values = tensor(
        alpha_plus,
        marked(alpha_plus, beta_plus, plus_shifts),
        plus_extensions,
        1 / slope,
    )
    for word in WORDS:
        source_scale = sp.prod(
            row_signs[index] for index in range(4) if word[index] == 0
        )
        assert (
            sp.factor(
                sp.cancel(source_scale * minus_values[word] - slope * plus_values[word])
            )
            == 0
        )

    active_minus = marked(alpha_minus, beta_minus, shifts)
    endpoint_results = {}
    for label, weight, diagonal in (
        ("lambda=0", sp.Integer(0), WORDS[0]),
        ("lambda=1", sp.Integer(1), WORDS[0]),
        ("lambda=-1", sp.Integer(-1), WORDS[-1]),
        ("lambda=infinity", "infinity", WORDS[0]),
    ):
        rows = coefficient_rows(
            tensor(alpha_minus, active_minus, extensions, weight), extensions
        )
        contained, basis_size = membership(rows, (s, k), shifts, diagonal)
        assert contained
        endpoint_results[label] = {
            "forced_diagonal": "all-alpha" if diagonal == WORDS[0] else "all-beta",
            "in_mixed_module": contained,
            "module_basis_size": basis_size,
        }

    print(
        json.dumps(
            {
                "status": "pass_with_projective_sheet_D01_weight_closure",
                "component": 25,
                "projective_leaf_sheet": "a=1, g=0, es=-1",
                "face_field": "Q(s,k)",
                "pure_support": {"1111": "-4/s"},
                "sample_pair_profile": sample_profile,
                "finite_generic_D01_transfers_from_es_one": True,
                "transfer": "X0<->X1, s->-s, lambda->1/lambda, alpha2->-alpha2",
                "endpoint_results": endpoint_results,
                "all_finite_special_weights_closed": False,
                "finite_D23_closed": False,
                "projective_sheet_weighted_H22_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
