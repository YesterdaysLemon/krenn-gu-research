#!/usr/bin/env python3
"""Exact replay for the S2BS coordinate split-lift exclusion."""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations, product

import sympy as sp

N = 3


def e3(i: int) -> sp.Matrix:
    return sp.eye(N)[:, i]


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
    a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, C: sp.Matrix
) -> sp.Matrix:
    return tensor3(a, e3(2), e3(1)) - tensor3(e3(1), b, e3(1)) + c_tensor(C, c)


def derivative_matrix(C: sp.Matrix) -> sp.Matrix:
    zero = sp.zeros(N, 1)
    columns = []
    for i in range(N):
        columns.append(derivative_value(e3(i), zero, zero, C))
    for i in range(N):
        columns.append(derivative_value(zero, e3(i), zero, C))
    for i in range(N):
        columns.append(derivative_value(zero, zero, e3(i), C))
    return sp.Matrix.hstack(*columns)


def split_root(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return v[:N, :], v[N : 2 * N, :], v[2 * N :, :]


def root_permanent(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    triples = [split_root(z) for z in (u, v, w)]
    out = sp.zeros(N**3, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            triples[sigma[0]][0], triples[sigma[1]][1], triples[sigma[2]][2]
        )
    return out


def canonical_cell() -> tuple[sp.Matrix, list[sp.Matrix], sp.Matrix]:
    C = e3(0) * e3(0).T + e3(1) * e3(1).T
    zero = sp.zeros(N, 1)
    k0 = e3(1).col_join(e3(2)).col_join(zero)
    k1 = zero.col_join(zero).col_join(e3(0))
    k2 = zero.col_join(-e3(1)).col_join(zero)
    k3 = e3(2).col_join(zero).col_join(e3(2))
    return C, [k0, k1, k2, k3], derivative_matrix(C)


def check_derivative_and_incidence() -> None:
    C, K, D = canonical_cell()
    Kmat = sp.Matrix.hstack(*K)
    DK = D * Kmat
    assert D.rank() == 8
    assert D.nullspace() == [K[0]]
    assert Kmat.rank() == 4
    assert DK.rank() == 3
    assert DK[:, 0] == sp.zeros(N**3, 1)
    assert DK[:, 1] == c_tensor(C, e3(0))
    assert DK[:, 2] == tensor3(e3(1), e3(1), e3(1))
    assert DK[:, 3] == tensor3(e3(2), e3(2), e3(1)) + c_tensor(C, e3(2))
    for start in (0, N, 2 * N):
        assert Kmat[start : start + N, :].rank() == 2


EXPECTED = {
    (0, 0, 1): 2 * tensor3(e3(1), e3(2), e3(0)),
    (0, 0, 3): 2 * tensor3(e3(1), e3(2), e3(2)),
    (0, 1, 2): -tensor3(e3(1), e3(1), e3(0)),
    (0, 1, 3): tensor3(e3(2), e3(2), e3(0)),
    (0, 2, 3): -tensor3(e3(1), e3(1), e3(2)),
    (0, 3, 3): 2 * tensor3(e3(2), e3(2), e3(2)),
    (1, 2, 3): -tensor3(e3(2), e3(1), e3(0)),
    (2, 3, 3): -2 * tensor3(e3(2), e3(1), e3(2)),
}


def check_eight_coefficient_quotient() -> None:
    _, K, D = canonical_cell()
    nonzero = {}
    for indices in combinations_with_replacement(range(4), 3):
        value = root_permanent(*(K[i] for i in indices))
        if value != sp.zeros(N**3, 1):
            nonzero[indices] = value
    assert nonzero == EXPECTED

    M = sp.Matrix.hstack(*nonzero.values())
    U = D * sp.Matrix.hstack(*K[1:])
    assert M.rank() == 8
    assert U.rank() == 3
    assert U.row_join(M).rank() == 11

    ddd = tensor3(e3(0), e3(0), e3(0))
    sss = tensor3(e3(1), e3(1), e3(1))
    ttt = tensor3(e3(2), e3(2), e3(2))
    ssd = tensor3(e3(1), e3(1), e3(0))
    assert ddd + ssd == U[:, 0]
    assert sss == U[:, 1]
    assert sp.Matrix.hstack(U, ttt).rank() != U.rank()
    assert EXPECTED[(0, 1, 2)] == -ssd
    assert EXPECTED[(0, 3, 3)] == 2 * ttt


S = 2


def source_basis(block: int, coordinate: int) -> sp.Matrix:
    out = sp.zeros(3 * S, 1)
    out[S * block + coordinate] = 1
    return out


def source_split(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return v[:S, :], v[S : 2 * S, :], v[2 * S :, :]


def source_tensor(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(S**3, 1)
    for i, j, k in product(range(S), repeat=3):
        out[S * S * i + S * j + k] = a[i] * b[j] * c[k]
    return out


def polarized(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    triples = [source_split(z) for z in (u, v, w)]
    out = sp.zeros(S**3, 1)
    for sigma in permutations(range(3)):
        out += source_tensor(
            triples[sigma[0]][0], triples[sigma[1]][1], triples[sigma[2]][2]
        )
    return out


def check_two_source_obstruction_identities() -> None:
    lam, mu, nu = sp.symbols("lambda mu nu")
    x = source_basis(0, 0)
    y = source_basis(1, 0)
    z = source_basis(2, 0)
    c = source_basis(2, 1)
    w = x - y
    v = x + y
    u = lam * w + z
    r = mu * w + c
    q = nu * w
    xyz = source_tensor(x[:S, :], y[S : 2 * S, :], z[2 * S :, :])
    xyc = source_tensor(x[:S, :], y[S : 2 * S, :], c[2 * S :, :])
    assert polarized(u, v, v) == 2 * xyz
    assert polarized(u, u, v) == sp.zeros(S**3, 1)
    assert polarized(u, r, v) == sp.zeros(S**3, 1)
    assert polarized(u, q, v) == sp.zeros(S**3, 1)
    assert polarized(q, v, v) == sp.zeros(S**3, 1)
    assert all(
        sp.expand(value) == 0
        for value in polarized(u, u, r) + 2 * lam**2 * xyc + 4 * lam * mu * xyz
    )
    r_forced = mu * w - 2 * mu * z
    target = polarized(w + z, r_forced, q)
    assert all(
        value == 0 for i, value in enumerate(target) if i != S * S * 0
    )


def check_three_source_obstruction_identities() -> None:
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    x = source_basis(0, 0)
    y = source_basis(1, 0)
    z = source_basis(2, 0)
    v = x + y + z
    u = alpha * x + beta * y + gamma * z
    xyz = source_tensor(x[:S, :], y[S : 2 * S, :], z[2 * S :, :])
    assert polarized(u, v, v) == 2 * (alpha + beta + gamma) * xyz
    assert polarized(u, u, v) == 2 * (
        alpha * beta + alpha * gamma + beta * gamma
    ) * xyz

    A, B, C = sp.symbols("A B C")
    h = A * x + B * y + C * z
    expected_mixed = (
        (beta + gamma) * A
        + (alpha + gamma) * B
        + (alpha + beta) * C
    ) * xyz
    assert all(sp.expand(value) == 0 for value in polarized(u, h, v) - expected_mixed)

    a = source_basis(0, 1)
    lam, mu = sp.symbols("lambda mu")
    pure_u = a
    r = A * x + lam * y - lam * z
    q = mu * y - mu * z
    assert polarized(pure_u, r, v) == sp.zeros(S**3, 1)
    assert polarized(pure_u, q, v) == sp.zeros(S**3, 1)
    assert polarized(q, v, v) == sp.zeros(S**3, 1)
    expected = -2 * lam * mu * xyz
    assert polarized(r, q, v) == expected
    assert polarized(pure_u, A * x, q) == sp.zeros(S**3, 1)


def main() -> None:
    check_derivative_and_incidence()
    check_eight_coefficient_quotient()
    check_two_source_obstruction_identities()
    check_three_source_obstruction_identities()
    print(
        "S2BS primary replay passed: rank-eight split lift; 8-term quotient; "
        "two-/three-source eight-product obstruction identities."
    )


if __name__ == "__main__":
    main()
