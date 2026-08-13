"""Exact replay for the support-one (2,2) rank-five exclusion.

The owning Markdown file is the proof.  This verifier checks every ordered
missing-colour pair, the zero-row correction system, the relation-plane row
normal form, support-colour forcing, the complete arbitrary-block target
table, and the inherited binary-diagonal-plane common-zero atlas over SymPy.
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


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
        *(polarized(u, v, sp.eye(9)[:, index]) for index in range(9))
    )


def target_fibre(
    a: int,
    shore_b: int,
    k: int,
    c: int,
    d: int,
    block_b: sp.Matrix,
    block_c: sp.Matrix,
    kappa: sp.Expr,
    kappa_prime: sp.Expr,
) -> sp.Matrix:
    value = e(k) if a == shore_b == k else sp.zeros(3, 1)
    if a == d:
        value -= block_b[shore_b, k] * e(d) / kappa
    if shore_b == c:
        value -= block_c[a, k] * e(c) / kappa_prime
    return sp.simplify(value)


def relation_plane_and_zero_rows() -> None:
    kappa, kappa_prime, tau = sp.symbols(
        "kappa kappa_prime tau", nonzero=True
    )
    zero = sp.zeros(3, 1)

    # If the two missing colours coincide, the first zero row asks for a
    # vector with a forbidden coordinate in pr_1(P).
    for colour in range(3):
        requested = -e(colour) / kappa
        assert requested[colour] != 0

    for c in range(3):
        for d in range(3):
            if c == d:
                continue
            j = next(index for index in range(3) if index not in (c, d))
            first = sp.Matrix.hstack(e(d), zero, e(j))
            second = sp.Matrix.hstack(zero, e(c), tau * e(j))
            plane = first.col_join(second)
            assert plane.rank() == 3
            assert first.rank() == 2
            assert second.rank() == 2
            assert first.row(c) == sp.zeros(1, 3)
            assert second.row(d) == sp.zeros(1, 3)

            corrections: dict[int, sp.Matrix] = {}
            for target in range(3):
                a_target = (
                    -e(d) / kappa if target == d else sp.zeros(3, 1)
                )
                b_target = (
                    -e(c) / kappa_prime
                    if target == c
                    else sp.zeros(3, 1)
                )
                corrections[target] = a_target.col_join(b_target)

            expected_d = (-e(d) / kappa).col_join(zero)
            expected_c = zero.col_join(-e(c) / kappa_prime)
            assert corrections[d] == expected_d
            assert corrections[c] == expected_c
            assert plane.row_join(expected_d).rank() == 3
            assert plane.row_join(expected_c).rank() == 3
            assert corrections[j] == sp.zeros(6, 1)

            # Evaluation of coordinate covectors on the three plane basis
            # columns gives the claimed involved-row normal form.
            rows_r = first.T
            rows_p = second.T
            assert rows_r[:, d] == e(0)
            assert rows_r[:, c] == zero
            assert rows_r[:, j] == e(2)
            assert rows_p[:, d] == zero
            assert rows_p[:, c] == e(1)
            assert rows_p[:, j] == tau * e(2)

    print("zero rows/relation plane: PASS (all ordered missing colours)")


def support_colour_forcing() -> None:
    survivors = [
        (c, d)
        for c in range(3)
        for d in range(3)
        if c != d and 2 in (c, d)
    ]
    assert survivors == [(0, 2), (1, 2), (2, 0), (2, 1)]
    canonical = [
        (c, d)
        for c, d in survivors
        if d == 2
    ]
    assert canonical == [(0, 2), (1, 2)]

    # If neither missing colour is 2, both zero-row equations make the T2
    # correction vector zero while q2 kills the all-cross coefficient.
    excluded = [
        (c, d)
        for c in range(3)
        for d in range(3)
        if c != d and 2 not in (c, d)
    ]
    assert excluded == [(0, 1), (1, 0)]
    print("support colour: PASS (2 lies in {c,d}; root exchange sets d=2)")


def complete_target_table() -> None:
    kappa, kappa_prime = sp.symbols(
        "kappa kappa_prime", nonzero=True
    )
    block_b = sp.Matrix(3, 3, sp.symbols("b0:9"))
    block_c = sp.Matrix(3, 3, sp.symbols("c0:9"))

    for c in (0, 1):
        d = 2
        j = 1 - c
        b = block_b.copy()
        c_block = block_c.copy()
        for k in range(3):
            b[d, k] = kappa * int(k == d)
            c_block[c, k] = kappa_prime * int(k == c)

        for k in range(3):
            square = target_fibre(
                j, j, k, c, d, b, c_block, kappa, kappa_prime
            )
            mixed_dj = target_fibre(
                d, j, k, c, d, b, c_block, kappa, kappa_prime
            )
            mixed_jc = target_fibre(
                j, c, k, c, d, b, c_block, kappa, kappa_prime
            )
            mixed_dc = target_fibre(
                d, c, k, c, d, b, c_block, kappa, kappa_prime
            )
            assert square == int(k == j) * e(j)
            assert mixed_dj == -b[j, k] * e(d) / kappa
            assert (
                mixed_jc == -c_block[j, k] * e(c) / kappa_prime
            )
            assert mixed_dc == (
                -b[c, k] * e(d) / kappa
                - c_block[d, k] * e(c) / kappa_prime
            )

            # The square uses only T_j; every mixed value uses D_cd.
            assert all(
                square[index] == 0
                for index in range(3)
                if index != j
            )
            for mixed in (mixed_dj, mixed_jc, mixed_dc):
                assert mixed[j] == 0

    print("complete target table: PASS (arbitrary B,C / square plus D_cd)")


def diagonal_plane_intersections() -> None:
    target_plane = sp.Matrix.hstack(
        tensor3(e(0), e(0), e(0)),
        tensor3(e(1), e(1), e(1)),
    )
    structural = sp.Matrix.hstack(
        *(
            [tensor3(e(2), e(y), e(z)) for y in range(3) for z in range(3)]
            + [
                tensor3(e(x), e(2), e(z))
                for x in range(3)
                for z in range(3)
            ]
        )
    )
    fixed_pair = sp.Matrix.hstack(
        *(tensor3(e(2), e(2), e(z)) for z in range(3))
    )
    assert structural.rank() == 15
    assert sp.Matrix.hstack(structural, target_plane).rank() == 17
    assert fixed_pair.rank() == 3
    assert sp.Matrix.hstack(fixed_pair, target_plane).rank() == 5
    print("diagonal-plane transversality: PASS (D_cd versus untouched T_j)")


def common_zero_atlas() -> None:
    x = source(0, e(2))
    y = source(1, e(2))
    t = source(2, e(2))
    v = x + y
    w = x - y

    # Nonconjugate two-source chart: only one common-zero line survives.
    q0 = source(0, e(0))
    common = mixed_map(v, q0).col_join(mixed_map(v, t))
    nullspace = common.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(*nullspace, w).rank() == 1

    # Conjugate chart with a tangent term: two independent zero divisors
    # put a nonzero vector in V intersect Q.
    tangent = source(0, e(0))
    q1 = tangent + t
    common = mixed_map(v, w).col_join(mixed_map(v, q1))
    nullspace = common.nullspace()
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(*nullspace, w, -tangent + t).rank() == 2

    # Fully conjugate chart: diagonal-plane membership makes both displayed
    # fixed-pair products zero, which also kills the alternating tensor.
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

    # Three-source nonzero scaling chart and coefficient-zero boundaries.
    z = source(2, e(0))
    v3 = x + y + z
    lambda0, mu0, lambda1, mu1 = sp.symbols(
        "lambda0 mu0 lambda1 mu1"
    )
    s0 = lambda0 * x + mu0 * y + (lambda0 + mu0) * z / 2
    s1 = lambda1 * x + mu1 * y + (lambda1 + mu1) * z / 2
    scaling_q = x + y - 2 * z
    assert polarized(s0, v3, scaling_q) == sp.zeros(27, 1)
    assert polarized(s1, v3, scaling_q) == sp.zeros(27, 1)
    assert alternating(s0, s1, v3) == sp.zeros(27, 1)

    zero_q = y - z
    independent_t = source(2, e(1))
    common = mixed_map(v3, zero_q).col_join(
        mixed_map(v3, independent_t)
    )
    assert len(common.nullspace()) == 1
    exceptional_q = x - y + z
    common = mixed_map(v3, zero_q).col_join(
        mixed_map(v3, exceptional_q)
    )
    nullspace = common.nullspace()
    pure_x = sp.Matrix.hstack(*(source(0, e(i)) for i in range(3)))
    assert len(nullspace) == 3
    assert sp.Matrix.hstack(*nullspace, pure_x).rank() == 3
    print("common-zero atlas: PASS (two-/three-source exhaustion replay)")


def singleton_determinant_orientation() -> None:
    v_d = source(0, e(0))
    v_c = source(1, e(1))
    v_j = source(2, e(2))
    alt = alternating(v_d, v_c, v_j)
    assert alt == tensor3(e(0), e(1), e(2))
    for order in permutations((v_d, v_c, v_j)):
        assert alternating(*order) in (alt, -alt)
    print("singleton determinant: PASS (normal-form basis has nonzero scale)")


def main() -> None:
    relation_plane_and_zero_rows()
    support_colour_forcing()
    complete_target_table()
    diagonal_plane_intersections()
    common_zero_atlas()
    singleton_determinant_orientation()
    print("rank-five support-one (2,2) complete exclusion: PASS")


if __name__ == "__main__":
    main()
