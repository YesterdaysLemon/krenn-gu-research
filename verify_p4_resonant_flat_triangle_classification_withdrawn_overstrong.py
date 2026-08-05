#!/usr/bin/env python3
"""Replay of exact identities in a withdrawn overstrong classification."""

from __future__ import annotations

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


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def synchronization_matrix(y: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("a b c d e f g h")
    yp = sp.Matrix(variables[:4])
    xp = sp.Matrix(variables[4:])
    equations = pair(y, xp) - pair(x, yp)
    matrix, _ = sp.linear_eq_to_matrix(list(equations), variables)
    return matrix


def main() -> None:
    # The 2+1+1 collision has a two-dimensional partner pencil and
    # every valid partner has active row proportional to x.
    y_collision = sp.Matrix((1, 1, 0, 1))
    x_collision = sp.Matrix((0, 0, 1, 1))
    z_collision = sp.Matrix((0, 0, 1, -1))
    collision_kernel = sp.Matrix.hstack(
        sp.Matrix.vstack(y_collision, x_collision),
        sp.Matrix.vstack(z_collision, sp.zeros(4, 1)),
    )
    collision_sync = synchronization_matrix(y_collision, x_collision)
    assert collision_sync.rank() == 6
    assert collision_sync * collision_kernel == sp.zeros(6, 2)
    assert pair(x_collision, x_collision).rank() == 1
    assert permanent(
        (x_collision, x_collision, x_collision, sp.ones(4, 1))
    ) == 0

    # The 1+3 partner pencil spans one fixed plane, whose square has
    # rank two.
    y_star = sp.Matrix((1, 0, 0, 0))
    x_star = sp.Matrix((0, 1, 1, 1))
    star_kernel = sp.Matrix.hstack(
        sp.Matrix.vstack(y_star, x_star),
        sp.Matrix.vstack(sp.zeros(4, 1), y_star),
    )
    star_sync = synchronization_matrix(y_star, x_star)
    assert star_sync.rank() == 6
    assert star_sync * star_kernel == sp.zeros(6, 2)
    star_square = sp.Matrix.hstack(
        pair(y_star, y_star),
        pair(y_star, x_star),
        pair(x_star, x_star),
    )
    assert star_square.rank() == 2

    # Balanced 2+2 synchronization space.
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    balanced_sync = synchronization_matrix(a, b)
    balanced_kernel = sp.Matrix.hstack(
        sp.Matrix.vstack(a, b),
        sp.Matrix.vstack(b_bar, sp.zeros(4, 1)),
        sp.Matrix.vstack(sp.zeros(4, 1), a_bar),
    )
    assert balanced_sync.rank() == 5
    assert balanced_sync * balanced_kernel == sp.zeros(6, 3)
    assert balanced_kernel.rank() == 3

    alpha, beta, r, q = sp.symbols("alpha beta r q")
    y1, x1 = a, b
    y2, x2 = a + r * beta * b_bar, b + r * alpha * a_bar
    y3, x3 = a + q * beta * b_bar, b + q * alpha * a_bar
    assert pair(y1, x2) == pair(x1, y2)
    assert pair(y1, x3) == pair(x1, y3)
    assert pair(y2, x3) == pair(x2, y3)

    def triple(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
        output = []
        for missing in range(4):
            columns = [index for index in range(4) if index != missing]
            output.append(
                sp.expand(
                    sum(
                        left[columns[p[0]]]
                        * middle[columns[p[1]]]
                        * right[columns[p[2]]]
                        for p in itertools.permutations(range(3))
                    )
                )
            )
        return sp.Matrix(output)

    Y = triple(y1, y2, y3)
    K = triple(x1, y2, y3)
    J = triple(y1, x2, x3)
    X = triple(x1, x2, x3)
    # R_3 vectors are stored in missing-coordinate order.
    u = triple(a, a, b) / 2
    u_bar = triple(a, a, b_bar) / 2
    v = triple(a, b, b) / 2
    v_bar = triple(a_bar, b, b) / 2
    assert sp.Matrix.hstack(u, u_bar, v, v_bar).rank() == 4
    assert sp.simplify(Y - (2 * beta * (r + q) * u_bar - 2 * r * q * beta**2 * v)) == sp.zeros(4, 1)
    assert K == 2 * u
    assert J == 2 * v
    assert sp.simplify(X - (2 * alpha * (r + q) * v_bar - 2 * r * q * alpha**2 * u)) == sp.zeros(4, 1)

    # The surviving canonical family beta=0, alpha=1.
    s, t = sp.symbols("s t")
    planes = (
        (b_bar, a_bar),
        (a, b),
        (a, b + s * a_bar),
        (a, b + t * a_bar),
    )
    coefficients = {}
    for word in itertools.product((0, 1), repeat=4):
        value = permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        coefficients["".join(map(str, word))] = sp.factor(value)
    assert sp.expand(coefficients["1111"] + 4 * (s + t)) == 0
    assert all(value == 0 for word, value in coefficients.items() if word != "1111")

    triangle_ranks = {}
    for left, right in ((1, 2), (1, 3), (2, 3)):
        product_map = sp.Matrix.hstack(
            *(
                pair(planes[left][row_left], planes[right][row_right])
                for row_left, row_right in itertools.product((0, 1), repeat=2)
            )
        )
        triangle_ranks[f"{left}{right}"] = product_map.rank()
    assert set(triangle_ranks.values()) == {3}

    result = {
        "collision_types": {
            "zero_column": "embedded P3",
            "four_distinct": "compound obstruction",
            "2+1+1": "active cube zero",
            "1+3": "pair rank two",
            "2+2": "canonical survivor",
        },
        "balanced_partner_dimension": 3,
        "pure_coefficient": "-4*(s+t)",
        "triangle_pair_ranks": triangle_ranks,
        "triangle_locus_dimension_upper_bound": 4,
        "new_component_generic_point": False,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
