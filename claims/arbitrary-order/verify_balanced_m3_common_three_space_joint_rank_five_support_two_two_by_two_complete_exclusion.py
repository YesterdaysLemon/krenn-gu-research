"""Exact replay for the rank-five support-two (2,2) complete exclusion."""

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
            sigma[i] > sigma[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        out += (-1) ** inversions * tensor3(
            forms[sigma[0]][0],
            forms[sigma[1]][1],
            forms[sigma[2]][2],
        )
    return sp.simplify(out)


def mixed_map(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(polarized(u, v, sp.eye(9)[:, j]) for j in range(9))
    )


def pair(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(u, v)


def place_13_2(c13: sp.Matrix, b2: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                out[9 * i + 3 * j + k] = c13[3 * i + k] * b2[j]
    return out


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


def embedded_pair(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(a, b, sp.zeros(3, 1))


def root_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def row(matrix: sp.Matrix, a: int, b: int, c: int) -> sp.Matrix:
    return matrix[root_index(a, b, c), :].T


def beta_zero_type_ii_collapse() -> None:
    z0, z1, z2 = sp.symbols("z0 z1 z2")
    kappa = sp.symbols("kappa", nonzero=True)
    z = sp.Matrix([z0, z1, z2])
    for coordinate_factor in range(3):
        block = sp.zeros(3, 3)
        block[coordinate_factor, :] = z.T
        for kernel_colour in range(3):
            difference = (
                block.row(kernel_colour).T - kappa * e(kernel_colour)
            )
            if kernel_colour != coordinate_factor:
                assert difference[kernel_colour] == -kappa
                continue
            solutions = sp.solve(
                list(difference), (z0, z1, z2), dict=True
            )
            expected = {
                z[index]: kappa if index == coordinate_factor else 0
                for index in range(3)
            }
            assert solutions == [expected]
    print("beta-zero Type-II collapse: PASS (coordinate factor -> monomial)")


def kernel_colour_planes() -> None:
    b23 = pair(e(0), e(0))
    xi = e(0) - e(1)
    a, b, g, d = sp.symbols("a b g d")
    c1 = (
        pair(e(1), e(1))
        + a * pair(e(0), xi)
        + b * pair(e(0), e(2))
        + g * pair(e(2), xi)
        + d * pair(e(2), e(2))
    )
    d1 = derivative(b23, c1)
    p10 = embedded_pair(e(0), sp.zeros(3, 1))
    p11 = embedded_pair(sp.zeros(3, 1), e(1))
    p12 = embedded_pair(e(2), e(2))
    image1 = [d1 * p for p in (p10, p11, p12)]
    assert image1 == [
        tensor3(e(0), e(0), e(0)),
        place_13_2(c1, e(1)),
        tensor3(e(2), e(0), e(0)) + place_13_2(c1, e(2)),
    ]

    # A concrete unrestricted nonmonomial representative remains transverse.
    c1_sample = c1.subs({a: 1, b: 2, g: 3, d: 5})
    assert derivative(b23, c1_sample).rank() == 6
    assert sp.Matrix.hstack(p10, p11, p12).rank() == 3

    # In the c=2 chart, row two of C is diagonal while C(eta) is e1.
    c2 = pair(e(1), e(0)) + pair(e(2), e(2))
    d2 = derivative(b23, c2)
    p20 = embedded_pair(e(0), sp.zeros(3, 1))
    p21 = embedded_pair(sp.zeros(3, 1), e(1))
    p22 = embedded_pair(e(1), e(2))
    image2 = [d2 * p for p in (p20, p21, p22)]
    assert image2 == [
        tensor3(e(0), e(0), e(0)),
        place_13_2(c2, e(1)),
        tensor3(e(1), e(0), e(0)) + place_13_2(c2, e(2)),
    ]
    assert d2.rank() == 6
    # The same singleton basis coefficient occurs nontrivially at E100 and
    # E222.  Both all-cross rows vanish, while only E222 has target T2.
    assert image2[2][root_index(1, 0, 0)] == 1
    assert image2[2][root_index(2, 2, 2)] == 1
    print("kernel-colour atlas: PASS (c=1 normal form / c=2 contradiction)")


def arbitrary_c_target_table() -> None:
    a, b, g, d, kappa = sp.symbols("a b g d kappa", nonzero=True)
    xi = e(0) - e(1)
    c13 = (
        kappa * pair(e(1), e(1))
        + a * pair(e(0), xi)
        + b * pair(e(0), e(2))
        + g * pair(e(2), xi)
        + d * pair(e(2), e(2))
    )
    u0 = tensor3(e(0), e(0), e(0))
    u1 = place_13_2(c13, e(1))
    targets = [tensor3(e(i), e(i), e(i)) for i in range(3)]

    target = sp.zeros(27, 27)
    for i in range(3):
        target[root_index(i, i, i), :] = targets[i].T
    # S0=-T0, S1=-T1/kappa, S2=0 are forced by the three zero rows.
    all_cross = target - u0 * targets[0].T - u1 * targets[1].T / kappa
    assert row(all_cross, 0, 0, 0) == sp.zeros(27, 1)
    assert row(all_cross, 2, 0, 0) == sp.zeros(27, 1)
    assert row(all_cross, 1, 1, 1) == sp.zeros(27, 1)

    for j in range(3):
        assert row(all_cross, 0, 2, j) == sp.zeros(27, 1)
        expected_square = targets[2] if j == 2 else sp.zeros(27, 1)
        assert row(all_cross, 2, 2, j) == expected_square
        assert row(all_cross, 0, 1, j) == -c13[3 * 0 + j] * targets[1] / kappa
        assert row(all_cross, 2, 1, j) == -c13[3 * 2 + j] * targets[1] / kappa

    # q0+q1=0 for eta=(1,1,0), and the arbitrary-C table respects it.
    assert row(all_cross, 0, 1, 0) + row(all_cross, 0, 1, 1) == sp.zeros(
        27, 1
    )
    assert row(all_cross, 2, 1, 0) + row(all_cross, 2, 1, 1) == sp.zeros(
        27, 1
    )
    print("full arbitrary-C target table: PASS (all 27 root coefficients retained)")


def transverse_line_forces_mixed_zero() -> None:
    symbols_u = sp.symbols("u0:9")
    symbols_q = sp.symbols("q0:9")
    u = sp.Matrix(symbols_u)
    q = sp.Matrix(symbols_q)
    x2 = source(0, e(2))
    y2 = source(1, e(2))
    target_1_index = root_index(1, 1, 1)

    # Two-source square: every mixed tensor contains x2 or y2.
    two_source = x2 + y2
    assert sp.expand(polarized(two_source, u, q)[target_1_index]) == 0

    # Three-source square whose decomposable image shares x2 and y2.
    z0, z1, z2 = sp.symbols("z0 z1 z2")
    qz0, qz1, qz2, qx, qy = sp.symbols("qz0 qz1 qz2 qx qy")
    three_source = x2 + y2 + source(2, sp.Matrix([z0, z1, z2]))
    tangent_q = (
        qx * x2
        + qy * y2
        + source(2, sp.Matrix([qz0, qz1, qz2]))
    )
    assert sp.expand(polarized(three_source, u, tangent_q)[target_1_index]) == 0
    print("fully transverse line: PASS (apparent T1 corrections force zero)")


def common_zero_atlas() -> None:
    x = source(0, e(2))
    y = source(1, e(2))
    t = source(2, e(2))
    v = x + y
    w = x - y

    # Nonconjugate square-kernel vector: one common-zero line.
    q0 = source(0, e(0))
    common = mixed_map(v, q0).col_join(mixed_map(v, t))
    nullspace = common.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(*nullspace, w).rank() == 1

    # Conjugate kernel with a nonzero tangent term: the common-zero plane
    # contains q0, so two independent singleton rows violate V cap Q=0.
    q0 = w
    d = source(0, e(0))
    q1 = d + t
    common = mixed_map(v, q0).col_join(mixed_map(v, q1))
    nullspace = common.nullspace()
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(*nullspace, w, -d + t).rank() == 2

    # Fully conjugate symbolic identities.  A fully transverse correction
    # cannot contain the displayed x2/y2 factor lines.
    alpha0, alpha1 = sp.symbols("alpha0 alpha1")
    z00, z01, z02, z10, z11, z12 = sp.symbols(
        "z00 z01 z02 z10 z11 z12"
    )
    z_0 = source(2, sp.Matrix([z00, z01, z02]))
    z_1 = source(2, sp.Matrix([z10, z11, z12]))
    u0 = alpha0 * w + z_0
    u1 = alpha1 * w + z_1
    expected_w = -2 * tensor3(
        e(2),
        e(2),
        alpha0 * sp.Matrix([z10, z11, z12])
        + alpha1 * sp.Matrix([z00, z01, z02]),
    )
    expected_t = -2 * alpha0 * alpha1 * tensor3(e(2), e(2), e(2))
    expected_alt = 2 * tensor3(
        e(2),
        e(2),
        alpha1 * sp.Matrix([z00, z01, z02])
        - alpha0 * sp.Matrix([z10, z11, z12]),
    )
    assert polarized(u0, u1, w) == expected_w
    assert polarized(u0, u1, t) == expected_t
    assert alternating(u0, u1, v) == expected_alt

    # Three-source scaling and zero-coefficient charts.
    z = source(2, e(0))
    v3 = x + y + z
    l0, m0, l1, m1 = sp.symbols("l0 m0 l1 m1")
    s0 = l0 * x + m0 * y + (l0 + m0) * z / 2
    s1 = l1 * x + m1 * y + (l1 + m1) * z / 2
    scaling_q = x + y - 2 * z
    assert polarized(s0, v3, scaling_q) == sp.zeros(27, 1)
    assert polarized(s1, v3, scaling_q) == sp.zeros(27, 1)
    assert alternating(s0, s1, v3) == sp.zeros(27, 1)

    zero_q = y - z
    independent_t = source(2, e(1))
    common = mixed_map(v3, zero_q).col_join(mixed_map(v3, independent_t))
    assert len(common.nullspace()) == 1
    exceptional_q = x - y + z
    common = mixed_map(v3, zero_q).col_join(mixed_map(v3, exceptional_q))
    nullspace = common.nullspace()
    pure_x = sp.Matrix.hstack(*(source(0, e(i)) for i in range(3)))
    assert len(nullspace) == 3
    assert sp.Matrix.hstack(*nullspace, pure_x).rank() == 3
    print("common-zero atlas: PASS (all two-/three-source boundaries)")


def transversality_sharpness() -> None:
    x = source(0, e(2))
    y = source(1, e(2))
    z0 = source(2, e(0))
    z1 = source(2, e(1))
    t = source(2, e(2))
    v = x + y
    w = x - y
    u0 = w + z0
    u1 = z1
    q_plane = (w, t)

    assert sp.Matrix.hstack(u0, u1, v, *q_plane).rank() == 5
    assert all(polarized(u0, v, q) == sp.zeros(27, 1) for q in q_plane)
    assert all(polarized(u1, v, q) == sp.zeros(27, 1) for q in q_plane)
    assert polarized(u0, u1, w) == -2 * tensor3(e(2), e(2), e(1))
    assert polarized(u0, u1, t) == sp.zeros(27, 1)
    assert polarized(v, v, w) == sp.zeros(27, 1)
    assert polarized(v, v, t) == 2 * tensor3(e(2), e(2), e(2))
    assert alternating(u0, u1, v) != sp.zeros(27, 1)
    print("transversality sharpness: PASS (shared-factor correction survives)")


def main() -> None:
    beta_zero_type_ii_collapse()
    kernel_colour_planes()
    arbitrary_c_target_table()
    transverse_line_forces_mixed_zero()
    common_zero_atlas()
    transversality_sharpness()
    print("rank-five support-two (2,2) complete exclusion: PASS")


if __name__ == "__main__":
    main()
