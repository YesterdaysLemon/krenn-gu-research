#!/usr/bin/env python3
"""Exact replay for the S2BR rank-four/rank-eight target-row atlas."""

from __future__ import annotations

from itertools import permutations

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
    for i in range(N):
        for j in range(N):
            out[i2(i, j)] = a[i] * b[j]
    return out


def outer3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                out[i3(i, j, k)] = a[i] * b[j] * c[k]
    return out


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i in range(N):
        for j in range(N):
            for k in range(N):
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
    cols = []
    for i in range(N):
        cols.append(derivative_value(x, y, w, C, basis(i), zero, zero))
    for i in range(N):
        cols.append(derivative_value(x, y, w, C, zero, basis(i), zero))
    for i in range(N):
        cols.append(derivative_value(x, y, w, C, zero, zero, basis(i)))
    return sp.Matrix.hstack(*cols)


def contract_first(alpha: sp.Matrix, t: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N * N, 1)
    for j in range(N):
        for k in range(N):
            out[i2(j, k)] = sum(alpha[i] * t[i3(i, j, k)] for i in range(N))
    return out


def contract_second(beta: sp.Matrix, t: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N * N, 1)
    for i in range(N):
        for k in range(N):
            out[i2(i, k)] = sum(beta[j] * t[i3(i, j, k)] for j in range(N))
    return out


def contract_third(gamma: sp.Matrix, t: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N * N, 1)
    for i in range(N):
        for j in range(N):
            out[i2(i, j)] = sum(gamma[k] * t[i3(i, j, k)] for k in range(N))
    return out


