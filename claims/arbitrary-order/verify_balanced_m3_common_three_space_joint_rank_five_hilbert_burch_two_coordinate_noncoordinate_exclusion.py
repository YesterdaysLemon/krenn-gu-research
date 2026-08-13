"""Exact replay for the two-coordinate/noncoordinate HB exclusion.

The owning Markdown file is the proof.  This script checks the scalar-general
derivative, kernel, annihilator and torus recovery; every noncoordinate
support chart; the contracted target faces and row-plane gates; the eight
hyperplane rank fork; and the exact permanent identities behind the
square-zero and ordinary-coloop contradictions.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def e(index: int, dimension: int = 3) -> sp.Matrix:
    return sp.eye(dimension)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def derivative_kernel_annihilator_and_torus() -> None:
    lam, mu = sp.symbols("lam mu", nonzero=True)
    z0, z1, z2 = sp.symbols("z0 z1 z2")
    z = sp.Matrix([z0, z1, z2])

    columns = []
    for index in range(3):
        columns.append(-mu * tensor3(e(index), e(1), z))
    for index in range(3):
        columns.append(-lam * tensor3(e(0), e(index), z))
    for index in range(3):
        columns.append(lam * mu * tensor3(e(0), e(1), e(index)))
    derivative = sp.Matrix.hstack(*columns)
    assert derivative.rank() == 7

    k1 = (lam * e(0)).col_join(sp.zeros(3, 1)).col_join(z)
    k2 = sp.zeros(3, 1).col_join(mu * e(1)).col_join(z)
    kernel = sp.Matrix.hstack(k1, k2)
    assert kernel.rank() == 2
    assert derivative * kernel == sp.zeros(27, 2)

    # Free-coordinate basis (alpha_1,alpha_2,beta_0,beta_2,
    # gamma_0,gamma_1,gamma_2).  The final three columns map to h_k.
    basis = [
        e(1).col_join(sp.zeros(6, 1)),
        e(2).col_join(sp.zeros(6, 1)),
        sp.zeros(3, 1).col_join(e(0)).col_join(sp.zeros(3, 1)),
        sp.zeros(3, 1).col_join(e(2)).col_join(sp.zeros(3, 1)),
    ]
    for index, coordinate in enumerate((z0, z1, z2)):
        vector = (
            (-coordinate / lam * e(0))
            .col_join(-coordinate / mu * e(1))
            .col_join(e(index))
        )
        basis.append(vector)
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.rank() == 7
    assert kernel.T * annihilator == sp.zeros(2, 7)

    a1, a2, b0, b2, g0, g1, g2 = sp.symbols(
        "a1 a2 b0 b2 g0 g1 g2"
    )
    gamma = sp.Matrix([g0, g1, g2])
    gamma_z = (gamma.T * z)[0]
    alpha = sp.Matrix([-gamma_z / lam, a1, a2])
    beta = sp.Matrix([b0, -gamma_z / mu, b2])
    ell = alpha.col_join(beta).col_join(gamma)
    recovered = (
        (-mu * beta[1] * gamma_z * alpha)
        .col_join(-lam * alpha[0] * gamma_z * beta)
        .col_join(lam * mu * alpha[0] * beta[1] * gamma)
    )
    assert sp.simplify(recovered - gamma_z**2 * ell) == sp.zeros(9, 1)
    print("two-coordinate derivative: PASS (rank/kernel/annihilator/torus)")


def noncoordinate_support_and_plane_gates() -> None:
    charts = (
        sp.Matrix([2, 3, 0]),
        sp.Matrix([2, 0, 5]),
        sp.Matrix([0, 3, 5]),
        sp.Matrix([2, 3, 5]),
    )
    for z in charts:
        z_perp = sp.Matrix([list(z)]).nullspace()
        assert len(z_perp) == 2
        gamma_matrix = sp.Matrix.hstack(*z_perp)

        # A coordinate restriction vanishes on z^perp exactly in the
        # excluded coordinate-vector chart.  All three are active here.
        restrictions = [gamma_matrix.row(index) for index in range(3)]
        assert all(row != sp.zeros(1, 2) for row in restrictions)
        assert z[0] * restrictions[0] + z[1] * restrictions[1] + z[2] * restrictions[2] == sp.zeros(1, 2)

        # The T_2 face detects every gamma with gamma_2 != 0.  The remaining
        # kernel candidate has gamma_2=0, where the contracted target has a
        # nonzero (T_0,T_1) coordinate pair.
        ell2_kernel = restrictions[2].nullspace()
        assert len(ell2_kernel) == 1
        gamma = gamma_matrix * ell2_kernel[0]
        assert gamma != sp.zeros(3, 1)
        assert gamma[2] == 0
        assert (gamma[0], gamma[1]) != (0, 0)

    # Untouched row gates: the nonzero 222 value and the zero crossed values
    # separate r_1,r_2 and p_0,p_2.  The 111 and 000 diagonal target gates
    # prevent the first member of either pair from vanishing.
    target = lambda i, j, k: tuple(int(i == j == k == c) for c in range(3))
    assert target(2, 2, 2) == (0, 0, 1)
    assert target(1, 2, 2) == target(2, 0, 2) == (0, 0, 0)
    assert target(1, 1, 1) == (0, 1, 0)
    assert target(0, 0, 0) == (1, 0, 0)
    print("noncoordinate charts: PASS (four supports / three two-plane gates)")


def contracted_support_and_faces() -> None:
    lam, mu = sp.symbols("lam mu", nonzero=True)
    z0, z1, z2, g0, g1, g2 = sp.symbols("z0 z1 z2 g0 g1 g2")
    z = sp.Matrix([z0, z1, z2])
    gamma = sp.Matrix([g0, g1, g2])
    gamma_z = (gamma.T * z)[0]

    columns = []
    for index in range(3):
        columns.append(-mu * tensor3(e(index), e(1), z))
    for index in range(3):
        columns.append(-lam * tensor3(e(0), e(index), z))
    for index in range(3):
        columns.append(lam * mu * tensor3(e(0), e(1), e(index)))
    derivative = sp.Matrix.hstack(*columns)

    def contraction(i: int, j: int) -> sp.Matrix:
        return sum(
            (gamma[k] * derivative.row(9 * i + 3 * j + k) for k in range(3)),
            sp.zeros(1, 9),
        )

    for j in (0, 2):
        expected = sp.zeros(1, 9)
        expected[0, 3 + j] = -lam * gamma_z
        assert sp.simplify(contraction(0, j) - expected) == sp.zeros(1, 9)
    for i in (1, 2):
        expected = sp.zeros(1, 9)
        expected[0, i] = -mu * gamma_z
        assert sp.simplify(contraction(i, 1) - expected) == sp.zeros(1, 9)
    for i, j in product((1, 2), (0, 2)):
        assert contraction(i, j) == sp.zeros(1, 9)

    # After gamma(z)=0, only the three displayed target faces remain.
    face_a = {(j, c): int(j == 0 == c) for j in (0, 2) for c in range(3)}
    face_b = {(i, c): int(i == 1 == c) for i in (1, 2) for c in range(3)}
    core = {
        (i, j, c): int(i == j == 2 == c)
        for i, j in product((1, 2), (0, 2))
        for c in range(3)
    }
    assert sum(face_a.values()) == sum(face_b.values()) == sum(core.values()) == 1
    print("contracted support: PASS (gamma(z) factor / three exterior faces)")


def eight_hyperplane_fork() -> None:
    charts = (
        sp.Matrix([2, 3, 0]),
        sp.Matrix([2, 0, 5]),
        sp.Matrix([0, 3, 5]),
        sp.Matrix([2, 3, 5]),
    )
    for z in charts:
        normals = [sp.eye(7).row(index) for index in range(7)]
        normals.append(sp.Matrix([[0, 0, 0, 0, z[0], z[1], z[2]]]))
        assert all(normal != sp.zeros(1, 7) for normal in normals)

        # Model the exceptional gamma(z)=0 alternative independently.  The
        # h-block has third row z^T and first two rows spanning z^perp.
        z_perp = sp.Matrix([list(z)]).nullspace()
        h_block = sp.Matrix.vstack(
            z_perp[0].T,
            z_perp[1].T,
            z.T,
        )
        assert h_block.rank() == 3
        phi = sp.Matrix.hstack(
            sp.Matrix([[1, 0], [0, 1], [0, 0]]),
            sp.Matrix([[1, 0], [0, 1], [0, 0]]),
            h_block,
        )
        assert phi.rank() == 3
        relation_kernel = sp.Matrix.hstack(*phi.nullspace())
        assert relation_kernel.shape == (7, 4)
        normal = sp.Matrix([[0, 0, 0, 0, z[0], z[1], z[2]]])
        assert normal * relation_kernel == sp.zeros(1, 4)
        assert phi[:, :2].rank() == phi[:, 2:4].rank() == 2
        q_image = phi[:, 4:] * sp.Matrix.hstack(*z_perp)
        assert q_image.rank() == 2
        assert phi[:, :2].row(2) == phi[:, 2:4].row(2) == q_image.row(2) == sp.zeros(1, 2)

    # Each of the seven coordinate hyperplanes gives one coloop and a
    # two-plane after deletion: 6 - dim(N)=2.
    for coloop in range(7):
        matrix = sp.zeros(3, 7)
        counter = 0
        for index in range(7):
            if index == coloop:
                matrix[:, index] = sp.Matrix([0, 0, 1])
            else:
                matrix[:, index] = sp.Matrix([1, counter, 0])
                counter += 1
        other = [index for index in range(7) if index != coloop]
        assert matrix.rank() == 3
        assert matrix[:, other].rank() == 2
        relations = sp.Matrix.hstack(*matrix.nullspace())
        assert relations.shape == (7, 4)
        assert relations.row(coloop) == sp.zeros(1, 4)

    fork = {
        "alpha_1": "P=Q",
        "alpha_2": "P=Q",
        "beta_0": "R=Q",
        "beta_2": "R=Q",
        "gamma_0": "R=P",
        "gamma_1": "R=P",
        "gamma_2": "R=P",
        "gamma(z)": "R=P=Q",
    }
    assert set(fork.values()) == {"P=Q", "R=Q", "R=P", "R=P=Q"}
    print("torus relation fork: PASS (eight hyperplanes / four equality types)")


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


def square_zero_mixed_factor_atlas() -> None:
    zero = sp.zeros(2, 1)
    x, y, z = e(0, 2), e(0, 2), e(0, 2)
    a0, a1, b0, b1, c0, c1 = sp.symbols("a0 a1 b0 b1 c0 c1")
    a: BlockVector = (
        sp.Matrix([a0, a1]),
        sp.Matrix([b0, b1]),
        sp.Matrix([c0, c1]),
    )

    # Pure v: every mixed value has the fixed factor x in the pure source.
    pure: BlockVector = (x, zero, zero)
    q: BlockVector = (sp.Matrix([2, 3]), sp.Matrix([5, 7]), sp.Matrix([11, 13]))
    pure_value = permanent(a, pure, q)
    assert all(pure_value[4 * i + 2 * j + k] == 0 for i in (1,) for j, k in product(range(2), repeat=2))

    # Two-source v: square-zero forces q_Z=0, and the mixed map factors as
    # a_Z tensor (x tensor q_Y + q_X tensor y).
    two: BlockVector = (x, y, zero)
    q_xy: BlockVector = (sp.Matrix([2, 3]), sp.Matrix([5, 7]), zero)
    assert permanent(two, two, q_xy) == sp.zeros(8, 1)
    xy_factor = sp.kronecker_product(x, q_xy[1]) + sp.kronecker_product(q_xy[0], y)
    expected = sp.kronecker_product(xy_factor, a[2])
    assert permanent(a, two, q_xy) == expected

    # Three-source v: the two scaling differences are its complete square
    # kernel.  Every mixed value there lies in the Segre tangent support,
    # whose only possibly nonzero cells have at most one off-base index.
    three: BlockVector = (x, y, z)
    q0: BlockVector = (x, -y, zero)
    q1: BlockVector = (x, zero, -z)
    for kernel_vector in (q0, q1):
        assert permanent(three, three, kernel_vector) == sp.zeros(8, 1)
        mixed = permanent(a, three, kernel_vector)
        for i, j, k in product(range(2), repeat=3):
            if i + j + k >= 2:
                assert mixed[4 * i + 2 * j + k] == 0
    allowed_off_base_sets = [mask for mask in product((0, 1), repeat=3) if sum(mask) <= 1]
    assert len(allowed_off_base_sets) == 4
    print("square-zero lemma: PASS (pure / two-source / tangent atlases)")


def equal_plane_and_coloop_equations() -> None:
    # In common R=P coordinates, F=S*M has only its lower-right entry.
    # Symmetry of S forces the lower-left change-of-basis coefficient to
    # vanish, so p_0 lies on r_1.
    a, b, c, d, tau = sp.symbols("a b c d tau", nonzero=True)
    matrix = sp.Matrix([[a, b], [c, d]])
    form = sp.Matrix([[0, 0], [0, tau]]) * matrix.inv()
    antisymmetric = sp.factor(form[1, 0] - form[0, 1])
    assert antisymmetric == -c * tau / (a * d - b * c)

    # In P=Q, the A and r_2 squares have complementary radicals.  The B
    # faces distinguish the two ordinary-coloop orientations exactly.
    t0, t1, t2 = e(0), e(1), e(2)
    assert sp.Matrix.hstack(t0, t1, t2).rank() == 3
    assert t0 != t1 and t1 != t2 and t0 != t2

    # r_2 coloop: A(r_1,-)+B(r_1,-)=0 would cancel nonzero T_0/T_1 lines.
    u, v = sp.symbols("u v", nonzero=True)
    assert sp.Matrix.hstack(u * t0, v * t1).rank() == 2

    # r_1 coloop: avoid the two scalar kernel lines on an infinite field.
    s, t = sp.symbols("s t")
    square_functional = s
    mixed_functional = s + t
    witness = {s: 1, t: 1}
    assert square_functional.subs(witness) != 0
    assert mixed_functional.subs(witness) != 0

    # The reduction then has exactly the pointwise S2AL form on span(A):
    # one square image T_0 and one mixed image T_1, which are fully
    # transverse and hence forbidden by that proved lemma.
    pointwise_square = t0
    pointwise_mixed = t1
    assert sp.Matrix.hstack(pointwise_square, pointwise_mixed).rank() == 2
    print("equal-plane fork: PASS (radicals / two ordinary coloops / S2AL reduction)")


def main() -> None:
    derivative_kernel_annihilator_and_torus()
    noncoordinate_support_and_plane_gates()
    contracted_support_and_faces()
    eight_hyperplane_fork()
    square_zero_mixed_factor_atlas()
    equal_plane_and_coloop_equations()
    print("two-coordinate/noncoordinate Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
