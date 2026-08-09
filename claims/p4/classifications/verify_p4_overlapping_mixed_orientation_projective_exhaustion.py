#!/usr/bin/env python3
"""Verify projective exhaustion of the overlapping mixed-orientation chart."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def leaves(A, H, C, D, P, R, Q):
    return (
        sp.Matrix(((0, 0, 1, 1), (A, H, C, D))),
        sp.Matrix(((P, R, 0, Q), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )


def contraction_data(A, H, C, D, P, R, Q):
    planes = leaves(A, H, C, D, P, R, Q)
    identity = sp.eye(4)
    rows = []
    active = None
    for bits in itertools.product((0, 1), repeat=3):
        covector = sp.Matrix(
            [[
                permanent(
                    (
                        identity.row(coordinate),
                        planes[0].row(bits[0]),
                        planes[1].row(bits[1]),
                        planes[2].row(bits[2]),
                    )
                )
                for coordinate in range(4)
            ]]
        )
        if bits == (0, 0, 0):
            active = covector
        elif covector != sp.zeros(1, 4):
            rows.append(covector)
    assert active is not None
    return sp.Matrix.vstack(*rows), active


def pluecker(plane: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([plane[:, pair].det() for pair in PAIRS])


def proportional(left: sp.Matrix, right: sp.Matrix) -> bool:
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i, j in itertools.combinations(range(len(left)), 2)
    )


def main() -> None:
    A, H, C, D, P, R, Q = sp.symbols("A H C D P R Q")
    matrix, escape = contraction_data(A, H, C, D, P, R, Q)
    expected_matrix = sp.Matrix(
        [
            [D * R + H * Q, A * Q + C * Q + D * P, D * R + H * Q, A * R + C * R + H * P],
            [C * R - D * R - H * Q, -A * Q + C * P - D * P, A * R + H * P, -A * R - H * P],
            [H, A - C + D, -H, H],
        ]
    )
    assert sp.simplify(matrix - expected_matrix) == sp.zeros(3, 4)
    assert sp.simplify(escape - sp.Matrix([[R, P + Q, R, R]])) == sp.zeros(1, 4)

    # The affine rank-one Springer base consists of exactly four lines.
    affine = matrix.subs({H: 1, R: 1})
    affine_minors = [
        sp.expand(affine.extract(rows, columns).det())
        for rows in itertools.combinations(range(3), 2)
        for columns in itertools.combinations(range(4), 2)
    ]
    rank_one_generators = [
        Q + D,
        P + A + C,
        D * (A + C),
        A * (C - D),
    ]
    groebner_minors = sp.groebner(affine_minors, Q, P, D, C, A, order="lex")
    groebner_generators = sp.groebner(rank_one_generators, Q, P, D, C, A, order="lex")
    assert tuple(poly.as_expr() for poly in groebner_minors.polys) == tuple(
        poly.as_expr() for poly in groebner_generators.polys
    )

    t = sp.symbols("t")
    lines = {
        "star": {A: 0, C: t, D: 0, P: -t, Q: 0},
        "path_A": {A: t, C: 0, D: 0, P: -t, Q: 0},
        "path_D": {A: 0, C: 0, D: t, P: 0, Q: -t},
        "first_component": {A: t, C: -t, D: -t, P: 0, Q: t},
    }
    affine_escape = escape.subs({H: 1, R: 1})
    line_relation_ranks = {}
    for name, specialization in lines.items():
        specialized_matrix = affine.subs(specialization)
        assert specialized_matrix.rank() == 1
        assert sp.Matrix.vstack(specialized_matrix, affine_escape.subs(specialization)).rank() == 2
        specialized_leaves = tuple(
            plane.subs({H: 1, R: 1, **specialization})
            for plane in leaves(A, H, C, D, P, R, Q)
        )
        ranks = []
        for left, right in ((0, 1), (0, 2), (1, 2)):
            product_map = pair_matrix(specialized_leaves[left], specialized_leaves[right])
            assert product_map.rank() == 3
            kernel = product_map.nullspace()
            assert len(kernel) == 1
            ranks.append(sp.Matrix(2, 2, tuple(kernel[0])).rank())
        line_relation_ranks[name] = tuple(ranks)

    assert line_relation_ranks == {
        "star": (1, 1, 1),
        "path_A": (1, 1, 1),
        "path_D": (1, 1, 1),
        "first_component": (2, 1, 1),
    }

    # The two path lines are the same orbit: source 0<->3, then
    # diag(-1,1,1,-1), together with mode 1<->2.
    path_A = tuple(
        plane.subs({H: 1, R: 1, **lines["path_A"]})
        for plane in leaves(A, H, C, D, P, R, Q)
    )
    path_D = tuple(
        plane.subs({H: 1, R: 1, **lines["path_D"]})
        for plane in leaves(A, H, C, D, P, R, Q)
    )
    source_sign = sp.diag(-1, 1, 1, -1)
    transformed = tuple(plane[:, (3, 1, 2, 0)] * source_sign for plane in path_A)
    transformed = (transformed[1], transformed[0], transformed[2])
    assert all(
        proportional(pluecker(left), pluecker(right))
        for left, right in zip(transformed, path_D, strict=True)
    )

    # H=0, R=1: rank <=2 is the main hyperplane plus one residual plane.
    h_boundary = matrix.subs({H: 0, R: 1})
    h_minors = tuple(
        sp.factor(h_boundary[:, columns].det())
        for columns in itertools.combinations(range(4), 3)
    )
    L = A - C + D
    assert h_minors == (
        -D * L**2,
        C * L * (A + C - D),
        0,
        -A * L * (A + C + D),
    )

    h_main = h_boundary.subs(D, -A + C)
    x_main = escape.subs({H: 0, R: 1, D: -A + C})
    assert sp.simplify(x_main - (h_main.row(0) + h_main.row(1)) / C) == sp.zeros(1, 4)
    assert sp.simplify(x_main.subs(A, 0) - h_main.row(0).subs(A, 0) / C) == sp.zeros(1, 4)
    assert h_main.subs(C, 0).rank() == 1
    assert sp.Matrix.vstack(h_main.subs(C, 0), x_main.subs(C, 0)).rank() == 2

    h_residual = h_boundary.subs({C: -A, D: 0})
    x_residual = escape.subs({H: 0, R: 1})
    assert h_residual.rank() == 2
    assert sp.Matrix.vstack(h_residual, x_residual).rank() == 3

    for specialization in ({A: 1, C: 0, D: -1}, {A: 1, C: -1, D: 0}):
        boundary_leaves = tuple(
            plane.subs({H: 0, R: 1, **specialization})
            for plane in leaves(A, H, C, D, P, R, Q)
        )
        assert pair_matrix(boundary_leaves[0], boundary_leaves[2]).rank() == 2

    # R=0, H!=0: the two rulings are P=Q and P=-Q.
    r_boundary = matrix.subs(R, 0)
    r_minors = tuple(
        sp.factor(r_boundary[:, columns].det())
        for columns in itertools.combinations(range(4), 3)
    )
    common = (P - Q) * (P + Q)
    assert r_minors == (
        D * H**2 * common,
        -C * H**2 * common,
        -H**3 * common,
        -A * H**2 * common,
    )
    assert escape.subs({R: 0, P: -Q}) == sp.zeros(1, 4)
    r_genuine_leaves = tuple(
        plane.subs({R: 0, H: 1, P: 1, Q: 1})
        for plane in leaves(A, H, C, D, P, R, Q)
    )
    assert pair_matrix(r_genuine_leaves[1], r_genuine_leaves[2]).rank() == 2

    # At H=R=0 all leaves lie in one coordinate hyperplane.  Every
    # forbidden and active contraction is a multiple of the same covector.
    corner_matrix = matrix.subs({H: 0, R: 0})
    corner_escape = escape.subs({H: 0, R: 0})
    assert all(
        corner_matrix[row, column] == 0
        for row in range(3)
        for column in (0, 2, 3)
    )
    assert all(corner_escape[0, column] == 0 for column in (0, 2, 3))
    corner_leaves = leaves(A, 0, C, D, P, 0, Q)
    assert all(plane[:, 1] == sp.zeros(2, 1) for plane in corner_leaves)

    print(
        json.dumps(
            {
                "status": "pass",
                "affine_rank_one_lines": tuple(lines),
                "line_relation_ranks": line_relation_ranks,
                "new_components": (16, 17),
                "H_boundary": "zero tensor or lower-pair closure",
                "R_boundary": "zero tensor or lower-pair closure",
                "H_R_corner": "zero tensor or embedded P3 closure",
                "projective_chart_exhausted": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
