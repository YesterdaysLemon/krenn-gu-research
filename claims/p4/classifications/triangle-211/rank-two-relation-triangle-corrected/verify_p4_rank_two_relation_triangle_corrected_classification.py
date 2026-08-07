#!/usr/bin/env python3
"""Exact replay of the corrected rank-two-relation triangle classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def product2(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def product3(*rows: sp.Matrix) -> sp.Matrix:
    values = []
    for omitted in range(4):
        columns = [index for index in range(4) if index != omitted]
        values.append(
            sp.expand(
                sum(
                    sp.prod(rows[index][columns[permutation[index]]] for index in range(3))
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(values)


def product4(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficient_matrix(
    first: tuple[sp.Matrix, sp.Matrix],
    second: tuple[sp.Matrix, sp.Matrix],
    third: tuple[sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    y, x = first
    y2, x2 = second
    y3, x3 = third
    return sp.Matrix.hstack(
        product3(y, y2, y3),
        product3(x, y2, y3),
        product3(y, x2, x3),
        product3(x, x2, x3),
    )


def pair_matrix(
    first: tuple[sp.Matrix, sp.Matrix], second: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[product2(left, right) for left in first for right in second]
    )


def synchronization_matrix(y: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("a0:4 b0:4")
    candidate_y = sp.Matrix(variables[:4])
    candidate_x = sp.Matrix(variables[4:])
    matrix, _ = sp.linear_eq_to_matrix(
        list(product2(y, candidate_x) - product2(x, candidate_y)), variables
    )
    return matrix


def minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def check_pencil(
    y: sp.Matrix, x: sp.Matrix, sharp_y: sp.Matrix, sharp_x: sp.Matrix
) -> None:
    sync = synchronization_matrix(y, x)
    basis = sp.Matrix.hstack(
        sp.Matrix.vstack(y, x), sp.Matrix.vstack(sharp_y, sharp_x)
    )
    assert sync.rank() == 6
    assert sync * basis == sp.zeros(6, 2)
    assert basis.rank() == 2


def main() -> None:
    t, u, r, s = sp.symbols("t u r s")

    # Kernel support three: after the already-proved distinct-ratio chart,
    # the only collision types are 2+1 and 3.  Their synchronizer points at
    # infinity have local rank one; all finite partners keep a common active
    # row of support at most two, so the active cube is zero.
    support_three = {
        "2+1": (
            sp.Matrix((1, 0, 1, 1)),
            sp.Matrix((0, 1, 0, 1)),
            sp.Matrix((0, -1, 0, 1)),
        ),
        "3": (
            sp.Matrix((1, 0, 1, 1)),
            sp.Matrix((0, 1, 0, 0)),
            sp.Matrix((0, 1, 0, 0)),
        ),
    }
    for y, x, sharp_y in support_three.values():
        check_pencil(y, x, sharp_y, sp.zeros(4, 1))
        assert product3(x, x, x) == sp.zeros(4, 1)

    # Kernel support two, distinct finite ratios.
    y = sp.Matrix((1, 1, 0, 0))
    x = sp.Matrix((0, 1, 1, 1))
    sharp_y = sp.zeros(4, 1)
    sharp_x = sp.Matrix((-1, 1, 0, 0))
    check_pencil(y, x, sharp_y, sharp_x)
    first = (y, x)
    second = (y, x + t * sharp_x)
    third = (y, x + u * sharp_x)
    C_distinct = coefficient_matrix(first, second, third)
    expected_distinct = sp.Matrix(
        (
            (0, 0, 2, 2 * t + 2 * u + 6),
            (0, 0, 2, -2 * t - 2 * u),
            (0, 2, 2, -2 * t * u - 2 * t - 2 * u),
            (0, 2, 2, -2 * t * u - 2 * t - 2 * u),
        )
    )
    assert C_distinct == expected_distinct
    assert C_distinct[:, :3].rank() == 2
    assert sp.factor(-8 * (2 * t + 2 * u + 3)) in minors(C_distinct, 3)

    # Kernel support two, coincident finite ratios.  The synchronizer is a
    # presymplectic plane with radical A.
    a = sp.Matrix((1, 1, 0, 0))
    abar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    bbar = sp.Matrix((0, 0, 1, -1))
    A = sp.Matrix.vstack(a, b)
    B0 = sp.Matrix.vstack(-bbar, sp.zeros(4, 1))
    B1 = sp.Matrix.vstack(sp.zeros(4, 1), -abar)
    sync_equal = synchronization_matrix(a, b)
    equal_basis = sp.Matrix.hstack(A, B0, B1)
    assert sync_equal.rank() == 5
    assert sync_equal * equal_basis == sp.zeros(6, 3)
    assert equal_basis.rank() == 3
    assert product2(a, abar) == product2(b, bbar) == sp.zeros(6, 1)

    D = r * B0 + s * B1
    dy, dx = D[:4, 0], D[4:, 0]
    equal_second = (a + t * dy, b + t * dx)
    equal_third = (a + u * dy, b + u * dx)
    C_equal = coefficient_matrix((a, b), equal_second, equal_third)
    expected_equal = sp.Matrix(
        (
            (-2 * r**2 * t * u, 0, 2, 2 * s * (t + u)),
            (-2 * r**2 * t * u, 0, 2, -2 * s * (t + u)),
            (2 * r * (t + u), 2, 0, -2 * s**2 * t * u),
            (-2 * r * (t + u), 2, 0, -2 * s**2 * t * u),
        )
    )
    assert sp.simplify(C_equal - expected_equal) == sp.zeros(4)
    compression = [
        sp.factor(C_equal.extract(rows, (0, 1, 2)).det())
        for rows in itertools.combinations(range(4), 3)
    ]
    assert compression == [0, 0, 16 * r * (t + u), 16 * r * (t + u)]
    assert -4 in minors(C_equal[:, :3], 2)
    assert sp.factor(-16 * s * (t + u)) in minors(C_equal, 3)
    # For r!=0 compression gives u=-t, after which every full cofactor
    # vanishes while the compressed span still has rank two.
    assert all(value == 0 for value in minors(C_equal.subs(u, -t), 3))

    # A projective direction is a valid local plane only for r*s!=0, but
    # its pair image with A already has rank two.
    projective_pair = pair_matrix((a, b), (dy, dx))
    assert all(value == 0 for value in minors(projective_pair, 3))
    assert any(value != 0 for value in minors(projective_pair, 2))

    # Kernel support one with no zero source column.  The synchronizer only
    # changes x by y, so every finite partner is the same plane.  Its square
    # has dimension two, not three.
    y_one = sp.Matrix((1, 0, 0, 0))
    x_one = sp.Matrix((0, 1, 1, 1))
    check_pencil(y_one, x_one, sp.zeros(4, 1), y_one)
    assert pair_matrix((y_one, x_one), (y_one, x_one)).rank() == 2

    # The unique surviving family and its forced fourth plane.
    alpha0, alpha1, alpha2 = sp.symbols("alpha0 alpha1 alpha2")
    alphas = (alpha0, alpha1, alpha2)
    leaves = tuple((a, b + alpha * abar) for alpha in alphas)
    C = coefficient_matrix(*leaves)
    e1 = alpha0 + alpha1 + alpha2
    e2 = alpha0 * alpha1 + alpha0 * alpha2 + alpha1 * alpha2
    expected_C = sp.Matrix(
        (
            (0, 0, 2, -2 * e1),
            (0, 0, 2, 2 * e1),
            (0, 2, 0, -2 * e2),
            (0, 2, 0, -2 * e2),
        )
    )
    assert C == expected_C
    assert C[:, :3].rank() == 2
    assert sp.factor(C.det()) == 0
    for left, right in itertools.combinations(leaves, 2):
        product = pair_matrix(left, right)
        assert product.rank() == 3
        assert 4 in minors(product, 3)

    opposite = (bbar, abar)
    planes = (opposite,) + leaves
    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        selected = tuple(planes[index][bits[index]] for index in range(4))
        coefficients["".join(map(str, bits))] = sp.factor(product4(selected))
    assert sp.expand(coefficients["1111"] + 4 * e1) == 0
    assert all(value == 0 for word, value in coefficients.items() if word != "1111")

    result = {
        "corrected_classification": "all pure rank-three triangles with three rank-two relations",
        "surviving_normal_form": "U0=<b_bar,a_bar>; Ui=<a,b+alpha_i*a_bar>",
        "purity_condition": "alpha0+alpha1+alpha2 != 0",
        "restricted_tensor": "-4*(alpha0+alpha1+alpha2)*x0*x1*x2*x3",
        "leaf_pair_ranks": [3, 3, 3],
        "excluded_kernel_supports": [4, 3, 1],
        "support_two_other_strata": "zero columns, zero escape, or pair-rank two",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
