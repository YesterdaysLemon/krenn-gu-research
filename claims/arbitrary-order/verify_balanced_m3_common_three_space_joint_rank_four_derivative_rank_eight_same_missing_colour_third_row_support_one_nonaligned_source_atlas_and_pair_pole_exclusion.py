#!/usr/bin/env python3
"""Exact replay for the S2BV nonaligned source atlas and pair pole."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(N)


def e3(index: int) -> sp.Matrix:
    return sp.eye(N)[:, index]


def basis(block: int, coordinate: int) -> sp.Matrix:
    out = sp.zeros(3 * N, 1)
    out[N * block + coordinate] = 1
    return out


def tensor_index(i: int, j: int, k: int) -> int:
    return N * N * i + N * j + k


def tensor3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[tensor_index(i, j, k)] = a[i] * b[j] * c[k]
    return out


def split_source(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return v[:N, :], v[N : 2 * N, :], v[2 * N :, :]


def polarized(u: sp.Matrix, v: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    roots = [split_source(value) for value in (u, v, z)]
    out = sp.zeros(N**3, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            roots[sigma[0]][0], roots[sigma[1]][1], roots[sigma[2]][2]
        )
    return out


def joined(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    return a.col_join(b).col_join(c)


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[tensor_index(i, j, k)] = C[i, j] * c[k]
    return out


def derivative_value(
    a: sp.Matrix,
    b: sp.Matrix,
    c: sp.Matrix,
    y: sp.Matrix,
    w: sp.Matrix,
    C: sp.Matrix,
) -> sp.Matrix:
    return tensor3(a, y, w) - tensor3(e3(S_COLOUR), b, w) + c_tensor(C, c)


def derivative_matrix(y: sp.Matrix, w: sp.Matrix, C: sp.Matrix) -> sp.Matrix:
    zero = sp.zeros(N, 1)
    columns = []
    for i in range(N):
        columns.append(derivative_value(e3(i), zero, zero, y, w, C))
    for i in range(N):
        columns.append(derivative_value(zero, e3(i), zero, y, w, C))
    for i in range(N):
        columns.append(derivative_value(zero, zero, e3(i), y, w, C))
    return sp.Matrix.hstack(*columns)


def assert_symbolic_zero(value: sp.Matrix) -> None:
    assert all(sp.expand(entry) == 0 for entry in value)


def check_two_source_reduction_identities() -> None:
    """Replay the decisive equations in the two-source branch of Lemma 1."""

    x, y, z = basis(0, T_COLOUR), basis(1, T_COLOUR), basis(2, T_COLOUR)
    alpha, beta, mu = sp.symbols("alpha beta mu")
    root_shear = -alpha - beta
    v = x + y
    u = alpha * x + beta * y + z
    h = u + root_shear * v
    q = mu * (x - y)
    assert polarized(u, v, v) == 2 * tensor3(
        x[:N, :], y[N : 2 * N, :], z[2 * N :, :]
    )
    assert_symbolic_zero(polarized(h, u, v))
    assert polarized(q, v, v) == sp.zeros(N**3, 1)
    assert polarized(h, q, v) == sp.zeros(N**3, 1)

    off_z = basis(2, S_COLOUR)
    square = polarized(u, u, off_z)
    expected = 2 * alpha * beta * tensor3(
        x[:N, :], y[N : 2 * N, :], off_z[2 * N :, :]
    )
    assert_symbolic_zero(square - expected)


def check_three_source_reduction_identities() -> None:
    """Replay the off-base and pure-source forks of Lemma 1."""

    x, y, z = basis(0, T_COLOUR), basis(1, T_COLOUR), basis(2, T_COLOUR)
    off_x = basis(0, S_COLOUR)
    beta, gamma, shear = sp.symbols("beta gamma shear")
    v = x + y + z
    u = off_x + beta * y + gamma * z
    h = u + shear * v
    mixed = polarized(h, u, v)
    target_off = tensor3(
        off_x[:N, :], y[N : 2 * N, :], z[2 * N :, :]
    )
    target_base = tensor3(x[:N, :], y[N : 2 * N, :], z[2 * N :, :])
    expected = 2 * (
        (beta + gamma + shear) * target_off
        + (beta * gamma + shear * (beta + gamma)) * target_base
    )
    assert_symbolic_zero(mixed - expected)

    pure_u = basis(0, T_COLOUR)
    q = y - z
    r = basis(0, D_COLOUR)
    assert polarized(q, v, v) == sp.zeros(N**3, 1)
    assert polarized(pure_u, q, v) == sp.zeros(N**3, 1)
    assert polarized(v, pure_u, r) == sp.zeros(N**3, 1)
    assert polarized(pure_u, q, r) == sp.zeros(N**3, 1)


def canonical_source_rows() -> tuple[list[sp.Matrix], dict[str, sp.Symbol]]:
    x_t = basis(0, T_COLOUR)
    y_t = basis(1, T_COLOUR)
    z_d, z_s, z_t = (basis(2, colour) for colour in range(N))
    b, mu = sp.symbols("b mu", nonzero=True)
    c_d, c_s, c_t = sp.symbols("c_d c_s c_t")
    r_d, r_s, r_t = sp.symbols("r_d r_s r_t")
    c = c_d * z_d + c_s * z_s + c_t * z_t
    r = r_d * z_d + r_s * z_s + r_t * z_t
    u = sp.Rational(1, 2) * z_t
    q = mu * (x_t - y_t)
    v = x_t + y_t + c
    rows = [u, r, b * u - q, v]
    return rows, {
        "b": b,
        "mu": mu,
        "c_d": c_d,
        "c_s": c_s,
        "c_t": c_t,
        "r_d": r_d,
        "r_s": r_s,
        "r_t": r_t,
    }


def check_exact_empty_control() -> None:
    d, s, t = e3(D_COLOUR), e3(S_COLOUR), e3(T_COLOUR)
    zero = sp.zeros(N, 1)
    rows, symbols = canonical_source_rows()
    g0, g1, g2, g3 = rows
    b, mu = symbols["b"], symbols["mu"]

    K = [
        joined(s, b * s + t, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(t, zero, t),
    ]
    C = d * d.T
    D = derivative_matrix(b * s + t, s, C)
    Kmat = sp.Matrix.hstack(*K)
    assert D.rank() == 8
    assert Kmat.rank() == 4
    assert (D * Kmat).rank() == 3
    assert D * K[0] == sp.zeros(N**3, 1)
    assert D * K[1] == tensor3(d, d, d)
    assert D * K[2] == tensor3(s, s, s)
    assert D * K[3] == (
        b * tensor3(t, s, s) + tensor3(t, t, s) + tensor3(d, d, t)
    )

    r_s_row, r_t_row = g0, g3
    p_s_row, p_t_row = b * g0 - g2, g0
    q_d_row, q_t_row = g1, g3
    target_t = tensor3(e3(T_COLOUR), e3(T_COLOUR), e3(T_COLOUR))
    coefficients = {
        (S_COLOUR, S_COLOUR, D_COLOUR): polarized(r_s_row, p_s_row, q_d_row),
        (S_COLOUR, T_COLOUR, D_COLOUR): polarized(r_s_row, p_t_row, q_d_row),
        (T_COLOUR, S_COLOUR, D_COLOUR): polarized(r_t_row, p_s_row, q_d_row),
        (T_COLOUR, T_COLOUR, D_COLOUR): polarized(r_t_row, p_t_row, q_d_row),
        (S_COLOUR, S_COLOUR, T_COLOUR): polarized(r_s_row, p_s_row, q_t_row),
        (S_COLOUR, T_COLOUR, T_COLOUR): polarized(r_s_row, p_t_row, q_t_row),
        (T_COLOUR, S_COLOUR, T_COLOUR): polarized(r_t_row, p_s_row, q_t_row),
        (T_COLOUR, T_COLOUR, T_COLOUR): polarized(r_t_row, p_t_row, q_t_row),
    }
    for root, value in coefficients.items():
        if root == (T_COLOUR, T_COLOUR, T_COLOUR):
            assert_symbolic_zero(value - target_t)
        else:
            assert_symbolic_zero(value)

    rational_rows = [value.subs({symbol: index + 2 for index, symbol in enumerate(symbols.values())}) for value in rows]
    assert sp.Matrix.hstack(*rational_rows).rank() == 4
    assert_symbolic_zero(p_s_row - mu * (basis(0, T_COLOUR) - basis(1, T_COLOUR)))


def check_singletons_and_pair_poles() -> None:
    xd, xs, xt, yd, ys, yt, zd, zs, zt = sp.symbols(
        "x_d x_s x_t y_d y_s y_t z_d z_s z_t"
    )
    b, mu = sp.symbols("b mu", nonzero=True)
    cd, cs, ct, rd, rs, rt = sp.symbols("c_d c_s c_t r_d r_s r_t")
    c = cd * zd + cs * zs + ct * zt
    r = rd * zd + rs * zs + rt * zt
    ell = sp.Rational(1, 2) * b * zt
    target_d = xd * yd * zd
    target_s = xs * ys * zs

    singleton = sp.Matrix(
        [[0, 0, r], [-mu * xt, mu * yt, ell], [xt, yt, c]]
    )
    assert sp.factor(singleton.det()) == -2 * mu * r * xt * yt

    C_z = target_d / r
    C_x = (-target_s + (ell - mu * c) * C_z) / (2 * mu * xt)
    C_y = (target_s - (ell + mu * c) * C_z) / (2 * mu * yt)
    solution = sp.Matrix([C_x, C_y, C_z])
    residual = sp.Matrix([target_d, target_s, 0])
    assert_symbolic_zero(singleton * solution - residual)

    numerator_x = sp.expand(-r * target_s + (ell - mu * c) * target_d)
    numerator_y = sp.expand(r * target_s - (ell + mu * c) * target_d)
    variables = (xd, xs, xt, yd, ys, yt, zd, zs, zt)
    assert sp.Poly(numerator_x, *variables).degree(xt) == 0
    assert sp.Poly(numerator_y, *variables).degree(yt) == 0
    assert sp.expand(numerator_x + numerator_y + 2 * mu * c * target_d) == 0
    after_c_zero = sp.expand(numerator_x.subs({cd: 0, cs: 0, ct: 0}))
    assert after_c_zero != 0
    monomials = sp.Poly(after_c_zero, *variables).monoms()
    assert any(monomial[1] and monomial[4] for monomial in monomials)
    assert any(monomial[0] and monomial[3] for monomial in monomials)


def main() -> None:
    check_two_source_reduction_identities()
    check_three_source_reduction_identities()
    check_exact_empty_control()
    check_singletons_and_pair_poles()
    print(
        "S2BV primary replay passed: deformed source forks; exact nonaligned "
        "control; singleton determinant; unique pair lift and incompatible residues."
    )


if __name__ == "__main__":
    main()
