#!/usr/bin/env python3
"""Exact replay for the S2BY one-deficient-row, q=3 exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp

N = 3
D, S, T = 0, 1, 2


def i2(a: int, b: int) -> int:
    return N * a + b


def unit4(index: int) -> sp.Matrix:
    return sp.eye(4)[:, index]


def check_one_missing_row_correction() -> None:
    kappa = sp.symbols("kappa", nonzero=True)
    columns = []
    for colour in (D, S, T):
        column = sp.zeros(N * N, 1)
        column[i2(D, colour)] = kappa
        columns.append(column)
    contraction = sp.Matrix.hstack(*columns)
    rhs = sp.zeros(N * N, 1)
    rhs[i2(D, D)] = -1
    expected = sp.Matrix([-1 / kappa, 0, 0])
    assert contraction.rank() == 3
    assert contraction.gauss_jordan_solve(rhs)[0] == expected


def target_value(a: int, b: int, c: int) -> sp.Matrix:
    """Source-target coordinates (T_d,T_s,T_t) after the rank step."""
    out = sp.zeros(3, 1)
    if a == b == c == S:
        out[S] = 1
    elif a == b == c == T:
        out[T] = 1
    return out


def check_mixed_binary_restriction() -> None:
    # The second and third rows are injective: all three indexed rows are
    # independent.  Their s,t restrictions are therefore two-planes.
    p_rows = [unit4(0), unit4(1), unit4(2)]
    q_rows = [unit4(0), unit4(2), unit4(3)]
    assert sp.Matrix.hstack(*p_rows).rank() == 3
    assert sp.Matrix.hstack(*q_rows).rank() == 3
    assert sp.Matrix.hstack(p_rows[S], p_rows[T]).rank() == 2
    assert sp.Matrix.hstack(q_rows[S], q_rows[T]).rank() == 2

    nonzero = []
    for a, b, c in product((S, T), (D, S, T), (D, S, T)):
        value = target_value(a, b, c)
        if value != sp.zeros(3, 1):
            nonzero.append((a, b, c, tuple(value)))
        if c == D:
            assert value == sp.zeros(3, 1)
        if b == D:
            assert value == sp.zeros(3, 1)
    assert nonzero == [
        (S, S, S, (0, 1, 0)),
        (T, T, T, (0, 0, 1)),
    ]


def check_arbitrary_kernel_shifts() -> None:
    lam_s, lam_t = sp.symbols("lam_s lam_t")
    for a, b, c in product((S, T), repeat=3):
        value = target_value(a, b, c)
        kernel = target_value(a, b, D)
        shifted = value + (lam_s if c == S else lam_t) * kernel
        assert shifted == value


def check_four_space_shift_trap() -> None:
    qd, qs, qt, h = (unit4(index) for index in range(4))
    q_space = sp.Matrix.hstack(qd, qs, qt)
    q_binary = sp.Matrix.hstack(qs, qt)

    # Every two-plane disjoint from Q_0 meets Q in one line.
    a, b, c = sp.symbols("a b c")
    ell = a * qs + b * qt + c * qd
    plane = sp.Matrix.hstack(ell, h)
    assert plane.row_join(q_space).rank() == 4
    assert sp.expand(plane.row_join(q_binary).det() ** 2) == c**2

    lam_s, lam_t = sp.symbols("lam_s lam_t")
    shifted_s = qs + lam_s * qd
    shifted_t = qt + lam_t * qd
    residual = sp.simplify(ell - a * shifted_s - b * shifted_t)
    assert residual == (c - a * lam_s - b * lam_t) * qd

    # One- and two-supported binary coefficients all enter a shifted plane.
    for aa, bb, cc in ((3, 0, 2), (0, -5, 7), (2, 3, 11)):
        if aa:
            ls, lt = sp.Rational(cc, aa), sp.Integer(0)
        else:
            ls, lt = sp.Integer(0), sp.Rational(cc, bb)
        line = aa * qs + bb * qt + cc * qd
        shifted = sp.Matrix.hstack(qs + ls * qd, qt + lt * qd)
        assert shifted.row_join(line).rank() == 2

    # The only coefficient mask not caught by a shift is the q_d endpoint.
    assert sp.Matrix.hstack(qd, 13 * qd).rank() == 1


def check_root_exchange() -> None:
    # The table is invariant under exchanging the first two arguments.
    for a, b, c in product((S, T), (D, S, T), (D, S, T)):
        assert target_value(a, b, c) == target_value(b, a, c)


def main() -> None:
    check_one_missing_row_correction()
    check_mixed_binary_restriction()
    check_arbitrary_kernel_shifts()
    check_four_space_shift_trap()
    check_root_exchange()
    print(
        "S2BY primary replay passed: one-row correction; injective mixed "
        "restriction; exact binary shifts; four-space line trap; root exchange."
    )


if __name__ == "__main__":
    main()
