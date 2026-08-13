"""Exact replay for the support-one higher-row-rank exclusion.

The owning Markdown file contains the proof.  This verifier checks the
displayed graph contractions, zero-row table, tangent lemmas, two-plane
atlas, and unequal-kernel binary chart over exact SymPy arithmetic.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def e(size: int, index: int) -> sp.Matrix:
    return sp.eye(size)[:, index]


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def tidx(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def derivative(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    """Matrix of q -> per(u,v,q), with three 3-dimensional sources."""
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tidx(x, y, z)
        out[row, 6 + z] = u[x] * v[3 + y] + v[x] * u[3 + y]
        out[row, 3 + y] = u[x] * v[6 + z] + v[x] * u[6 + z]
        out[row, x] = u[3 + y] * v[6 + z] + v[3 + y] * u[6 + z]
    return out


def graph_contraction_injectivity() -> None:
    graph = sp.Matrix([[2, 0, 1], [0, 3, 1], [0, 0, 4]])
    beta = sp.Rational(5)
    c = e(3, 2) - beta * graph.inv() * e(3, 2)

    columns = []
    for index in range(3):
        a = e(3, index)
        columns.append(beta * pair(a, e(3, 2)) + pair(c, graph * a))
    phi = sp.Matrix.hstack(*columns)
    assert phi.rank() == 3

    preimage = graph.inv() * e(3, 2)
    assert sp.simplify(
        beta * pair(preimage, e(3, 2))
        + pair(c, graph * preimage)
        - pair(e(3, 2), e(3, 2))
    ) == sp.zeros(9, 1)
    assert graph * c != -beta * e(3, 2)

    zero_c = sp.Matrix.hstack(
        *[beta * pair(e(3, i), e(3, 2)) for i in range(3)]
    )
    assert zero_c.rank() == 3
    print("support-one graph contraction: PASS (target preimage / injectivity)")


def zero_row_correction_table() -> None:
    kappa = sp.symbols("kappa", nonzero=True)
    targets = [e(27, tidx(i, i, i)) for i in range(3)]

    for missing in range(3):
        corrections = [sp.zeros(27, 1) for _ in range(3)]
        corrections[missing] = -targets[missing] / kappa
        for first in range(3):
            for third in range(3):
                left = -int(first == third == missing) * targets[missing]
                right = (
                    kappa * int(third == missing) * corrections[first]
                )
                assert left == right

        support_target = targets[2]
        correction_space = sp.Matrix.hstack(targets[missing])
        absorbable = (
            correction_space.row_join(support_target).rank()
            == correction_space.rank()
        )
        assert absorbable == (missing == 2)

    print("mixed zero row: PASS (all corrections on T_d / support forces d=2)")


def graph_row_profiles() -> None:
    full = sp.Matrix([[2, 0, 5], [0, 3, 7], [0, 0, 11]])
    for index, scale in ((0, 2), (1, 3)):
        beta = e(3, index) / scale
        alpha = full.T * beta
        assert alpha[index] == 1
        target_weights = sp.Matrix(
            [alpha[i] * beta[i] for i in range(3)]
        )
        assert target_weights == e(3, index) / scale
    beta_1 = e(3, 1) / 3
    alpha_0 = full.T * (e(3, 0) / 2)
    assert all(alpha_0[i] * beta_1[i] == 0 for i in range(3))

    same = sp.diag(2, 3, 0)
    assert same.rank() == 2
    assert same * e(3, 2) == sp.zeros(3, 1)

    # Kernel colour s=0, missing colour d=2, remaining colour j=1.
    different = sp.Matrix([[0, 0, 5], [0, 3, 7], [0, 0, 0]])
    assert different.rank() == 2
    assert different * e(3, 0) == sp.zeros(3, 1)
    assert different.row(2) == sp.zeros(1, 3)
    assert different.row(0) == sp.Matrix([[0, 0, 5]])
    assert different.row(1) == sp.Matrix([[0, 3, 7]])
    print("graph row profiles: PASS ((3,3), equal-kernel, unequal-kernel)")


def tangent_line_separation() -> None:
    variables = sp.Matrix(sp.symbols("v0:9"))

    two = e(9, 0) + e(9, 3)
    q_two = sp.Matrix.hstack(e(9, 0) - e(9, 3), e(9, 6))
    square_two = derivative(two, two) * q_two
    assert square_two.rank() == 1
    assert [i for i, value in enumerate(square_two[:, 1]) if value] == [
        tidx(0, 0, 0)
    ]
    assert sp.Matrix.hstack(
        derivative(two, two), e(27, tidx(2, 2, 2))
    ).rank() == derivative(two, two).rank() + 1

    mixed = derivative(two, variables) * q_two
    forbidden = [index for index in range(27) if index != tidx(2, 2, 2)]
    solutions = sp.linsolve(list(mixed[forbidden, :]), list(variables))
    for solution in solutions:
        image = mixed.subs(dict(zip(variables, solution, strict=True)))
        assert image[tidx(2, 2, 2), :] == sp.zeros(1, 2)

    full = e(9, 0) + e(9, 3) + e(9, 6)
    q_full = sp.Matrix.hstack(e(9, 0) - e(9, 3), e(9, 1))
    square_full = derivative(full, full) * q_full
    assert square_full.rank() == 1
    assert [i for i, value in enumerate(square_full[:, 1]) if value] == [
        tidx(1, 0, 0)
    ]
    assert sp.Matrix.hstack(
        derivative(full, full), e(27, tidx(2, 2, 2))
    ).rank() == derivative(full, full).rank() + 1
    print("tangent-line lemma: PASS (separation / mixed factor sharing)")


def two_plane_square_pencil_atlas() -> None:
    variables = sp.Matrix(sp.symbols("w0:9"))
    two = e(9, 0) + e(9, 3)

    # Nonconjugate kernel row: every common mixed zero is x-y.
    nonconjugate = sp.Matrix.hstack(e(9, 1), e(9, 6))
    solution = next(
        iter(
            sp.linsolve(
                list(derivative(two, variables) * nonconjugate),
                list(variables),
            )
        )
    )
    free = sorted(set().union(*(entry.free_symbols for entry in solution)), key=str)
    assert len(free) == 1
    vector = sp.Matrix(solution).subs(free[0], 1)
    assert vector == e(9, 3) - e(9, 0)
    nonconjugate_square = derivative(vector, vector) * nonconjugate
    assert nonconjugate_square.rank() == 1
    assert [i for i, value in enumerate(nonconjugate_square[:, 1]) if value] == [
        tidx(0, 0, 0)
    ]

    # Conjugate kernel row: the common-zero family is lambda(x-y)+z'.
    conjugate = sp.Matrix.hstack(e(9, 0) - e(9, 3), e(9, 6))
    conjugate_solution = next(
        iter(
            sp.linsolve(
                list(derivative(two, variables) * conjugate),
                list(variables),
            )
        )
    )
    assert conjugate_solution[0] == -conjugate_solution[3]
    assert all(conjugate_solution[i] == 0 for i in (1, 2, 4, 5))

    # Three-source chart with a!=0: v remains on the three base lines.
    full = e(9, 0) + e(9, 3) + e(9, 6)
    scaling = e(9, 0) + e(9, 3) - 2 * e(9, 6)
    full_plane = sp.Matrix.hstack(scaling, e(9, 1))
    full_solution = next(
        iter(
            sp.linsolve(
                list(derivative(full, variables) * full_plane),
                list(variables),
            )
        )
    )
    assert all(full_solution[i] == 0 for i in (1, 2, 4, 5, 7, 8))
    assert full_solution[0] == 3 * full_solution[6]
    assert full_solution[3] == -full_solution[6]

    # Boundary a=0: every common mixed zero is pure in X, so its square is 0.
    boundary = sp.Matrix.hstack(e(9, 3) - e(9, 6), e(9, 1))
    boundary_solution = next(
        iter(
            sp.linsolve(
                list(derivative(full, variables) * boundary),
                list(variables),
            )
        )
    )
    assert all(boundary_solution[i] == 0 for i in range(3, 9))
    print("two-plane square pencil: PASS (two-source / three-source atlas)")


def binary_five_product_replay() -> None:
    # Replay the three source-support mechanisms used by the inherited S2AF
    # lemma on a binary projected target.
    full = e(9, 0) + e(9, 3) + e(9, 6)
    scaling = sp.Matrix.hstack(e(9, 0) - e(9, 3), e(9, 0) - e(9, 6))
    assert derivative(full, full) * scaling == sp.zeros(27, 2)

    variables = sp.Matrix(sp.symbols("z0:9"))
    full_zero = derivative(full, variables) * scaling
    parameterization = next(
        iter(sp.linsolve(list(full_zero), list(variables)))
    )
    assert all(
        sp.simplify(parameterization[index] - parameterization[0] * full[index])
        == 0
        for index in range(9)
    )

    pure = e(9, 0)
    mixed = e(9, 3) + e(9, 6)
    q_plane = sp.Matrix.hstack(e(9, 1), e(9, 3) - e(9, 6))
    assert derivative(pure, mixed) * q_plane == sp.zeros(27, 2)
    square = derivative(mixed, mixed) * q_plane
    assert square.rank() == 1
    assert [i for i, value in enumerate(square[:, 0]) if value] == [
        tidx(1, 0, 0)
    ]
    print("binary five-product chart: PASS (full / boundary source supports)")


def main() -> None:
    graph_contraction_injectivity()
    zero_row_correction_table()
    graph_row_profiles()
    tangent_line_separation()
    two_plane_square_pencil_atlas()
    binary_five_product_replay()
    print("rank-five support-one higher-row-rank exclusion: PASS")


if __name__ == "__main__":
    main()
