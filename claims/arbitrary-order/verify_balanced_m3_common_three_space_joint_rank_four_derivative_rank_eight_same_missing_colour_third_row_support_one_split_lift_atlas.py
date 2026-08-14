#!/usr/bin/env python3
"""Exact replay for the S2BT support-one split-lift atlas."""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations, product

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


def contract_first(tensor: sp.Matrix, colour: int) -> sp.Matrix:
    return sp.Matrix(
        [tensor[root_index(colour, j, k)] for j, k in product(range(N), repeat=2)]
    )


def contract_third(tensor: sp.Matrix, colour: int) -> sp.Matrix:
    return sp.Matrix(
        [tensor[root_index(i, j, colour)] for i, j in product(range(N), repeat=2)]
    )


def split_root(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return v[:N, :], v[N : 2 * N, :], v[2 * N :, :]


def root_permanent(u: sp.Matrix, v: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    triples = [split_root(q) for q in (u, v, z)]
    out = sp.zeros(N**3, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            triples[sigma[0]][0], triples[sigma[1]][1], triples[sigma[2]][2]
        )
    return out


def joined(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    return a.col_join(b).col_join(c)


def isolated_C() -> sp.Matrix:
    return sp.Matrix([[2, 0, 0], [0, 1, 2], [0, 3, 5]])


def check_affine_contraction_rigidity() -> None:
    """The two contraction systems have only the asserted syzygy freedom."""

    zero = sp.zeros(N, 1)
    s = e3(S_COLOUR)
    d = e3(D_COLOUR)
    C = isolated_C()
    w = d + 5 * s + 7 * e3(T_COLOUR)

    for y in (2 * s + 3 * e3(T_COLOUR), s):
        D = derivative_matrix(y, w, C)
        assert D.rank() == 8
        syzygy = joined(s, y, zero)
        kernel = D.nullspace()
        assert len(kernel) == 1
        assert sp.Matrix.hstack(kernel[0], syzygy).rank() == 1

        contracted = sp.Matrix.vstack(
            sp.Matrix.hstack(
                *(contract_first(D[:, j], D_COLOUR) for j in range(3 * N))
            ),
            sp.Matrix.hstack(
                *(contract_third(D[:, j], S_COLOUR) for j in range(3 * N))
            ),
        )
        assert contracted.rank() == 8
        contracted_kernel = contracted.nullspace()
        assert len(contracted_kernel) == 1
        assert sp.Matrix.hstack(contracted_kernel[0], syzygy).rank() == 1

        rhs_d = sp.Matrix.vstack(
            -sp.kronecker_product(d, d), sp.zeros(N**2, 1)
        )
        vertical_d = joined(zero, zero, -sp.Rational(1, 2) * d)
        assert contracted * vertical_d == rhs_d

        rhs_s = sp.Matrix.vstack(
            sp.zeros(N**2, 1), -sp.kronecker_product(s, s)
        )
        split_s = joined(zero, sp.Rational(1, 5) * s, zero)
        assert contracted * split_s == rhs_s


def nonaligned_data() -> tuple[sp.Matrix, sp.Matrix, list[sp.Matrix], sp.Matrix, sp.Matrix]:
    zero = sp.zeros(N, 1)
    s, d, t = e3(S_COLOUR), e3(D_COLOUR), e3(T_COLOUR)
    y = 2 * s + 3 * t
    a = 5 * s + 7 * t
    w = s
    C = isolated_C()
    K = [
        joined(s, y, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(a, zero, t),
    ]
    return C, w, K, y, a


def aligned_data() -> tuple[sp.Matrix, sp.Matrix, list[sp.Matrix], int, int, int]:
    zero = sp.zeros(N, 1)
    s, d, t = e3(S_COLOUR), e3(D_COLOUR), e3(T_COLOUR)
    lam, alpha, beta = 4, 2, 3
    C = isolated_C()
    K = [
        joined(s, lam * s, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(alpha * t, beta * t, t),
    ]
    return C, s, K, lam, alpha, beta


def nonzero_products(K: list[sp.Matrix]) -> dict[tuple[int, int, int], sp.Matrix]:
    found = {}
    for indices in combinations_with_replacement(range(4), 3):
        value = root_permanent(*(K[i] for i in indices))
        if value != sp.zeros(N**3, 1):
            found[indices] = value
    return found


def root_box() -> sp.Matrix:
    s, t, d = e3(S_COLOUR), e3(T_COLOUR), e3(D_COLOUR)
    return sp.Matrix.hstack(
        *(tensor3(a, b, c) for a, b, c in product((s, t), (s, t), (d, t)))
    )


def check_common_incidence(
    C: sp.Matrix, w: sp.Matrix, K: list[sp.Matrix], y: sp.Matrix
) -> tuple[sp.Matrix, sp.Matrix]:
    D = derivative_matrix(y, w, C)
    Kmat = sp.Matrix.hstack(*K)
    U = D * sp.Matrix.hstack(*K[1:])
    assert D.rank() == 8
    kernel = D.nullspace()
    assert len(kernel) == 1
    assert sp.Matrix.hstack(kernel[0], K[0]).rank() == 1
    assert Kmat.rank() == 4
    assert U.rank() == 3
    assert D * K[0] == sp.zeros(N**3, 1)
    for start in (0, N, 2 * N):
        assert Kmat[start : start + N, :].rank() == 2
    L = root_box()
    assert L.rank() == 8
    assert U.row_join(L).rank() == 11

    d = e3(D_COLOUR)
    C_bar = C - C[D_COLOUR, D_COLOUR] * d * d.T
    assert D * K[1] == c_tensor(C, d)
    assert D * K[1] == (
        C[D_COLOUR, D_COLOUR] * tensor3(d, d, d) + c_tensor(C_bar, d)
    )
    return D, U


def check_nonaligned_root_box() -> None:
    C, w, K, y, a = nonaligned_data()
    s, d, t = e3(S_COLOUR), e3(D_COLOUR), e3(T_COLOUR)
    expected = {
        (0, 0, 1): 2 * tensor3(s, y, d),
        (0, 0, 3): 2 * tensor3(s, y, t),
        (0, 1, 2): -tensor3(s, s, d),
        (0, 1, 3): tensor3(a, y, d),
        (0, 2, 3): -tensor3(s, s, t),
        (0, 3, 3): 2 * tensor3(a, y, t),
        (1, 2, 3): -tensor3(a, s, d),
        (2, 3, 3): -2 * tensor3(a, s, t),
    }
    found = nonzero_products(K)
    assert found == expected
    assert sp.Matrix.hstack(*found.values()).rank() == 8
    check_common_incidence(C, w, K, y)


def check_aligned_root_box() -> None:
    C, w, K, lam, alpha, beta = aligned_data()
    s, d, t = e3(S_COLOUR), e3(D_COLOUR), e3(T_COLOUR)
    expected = {
        (0, 0, 1): 2 * lam * tensor3(s, s, d),
        (0, 0, 3): 2 * lam * tensor3(s, s, t),
        (0, 1, 2): -tensor3(s, s, d),
        (0, 1, 3): beta * tensor3(s, t, d)
        + alpha * lam * tensor3(t, s, d),
        (0, 2, 3): -tensor3(s, s, t),
        (0, 3, 3): 2 * beta * tensor3(s, t, t)
        + 2 * alpha * lam * tensor3(t, s, t),
        (1, 2, 3): -alpha * tensor3(t, s, d),
        (1, 3, 3): 2 * alpha * beta * tensor3(t, t, d),
        (2, 3, 3): -2 * alpha * tensor3(t, s, t),
        (3, 3, 3): 6 * alpha * beta * tensor3(t, t, t),
    }
    found = nonzero_products(K)
    assert found == expected
    assert sp.Matrix.hstack(*found.values()).rank() == 8
    check_common_incidence(C, w, K, lam * s)


def check_symbolic_tables() -> None:
    """Replay both tables before any rational specialization."""

    zero = sp.zeros(N, 1)
    s, d, t = e3(S_COLOUR), e3(D_COLOUR), e3(T_COLOUR)
    y_s, y_t, a_s, a_t = sp.symbols("y_s y_t a_s a_t", nonzero=True)
    y = y_s * s + y_t * t
    a = a_s * s + a_t * t
    nonaligned = [
        joined(s, y, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(a, zero, t),
    ]
    assert nonzero_products(nonaligned)[(0, 1, 3)] == tensor3(a, y, d)
    assert nonzero_products(nonaligned)[(2, 3, 3)] == -2 * tensor3(a, s, t)

    lam, alpha, beta = sp.symbols("lambda alpha beta", nonzero=True)
    aligned = [
        joined(s, lam * s, zero),
        joined(zero, zero, d),
        joined(zero, -s, zero),
        joined(alpha * t, beta * t, t),
    ]
    found = nonzero_products(aligned)
    assert found[(0, 1, 3)] == (
        beta * tensor3(s, t, d) + alpha * lam * tensor3(t, s, d)
    )
    assert found[(3, 3, 3)] == 6 * alpha * beta * tensor3(t, t, t)


def main() -> None:
    check_affine_contraction_rigidity()
    check_symbolic_tables()
    check_nonaligned_root_box()
    check_aligned_root_box()
    print(
        "S2BT primary replay passed: vertical d/s lifts; exhaustive aligned/"
        "nonaligned K atlases; exact 8-dimensional root boxes and quotient."
    )


if __name__ == "__main__":
    main()
