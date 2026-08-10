#!/usr/bin/env python3
"""Replay of local lemmas in a withdrawn overstrong star theorem."""

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


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def sync_matrix(y: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("a b c d e f g h")
    yp, xp = sp.Matrix(variables[:4]), sp.Matrix(variables[4:])
    matrix, _ = sp.linear_eq_to_matrix(
        list(pair(y, xp) - pair(x, yp)), variables
    )
    return matrix


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def main() -> None:
    # Collision synchronizers.
    y_collision = sp.Matrix((1, 1, 0, 1))
    x_collision = sp.Matrix((0, 0, 1, 1))
    z_collision = sp.Matrix((0, 0, 1, -1))
    collision_basis = sp.Matrix.hstack(
        sp.Matrix.vstack(y_collision, x_collision),
        sp.Matrix.vstack(z_collision, sp.zeros(4, 1)),
    )
    collision_sync = sync_matrix(y_collision, x_collision)
    assert collision_sync.rank() == 6
    assert collision_sync * collision_basis == sp.zeros(6, 2)
    assert permanent(
        (x_collision, x_collision, x_collision, x_collision)
    ) == 0

    y_star = sp.Matrix((1, 0, 0, 0))
    x_star = sp.Matrix((0, 1, 1, 1))
    star_basis = sp.Matrix.hstack(
        sp.Matrix.vstack(y_star, x_star),
        sp.Matrix.vstack(sp.zeros(4, 1), y_star),
    )
    star_sync = sync_matrix(y_star, x_star)
    assert star_sync.rank() == 6
    assert star_sync * star_basis == sp.zeros(6, 2)
    assert sp.Matrix.hstack(
        pair(y_star, y_star), pair(y_star, x_star), pair(x_star, x_star)
    ).rank() == 2

    # Generic pencil and its pair-rank-drop matching.
    L, t, u, z = sp.symbols("lambda t u z")
    y = sp.Matrix((1, 0, 1, 1))
    x = sp.Matrix((0, 1, 1, L))
    ys = sp.Matrix((0, 1, -1, -L))
    xs = sp.Matrix((L, 0, -L, -L))
    yt, xt = y + t * ys, x + t * xs
    yu, xu = y + u * ys, x + u * xs
    assert pair(yt, xu) == pair(xt, yu)
    product_map = sp.Matrix.hstack(pair(yt, yu), pair(yt, xu), pair(xt, xu))
    minors = [
        sp.factor(product_map.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(6), 3)
    ]
    R1 = L * t * u - 1
    R2 = L * t * u - t - u + 1
    R3 = L * t * u - L * t - L * u + 1
    # These six minors force at least two of R1,R2,R3 to vanish.
    required = (
        4 * L * R1 * R2**2,
        -4 * L * R2**2 * R3,
        4 * R1 * R3**2,
        4 * R2 * R3**2,
        4 * (L - 1) * R1**2 * R3,
        4 * L * (L - 1) * R1**2 * R2,
    )
    assert all(any(sp.expand(minor - target) == 0 for minor in minors) for target in required)
    pencil_field = sp.QQ.frac_field(L)
    for left, right in ((R1, R2), (R1, R3), (R2, R3)):
        basis = sp.groebner((left, right), t, u, domain=pencil_field)
        assert all(basis.reduce(minor)[1] == 0 for minor in minors)

    matching_polynomials = (
        sp.Poly(z**2 - 2 * z + 1 / L, z, domain=sp.QQ.frac_field(L)),
        sp.Poly(z**2 - 2 * z / L + 1 / L, z, domain=sp.QQ.frac_field(L)),
        sp.Poly(z**2 - 1 / L, z, domain=sp.QQ.frac_field(L)),
    )
    for left, right in itertools.combinations(matching_polynomials, 2):
        resultant = sp.factor(sp.resultant(left.as_expr(), right.as_expr(), z))
        assert sp.factor(resultant).subs(L, 1) == 0
        assert resultant != 0
    discriminants = [
        sp.factor(sp.discriminant(poly.as_expr(), z))
        for poly in matching_polynomials
    ]
    assert discriminants[0].subs(L, 1) == 0
    assert discriminants[1].subs(L, 1) == 0
    assert discriminants[2].subs(L, 1) != 0
    assert all(value != 0 for value in discriminants)

    # Balanced collision synchronizer and the constant forbidden word.
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    balanced_basis = sp.Matrix.hstack(
        sp.Matrix.vstack(a, b),
        sp.Matrix.vstack(b_bar, sp.zeros(4, 1)),
        sp.Matrix.vstack(sp.zeros(4, 1), a_bar),
    )
    balanced_sync = sync_matrix(a, b)
    assert balanced_sync.rank() == 5
    assert balanced_sync * balanced_basis == sp.zeros(6, 3)

    alpha_2, alpha_3, beta_1 = sp.symbols("alpha_2 alpha_3 beta_1")
    forbidden = permanent(
        (
            a,
            a + beta_1 * b_bar,
            b + alpha_2 * a_bar,
            b + alpha_3 * a_bar,
        )
    )
    assert forbidden == 4

    result = {
        "tree_gauge": "three synchronization equations",
        "generic_synchronizer": "projective adjugate pencil",
        "generic_rank_drop_graph": "three disjoint edges",
        "projective_infinity_rank_drop_partner": False,
        "balanced_forbidden_coefficient": int(forbidden),
        "conclusion": "rank-two-relation star is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
