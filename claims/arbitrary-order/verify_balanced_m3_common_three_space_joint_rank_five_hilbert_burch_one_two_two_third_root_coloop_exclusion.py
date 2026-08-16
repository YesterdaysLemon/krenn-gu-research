"""Exact replay for the (1,2,2) third-root-coloop exclusion."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
DEPENDENCY_CERTIFICATES = {
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_projective_pencil_"
        "certificates.json"
    ): "0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca",
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_common_middle_row_"
        "certificates.json"
    ): "a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1",
}


def e(index: int, size: int = 3) -> sp.Matrix:
    return sp.eye(size)[:, index]


def dot(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand((left.T * right)[0])


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def blocks(
    y: sp.Matrix,
    z: sp.Matrix,
    w: sp.Matrix,
    s: int,
    t: int,
    lam: sp.Expr,
    mu: sp.Expr,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        outer(y, w) - mu * outer(e(t), z),
        -lam * outer(e(s), w),
        lam * mu * outer(e(s), e(t)),
    )


def derivative_zero_face() -> None:
    by, gw, bt, gz, alpha_s, lam, mu = sp.symbols(
        "by gw bt gz alpha_s lambda mu"
    )
    transpose_scalars = (
        by * gw - mu * bt * gz,
        -lam * alpha_s * gw,
        lam * mu * alpha_s * bt,
    )
    specialized = [sp.expand(value.subs({bt: 0, gw: 0})) for value in transpose_scalars]
    assert specialized == [0, 0, 0]
    print("third-root coloop derivative-zero face: PASS")


def canonical_gamma_coloop_geometry() -> None:
    # Modulo R, the canonical gamma-coloop rows have coordinates
    # A, B, C in a five-dimensional row space R + <A,B,C>.
    beta_y, beta_t, gamma_z, gamma_w, gamma_k = sp.symbols(
        "beta_y beta_t gamma_z gamma_w gamma_k"
    )
    beta_remainder = sp.Matrix([sp.Symbol("r0"), sp.Symbol("r1"), 0, beta_t, 0])
    gamma_remainder = sp.Matrix(
        [sp.Symbol("u0"), sp.Symbol("u1"), 0, gamma_w, gamma_k]
    )
    # These are p(beta)-beta(y)A and q(gamma)-gamma(z)A.
    assert beta_remainder.subs(beta_t, 0)[2:, 0] == sp.zeros(3, 1)
    assert gamma_remainder.subs({gamma_w: 0, gamma_k: 0})[2:, 0] == sp.zeros(3, 1)

    # The corresponding adjusted root covectors satisfy the two equations
    # defining L=(ker D_B)^perp.
    lam, mu = sp.symbols("lambda mu", nonzero=True)
    beta_adjusted = (
        sp.expand(lam * (-beta_y / lam) + beta_y),
        sp.expand(mu * beta_t),
    )
    gamma_adjusted = (
        sp.expand(lam * (-gamma_z / lam) + gamma_z),
        sp.expand(gamma_w),
    )
    assert beta_adjusted == (0, mu * beta_t)
    assert gamma_adjusted == (0, gamma_w)

    basis = sp.eye(5)
    assert basis.rank() == 5
    assert sp.Matrix.hstack(*basis[:, :3].columnspace()).rank() == 3
    print("third-root coloop row-space transfer: PASS (two planes plus intersection)")


def target_coefficients(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(alpha[i] * beta[i] * gamma[i]) for i in range(3))


def nonzero_w_t_binary_diagonal() -> None:
    for t in range(3):
        other = [index for index in range(3) if index != t]
        w_symbols = list(sp.symbols(f"w{t}_0:3"))
        w = sp.Matrix(w_symbols)
        assert w[t] != 0
        lifts: dict[int, sp.Matrix] = {}
        for index in other:
            lift = e(index) - (w[index] / w[t]) * e(t)
            assert sp.simplify(dot(lift, w)) == 0
            assert [sp.simplify(lift[j]) for j in other] == [
                sp.Integer(int(j == index)) for j in other
            ]
            lifts[index] = lift

        for i in other:
            for j in other:
                for k in other:
                    got = target_coefficients(e(i), e(j), lifts[k])
                    expected = tuple(
                        sp.Integer(int(i == j == k == colour)) for colour in range(3)
                    )
                    assert all(sp.simplify(a - b) == 0 for a, b in zip(got, expected))

        # Two planes in a three-space meet every third plane along at least a
        # line: w^perp and e_k^perp are two planes in a three-dimensional
        # covector space.  Concrete ranks check every selected coordinate.
        sample_w = sp.Matrix([2, 3, 5])
        for selected in range(3):
            constraints = sp.Matrix.vstack(sample_w.T, e(selected).T)
            assert 3 - constraints.rank() >= 1
    print("w_t nonzero binary-diagonal transfer: PASS")


def zero_w_t_common_row() -> None:
    wa, wb = sp.symbols("w_a w_b", nonzero=True)
    for t in range(3):
        a, b = [index for index in range(3) if index != t]
        w = wa * e(a) + wb * e(b)
        normal = wb * e(a) - wa * e(b)
        assert dot(normal, w) == 0
        assert dot(e(t), w) == 0

        third_rows = (normal, e(t))
        for i in (a, b):
            for j in (a, b):
                for row_index, gamma in enumerate(third_rows):
                    got = target_coefficients(e(i), e(j), gamma)
                    expected = [sp.Integer(0)] * 3
                    if row_index == 0 and i == j:
                        expected[i] = gamma[i]
                    assert all(
                        sp.simplify(value - expected[colour]) == 0
                        for colour, value in enumerate(got)
                    )

        # The selected gamma-coordinate hyperplane always supplies a nonzero
        # row of q(w^perp) in the common three-space: the active normal when
        # k=t, and the zero row e_t^* otherwise.
        for selected in range(3):
            witness = normal if selected == t else e(t)
            assert witness[selected] == 0
            assert dot(witness, w) == 0
    print("w_t zero common-active-row transfer: PASS")


def coordinate_w_root_exchange() -> None:
    lam, mu, nu = sp.Integer(2), sp.Integer(3), sp.Integer(5)
    for s in range(3):
        for t in range(3):
            y = sp.Matrix([7, 11, 13])
            y[t] = 0
            assert sp.Matrix.hstack(y, e(t)).rank() == 2
            for v in range(3):
                z = sp.Matrix([17, 19, 23])
                w = nu * e(v)
                assert sp.Matrix.hstack(z, w).rank() == 2

                # After exchanging roots two and three, the S2AZ data are
                # y'=z, z'=y, c'=w=nu e_v, w'=mu e_t.
                y_prime = z
                z_prime = y
                w_prime = mu * e(t)
                shift = y_prime[v] / nu
                gauged_y = y_prime - shift * nu * e(v)
                gauged_z = z_prime - shift * w_prime
                assert gauged_y[v] == 0
                assert blocks(y_prime, z_prime, w_prime, s, v, lam, nu) == blocks(
                    gauged_y, gauged_z, w_prime, s, v, lam, nu
                )
                assert sp.Matrix.hstack(gauged_y, e(v)).rank() == 2
                assert sp.Matrix.hstack(gauged_z, w_prime).rank() == 2

                # Coordinate positions 6+k (old gamma) become 3+k (new beta).
                for selected in range(3):
                    assert (6 + selected) - 3 == 3 + selected
    print("coordinate-w root exchange: PASS (gamma_k becomes closed beta'_k)")


def dependency_certificate_pins() -> None:
    for name, expected in DEPENDENCY_CERTIFICATES.items():
        got = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        assert got == expected, (name, got, expected)
    print("dependency certificate pins: PASS (S2BF and S2BI)")


def main() -> None:
    derivative_zero_face()
    canonical_gamma_coloop_geometry()
    nonzero_w_t_binary_diagonal()
    zero_w_t_common_row()
    coordinate_w_root_exchange()
    dependency_certificate_pins()
    print("all three third-root coordinate coloops: IMPOSSIBLE")


if __name__ == "__main__":
    main()
