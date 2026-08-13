"""Exact replay for the source-aligned exceptional-root-row obstruction."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def mixed_product_matrix(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    """Return p=(v,w) -> v tensor y + x tensor w."""
    out = sp.zeros(9, 6)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j, i] = y[j]
        out[3 * i + j, 3 + j] = x[i]
    return out


def check_zero_divisor_dimensions() -> None:
    e0 = sp.Matrix([1, 0, 0])
    zero = sp.zeros(3, 1)

    pure_v = mixed_product_matrix(e0, zero)
    pure_w = mixed_product_matrix(zero, e0)
    mixed = mixed_product_matrix(e0, e0)

    assert pure_v.rank() == 3 and len(pure_v.nullspace()) == 3
    assert pure_w.rank() == 3 and len(pure_w.nullspace()) == 3
    assert mixed.rank() == 5 and len(mixed.nullspace()) == 1
    assert mixed.nullspace()[0] == sp.Matrix([-1, 0, 0, 1, 0, 0])
    print("mixed-product zero divisors: PASS (pure nullity 3; mixed nullity 1)")


def check_pigeonhole_patterns() -> None:
    # A pure V vector q has Z(q)=V; a pure W vector has Z(q)=W.
    # For every assignment of the three q_j to V/W, compute the allowed
    # summand for p_i after imposing m(p_i,q_j)=0 for j != i.
    checked = 0
    for q_types in product(("V", "W"), repeat=3):
        allowed: list[str] = []
        for i in range(3):
            constraints = {q_types[j] for j in range(3) if j != i}
            allowed.append(next(iter(constraints)) if len(constraints) == 1 else "0")

        if len(set(q_types)) == 1:
            # All six q_j and possible p_i occupy the same 3-space.
            assert allowed == [q_types[0]] * 3
        else:
            # Two p_i are forced to zero and the third into the majority block.
            assert allowed.count("0") == 2
        checked += 1
    assert checked == 8
    print("three-vector purity patterns: PASS (8/8 incompatible with a 6-basis)")


def check_sparse_support_reduction() -> None:
    # With exceptional line A_1 tensor e_s tensor e_s, every output row whose
    # root-2 and root-3 colours differ is forbidden, for every root-1 colour.
    for s in range(3):
        allowed = {(a, s, s) for a in range(3)} | {
            (c, c, c) for c in range(3)
        }
        off_diagonal = {
            (a, b, c)
            for a, b, c in product(range(3), repeat=3)
            if b != c
        }
        assert len(allowed) == 5
        assert len(off_diagonal) == 18
        assert allowed.isdisjoint(off_diagonal)
    print("GHZ-plus-root-line off-diagonal grid: PASS (18 forbidden rows)")


def check_aligned_block_permanent_identity() -> None:
    # Root 1 is aligned with source X.  Its row r has no Y/Z component, so
    # the (r,p,q) block-permanent row is r tensor (p_Y q_Z + q_Y p_Z).
    values = [sp.Rational(((23 * k + 5) % 17) - 8) for k in range(54)]
    p = [sp.Matrix(3, 3, values[9 * u : 9 * (u + 1)]) for u in range(3)]
    q = [
        sp.Matrix(3, 3, values[27 + 9 * u : 27 + 9 * (u + 1)])
        for u in range(3)
    ]
    root_one = [sp.zeros(3), sp.zeros(3), sp.zeros(3)]
    root_one[0] = sp.diag(2, -3, 5)

    checked = 0
    for a, b, c, x, y, z in product(range(3), repeat=6):
        source_colours = (x, y, z)
        direct = sum(
            root_one[sigma[0]][a, source_colours[sigma[0]]]
            * p[sigma[1]][b, source_colours[sigma[1]]]
            * q[sigma[2]][c, source_colours[sigma[2]]]
            for sigma in permutations(range(3))
        )
        mixed = root_one[0][a, x] * (
            p[1][b, y] * q[2][c, z] + q[1][c, y] * p[2][b, z]
        )
        assert direct == mixed
        checked += 1
    assert checked == 729
    print("aligned block-permanent/mixed-product identity: PASS (729/729)")


def main() -> None:
    check_zero_divisor_dimensions()
    check_pigeonhole_patterns()
    check_sparse_support_reduction()
    check_aligned_block_permanent_identity()
    print("source-aligned exceptional-root-row obstruction: PASS")


if __name__ == "__main__":
    main()
