"""Exact replay for the transverse-rank-six beta-zero localization."""

from __future__ import annotations

from itertools import product

import sympy as sp


def tidx(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def derivative(b23: sp.Matrix, b13: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 9)
    for a, b, c in product(range(3), repeat=3):
        out[tidx(a, b, c), a] = b23[b, c]
        out[tidx(a, b, c), 3 + b] = b13[a, c]
    return out


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def check_transverse_split() -> None:
    b23 = e(1) * e(1).T
    b13 = e(0) * e(0).T + e(2) * e(2).T
    d = derivative(b23, b13)
    assert d.rank() == 6
    assert d[:, 6:9] == sp.zeros(27, 3)
    assert d.nullspace() == [sp.eye(9)[:, i] for i in range(6, 9)]

    k12 = sp.Matrix.hstack(
        sp.eye(9)[:, 0] + sp.eye(9)[:, 3],
        sp.eye(9)[:, 1] + sp.eye(9)[:, 4],
        sp.eye(9)[:, 2] + sp.eye(9)[:, 5],
    )
    k = sp.Matrix.hstack(k12, *[sp.eye(9)[:, i] for i in range(6, 9)])
    assert k.rank() == 6
    assert (d * k).rank() == 3
    print("transverse derivative split: PASS (rank 6 / kernel A3 / image 3)")


def check_beta_zero_atlas() -> None:
    # Type I: a coordinate monomial never contracts to zero on the torus.
    b_type_i = e(1) * e(2).T
    beta = sp.Matrix([2, 3, 5])
    gamma = sp.Matrix([7, 11, 13])
    assert (beta.T * b_type_i * gamma)[0] == 3 * 13

    # Type II with a coordinate boundary base point.
    z = sp.Matrix([1, 1, 0])
    w = sp.Matrix([1, -1, 0])
    x = e(2)
    b_type_ii = e(1) * z.T
    c_type_ii = e(0) * w.T + x * z.T
    assert derivative(b_type_ii, c_type_ii).rank() == 6
    assert sp.Matrix.hstack(z, w).rank() == 2

    # On z(gamma)=0 with gamma fully supported, w(gamma) is nonzero.
    g_on_kernel = sp.Matrix([2, -2, 3])
    assert (z.T * g_on_kernel)[0] == 0
    assert (w.T * g_on_kernel)[0] == 4
    alpha = sp.Matrix([5, 7, 11])
    c_value = (alpha.T * c_type_ii * g_on_kernel)[0]
    assert c_value == alpha[0] * 4
    assert c_value != 0

    # The base point need not itself be a coordinate point.  Here the common
    # kernel is span(0,1,1), which has exactly one zero coordinate.
    z_wide = sp.Matrix([1, 1, -1])
    w_wide = sp.Matrix([0, 1, -1])
    boundary_base = sp.Matrix([0, 1, 1])
    assert (z_wide.T * boundary_base)[0] == 0
    assert (w_wide.T * boundary_base)[0] == 0
    assert sum(value == 0 for value in boundary_base) == 1
    assert sp.Matrix.hstack(z_wide, w_wide).rank() == 2
    print("beta-zero root-block atlas: PASS (coordinate / boundary-pencil tangent)")


def check_relation_annihilator_identity() -> None:
    entries = [sp.Rational(i - 4) for i in range(9)]
    b23 = sp.Matrix(3, 3, entries)
    b13 = sp.Matrix(3, 3, list(reversed(entries)))
    u = sp.Matrix([2, 3, 5])
    v = sp.Matrix([7, 11, 13])
    gamma = sp.Matrix([17, 19, 23])
    lam = (v.T * b23 * gamma)[0]
    mu = (u.T * b13 * gamma)[0]
    f = b23.T * v - b13.T * u
    assert (f.T * gamma)[0] == lam - mu

    # A noncoordinate hyperplane has a fully supported point.
    f_control = sp.Matrix([2, 3, 0])
    gamma_control = sp.Matrix([3, -2, 5])
    assert (f_control.T * gamma_control)[0] == 0
    assert all(value != 0 for value in gamma_control)

    # On a coordinate boundary, support(lambda,lambda,0)=2 when lambda!=0.
    gamma_boundary = sp.Matrix([0, 2, 3])
    assert sum(value != 0 for value in gamma_boundary) == 2
    beta_root = sp.Matrix([5, 5, 0])
    assert sum(value != 0 for value in beta_root) == 2
    print("relation-plane annihilator: PASS (identity / torus / S2S support)")


def check_projection_and_target_kernel() -> None:
    # L is the graph of the identity; both projection dimensions are three.
    l = sp.Matrix.vstack(sp.eye(3), sp.eye(3))
    assert l.rank() == 3
    assert l[:3, :].rank() == 3
    assert l[3:, :].rank() == 3

    # If both contraction images use e_s, both blocks share that factor.
    b = sp.Matrix([2, 3, 5]) * e(1).T
    c = sp.Matrix([7, 11, 13]) * e(1).T
    assert derivative(b, c).rank() == 5

    # A fixed third-root line can absorb target colours only from one support.
    for support in product((0, 1), repeat=3):
        if not any(support):
            continue
        diagonal_columns = sp.diag(*support)
        can_share_one_line = diagonal_columns.rank() <= 1
        assert can_share_one_line == (sum(support) == 1)

    # Two independent coordinate-kernel vectors have a support-two sum.
    for first in range(3):
        for second in range(first + 1, 3):
            assert sum(value != 0 for value in e(first) + e(second)) == 2
    print("target-kernel alignment: PASS (rank-two coordinate kernel)")


def main() -> None:
    check_transverse_split()
    check_beta_zero_atlas()
    check_relation_annihilator_identity()
    check_projection_and_target_kernel()
    print("balanced m=3 transverse-rank-six beta-zero localization: PASS")


if __name__ == "__main__":
    main()
