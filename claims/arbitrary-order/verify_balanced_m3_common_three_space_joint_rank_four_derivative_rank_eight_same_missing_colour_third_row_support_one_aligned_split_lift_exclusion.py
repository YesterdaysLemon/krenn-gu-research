#!/usr/bin/env python3
"""Exact replay for the S2BU aligned split-lift exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(N)


def e3(index: int) -> sp.Matrix:
    return sp.eye(N)[:, index]


def root_index(i: int, j: int, k: int) -> int:
    return N * N * i + N * j + k


def tensor3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[root_index(i, j, k)] = a[i] * b[j] * c[k]
    return out


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[root_index(i, j, k)] = C[i, j] * c[k]
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


def joined(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    return a.col_join(b).col_join(c)


def root_box() -> sp.Matrix:
    d, s, t = e3(D_COLOUR), e3(S_COLOUR), e3(T_COLOUR)
    return sp.Matrix.hstack(
        *(tensor3(a, b, c) for a, b, c in product((s, t), (s, t), (d, t)))
    )


def check_arbitrary_w_direct_quotient() -> None:
    d, s, t = e3(D_COLOUR), e3(S_COLOUR), e3(T_COLOUR)
    zero = sp.zeros(N, 1)
    lam, alpha, beta = map(sp.Integer, (2, 3, 5))
    wd, ws, wt = map(sp.Integer, (7, 11, 13))
    w = wd * d + ws * s + wt * t
    y = lam * s
    C = sp.Matrix([[17, 0, 0], [0, 19, 23], [0, 29, 31]])
    K = [
        joined(s, y, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(alpha * t, beta * t, t),
    ]
    D = derivative_matrix(y, w, C)
    Kmat = sp.Matrix.hstack(*K)
    U = D * sp.Matrix.hstack(*K[1:])
    L = root_box()

    assert D.rank() == 8
    assert Kmat.rank() == 4
    assert U.rank() == 3
    assert L.rank() == 8
    assert U.row_join(L).rank() == 11
    assert D * K[0] == sp.zeros(N**3, 1)
    assert D * K[1] == c_tensor(C, d)
    assert D * K[2] == tensor3(s, s, w)
    tangent = lam * alpha * tensor3(t, s, w) - beta * tensor3(s, t, w)
    assert D * K[3] == tangent + c_tensor(C, t)

    C_bar = C - C[D_COLOUR, D_COLOUR] * d * d.T
    rep_d = -sp.Rational(1, 17) * c_tensor(C_bar, d)
    assert tensor3(d, d, d) - rep_d == sp.Rational(1, 17) * D * K[1]

    rep_s = -sp.Rational(wd, ws) * tensor3(s, s, d) - sp.Rational(
        wt, ws
    ) * tensor3(s, s, t)
    assert tensor3(s, s, s) - rep_s == sp.Rational(1, ws) * D * K[2]


SOURCE_WIDTH = 2


def source_index(i: int, j: int, k: int) -> int:
    return SOURCE_WIDTH * SOURCE_WIDTH * i + SOURCE_WIDTH * j + k


def source_tensor(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(SOURCE_WIDTH**3, 1)
    for i, j, k in product(range(SOURCE_WIDTH), repeat=3):
        out[source_index(i, j, k)] = a[i] * b[j] * c[k]
    return out


def source_split(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    n = SOURCE_WIDTH
    return v[:n, :], v[n : 2 * n, :], v[2 * n :, :]


def polarized(u: sp.Matrix, v: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    roots = [source_split(value) for value in (u, v, z)]
    out = sp.zeros(SOURCE_WIDTH**3, 1)
    for sigma in permutations(range(3)):
        out += source_tensor(
            roots[sigma[0]][0], roots[sigma[1]][1], roots[sigma[2]][2]
        )
    return out


def generic_source_vector(prefix: str) -> sp.Matrix:
    return sp.Matrix(sp.symbols(f"{prefix}0:{3 * SOURCE_WIDTH}"))


def assert_symbolic_zero(value: sp.Matrix) -> None:
    assert all(sp.expand(entry) == 0 for entry in value)


def check_four_root_row_coefficients() -> None:
    lam, alpha, beta = sp.symbols("lambda alpha beta", nonzero=True)
    g0, g1, g2, g3 = (generic_source_vector(f"g{i}_") for i in range(4))
    r_s, r_t = g0, alpha * g3
    p_s, p_t = lam * g0 - g2, beta * g3
    q_d, q_t = g1, g3

    assert_symbolic_zero(
        polarized(r_s, p_t, q_t) - beta * polarized(g0, g3, g3)
    )
    assert_symbolic_zero(
        polarized(r_t, p_s, q_t)
        - alpha * lam * polarized(g0, g3, g3)
        + alpha * polarized(g2, g3, g3)
    )
    assert_symbolic_zero(
        polarized(r_t, p_t, q_t) - alpha * beta * polarized(g3, g3, g3)
    )
    assert_symbolic_zero(
        polarized(r_t, p_t, q_d) - alpha * beta * polarized(g1, g3, g3)
    )


def source_basis(block: int, coordinate: int) -> sp.Matrix:
    out = sp.zeros(3 * SOURCE_WIDTH, 1)
    out[SOURCE_WIDTH * block + coordinate] = 1
    return out


def check_segre_tangent_kernel() -> None:
    x = source_basis(0, 0)
    y = source_basis(1, 0)
    z = source_basis(2, 0)
    v = x + y + z
    target_t = source_tensor(x[:SOURCE_WIDTH, :], y[SOURCE_WIDTH : 2 * SOURCE_WIDTH, :], z[2 * SOURCE_WIDTH :, :])
    target_d = source_tensor(
        source_basis(0, 1)[:SOURCE_WIDTH, :],
        source_basis(1, 1)[SOURCE_WIDTH : 2 * SOURCE_WIDTH, :],
        source_basis(2, 1)[2 * SOURCE_WIDTH :, :],
    )

    assert polarized(v, v, v) == 6 * target_t
    phi = sp.Matrix.hstack(
        *(polarized(source_basis(block, coordinate), v, v) for block in range(3) for coordinate in range(SOURCE_WIDTH))
    )
    assert phi.rank() == 4
    assert len(phi.nullspace()) == 2
    assert phi * (x - y) == sp.zeros(SOURCE_WIDTH**3, 1)
    assert phi * (x - z) == sp.zeros(SOURCE_WIDTH**3, 1)
    assert phi.row_join(target_d).rank() == 5

    a0, b0, a1, b1, a2, b2 = sp.symbols("a0 b0 a1 b1 a2 b2")
    g0 = a0 * (x - y) + b0 * (x - z)
    g1 = a1 * (x - y) + b1 * (x - z)
    g2 = a2 * (x - y) + b2 * (x - z)
    assert sp.Matrix.hstack(g0, g1, g2, v).rank() <= 3


def main() -> None:
    check_arbitrary_w_direct_quotient()
    check_four_root_row_coefficients()
    check_segre_tangent_kernel()
    print(
        "S2BU primary replay passed: arbitrary-w direct root box; four forced "
        "coefficients; Segre-tangent kernel and independence contradiction."
    )


if __name__ == "__main__":
    main()
