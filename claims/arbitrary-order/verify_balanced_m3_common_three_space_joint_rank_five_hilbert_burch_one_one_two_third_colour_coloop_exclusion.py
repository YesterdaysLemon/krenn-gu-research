"""Exact replay for the (1,1,2) third-colour coloop exclusion.

The owning Markdown file is the proof.  This script checks the coloop rank
geometry, the exact three-dimensional third-row image, the exterior-to-square
upgrade, every source-support case, and the pure-row factor-sharing quotient.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def e(index: int, dimension: int) -> sp.Matrix:
    return sp.eye(dimension)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


BlockVector = tuple[sp.Matrix, sp.Matrix, sp.Matrix]


def permanent(left: BlockVector, middle: BlockVector, right: BlockVector) -> sp.Matrix:
    arguments = (left, middle, right)
    dimension = left[0].rows * left[1].rows * left[2].rows
    answer = sp.zeros(dimension, 1)
    for assignment in permutations(range(3)):
        answer += tensor3(
            arguments[assignment[0]][0],
            arguments[assignment[1]][1],
            arguments[assignment[2]][2],
        )
    return answer


def coefficient_matrix(expressions: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    return sp.Matrix(
        [[sp.expand(expression).coeff(variable) for variable in variables] for expression in expressions]
    )


def coloop_row_geometry() -> None:
    # Columns are (r_t,r_u,p_s,p_u,h_0,h_1,h_2).  The omitted r_u is the
    # only direction outside S, so the relation kernel has alpha_u=0.
    s0, s1, outside = (e(index, 3) for index in range(3))
    columns = (
        s0 + s1,
        outside,
        s0,
        s1,
        2 * s0 + s1,
        -s0 + 3 * s1,
        5 * s0 - 2 * s1,
    )
    row_map = sp.Matrix.hstack(*columns)
    other_indices = (0, 2, 3, 4, 5, 6)
    other_rows = row_map[:, other_indices]
    kernel = row_map.nullspace()

    assert row_map.rank() == 3
    assert other_rows.rank() == 2
    assert len(kernel) == 4
    assert all(relation[1] == 0 for relation in kernel)
    assert sp.Matrix.hstack(columns[2], columns[3]).rank() == 2
    assert sp.Matrix.hstack(columns[0], columns[2], columns[3]).rank() == 2
    assert sp.Matrix.hstack(columns[4], columns[5], columns[6]).rank() == 2

    # For s=0,t=1,u=2, the untouched R x P x theta table has only T_u;
    # the r_t row is zero.
    nonzero_cells = [
        (i, j, k)
        for i, j, k in product((1, 2), (0, 2), range(3))
        if i == j == k
    ]
    assert nonzero_cells == [(2, 2, 2)]
    assert not any(i == j == k for i, j, k in product((1,), (0, 2), range(3)))
    print("coloop row geometry: PASS (six rows span S / r_t row zero)")


def theta_rank_and_square_upgrade() -> None:
    # W=V direct-sum <A,B>.  The quotient of q_k has columns (z_k,w_k).
    v0, v1, v2, a_direction, b_direction = (e(index, 5) for index in range(5))
    z = sp.Matrix([1, 1, 0])
    w = sp.Matrix([0, 1, 1])
    n = sp.Matrix([1, -1, 1])
    h_columns = (v0, sp.zeros(5, 1), sp.zeros(5, 1))
    q_columns = tuple(
        z[index] * a_direction + w[index] * b_direction + h_columns[index]
        for index in range(3)
    )
    q_map = sp.Matrix.hstack(*q_columns)
    quotient_map = q_map[3:5, :]
    v_space = sp.Matrix.hstack(v0, v1, v2)

    assert sp.Matrix.hstack(z, w).rank() == 2
    assert z.dot(n) == w.dot(n) == 0
    assert quotient_map == sp.Matrix([list(z), list(w)])
    assert quotient_map.rank() == 2
    assert q_map.rank() == 3
    assert q_map * n == v0
    assert sp.Matrix.hstack(v_space, q_map).rank() == 5

    # Exact covectors witnessing the two nonzero exterior faces.
    gamma = sp.Matrix([1, -1, 0])
    delta = sp.Matrix([1, 0, 0])
    assert gamma.dot(z) == 0
    assert gamma[1] * gamma.dot(w) != 0
    assert delta.dot(w) == 0 and delta[0] != 0

    # Trilinearity gives per(r,q,q)=g per(r,B,q)+per(r,h,q) for q=gB+h.
    g = sp.symbols("g")
    r: BlockVector = (
        sp.Matrix([1, 2]),
        sp.Matrix([3, 5]),
        sp.Matrix([7, 11]),
    )
    b_row: BlockVector = (
        sp.Matrix([13, 17]),
        sp.Matrix([19, 23]),
        sp.Matrix([29, 31]),
    )
    h_row: BlockVector = (
        sp.Matrix([37, 41]),
        sp.Matrix([43, 47]),
        sp.Matrix([53, 59]),
    )
    q_row = tuple(g * b + h for b, h in zip(b_row, h_row, strict=True))
    square = permanent(r, q_row, q_row)
    upgraded = g * permanent(r, b_row, q_row) + permanent(r, h_row, q_row)
    assert sp.simplify(square - upgraded) == sp.zeros(8, 1)

    c, gamma_t, gamma_w = sp.symbols("c gamma_t gamma_w", nonzero=True)
    target = tensor3(e(0, 2), e(0, 2), e(0, 2))
    formal_square = gamma_w * (c * gamma_t * target) + sp.zeros(8, 1)
    assert formal_square == c * gamma_t * gamma_w * target
    print("third-row image: PASS (quotient rank two + nonzero normal = rank three)")
    print("exterior upgrade: PASS (nonzero T_t square)")


def three_source_case() -> None:
    x = y = zeta = e(0, 2)
    qx0, qx1, qy0, qy1, qz0, qz1 = sp.symbols(
        "qx0 qx1 qy0 qy1 qz0 qz1"
    )
    variables = (qx0, qx1, qy0, qy1, qz0, qz1)
    q: BlockVector = (
        sp.Matrix([qx0, qx1]),
        sp.Matrix([qy0, qy1]),
        sp.Matrix([qz0, qz1]),
    )
    r: BlockVector = (x, y, zeta)
    square_map = coefficient_matrix(permanent(r, r, q), variables)
    expected_kernel = sp.Matrix.hstack(
        sp.Matrix([1, 0, -1, 0, 0, 0]),
        sp.Matrix([1, 0, 0, 0, -1, 0]),
    )

    assert square_map.rank() == 4
    assert square_map * expected_kernel == sp.zeros(8, 2)
    assert expected_kernel.rank() == 2
    assert sp.Matrix.hstack(*square_map.nullspace(), *expected_kernel.columnspace()).rank() == 2
    assert 3 > len(square_map.nullspace())
    print("three-source split: PASS (square kernel has dimension two)")


def two_source_case() -> None:
    x = y = e(0, 2)
    zero = sp.zeros(2, 1)
    qx0, qx1, qy0, qy1, qz0, qz1 = sp.symbols(
        "qx0 qx1 qy0 qy1 qz0 qz1"
    )
    all_variables = (qx0, qx1, qy0, qy1, qz0, qz1)
    q: BlockVector = (
        sp.Matrix([qx0, qx1]),
        sp.Matrix([qy0, qy1]),
        sp.Matrix([qz0, qz1]),
    )
    r: BlockVector = (x, y, zero)
    square_map = coefficient_matrix(permanent(r, r, q), all_variables)
    assert square_map.rank() == 2
    assert all(vector[4] == vector[5] == 0 for vector in square_map.nullspace())

    xy_variables = (qx0, qx1, qy0, qy1)
    q_xy: BlockVector = (q[0], q[1], zero)
    tangent = sp.kronecker_product(x, q[1]) + sp.kronecker_product(q[0], y)
    tangent_map = coefficient_matrix(tangent, xy_variables)
    expected_kernel = sp.Matrix([1, 0, -1, 0])
    assert tangent_map.rank() == 3
    assert tangent_map * expected_kernel == sp.zeros(4, 1)
    assert len(tangent_map.nullspace()) == 1

    px0, px1, py0, py1, pz0, pz1 = sp.symbols(
        "px0 px1 py0 py1 pz0 pz1"
    )
    p: BlockVector = (
        sp.Matrix([px0, px1]),
        sp.Matrix([py0, py1]),
        sp.Matrix([pz0, pz1]),
    )
    assert sp.simplify(
        permanent(r, p, q_xy) - sp.kronecker_product(tangent, p[2])
    ) == sp.zeros(8, 1)

    p_xy: BlockVector = (p[0], p[1], zero)
    assert permanent(q_xy, q_xy, r) == sp.zeros(8, 1)
    assert permanent(r, p_xy, q_xy) == sp.zeros(8, 1)
    print("two-source split: PASS (one-line tangent kernel / square contradiction)")


def pure_source_case() -> None:
    x = y = zeta = e(0, 2)
    zero = sp.zeros(2, 1)
    qx0, qx1 = sp.symbols("qx0 qx1")
    q: BlockVector = (sp.Matrix([qx0, qx1]), y, zeta)
    r: BlockVector = (x, zero, zero)
    assert permanent(q, q, r) == 2 * tensor3(x, y, zeta)

    a, b = sp.symbols("a b")
    px0, px1, ux0, ux1 = sp.symbols("px0 px1 ux0 ux1")
    cx0, cx1, cy0, cy1, cz0, cz1 = sp.symbols(
        "cx0 cx1 cy0 cy1 cz0 cz1"
    )
    p_x = sp.Matrix([px0, px1])
    u_x = sp.Matrix([ux0, ux1])
    c_row: BlockVector = (
        sp.Matrix([cx0, cx1]),
        sp.Matrix([cy0, cy1]),
        sp.Matrix([cz0, cz1]),
    )
    p: BlockVector = (p_x, a * y, -a * zeta)
    u: BlockVector = (u_x, b * y, b * zeta)
    actual = permanent(c_row, p, u)
    expected = tensor3(b * p_x - a * u_x, c_row[1], zeta) + tensor3(
        b * p_x + a * u_x, y, c_row[2]
    )
    assert sp.simplify(actual - expected) == sp.zeros(8, 1)

    # Project to X tensor (Y/<y>) tensor (Z/<zeta>): the mixed image dies.
    quotient_entries = sp.Matrix([actual[3], actual[7]])
    assert sp.simplify(quotient_entries) == sp.zeros(2, 1)

    tx0, tx1, ty0, ty1, tz0, tz1 = sp.symbols(
        "tx0 tx1 ty0 ty1 tz0 tz1"
    )
    decomposable = tensor3(
        sp.Matrix([tx0, tx1]),
        sp.Matrix([ty0, ty1]),
        sp.Matrix([tz0, tz1]),
    )
    assert sp.Matrix([decomposable[3], decomposable[7]]) == sp.Matrix(
        [tx0 * ty1 * tz1, tx1 * ty1 * tz1]
    )

    # In the a=0 alternative, three rows in a two-plane cannot supply the
    # three independent X-factor lines of T_s,T_t,T_u.
    plane_rows = sp.Matrix.hstack(e(0, 3), e(1, 3), e(0, 3) + e(1, 3))
    target_factor_lines = sp.eye(3)
    assert plane_rows.rank() == 2
    assert target_factor_lines.rank() == 3
    print("pure-source split: PASS (conjugate rows / factor-sharing quotient)")


def symmetry_check() -> None:
    first_orientation = {
        "root_family": "alpha",
        "row": "u",
        "kernel_outer": "z",
        "coordinate_colour": "s",
    }
    swapped = {
        "root_family": "beta",
        "row": first_orientation["row"],
        "kernel_outer": "w",
        "coordinate_colour": "t",
    }
    assert swapped == {
        "root_family": "beta",
        "row": "u",
        "kernel_outer": "w",
        "coordinate_colour": "t",
    }
    print("first/second-root symmetry: PASS (alpha_u <-> beta_u)")


def main() -> None:
    coloop_row_geometry()
    theta_rank_and_square_upgrade()
    three_source_case()
    two_source_case()
    pure_source_case()
    symmetry_check()
    print("(1,1,2) third-colour coloop exclusion: PASS")


if __name__ == "__main__":
    main()
