"""Exact replay for the support-two (3,3) rank-five exclusion.

The owning Markdown file is the proof.  This verifier checks its symbolic
graph contractions, correction tensors, permanent-symmetry step, target-plane
table, and common-zero atlas over SymPy.
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


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


def contracted_graph_and_corrections() -> None:
    eta0, eta1, beta, chi, alpha, nu = sp.symbols(
        "eta0 eta1 beta chi alpha nu", nonzero=True
    )
    l02, l12, l22 = sp.symbols("l02 l12 l22")
    graph = sp.Matrix(
        [
            [0, -beta / chi, l02],
            [alpha, nu / chi, l12],
            [0, 0, l22],
        ]
    )

    def contracted(a: sp.Matrix) -> sp.Matrix:
        return beta * pair(a, e(0)) + chi * pair(e(1), graph * a)

    assert sp.simplify(contracted(e(1)) - nu * pair(e(1), e(1))) == sp.zeros(
        9, 1
    )
    preimage_0 = e(0) - alpha * chi * e(1) / nu
    assert sp.simplify(
        contracted(preimage_0) - beta * pair(e(0), e(0))
    ) == sp.zeros(9, 1)

    # Rows record coefficients on T0,T1,T2.
    corrections = sp.Matrix(
        [
            [-eta0 / beta, 0, 0],
            [chi * alpha * eta0 / (beta * nu), -eta1 / nu, 0],
            [0, 0, 0],
        ]
    )
    for a in range(3):
        for b in range(3):
            left = sp.Matrix(
                [
                    -eta0 * int(a == b == 0),
                    -eta1 * int(a == b == 1),
                    0,
                ]
            )
            right = beta * int(b == 0) * corrections.row(a).T
            if a == 1:
                right += chi * sum(
                    (
                        graph[b, index] * corrections.row(index).T
                        for index in range(3)
                    ),
                    sp.zeros(3, 1),
                )
            assert sp.simplify(left - right) == sp.zeros(3, 1)

    assert corrections[:, 2] == sp.zeros(3, 1)
    assert corrections[:2, :2].det() != 0
    print("contracted graph/corrections: PASS (all corrections in D01)")


def permanent_symmetry_third_colour() -> None:
    beta, chi, alpha, nu, ell = sp.symbols(
        "beta chi alpha nu ell", nonzero=True
    )
    l02, l12 = sp.symbols("l02 l12")
    graph = sp.Matrix(
        [
            [0, -beta / chi, l02],
            [alpha, nu / chi, l12],
            [0, 0, ell],
        ]
    )
    e22 = sp.zeros(3)
    e22[2, 2] = 1
    skew = sp.simplify(graph * e22 - (graph * e22).T)
    assert skew[0, 2] == l02
    assert skew[1, 2] == l12
    assert sp.solve(
        [skew[0, 2], skew[1, 2]], (l02, l12), dict=True
    ) == [{l02: 0, l12: 0}]

    fixed = graph.subs({l02: 0, l12: 0})
    assert fixed * e(0) == alpha * e(1)
    assert fixed * e(1) == -beta * e(0) / chi + nu * e(1) / chi
    assert fixed * e(2) == ell * e(2)
    # Rows of L are the coefficients of p_b in the r_i basis.
    assert fixed.row(0) == sp.Matrix([[0, -beta / chi, 0]])
    assert fixed.row(2) == sp.Matrix([[0, 0, ell]])
    print("permanent symmetry: PASS (third graph column is ell*e2)")


def complete_target_plane_table() -> None:
    eta0, eta1, beta, chi, alpha, nu, ell = sp.symbols(
        "eta0 eta1 beta chi alpha nu ell", nonzero=True
    )
    graph = sp.Matrix(
        [
            [0, -beta / chi, 0],
            [alpha, nu / chi, 0],
            [0, 0, ell],
        ]
    )
    corrections = sp.Matrix(
        [
            [-eta0 / beta, 0, 0],
            [chi * alpha * eta0 / (beta * nu), -eta1 / nu, 0],
            [0, 0, 0],
        ]
    )
    block_b = sp.Matrix(3, 3, sp.symbols("b0:9"))
    block_c = sp.Matrix(3, 3, sp.symbols("c0:9"))

    def fibre(a: int, b: int, c: int) -> sp.Matrix:
        value = sp.Matrix(
            [
                int(a == b == c == 0),
                int(a == b == c == 1),
                int(a == b == c == 2),
            ]
        )
        for index in range(3):
            singleton = (
                int(a == index) * block_b[b, c]
                + block_c[a, c] * graph[b, index]
            )
            value += singleton * corrections.row(index).T
        return sp.simplify(value)

    for c in range(3):
        expected_square = sp.Matrix([0, 0, int(c == 2)])
        assert fibre(2, 2, c) == expected_square
        for a in (0, 1):
            assert fibre(a, 2, c)[2] == 0
        assert fibre(0, 0, c)[2] == 0

    # p2=ell*r2 and p0=-(beta/chi)*r1 turn those coefficient
    # containments into the three mixed-map hypotheses of the lemma.
    assert graph.row(2) == sp.Matrix([[0, 0, ell]])
    assert graph.row(0) == sp.Matrix([[0, -beta / chi, 0]])
    print("complete target table: PASS (square T2 / mixed maps in D01)")


def diagonal_plane_intersections() -> None:
    target_plane = sp.Matrix.hstack(
        tensor3(e(0), e(0), e(0)),
        tensor3(e(1), e(1), e(1)),
    )
    structural = sp.Matrix.hstack(
        *(
            [tensor3(e(2), e(j), e(k)) for j in range(3) for k in range(3)]
            + [
                tensor3(e(i), e(2), e(k))
                for i in range(3)
                for k in range(3)
            ]
        )
    )
    fixed_pair = sp.Matrix.hstack(
        *(tensor3(e(2), e(2), e(k)) for k in range(3))
    )
    assert structural.rank() == 15
    assert sp.Matrix.hstack(structural, target_plane).rank() == 17
    assert fixed_pair.rank() == 3
    assert sp.Matrix.hstack(fixed_pair, target_plane).rank() == 5
    print("diagonal-plane intersections: PASS (D01 fully transverse to T2)")


def common_zero_atlas() -> None:
    x = source(0, e(2))
    y = source(1, e(2))
    t = source(2, e(2))
    v = x + y
    w = x - y

    # Nonconjugate two-source chart: one common-zero line.
    q0 = source(0, e(0))
    common = mixed_map(v, q0).col_join(mixed_map(v, t))
    nullspace = common.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(*nullspace, w).rank() == 1

    # Conjugate chart with a tangent term: the common-zero plane contains
    # q0, so two independent zero divisors violate V intersect Q=0.
    q0 = w
    tangent = source(0, e(0))
    q1 = tangent + t
    common = mixed_map(v, q0).col_join(mixed_map(v, q1))
    nullspace = common.nullspace()
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(*nullspace, w, -tangent + t).rank() == 2

    # Fully conjugate chart.  Membership in D01 forces both displayed
    # x2*y2-valued products to vanish, and then the alternating tensor does.
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

    # Three-source scaling and coefficient-zero charts.
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
    common = mixed_map(v3, zero_q).col_join(mixed_map(v3, independent_t))
    assert len(common.nullspace()) == 1
    exceptional_q = x - y + z
    common = mixed_map(v3, zero_q).col_join(mixed_map(v3, exceptional_q))
    nullspace = common.nullspace()
    pure_x = sp.Matrix.hstack(*(source(0, e(i)) for i in range(3)))
    assert len(nullspace) == 3
    assert sp.Matrix.hstack(*nullspace, pure_x).rank() == 3
    print("common-zero atlas: PASS (all two-/three-source boundaries)")


def transverse_plane_sharpness() -> None:
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
    shared_factor = -2 * tensor3(e(2), e(2), e(1))
    assert polarized(u0, u1, w) == shared_factor
    assert polarized(u0, u1, t) == sp.zeros(27, 1)
    assert alternating(u0, u1, v) != sp.zeros(27, 1)
    target_plane = sp.Matrix.hstack(
        tensor3(e(0), e(0), e(0)),
        tensor3(e(1), e(1), e(1)),
    )
    assert sp.Matrix.hstack(target_plane, shared_factor).rank() == 3
    print("sharpness: PASS (shared-T2-factor correction lies outside D01)")


def main() -> None:
    contracted_graph_and_corrections()
    permanent_symmetry_third_colour()
    complete_target_plane_table()
    diagonal_plane_intersections()
    common_zero_atlas()
    transverse_plane_sharpness()
    print("rank-five support-two (3,3) exclusion: PASS")


if __name__ == "__main__":
    main()
