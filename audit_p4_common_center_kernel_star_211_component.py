#!/usr/bin/env python3
"""Independent exact audit of the common-center-kernel component 23."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_common_center_kernel_star_211_component.py"
BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "component twenty-three",
        "unordered outward flag pairs",
        "No finite-field sample is used as proof",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    assert '"all_pure_components_classified": False' in primary
    assert '"global_conjecture_resolved": False' in primary

    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    s, r, t = sp.Integer(1), sp.Integer(2), sp.Integer(3)
    k = sp.Rational(1 - r * t, s * (t - r))
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((s * (A - C) + B + r * D).T, C.T),
        sp.Matrix.vstack((-s * (A + C) + B + t * D).T, C.T),
    )

    permutation = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)
    transformed = tuple(
        sp.Matrix(
            [
                [scales[column] * plane[row, permutation[column]] for column in range(4)]
                for row in range(2)
            ]
        )
        for plane in planes
    )
    coefficients = {
        bits: permanent([transformed[i].row(bits[i]) for i in range(4)])
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert support == {(1, 1, 1, 1): -840}

    profile = tuple(
        pair_matrix(transformed[i], transformed[j]).rank() for i, j in PAIRS
    )
    assert profile == (3, 3, 3, 4, 4, 4)
    relation_ranks = []
    for edge in ((0, 1), (0, 2), (0, 3)):
        kernel = pair_matrix(transformed[edge[0]], transformed[edge[1]]).nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    # Independently check that the implicit equation retains both denominator
    # boundaries of the dense k-chart.
    s_symbol, r_symbol, t_symbol, k_symbol = sp.symbols("s r t k")
    boundary_polynomial = (
        1 - r_symbol * t_symbol - k_symbol * s_symbol * (t_symbol - r_symbol)
    )
    assert boundary_polynomial.subs(
        {s_symbol: 0, r_symbol: 2, t_symbol: sp.Rational(1, 2)}
    ) == 0
    assert boundary_polynomial.subs({r_symbol: 1, t_symbol: 1}) == 0
    assert boundary_polynomial.subs({r_symbol: -1, t_symbol: -1}) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import audit",
                "field": "Q",
                "source_permutation": permutation,
                "source_scales": scales,
                "pure_support": {"1111": "-840"},
                "pair_profile": profile,
                "relation_ranks": relation_ranks,
                "implicit_boundary_charts_retained": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
