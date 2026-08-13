"""Exact replay for the rank-five support-two double-monomial exclusion."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def e(i: int) -> sp.Matrix:
    return sp.eye(3)[:, i]


def source(group: int, vector: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(9, 1)
    out[3 * group : 3 * group + 3, 0] = vector
    return out


def components(vector: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return vector[:3, :], vector[3:6, :], vector[6:9, :]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    forms = (components(u), components(v), components(q))
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            forms[sigma[0]][0],
            forms[sigma[1]][1],
            forms[sigma[2]][2],
        )
    return sp.simplify(out)


def alternating(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    forms = (components(u), components(v), components(w))
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        inversions = sum(
            sigma[i] > sigma[j] for i in range(3) for j in range(i + 1, 3)
        )
        out += (-1) ** inversions * tensor3(
            forms[sigma[0]][0],
            forms[sigma[1]][1],
            forms[sigma[2]][2],
        )
    return sp.simplify(out)


def mixed_map(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    columns = []
    for j in range(9):
        basis = sp.eye(9)[:, j]
        columns.append(polarized(u, v, basis))
    return sp.Matrix.hstack(*columns)


def pair(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(u, v)


def derivative(b23: sp.Matrix, b13: sp.Matrix) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for i in range(3):
        columns.append(sp.kronecker_product(e(i), b23))
    for j in range(3):
        column = sp.zeros(27, 1)
        for i in range(3):
            for k in range(3):
                column[9 * i + 3 * j + k] = b13[3 * i + k]
        columns.append(column)
    columns.extend(sp.zeros(27, 1) for _ in range(3))
    return sp.Matrix.hstack(*columns)


def canonical_root_plane() -> None:
    b23 = pair(e(0), e(0))
    b13 = pair(e(1), e(1))
    dmat = derivative(b23, b13)

    p0 = sp.Matrix.vstack(e(0), sp.zeros(3, 1), sp.zeros(3, 1))
    p1 = sp.Matrix.vstack(sp.zeros(3, 1), e(1), sp.zeros(3, 1))
    p2 = sp.Matrix.vstack(e(2), e(2), sp.zeros(3, 1))
    n0 = sp.Matrix.vstack(sp.zeros(6, 1), e(0) - e(1))
    n1 = sp.Matrix.vstack(sp.zeros(6, 1), e(2))
    h_image = sp.Matrix.hstack(p0, p1, p2, n0, n1)

    assert dmat.rank() == 6
    assert h_image.rank() == 5
    assert (dmat * h_image).rank() == 3
    assert h_image[:6, :].rank() == 3
    assert h_image[6:9, :].rank() == 2

    u_columns = [dmat * column for column in (p0, p1, p2)]
    assert sp.Matrix.hstack(*u_columns).rank() == 3
    expected = [
        tensor3(e(0), e(0), e(0)),
        tensor3(e(1), e(1), e(1)),
        tensor3(e(2), e(0), e(0)) + tensor3(e(1), e(2), e(1)),
    ]
    assert u_columns == expected
    print("canonical support-two (2,2) plane: PASS (rank 5 -> singleton span 3)")


def two_source_cases() -> None:
    x = source(0, e(0))
    y = source(1, e(0))
    t = source(2, e(0))
    v2 = x + y
    w = x - y

    # Nonconjugate kernel vector: the common mixed-zero space is one line.
    q0 = source(0, e(1))
    q1 = t
    common = mixed_map(v2, q0).col_join(mixed_map(v2, q1))
    nullspace = common.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(*nullspace, w).rank() == 1

    # Conjugate q0 with a nonzero tangent term: a two-plane results, but it
    # contains q0 itself and therefore cannot be disjoint from V if both
    # singleton rows span it.
    q0 = w
    d = source(0, e(1))
    q1 = d + t
    common = mixed_map(v2, q0).col_join(mixed_map(v2, q1))
    nullspace = common.nullspace()
    s = -d + t
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(*nullspace, w, s).rank() == 2

    # Fully conjugate case.  Replay the two vector equations and the
    # alternating determinant formula symbolically.
    a0, a1 = sp.symbols("a0 a1")
    z00, z01, z02, z10, z11, z12 = sp.symbols(
        "z00 z01 z02 z10 z11 z12"
    )
    z0 = source(2, sp.Matrix([z00, z01, z02]))
    z1 = source(2, sp.Matrix([z10, z11, z12]))
    u0 = a0 * w + z0
    u1 = a1 * w + z1
    expected_w = -2 * tensor3(
        e(0), e(0), a0 * sp.Matrix([z10, z11, z12]) + a1 * sp.Matrix([z00, z01, z02])
    )
    expected_t = -2 * a0 * a1 * tensor3(e(0), e(0), e(0))
    expected_alt = 2 * tensor3(
        e(0), e(0), a1 * sp.Matrix([z00, z01, z02]) - a0 * sp.Matrix([z10, z11, z12])
    )
    assert polarized(u0, u1, w) == expected_w
    assert polarized(u0, u1, t) == expected_t
    assert alternating(u0, u1, v2) == expected_alt
    print("two-source mixed-product atlas: PASS (line / intersecting plane / conjugate)")


def three_source_cases() -> None:
    x = source(0, e(0))
    y = source(1, e(0))
    z = source(2, e(0))
    v2 = x + y + z

    # All three scaling coefficients are nonzero.  The two common zero
    # divisors and v2 have scalar rows in one plane, so their alternating
    # separated tensor vanishes.
    l0, m0, l1, m1 = sp.symbols("l0 m0 l1 m1")
    u0 = l0 * x + m0 * y + (l0 + m0) * z / 2
    u1 = l1 * x + m1 * y + (l1 + m1) * z / 2
    q0 = x + y - 2 * z
    assert polarized(u0, v2, q0) == sp.zeros(27, 1)
    assert polarized(u1, v2, q0) == sp.zeros(27, 1)
    assert alternating(u0, u1, v2) == sp.zeros(27, 1)

    # One zero scaling coefficient and a target line independent of z.
    q0 = y - z
    q1 = source(2, e(1))
    common = mixed_map(v2, q0).col_join(mixed_map(v2, q1))
    assert len(common.nullspace()) == 1

    # Exceptional proportional target line: the entire common zero-divisor
    # space is the pure source X, whose alternating tensor is zero.
    q1 = x - y + z
    common = mixed_map(v2, q0).col_join(mixed_map(v2, q1))
    nullspace = common.nullspace()
    assert len(nullspace) == 3
    pure_x = sp.Matrix.hstack(source(0, e(0)), source(0, e(1)), source(0, e(2)))
    assert sp.Matrix.hstack(*nullspace, pure_x).rank() == 3
    assert alternating(source(0, e(1)), source(0, e(2)), v2) == sp.zeros(27, 1)
    print("three-source tangent atlas: PASS (scaling plane / line / pure-source exception)")


def sharp_rank_drop_fixture() -> None:
    x2 = source(0, e(2))
    y2 = source(1, e(2))
    z0 = source(2, e(0))
    z1 = source(2, e(1))
    z2 = source(2, e(2))

    v0 = z1
    v1 = z0
    v2 = x2 + y2
    q0 = x2 - y2
    q2 = z2 / 2
    q_plane = [q0, q2]

    assert sp.Matrix.hstack(v0, v1, v2, q0, q2).rank() == 5
    for left, right in ((v0, v1), (v0, v2), (v1, v2)):
        assert all(polarized(left, right, q) == sp.zeros(27, 1) for q in q_plane)
    assert polarized(v2, v2, q0) == sp.zeros(27, 1)
    assert polarized(v2, v2, q2) == tensor3(e(2), e(2), e(2))
    assert alternating(v0, v1, v2) == sp.zeros(27, 1)

    # Reconstruct every root coefficient of the empty permanent.
    root_1 = [v0, sp.zeros(9, 1), v2]
    root_2 = [sp.zeros(9, 1), v1, v2]
    root_3 = [q0, -q0, q2]
    empty = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                empty.append(polarized(root_1[a], root_2[b], root_3[c]))
    nonzero = [index for index, coefficient in enumerate(empty) if coefficient != sp.zeros(27, 1)]
    assert nonzero == [26]
    assert empty[26] == tensor3(e(2), e(2), e(2))

    # P-coordinate singleton rows: X and Y have the same image line.
    x_row = sp.Matrix([0, 0, 1])
    y_row = sp.Matrix([0, 0, 1])
    z_row_0 = sp.Matrix([0, 1, 0])
    z_row_1 = sp.Matrix([1, 0, 0])
    assert sp.Matrix.hstack(x_row, y_row, z_row_0).rank() == 2
    assert sp.Matrix.hstack(x_row, y_row, z_row_1).rank() == 2
    print("sharp rank-drop fixture: PASS (joint rank 5, target table, singleton rank <=2)")


def main() -> None:
    canonical_root_plane()
    two_source_cases()
    three_source_cases()
    sharp_rank_drop_fixture()
    print("rank-five support-two double-monomial exclusion: PASS")


if __name__ == "__main__":
    main()
