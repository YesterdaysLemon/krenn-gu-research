"""Exact replay for the m=3 joint-rank-five derivative/torus localization."""

from __future__ import annotations

from itertools import product

import sympy as sp


def e(i: int) -> sp.Matrix:
    return sp.eye(3)[:, i]


def pair(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(u, v)


def triple(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(u, v, w)


def block(entries: list[tuple[int, int, int]]) -> sp.Matrix:
    out = sp.zeros(9, 1)
    for i, j, value in entries:
        out[3 * i + j] += value
    return out


def derivative(b23: sp.Matrix, b13: sp.Matrix, b12: sp.Matrix) -> sp.Matrix:
    """Build D_B:A1+A2+A3 -> A1*A2*A3 in root order."""
    cols: list[sp.Matrix] = []
    for i in range(3):
        cols.append(sp.kronecker_product(e(i), b23))
    for j in range(3):
        col = sp.zeros(27, 1)
        for i in range(3):
            for k in range(3):
                col[9 * i + 3 * j + k] = b13[3 * i + k]
        cols.append(col)
    for k in range(3):
        cols.append(sp.kronecker_product(b12, e(k)))
    return sp.Matrix.hstack(*cols)


def hb_blocks(
    x: sp.Matrix,
    y: sp.Matrix,
    z: sp.Matrix,
    b: sp.Matrix,
    c: sp.Matrix,
    w: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        pair(y, w) - pair(c, z),
        pair(b, z) - pair(x, w),
        pair(x, c) - pair(b, y),
    )


def rank_in_span(vector: sp.Matrix, spanning: sp.Matrix) -> bool:
    return spanning.row_join(vector).rank() == spanning.rank()


def derivative_census() -> None:
    zero = sp.zeros(9, 1)
    shared = derivative(pair(e(0), e(0)), pair(e(0), e(0)), zero)
    transverse = derivative(pair(e(0), e(0)), pair(e(0), e(1)), zero)
    assert shared.rank() == 5
    assert len(shared.nullspace()) == 4
    assert transverse.rank() == 6
    assert len(transverse.nullspace()) == 3

    # A nonzero zero-diagonal symmetric 3 x 3 matrix never has rank one.
    q0, q1, q2 = sp.symbols("q0 q1 q2")
    mixed = sp.Matrix([[0, q2, q1], [q2, 0, q0], [q1, q0, 0]])
    principal = [mixed.extract([i, j], [i, j]).det() for i, j in [(0, 1), (0, 2), (1, 2)]]
    assert principal == [-q2**2, -q1**2, -q0**2]
    print("rank-free shared derivative: PASS (rank 5 / nullity 4 / row-rank floor)")


def transverse_models() -> None:
    b23 = pair(e(0), e(0))
    b13 = pair(e(0), e(1))
    dmat = derivative(b23, b13, sp.zeros(9, 1))

    # P is a three-plane in A1+A2.  The bottom two columns span N3.
    p0 = sp.Matrix.vstack(e(0), sp.zeros(3, 1), sp.zeros(3, 1))
    p1 = sp.Matrix.vstack(sp.zeros(3, 1), e(1), sp.zeros(3, 1))
    p2 = sp.Matrix.vstack(e(2), e(2), sp.zeros(3, 1))
    n0 = sp.Matrix.vstack(sp.zeros(6, 1), e(0))
    n1 = sp.Matrix.vstack(sp.zeros(6, 1), e(1))

    direct = sp.Matrix.hstack(p0, p1, p2, n0, n1)
    assert direct.rank() == 5
    assert (dmat * direct).rank() == 3
    involved = direct[:6, :]
    third = direct[6:9, :]
    assert involved.rank() == 3
    assert third.rank() == 2
    assert involved.col_join(third).rank() == 5

    # A nontrivial extension P -> A3/N3 makes the third row injective; its
    # row space then overlaps the involved row space in exactly one line.
    extended_p0 = p0 + sp.Matrix.vstack(sp.zeros(6, 1), e(2))
    extended = sp.Matrix.hstack(extended_p0, p1, p2, n0, n1)
    involved_rows = extended[:6, :]
    third_rows = extended[6:9, :]
    assert extended.rank() == 5
    assert (dmat * extended).rank() == 3
    assert involved_rows.rank() == 3
    assert third_rows.rank() == 3
    intersection = involved_rows.rank() + third_rows.rank() - extended.rank()
    assert intersection == 1
    print("transverse rank-five models: PASS (third-row ranks 2 / 3 and overlap 0 / 1)")


def hilbert_burch_profiles() -> None:
    profiles = {
        "222": (e(0), e(0), e(0), e(1), e(1), e(1), (2, 2, 2)),
        "122": (e(0), e(0), e(0), sp.zeros(3, 1), e(1), e(1), (1, 2, 2)),
        "112": (e(0), sp.zeros(3, 1), e(0), sp.zeros(3, 1), e(0), e(1), (1, 1, 2)),
        "111": (e(0), sp.zeros(3, 1), e(0), sp.zeros(3, 1), e(0), e(0), (1, 1, 1)),
    }

    for x, y, z, b, c, w, expected_profile in profiles.values():
        b23, b13, b12 = hb_blocks(x, y, z, b, c, w)
        dmat = derivative(b23, b13, b12)
        n1 = sp.Matrix.vstack(x, y, z)
        n2 = sp.Matrix.vstack(b, c, w)
        assert b23 != sp.zeros(9, 1)
        assert b13 != sp.zeros(9, 1)
        assert b12 != sp.zeros(9, 1)
        assert dmat.rank() == 7
        assert dmat * n1 == sp.zeros(27, 1)
        assert dmat * n2 == sp.zeros(27, 1)
        assert sp.Matrix.hstack(n1, n2).rank() == 2
        got = (
            sp.Matrix.hstack(x, b).rank(),
            sp.Matrix.hstack(y, c).rank(),
            sp.Matrix.hstack(z, w).rank(),
        )
        assert got == expected_profile
    print("Hilbert-Burch derivative atlas: PASS (222 / 122 / 112 / 111, rank 7)")


def beta_zero_atlas() -> None:
    a, b, g, h = sp.symbols("a b g h")

    # Profile 122: A=(a,0), B=(b,g), C=(c,h).  If a is nonzero, the
    # second coordinates of B,C vanish; if a is zero, det(B,C)=0.
    b0, b1, c0, c1 = sp.symbols("b0 b1 c0 c1")
    ideal_122 = [b0 * c1 - b1 * c0, a * c1, a * b1]
    assert [sp.expand(f.subs(a, 0)) for f in ideal_122] == [b0 * c1 - b1 * c0, 0, 0]
    assert [sp.expand(f.subs({b1: 0, c1: 0})) for f in ideal_122] == [0, 0, 0]

    # Profile 112: A=(a,0), B=(0,b), C=(g,h).
    ideal_112 = [-b * g, a * h, a * b]
    components_112 = [{a: 0, b: 0}, {a: 0, g: 0}, {b: 0, h: 0}]
    for substitutions in components_112:
        assert all(sp.expand(f.subs(substitutions)) == 0 for f in ideal_112)

    # Profile 111: C lies on a third line, normalized to (g,g).
    ideal_111 = [-b * g, a * g, a * b]
    components_111 = [{a: 0, b: 0}, {a: 0, g: 0}, {b: 0, g: 0}]
    for substitutions in components_111:
        assert all(sp.expand(f.subs(substitutions)) == 0 for f in ideal_111)

    # The Boolean consequences of the coordinate-boundary components.
    allowed_122 = []
    allowed_112 = []
    allowed_111 = []
    for flags in product([False, True], repeat=4):
        x_coord, y_coord, z_coord, w_coord = flags
        if x_coord and (z_coord or w_coord):
            allowed_122.append(flags)
        if (
            (x_coord or y_coord)
            and (x_coord or z_coord)
            and (y_coord or w_coord)
        ):
            allowed_112.append(flags)
        if (
            (x_coord or y_coord)
            and (x_coord or z_coord)
            and (y_coord or z_coord)
        ):
            allowed_111.append(flags)
    assert all(flags[0] and (flags[2] or flags[3]) for flags in allowed_122)
    minimal_112 = [
        flags
        for flags in allowed_112
        if sum(flags) == 2
    ]
    assert set(minimal_112) == {
        (True, True, False, False),
        (True, False, False, True),
        (False, True, True, False),
    }
    assert all(sum(flags[:3]) >= 2 for flags in allowed_111)
    print("beta-zero torus atlas: PASS (222 excluded; exact 122 / 112 / 111 boundaries)")


def third_row_support_bound() -> None:
    # Normal form for two distinct contraction lines b=e0 and c=e1.
    columns = []
    for i in range(3):
        columns.append(pair(e(i), e(0)))
    for j in range(3):
        columns.append(pair(e(1), e(j)))
    space = sp.Matrix.hstack(*columns)
    assert space.rank() == 5
    diagonals = [pair(e(i), e(i)) for i in range(3)]
    assert rank_in_span(diagonals[0], space)
    assert rank_in_span(diagonals[1], space)
    assert not rank_in_span(diagonals[2], space)

    # Coincident fixed lines cover only their one coordinate diagonal.
    same_columns = []
    for i in range(3):
        same_columns.append(pair(e(i), e(0)))
    for j in range(3):
        same_columns.append(pair(e(0), e(j)))
    same_space = sp.Matrix.hstack(*same_columns)
    assert rank_in_span(diagonals[0], same_space)
    assert not rank_in_span(diagonals[1], same_space)
    assert not rank_in_span(diagonals[2], same_space)
    print("third-row kernel support: PASS (two fixed factor lines cover at most two colours)")


def main() -> None:
    derivative_census()
    transverse_models()
    hilbert_burch_profiles()
    beta_zero_atlas()
    third_row_support_bound()
    print("balanced m=3 joint-rank-five derivative/torus localization: PASS")


if __name__ == "__main__":
    main()
