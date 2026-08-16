#!/usr/bin/env python3
"""Exact replay for the S2BZ support-two mixed-cell exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3


def i2(a: int, b: int) -> int:
    return N * a + b


def i3(a: int, b: int, c: int) -> int:
    return N * N * a + N * b + c


def basis(i: int) -> sp.Matrix:
    return sp.eye(N)[:, i]


def outer2(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N * N, 1)
    for i, j in product(range(N), repeat=2):
        out[i2(i, j)] = a[i] * b[j]
    return out


def outer3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[i3(i, j, k)] = a[i] * b[j] * c[k]
    return out


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[i3(i, j, k)] = C[i, j] * c[k]
    return out


def derivative_value(
    x: sp.Matrix,
    y: sp.Matrix,
    w: sp.Matrix,
    C: sp.Matrix,
    a: sp.Matrix,
    b: sp.Matrix,
    c: sp.Matrix,
) -> sp.Matrix:
    return outer3(a, y, w) - outer3(x, b, w) + c_tensor(C, c)


def derivative_matrix(
    x: sp.Matrix, y: sp.Matrix, w: sp.Matrix, C: sp.Matrix
) -> sp.Matrix:
    zero = sp.zeros(N, 1)
    columns = [
        derivative_value(x, y, w, C, basis(i), zero, zero) for i in range(N)
    ]
    columns.extend(
        derivative_value(x, y, w, C, zero, basis(i), zero) for i in range(N)
    )
    columns.extend(
        derivative_value(x, y, w, C, zero, zero, basis(i)) for i in range(N)
    )
    return sp.Matrix.hstack(*columns)


def projection_matrix(vectors: list[sp.Matrix], block: int) -> sp.Matrix:
    return sp.Matrix.hstack(*(vector[block * N : (block + 1) * N, :] for vector in vectors))


def check_mixed_support_two_fixture() -> None:
    d, s, t = 0, 1, 2
    x, y = basis(s), basis(t)
    w = basis(s) + basis(t)
    C = basis(d) * basis(d).T
    D = derivative_matrix(x, y, w, C)
    assert D.rank() == 8

    n = x.col_join(y).col_join(sp.zeros(N, 1))
    h = basis(t).col_join(sp.zeros(N, 1)).col_join(sp.zeros(N, 1))
    v_d = sp.zeros(N, 1).col_join(basis(d)).col_join(basis(d))
    v_u = basis(t).col_join(basis(s)).col_join(basis(s) - basis(t))
    K = [n, h, v_d, v_u]
    K_matrix = sp.Matrix.hstack(*K)
    assert K_matrix.rank() == 4
    assert projection_matrix(K, 0).rank() == 2
    assert projection_matrix(K, 1).rank() == 3
    assert projection_matrix(K, 2).rank() == 2
    assert (D * K_matrix).rank() == 3

    zero = sp.zeros(N, 1)
    u0 = derivative_value(x, y, w, C, basis(t), zero, zero)
    assert u0 == outer3(basis(t), basis(t), w)
    assert u0 != sp.zeros(N**3, 1)

    eta = basis(s) + basis(t)
    assert eta[d] == 0
    assert eta[s] * eta[t] * eta.dot(w) != 0


def check_first_contraction_system() -> None:
    kappa = sp.symbols("kappa", nonzero=True)
    d = 0
    columns = []
    for colour in range(N):
        column = sp.zeros(N * N, 1)
        column[i2(d, colour)] = kappa
        columns.append(column)
    contraction = sp.Matrix.hstack(*columns)
    for source_colour in range(N):
        rhs = sp.zeros(N * N, 1)
        if source_colour == d:
            rhs[i2(d, d)] = -1
        solution = contraction.gauss_jordan_solve(rhs)[0]
        expected = sp.zeros(N, 1)
        if source_colour == d:
            expected[d] = -1 / kappa
        assert solution == expected


def check_incompatible_target_lines() -> None:
    for d, s, t in permutations(range(N)):
        diagonal_s = outer2(basis(s), basis(s))
        diagonal_t = outer2(basis(t), basis(t))
        assert sp.Matrix.hstack(diagonal_s, diagonal_t).rank() == 2

        # The T_s coefficient makes R a nonzero multiple of diagonal_s.
        sigma_s, eta_s, eta_w = sp.symbols(
            "sigma_s eta_s eta_w", nonzero=True
        )
        forced_r = -(eta_s / (eta_w * sigma_s)) * diagonal_s
        assert sp.Matrix.hstack(forced_r, diagonal_s).rank() == 1
        assert sp.Matrix.hstack(forced_r, diagonal_t).rank() == 2


def main() -> None:
    check_mixed_support_two_fixture()
    check_first_contraction_system()
    check_incompatible_target_lines()
    print(
        "S2BZ primary replay passed: rank-(2,3,2) fixture; one correction "
        "line; support-two contraction; incompatible diagonal root lines."
    )


if __name__ == "__main__":
    main()
