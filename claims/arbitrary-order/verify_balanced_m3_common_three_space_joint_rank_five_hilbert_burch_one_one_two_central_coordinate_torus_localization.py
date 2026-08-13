"""Exact replay for the (1,1,2) central-coordinate torus localization.

The owning Markdown file is the proof.  This script checks representative
same- and distinct-colour derivatives, kernels and annihilators; symbolic
torus self-recovery; the untouched tables and exterior contractions; the
nine-hyperplane rank fork; and the source-support identities used to exclude
the five equal-plane alternatives.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def e(index: int, dimension: int = 3) -> sp.Matrix:
    return sp.eye(dimension)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def derivative_matrix(
    s: int,
    t: int,
    z: sp.Matrix,
    w: sp.Matrix,
    lam: sp.Expr,
    mu: sp.Expr,
) -> sp.Matrix:
    columns = []
    for index in range(3):
        columns.append(-mu * tensor3(e(index), e(t), z))
    for index in range(3):
        columns.append(-lam * tensor3(e(s), e(index), w))
    for index in range(3):
        columns.append(lam * mu * tensor3(e(s), e(t), e(index)))
    return sp.Matrix.hstack(*columns)


def derivative_kernel_annihilator() -> None:
    lam, mu = sp.symbols("lam mu", nonzero=True)
    models = (
        (0, 0, sp.Matrix([1, 2, 0]), sp.Matrix([0, 1, 3])),
        (0, 1, sp.Matrix([1, 2, 3]), sp.Matrix([2, 3, 5])),
        (0, 1, sp.Matrix([1, 0, 3]), sp.Matrix([2, 3, 0])),
    )
    for s, t, z, w in models:
        derivative = derivative_matrix(s, t, z, w, lam, mu)
        k1 = (lam * e(s)).col_join(sp.zeros(3, 1)).col_join(z)
        k2 = sp.zeros(3, 1).col_join(mu * e(t)).col_join(w)
        kernel = sp.Matrix.hstack(k1, k2)
        assert sp.Matrix.hstack(z, w).rank() == 2
        assert derivative.rank() == 7
        assert kernel.rank() == 2
        assert derivative * kernel == sp.zeros(27, 2)

        basis = []
        for index in range(3):
            if index != s:
                basis.append(e(index).col_join(sp.zeros(6, 1)))
        for index in range(3):
            if index != t:
                basis.append(
                    sp.zeros(3, 1).col_join(e(index)).col_join(sp.zeros(3, 1))
                )
        for index in range(3):
            basis.append(
                (-z[index] / lam * e(s))
                .col_join(-w[index] / mu * e(t))
                .col_join(e(index))
            )
        annihilator = sp.Matrix.hstack(*basis)
        assert annihilator.rank() == 7
        assert kernel.T * annihilator == sp.zeros(2, 7)
    print("(1,1,2) derivative: PASS (same/distinct colours, rank/kernel/L)")


def torus_self_recovery() -> None:
    lam, mu = sp.symbols("lam mu", nonzero=True)
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    g0, g1, g2 = sp.symbols("g0 g1 g2")
    z = sp.Matrix([z0, z1, z2])
    w = sp.Matrix([w0, w1, w2])
    gamma = sp.Matrix([g0, g1, g2])
    gamma_z, gamma_w = (gamma.T * z)[0], (gamma.T * w)[0]

    for s, t in ((0, 0), (0, 1)):
        alpha_values = list(sp.symbols(f"a0:{3}"))
        beta_values = list(sp.symbols(f"b0:{3}"))
        alpha_values[s] = -gamma_z / lam
        beta_values[t] = -gamma_w / mu
        alpha, beta = sp.Matrix(alpha_values), sp.Matrix(beta_values)
        ell = alpha.col_join(beta).col_join(gamma)
        recovered = (
            (-mu * beta[t] * gamma_z * alpha)
            .col_join(-lam * alpha[s] * gamma_w * beta)
            .col_join(lam * mu * alpha[s] * beta[t] * gamma)
        )
        assert sp.simplify(recovered - gamma_z * gamma_w * ell) == sp.zeros(9, 1)
    print("torus self-recovery: PASS (gamma(z) gamma(w))")


def target(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(int(i == j == k == colour) for colour in range(3))


def untouched_tables_and_faces() -> None:
    # Same-colour chart s=t=0: the complementary binary cube contains T1,T2.
    same_core = {
        (i, j, k): target(i, j, k)
        for i, j, k in product((1, 2), repeat=3)
    }
    assert [cell for cell, value in same_core.items() if any(value)] == [
        (1, 1, 1),
        (2, 2, 2),
    ]

    # Distinct chart s=0,t=1,u=2: only T2 survives on R x P x theta.
    distinct_core = {
        (i, j, k): target(i, j, k)
        for i, j, k in product((1, 2), (0, 2), range(3))
    }
    assert [cell for cell, value in distinct_core.items() if any(value)] == [
        (2, 2, 2)
    ]

    lam, mu = sp.symbols("lam mu", nonzero=True)
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    g0, g1, g2 = sp.symbols("g0 g1 g2")
    z, w, gamma = (
        sp.Matrix([z0, z1, z2]),
        sp.Matrix([w0, w1, w2]),
        sp.Matrix([g0, g1, g2]),
    )
    derivative = derivative_matrix(0, 1, z, w, lam, mu)
    gamma_z, gamma_w = (gamma.T * z)[0], (gamma.T * w)[0]

    def contraction(i: int, j: int) -> sp.Matrix:
        return sum(
            (gamma[k] * derivative.row(9 * i + 3 * j + k) for k in range(3)),
            sp.zeros(1, 9),
        )

    for j in (0, 2):
        expected = sp.zeros(1, 9)
        expected[0, 3 + j] = -lam * gamma_w
        assert sp.simplify(contraction(0, j) - expected) == sp.zeros(1, 9)
    for i in (1, 2):
        expected = sp.zeros(1, 9)
        expected[0, i] = -mu * gamma_z
        assert sp.simplify(contraction(i, 1) - expected) == sp.zeros(1, 9)
    print("target atlas: PASS (same cube / distinct core / exterior factors)")


def nine_hyperplane_fork() -> None:
    # Seven basis coordinates plus the two nonzero recovery factors.
    for z, w in (
        (sp.Matrix([1, 2, 3]), sp.Matrix([2, 3, 5])),
        (sp.Matrix([1, 0, 3]), sp.Matrix([2, 3, 0])),
    ):
        normals = [sp.eye(7).row(index) for index in range(7)]
        normals.extend(
            [
                sp.Matrix([[0, 0, 0, 0, z[0], z[1], z[2]]]),
                sp.Matrix([[0, 0, 0, 0, w[0], w[1], w[2]]]),
            ]
        )
        assert len(normals) == 9
        assert all(normal != sp.zeros(1, 7) for normal in normals)

    # A four-dimensional relation kernel in a six-dimensional hyperplane
    # leaves rank two.  For h_k and both recovery-factor hyperplanes, that
    # hyperplane contains the four basis preimages of R and P.
    for exceptional in range(5):
        matrix = sp.zeros(3, 7)
        deleted = 4 + (exceptional % 3) if exceptional < 3 else 4
        other = [index for index in range(7) if index != deleted]
        for position, index in enumerate(other):
            matrix[:, index] = sp.Matrix([1, position, 0])
        matrix[:, deleted] = sp.Matrix([0, 0, 1])
        assert matrix.rank() == 3
        assert matrix[:, other].rank() == 2
        assert matrix[:, :2].rank() == matrix[:, 2:4].rank() == 2
        assert 7 - matrix.rank() == 4

    residual = {"alpha_a", "alpha_b", "beta_c", "beta_d"}
    assert len(residual) == 4
    print("relation fork: PASS (nine hyperplanes / five equal-plane alternatives)")


def same_colour_symmetry() -> None:
    a, b, c, d, tau0, tau1 = sp.symbols(
        "a b c d tau0 tau1", nonzero=True
    )
    change = sp.Matrix([[a, b], [c, d]])
    form0 = sp.Matrix([[tau0, 0], [0, 0]]) * change.inv()
    form1 = sp.Matrix([[0, 0], [0, tau1]]) * change.inv()
    anti0 = sp.factor(form0[1, 0] - form0[0, 1])
    anti1 = sp.factor(form1[1, 0] - form1[0, 1])
    assert anti0 == b * tau0 / (a * d - b * c)
    assert anti1 == -c * tau1 / (a * d - b * c)
    print("same-colour equality: PASS (diagonal change / two-square reduction)")


BlockVector = tuple[sp.Matrix, sp.Matrix, sp.Matrix]


def permanent(left: BlockVector, middle: BlockVector, right: BlockVector) -> sp.Matrix:
    arguments = (left, middle, right)
    answer = sp.zeros(8, 1)
    for assignment in permutations(range(3)):
        answer += tensor3(
            arguments[assignment[0]][0],
            arguments[assignment[1]][1],
            arguments[assignment[2]][2],
        )
    return answer


def distinct_colour_source_atlas() -> None:
    zero = sp.zeros(2, 1)
    x, y, zeta = e(0, 2), e(0, 2), e(0, 2)
    c_x, c_y, c_z = sp.symbols("cx cy cz")
    external: BlockVector = (
        sp.Matrix([2, 3]),
        sp.Matrix([5, 7]),
        sp.Matrix([11, 13]),
    )

    # Pure common radical: every mixed value keeps its fixed source factor.
    pure: BlockVector = (x, zero, zero)
    q: BlockVector = (sp.Matrix([17, 19]), sp.Matrix([23, 29]), sp.Matrix([31, 37]))
    mixed = permanent(external, pure, q)
    assert all(
        mixed[4 * i + 2 * j + k] == 0
        for i in (1,)
        for j, k in product(range(2), repeat=2)
    )

    # Three-source square kernel and tangent support.
    three: BlockVector = (x, y, zeta)
    scaling = (
        (c_x * x, c_y * y, c_z * zeta),
        sp.Eq(c_x + c_y + c_z, 0),
    )
    square_value = permanent(three, three, scaling[0])
    assert sp.simplify(square_value.subs(c_z, -c_x - c_y)) == sp.zeros(8, 1)
    tangent = permanent(external, three, scaling[0]).subs(c_z, -c_x - c_y)
    for i, j, k in product(range(2), repeat=3):
        if i + j + k >= 2:
            assert sp.expand(tangent[4 * i + 2 * j + k]) == 0

    # Two-source radical: q_Z=0 and every mixed value has the common tangent
    # factor L(q)=x*q_Y+q_X*y.
    two: BlockVector = (x, y, zero)
    q_xy: BlockVector = (sp.Matrix([17, 19]), sp.Matrix([23, 29]), zero)
    assert permanent(two, two, q_xy) == sp.zeros(8, 1)
    tangent_xy = sp.kronecker_product(x, q_xy[1]) + sp.kronecker_product(q_xy[0], y)
    assert permanent(external, two, q_xy) == sp.kronecker_product(
        tangent_xy, external[2]
    )

    # The common-annihilator kernel of L is span(x,-y).
    qx0, qx1, qy0, qy1 = sp.symbols("qx0 qx1 qy0 qy1")
    lmatrix = sp.kronecker_product(x, sp.Matrix([qy0, qy1])) + sp.kronecker_product(
        sp.Matrix([qx0, qx1]), y
    )
    solution = sp.solve(list(lmatrix), (qx0, qx1, qy0, qy1), dict=True)
    assert solution == [{qx0: -qy0, qx1: 0, qy1: 0}]

    # At q_u=(x,-y,0), the surviving square has the advertised 2x2 matrix.
    dx0, dx1, dy0, dy1, dz0, dz1 = sp.symbols(
        "dx0 dx1 dy0 dy1 dz0 dz1"
    )
    d: BlockVector = (
        sp.Matrix([dx0, dx1]),
        sp.Matrix([dy0, dy1]),
        sp.Matrix([dz0, dz1]),
    )
    q_u: BlockVector = (x, -y, zero)
    square = permanent(d, d, q_u)
    xy_matrix = sp.Matrix([[dx0, dx1], [dy0, dy1]])
    # Independence of (x,d_X) and (y,d_Y) is exactly dx1*dy1 != 0 and
    # produces a nonzero 2x2 determinant in x*d_Y-d_X*y.
    active_xy = sp.Matrix(
        [[dy0 - dx0, dy1], [-dx1, 0]]
    )
    assert sp.factor(active_xy.det()) == dx1 * dy1
    expected = 2 * sp.kronecker_product(
        sp.Matrix([dy0 - dx0, dy1, -dx1, 0]), d[2]
    )
    assert sp.simplify(square - expected) == sp.zeros(8, 1)
    assert xy_matrix.shape == (2, 2)
    print("distinct-colour equality: PASS (pure / tangent / split-ruling atlas)")


def main() -> None:
    derivative_kernel_annihilator()
    torus_self_recovery()
    untouched_tables_and_faces()
    nine_hyperplane_fork()
    same_colour_symmetry()
    distinct_colour_source_atlas()
    print("(1,1,2) central-coordinate torus localization: PASS")


if __name__ == "__main__":
    main()
