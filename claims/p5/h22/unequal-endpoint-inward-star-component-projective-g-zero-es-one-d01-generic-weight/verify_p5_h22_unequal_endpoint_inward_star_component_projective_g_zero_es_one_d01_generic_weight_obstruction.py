#!/usr/bin/env python3
"""Verify the generic finite-D01 obstruction on component 25's g=0, es=1 face."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from verify_p5_h31_marked_basis_open_branch import permanent



import itertools
import json
import time

import sympy as sp
from sympy.polys.domains import QQ


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def boundary_basis(s, k):
    """Adapt the pure basis to g=0 and es=1, after scaling away j."""
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    e = 1 / s
    alpha = (
        add(cap_a, scale(-e, cap_b)),
        add(cap_a, scale(k, cap_d), scale(-e, cap_b), scale(-1, cap_c)),
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


def contract(row, extension, slope=None):
    if slope is None:
        return (row[0], row[2], row[3], extension)
    return (slope * row[0] + row[1], row[2], row[3], extension)


def coefficient_rows(alpha, beta, extensions, slope=None):
    rows = {}
    for word in WORDS:
        value = permanent(
            tuple(
                contract(
                    beta[index] if word[index] else alpha[index],
                    extensions[4 + index] if word[index] else extensions[index],
                    slope,
                )
                for index in range(4)
            )
        )
        rows[word] = tuple(sp.cancel(sp.diff(value, z)) for z in extensions)
    return rows


def module_obstruction(rows, parameters, shifts, *, top):
    field = QQ.frac_field(*parameters)
    ring = field.old_poly_ring(*shifts)
    free = ring.free_module(8)
    module = free.submodule(
        *(free.convert(rows[word]) for word in MIXED), order="lex", TOP=top
    )
    all_alpha = free.convert(rows[WORDS[0]])
    contained = all_alpha in module
    return contained, len(module._groebner())


def pair_product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(pair_product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def main():
    started = time.perf_counter()
    s, k, slope = sp.symbols("s k lambda")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    alpha, beta = boundary_basis(s, k)

    # This is the g=0, a=1, es=1 sheet of the homogeneous component equation.
    e, j, a, g = sp.symbols("e j a g")
    homogeneous = sp.expand(
        (e * j + a * g * k**2) * (a * g + e * j * s**2)
        - (a * j + e * g) ** 2
    )
    assert sp.factor(homogeneous.subs({a: 1, g: 0, e: 1 / s})) == 0

    pure = {
        word: sp.factor(
            permanent(
                tuple(beta[index] if word[index] else alpha[index] for index in range(4))
            )
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4 / s
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    # The face is genuinely all-pair at a rational point, not a lower-pair artefact.
    sample_planes = tuple(
        sp.Matrix.vstack(sp.Matrix(alpha[index]).T, sp.Matrix(beta[index]).T).subs(
            {s: 1, k: 2}
        )
        for index in range(4)
    )
    sample_profile = tuple(
        pair_matrix(sample_planes[left], sample_planes[right]).rank()
        for left, right in itertools.combinations(range(4), 2)
    )
    assert sample_profile == (3, 3, 3, 4, 4, 4)

    active = marked(alpha, beta, shifts)
    finite_rows = coefficient_rows(alpha, active, extensions, slope)
    finite_contained, finite_basis_size = module_obstruction(
        finite_rows, (s, k, slope), shifts, top=True
    )
    assert finite_contained

    infinity_rows = coefficient_rows(alpha, active, extensions)
    infinity_contained, infinity_basis_size = module_obstruction(
        infinity_rows, (s, k), shifts, top=True
    )
    assert infinity_contained

    print(
        json.dumps(
            {
                "status": "pass_with_projective_face_partial_closure",
                "component": 25,
                "projective_leaf_face": "g=0, a=1, es=1",
                "face_field": "Q(s,k)",
                "pure_support": {"1111": "4/s"},
                "sample_pair_profile": sample_profile,
                "finite_D01_weight_field": "Q(s,k,lambda)",
                "finite_D01_all_alpha_in_mixed_module": finite_contained,
                "finite_D01_module_basis_size": finite_basis_size,
                "D01_weight_infinity_all_alpha_in_mixed_module": infinity_contained,
                "D01_weight_infinity_module_basis_size": infinity_basis_size,
                "finite_special_weights_closed": False,
                "finite_D23_closed": False,
                "opposite_es_sign_closed": False,
                "projective_face_weighted_H22_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
