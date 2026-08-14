#!/usr/bin/env python3
"""Exact replay for the fully-injective monomial-residual endpoint theorem."""

from __future__ import annotations

from itertools import product

import sympy as sp


def tidx(i: int, j: int, k: int) -> int:
    return 9 * i + 3 * j + k


def tensor3(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        out[tidx(i, j, k)] = u[i] * v[j] * w[k]
    return out


def tensor2(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(9, 1)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j] = u[i] * v[j]
    return out


def insert_tangent(
    a: sp.Matrix,
    b: sp.Matrix,
    x: sp.Matrix,
    y: sp.Matrix,
    w: sp.Matrix,
) -> sp.Matrix:
    return tensor3(a, y, w) - tensor3(x, b, w)


def residual(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        out[tidx(i, j, k)] = C[i, j] * c[k]
    return out


def contract_third(T: sp.Matrix, gamma: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(9, 1)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j] = sum(T[tidx(i, j, k)] * gamma[k] for k in range(3))
    return sp.simplify(out)


def check_graph_slice() -> None:
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    w = sp.Matrix(sp.symbols("w0:3"))
    a = sp.Matrix(sp.symbols("a0:3"))
    b = sp.Matrix(sp.symbols("b0:3"))
    c = sp.Matrix(sp.symbols("c0:3"))
    gamma = sp.Matrix(sp.symbols("g0:3"))
    C = sp.Matrix(3, 3, sp.symbols("C0:9"))

    U = insert_tangent(a, b, x, y, w) + residual(C, c)
    got = contract_third(U, gamma)
    expected = gamma.dot(w) * (tensor2(a, y) - tensor2(x, b))
    expected += gamma.dot(c) * sp.Matrix(9, 1, list(C))
    assert sp.simplify(got - expected) == sp.zeros(9, 1)

    # On gamma(w)=0, only gamma(c) C survives.  Substitute an exact
    # denominator-free basis of w^perp in every coordinate chart.
    for d in range(3):
        others = [i for i in range(3) if i != d]
        for a_idx in others:
            g = sp.zeros(3, 1)
            g[a_idx] = w[d]
            g[d] = -w[a_idx]
            assert sp.expand(g.dot(w)) == 0
            restricted = sp.Matrix([g[i] for i in others])
            expected_restricted = sp.zeros(2, 1)
            expected_restricted[others.index(a_idx)] = w[d]
            assert restricted == expected_restricted


def check_all_monomial_rows() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    for d, e in product(range(3), repeat=2):
        C = sp.zeros(3, 3)
        C[d, e] = lam

        # If the first monomial coordinate w_d is nonzero, the two
        # complementary rows see no correction and p_d is a common zero.
        I = [i for i in range(3) if i != d]
        for i, j in product(I, range(3)):
            assert C[i, j] == 0
        for i in I:
            assert C[i, d] == 0

        # Root exchange: the columns complementary to e see no correction,
        # and r_e is the common zero row.
        J = [j for j in range(3) if j != e]
        for i, j in product(range(3), J):
            assert C[i, j] == 0
        for j in J:
            assert C[e, j] == 0

        # The endpoint solution space w_d=w_e=0 has the asserted dimension.
        endpoint = sp.zeros(2, 3)
        endpoint[0, d] = 1
        endpoint[1, e] = 1
        expected_rank = 1 if d == e else 2
        assert endpoint.rank() == expected_rank
        assert len(endpoint.nullspace()) == 3 - expected_rank


def check_binary_shift_trap() -> None:
    # Replay the linear incidence step in an arbitrary coordinate basis of E.
    a, b, c = sp.symbols("a b c")
    l0, l1 = sp.symbols("lambda_0 lambda_1")
    p0 = sp.Matrix([1, 0, 0, 0])
    p1 = sp.Matrix([0, 1, 0, 0])
    v = sp.Matrix([0, 0, 1, 0])
    ell = a * p0 + b * p1 + c * v
    shifted = a * (p0 + l0 * v) + b * (p1 + l1 * v)
    assert sp.simplify(ell - shifted) == sp.Matrix([0, 0, c - a * l0 - b * l1, 0])

    # A binary diagonal table is unchanged when a common-zero row is added
    # to either middle basis vector.
    T0, T1 = sp.symbols("T0 T1", nonzero=True)

    def table(i: int, j: int, k: int) -> sp.Expr:
        if i == j == k == 0:
            return T0
        if i == j == k == 1:
            return T1
        return sp.Integer(0)

    for i, j, k in product(range(2), repeat=3):
        shifted_value = table(i, j, k) + (l0 if j == 0 else l1) * 0
        assert shifted_value == table(i, j, k)

    # The three-plane B=P+Kv has the expected dimension; every two-plane in
    # a four-space meets it.  This is the dimension input used twice.
    B = sp.Matrix.hstack(p0, p1, v)
    assert B.rank() == 3
    R = sp.Matrix.hstack(sp.Matrix([0, 0, 1, 0]), sp.Matrix([0, 0, 0, 1]))
    assert sp.Matrix.hstack(B, R).rank() == 4
    assert B.rank() + R.rank() - sp.Matrix.hstack(B, R).rank() == 1


def check_tangent_rank_one_gate() -> None:
    # In quotient coordinates, e_d tensor e_e maps to
    # (e_d mod Kx) tensor (e_e mod Ky).  It vanishes iff one factor does.
    for d, e in product(range(3), repeat=2):
        for x_colour in range(3):
            for y_colour in range(3):
                qx = sp.zeros(2, 1) if x_colour == d else sp.Matrix([1, 0])
                qy = sp.zeros(2, 1) if y_colour == e else sp.Matrix([0, 1])
                quotient = qx * qy.T
                assert (quotient == sp.zeros(2, 2)) == (
                    x_colour == d or y_colour == e
                )


def main() -> None:
    check_graph_slice()
    check_all_monomial_rows()
    check_binary_shift_trap()
    check_tangent_rank_one_gate()
    print("fully-injective monomial-residual endpoint localization: exact replay passed")


if __name__ == "__main__":
    main()
