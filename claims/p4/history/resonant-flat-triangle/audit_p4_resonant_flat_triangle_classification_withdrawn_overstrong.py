#!/usr/bin/env python3
"""Audit of exact normal forms in a withdrawn overstrong classification."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import itertools
import json

import sympy as sp


def permanent_dp(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    next_states[new_mask] = next_states.get(new_mask, 0) + value * entry
        states = next_states
    return sp.expand(states[15])


def pair_vector(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def main() -> None:
    # Use the crossed partition {0,2}|{1,3}.
    a = sp.Matrix((1, 0, 1, 0))
    a_bar = sp.Matrix((1, 0, -1, 0))
    b = sp.Matrix((0, 1, 0, 1))
    b_bar = sp.Matrix((0, 1, 0, -1))
    s, t = sp.symbols("sigma tau")
    planes = (
        (b_bar, a_bar),
        (a, b),
        (a, b + s * a_bar),
        (a, b + t * a_bar),
    )

    coefficients = {}
    for word in itertools.product((0, 1), repeat=4):
        rows = tuple(
            tuple(planes[mode][word[mode]][column] for column in range(4))
            for mode in range(4)
        )
        coefficients[word] = sp.factor(permanent_dp(rows))
    assert sp.expand(coefficients[(1, 1, 1, 1)] + 4 * (s + t)) == 0
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word != (1, 1, 1, 1)
    )

    relation_ranks = {}
    for left, right in ((1, 2), (1, 3), (2, 3)):
        products = sp.Matrix.hstack(
            *(
                pair_vector(planes[left][i], planes[right][j])
                for i, j in itertools.product((0, 1), repeat=2)
            )
        )
        relation_ranks[f"{left}{right}"] = products.rank()
        kernel = products.nullspace()
        assert len(kernel) == 1
        relation_matrix = sp.Matrix(2, 2, list(kernel[0]))
        assert relation_matrix.det() != 0
    assert set(relation_ranks.values()) == {3}

    # A concrete point independently checks nonzero purity and the
    # lower-rank edge outside the triangle.
    point = {s: 1, t: 2}
    assert coefficients[(1, 1, 1, 1)].subs(point) == -12
    edge_01 = sp.Matrix.hstack(
        *(
            pair_vector(planes[0][i], planes[1][j])
            for i, j in itertools.product((0, 1), repeat=2)
        )
    )
    assert edge_01.rank() == 2

    result = {
        "crossed_partition": "{0,2}|{1,3}",
        "nonzero_integer_coefficient": -12,
        "triangle_pair_ranks": relation_ranks,
        "triangle_relation_matrix_ranks": 2,
        "outside_edge_01_rank": edge_01.rank(),
        "dimension_comparison": "triangle <=4, every nonzero incidence component >=5",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
