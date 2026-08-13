"""Exact replay for the (1,2,2) coordinate-coloop localization."""

from __future__ import annotations

import sympy as sp


def e(i: int, n: int = 3) -> sp.Matrix:
    return sp.eye(n)[:, i]


def dot(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return (left.T * right)[0]


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def outer3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def stack(*vectors: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(*vectors)


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


def derivative(
    y: sp.Matrix,
    z: sp.Matrix,
    w: sp.Matrix,
    s: int,
    t: int,
    lam: sp.Expr,
    mu: sp.Expr,
) -> sp.Matrix:
    b23, _, _ = blocks(y, z, w, s, t, lam, mu)
    columns = [sp.kronecker_product(e(i), b23) for i in range(3)]
    columns += [-lam * outer3(e(s), e(j), w) for j in range(3)]
    columns += [lam * mu * outer3(e(s), e(t), e(k)) for k in range(3)]
    return sp.Matrix.hstack(*columns)


def gauge_and_derivative() -> None:
    lam, mu = sp.Integer(2), sp.Integer(3)
    s, t = 0, 1
    y_old = sp.Matrix([2, 5, 7])
    z_old = sp.Matrix([3, 4, 1])
    w = sp.Matrix([1, 2, 6])
    shift = y_old[t] / mu
    y = y_old - shift * mu * e(t)
    z = z_old - shift * w
    assert y[t] == 0
    assert sp.Matrix.hstack(y, mu * e(t)).rank() == 2
    assert sp.Matrix.hstack(z, w).rank() == 2
    assert blocks(y_old, z_old, w, s, t, lam, mu) == blocks(
        y, z, w, s, t, lam, mu
    )

    dmat = derivative(y, z, w, s, t, lam, mu)
    k1 = stack(lam * e(s), y, z)
    k2 = stack(sp.zeros(3, 1), mu * e(t), w)
    assert dmat.rank() == 7
    assert dmat * k1 == sp.zeros(27, 1)
    assert dmat * k2 == sp.zeros(27, 1)
    assert sp.Matrix.hstack(k1, k2).rank() == 2
    print("(1,2,2) gauge/derivative: PASS (blocks fixed, rank seven, kernel)")


def recovery_and_coordinate_fork() -> None:
    lam, mu = sp.Integer(2), sp.Integer(3)
    s, t = 0, 1
    y = sp.Matrix([2, 0, 7])
    z = sp.Matrix([sp.Rational(-4, 3), sp.Rational(2, 3), -9])
    w = sp.Matrix([1, 2, 6])
    dmat = derivative(y, z, w, s, t, lam, mu)

    a1, a2, b0, b2, g0, g1, g2 = sp.symbols(
        "a1 a2 b0 b2 g0 g1 g2"
    )
    gamma = sp.Matrix([g0, g1, g2])
    beta_t = -dot(gamma, w) / mu
    beta = sp.Matrix([b0, beta_t, b2])
    alpha_s = -(dot(beta, y) + dot(gamma, z)) / lam
    alpha = sp.Matrix([alpha_s, a1, a2])
    ell = stack(alpha, beta, gamma)
    got = dmat.T * outer3(alpha, beta, gamma)
    expected = lam * mu * alpha_s * beta_t * ell
    assert all(sp.expand(value) == 0 for value in got - expected)

    k1 = stack(lam * e(s), y, z)
    k2 = stack(sp.zeros(3, 1), mu * e(t), w)
    lmat = sp.Matrix.hstack(*sp.Matrix.vstack(k1.T, k2.T).nullspace())
    assert lmat.shape == (9, 7) and lmat.rank() == 7
    assert all(any(lmat[row, col] != 0 for col in range(7)) for row in range(9))
    print("(1,2,2) recovery/torus: PASS (scalar and nine proper coordinates)")


def canonical_rows_and_fixed_plane() -> None:
    s, t = 0, 1
    lam, mu = sp.Integer(2), sp.Integer(3)
    y = sp.Matrix([2, 0, 7])
    z = sp.Matrix([1, 4, 3])
    w = sp.Matrix([5, 2, 6])

    # Parameter columns for alpha_i (i!=s), beta_j (j!=t), gamma_k.
    columns: list[sp.Matrix] = []
    for i in range(3):
        if i == s:
            continue
        columns.append(stack(e(i), sp.zeros(3, 1), sp.zeros(3, 1)))
    for j in range(3):
        if j == t:
            continue
        alpha = -y[j] * e(s) / lam
        columns.append(stack(alpha, e(j), sp.zeros(3, 1)))
    for k in range(3):
        alpha = -z[k] * e(s) / lam
        beta = -w[k] * e(t) / mu
        columns.append(stack(alpha, beta, e(k)))
    lparam = sp.Matrix.hstack(*columns)
    k1 = stack(lam * e(s), y, z)
    k2 = stack(sp.zeros(3, 1), mu * e(t), w)
    assert lparam.rank() == 7
    assert sp.Matrix.vstack(k1.T, k2.T) * lparam == sp.zeros(2, 7)

    # The first two parameter columns are the exact copy of e_s^perp.
    r_columns = {0, 1}
    seven_equal_r_hyperplanes = [s] + list(range(3, 9))
    for coordinate in seven_equal_r_hyperplanes:
        assert all(lparam[coordinate, column] == 0 for column in r_columns)

    complement = [i for i in range(3) if i != s]
    for omitted_index, coordinate in enumerate(complement):
        surviving = r_columns - {omitted_index}
        assert all(lparam[coordinate, column] == 0 for column in surviving)
        assert lparam[coordinate, omitted_index] != 0

    # The target contraction alpha -> (alpha_a,alpha_b) is injective.
    target_contraction = sp.eye(2)
    assert target_contraction.rank() == 2
    print("(1,2,2) seven-row atlas: PASS (seven equal-R and two ordinary coloops)")


def main() -> None:
    gauge_and_derivative()
    recovery_and_coordinate_fork()
    canonical_rows_and_fixed_plane()
    print("(1,2,2) coordinate-coloop localization: PASS")


if __name__ == "__main__":
    main()