def tangent_matrix(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    cols = [outer2(basis(i), y) for i in range(N)]
    cols.extend(outer2(x, basis(j)) for j in range(N))
    return sp.Matrix.hstack(*cols)


def in_span(v: sp.Matrix, M: sp.Matrix) -> bool:
    return M.row_join(v).rank() == M.rank()


def coordinate_line(v: sp.Matrix, s: int) -> bool:
    return all(v[i] == 0 for i in range(N) if i != s) and v[s] != 0


def check_symbolic_contractions() -> None:
    xs = sp.symbols("x0:3")
    ys = sp.symbols("y0:3")
    ws = sp.symbols("w0:3")
    aa = sp.symbols("a0:3")
    bb = sp.symbols("b0:3")
    cc = sp.symbols("c0:3")
    al = sp.symbols("al0:3")
    be = sp.symbols("be0:3")
    ga = sp.symbols("ga0:3")
    cs = sp.symbols("C0:9")

    x, y, w = map(sp.Matrix, (xs, ys, ws))
    a, b, c = map(sp.Matrix, (aa, bb, cc))
    alpha, beta, gamma = map(sp.Matrix, (al, be, ga))
    C = sp.Matrix(N, N, cs)
    value = derivative_value(x, y, w, C, a, b, c)

    first_expected = (
        alpha.dot(a) * outer2(y, w)
        - alpha.dot(x) * outer2(b, w)
        + outer2(C.T * alpha, c)
    )
    second_expected = (
        beta.dot(y) * outer2(a, w)
        - beta.dot(b) * outer2(x, w)
        + outer2(C * beta, c)
    )
    third_expected = (
        gamma.dot(w) * (outer2(a, y) - outer2(x, b))
        + gamma.dot(c) * sp.Matrix(N * N, 1, list(C))
    )
    assert all(
        sp.expand(z) == 0 for z in contract_first(alpha, value) - first_expected
    )
    assert all(
        sp.expand(z) == 0 for z in contract_second(beta, value) - second_expected
    )
    assert all(
        sp.expand(z) == 0 for z in contract_third(gamma, value) - third_expected
    )


def check_rank_eight_normal_form() -> None:
    x = sp.Matrix([1, 1, 0])
    y = sp.Matrix([0, 1, 1])
    w = basis(2)
    C = basis(0) * basis(0).T
    D = derivative_matrix(x, y, w, C)
    n = x.col_join(y).col_join(sp.zeros(N, 1))
    assert D.rank() == 8
    assert D * n == sp.zeros(N**3, 1)
    assert D.nullspace() == [n]


def check_tangent_coordinate_test() -> None:
    vectors = [basis(i) for i in range(N)]
    vectors.extend(
        [sp.Matrix([1, 1, 0]), sp.Matrix([0, 1, 1]), sp.Matrix([1, 1, 1])]
    )
    tested = 0
    for x in vectors:
        for y in vectors:
            tangent = tangent_matrix(x, y)
            assert tangent.rank() == 5
            for s in range(N):
                diagonal = outer2(basis(s), basis(s))
                expected = coordinate_line(x, s) or coordinate_line(y, s)
                assert in_span(diagonal, tangent) == expected
                tested += 1
    assert tested == len(vectors) ** 2 * N


def check_distinct_missing_colour_contradiction() -> None:
    checked = 0
    for d, e, f in permutations(range(N)):
        kappa = sp.Integer(d + 2)
        lam = sp.Integer(e + 5)
        mu = sp.Integer(f + 11)
        x, y, w = basis(e), basis(d), basis(f)
        C = (
            kappa * basis(d) * basis(d).T
            + lam * basis(e) * basis(e).T
            + mu * basis(f) * basis(f).T
        )
        D = derivative_matrix(x, y, w, C)
        assert D.rank() == 8
        c_d = -basis(d) / kappa
        u_d = derivative_value(
            x, y, w, C, sp.zeros(N, 1), sp.zeros(N, 1), c_d
        )
        first = contract_first(basis(d), u_d)
        second = contract_second(basis(e), u_d)
        assert first == -outer2(basis(d), basis(d))
        assert second == -(lam / kappa) * outer2(basis(e), basis(d))
        assert second != sp.zeros(N * N, 1)
        checked += 1
    assert checked == 6


def check_same_missing_colour_shape() -> None:
    for d in range(N):
        s, t = [i for i in range(N) if i != d]
        kappa = sp.Integer(d + 2)
        mu = sp.Integer(d + 7)
        x, y, w = basis(s), basis(t), basis(s)
        C = (
            kappa * basis(d) * basis(d).T
            + mu * basis(s) * basis(s).T
        )
        D = derivative_matrix(x, y, w, C)
        assert D.rank() == 8
        assert all(C[d, j] == (kappa if j == d else 0) for j in range(N))
        assert all(C[i, d] == (kappa if i == d else 0) for i in range(N))
        assert x[d] == y[d] == 0
        c_d = -basis(d) / kappa
        u_d = derivative_value(
            x, y, w, C, sp.zeros(N, 1), sp.zeros(N, 1), c_d
        )
        assert contract_first(basis(d), u_d) == -outer2(basis(d), basis(d))
        assert contract_second(basis(d), u_d) == -outer2(basis(d), basis(d))


def check_third_kernel_support_table() -> None:
    for support_size in (1, 2):
        for support in permutations(range(N), support_size):
            support = tuple(sorted(support))
            if len(set(support)) != support_size:
                continue
            x = basis(support[0])
            y = basis(support[-1])
            gamma = sum((basis(i) for i in support), sp.zeros(N, 1))
            w = basis(support[0])
            assert gamma.dot(w) != 0
            tangent = tangent_matrix(x, y)
            for s in range(N):
                represented = in_span(outer2(basis(s), basis(s)), tangent)
                assert represented == (s in set(support))


def main() -> None:
    check_symbolic_contractions()
    check_rank_eight_normal_form()
    check_tangent_coordinate_test()
    check_distinct_missing_colour_contradiction()
    check_same_missing_colour_shape()
    check_third_kernel_support_table()
    print(
        "S2BR primary replay passed: rank-eight derivative; three target "
        "contractions; tangent-coordinate iff; 6 distinct-missing-colour "
        "contradictions; same-colour survivor shape."
    )


if __name__ == "__main__":
    main()
