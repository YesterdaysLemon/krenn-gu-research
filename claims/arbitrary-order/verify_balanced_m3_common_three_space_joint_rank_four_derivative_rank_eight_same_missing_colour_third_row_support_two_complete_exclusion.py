#!/usr/bin/env python3
"""Exact replay for the S2BW support-two third-row exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp

N = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(N)


def e3(index: int) -> sp.Matrix:
    return sp.eye(N)[:, index]


def tensor_index(i: int, j: int, k: int) -> int:
    return N * N * i + N * j + k


def tensor3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[tensor_index(i, j, k)] = a[i] * b[j] * c[k]
    return out


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[tensor_index(i, j, k)] = C[i, j] * c[k]
    return out


def derivative_value(
    a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, w: sp.Matrix, C: sp.Matrix
) -> sp.Matrix:
    return tensor3(a, e3(T_COLOUR), w) - tensor3(
        e3(S_COLOUR), b, w
    ) + c_tensor(C, c)


def derivative_matrix(w: sp.Matrix, C: sp.Matrix) -> sp.Matrix:
    zero = sp.zeros(N, 1)
    columns = []
    for i in range(N):
        columns.append(derivative_value(e3(i), zero, zero, w, C))
    for i in range(N):
        columns.append(derivative_value(zero, e3(i), zero, w, C))
    for i in range(N):
        columns.append(derivative_value(zero, zero, e3(i), w, C))
    return sp.Matrix.hstack(*columns)


def contract_first(tensor: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [tensor[tensor_index(D_COLOUR, j, k)] for j, k in product(range(N), repeat=2)]
    )


def contract_eta(tensor: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(eta[k] * tensor[tensor_index(i, j, k)] for k in range(N))
            for i, j in product(range(N), repeat=2)
        ]
    )


def joined(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    return a.col_join(b).col_join(c)


def check_three_affine_corrections() -> None:
    d, s, t = e3(D_COLOUR), e3(S_COLOUR), e3(T_COLOUR)
    zero = sp.zeros(N, 1)
    eta = s + 2 * t
    w = s + t
    delta = (eta.T * w)[0]
    assert delta == 3
    C = sp.Matrix([[2, 0, 0], [0, 5, 7], [0, 11, 13]])
    D = derivative_matrix(w, C)
    syzygy = joined(s, t, zero)
    assert D.rank() == 8
    kernel = D.nullspace()
    assert len(kernel) == 1
    assert sp.Matrix.hstack(kernel[0], syzygy).rank() == 1

    constraints = sp.Matrix.vstack(
        sp.Matrix.hstack(*(contract_first(D[:, j]) for j in range(3 * N))),
        sp.Matrix.hstack(*(contract_eta(D[:, j], eta) for j in range(3 * N))),
    )
    assert constraints.rank() == 8
    affine_kernel = constraints.nullspace()
    assert len(affine_kernel) == 1
    assert sp.Matrix.hstack(affine_kernel[0], syzygy).rank() == 1

    rhs_d = sp.Matrix.vstack(
        -sp.kronecker_product(d, d), sp.zeros(N**2, 1)
    )
    vertical_d = joined(zero, zero, -sp.Rational(1, 2) * d)
    assert constraints * vertical_d == rhs_d

    rhs_s = sp.Matrix.vstack(
        sp.zeros(N**2, 1), -sp.kronecker_product(s, s)
    )
    split_s = joined(zero, sp.Rational(1, delta) * s, zero)
    assert constraints * split_s == rhs_s

    rhs_t = sp.Matrix.vstack(
        sp.zeros(N**2, 1), -2 * sp.kronecker_product(t, t)
    )
    split_t = joined(-sp.Rational(2, delta) * t, zero, zero)
    assert constraints * split_t == rhs_t

    forced = sp.Matrix.hstack(syzygy, vertical_d, split_s, split_t)
    assert forced.rank() == 4
    assert forced[2 * N :, :].rank() == 1
    assert forced[:N, :].rank() == 2
    assert forced[N : 2 * N, :].rank() == 2


def check_symbolic_tangent_representatives() -> None:
    """Replay the quotient solutions without fixing the nonzero scalars."""

    d, s, t = e3(D_COLOUR), e3(S_COLOUR), e3(T_COLOUR)
    zero = sp.zeros(N, 1)
    delta, eta_s, eta_t, kappa = sp.symbols(
        "delta eta_s eta_t kappa", nonzero=True
    )
    vertical = joined(zero, zero, -d / kappa)
    split_s = joined(zero, eta_s * s / delta, zero)
    split_t = joined(-eta_t * t / delta, zero, zero)
    assert sp.Matrix.hstack(joined(s, t, zero), vertical, split_s, split_t).rank() == 4


def main() -> None:
    check_three_affine_corrections()
    check_symbolic_tangent_representatives()
    print(
        "S2BW primary replay passed: three pure-target affine systems, forced "
        "four-space basis, and third-projection rank-one contradiction."
    )


if __name__ == "__main__":
    main()
