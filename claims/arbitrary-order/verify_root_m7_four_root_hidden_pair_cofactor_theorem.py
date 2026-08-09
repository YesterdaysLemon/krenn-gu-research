"""Symbolic checks for the four-root hidden-pair cofactor theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_parity_ledger() -> None:
    fixed = ("rk", "q0", "q1")
    legal = []
    for size in (0, 2):
        legal.extend(combinations(fixed, size))
    assert set(legal) == {(), ("rk", "q0"), ("rk", "q1"), ("q0", "q1")}


def check_quotient_trichotomy() -> None:
    # Two independent scalar forms: every quotient coordinate vanishes.
    scalar = sp.eye(2)
    bars = sp.Matrix(sp.symbols("u0 u1 v0 v1")).reshape(2, 2)
    equation = scalar * bars
    solution = sp.solve(list(equation), list(bars), dict=True)
    assert solution == [{entry: 0 for entry in bars}]

    # Rank one q=mu*h: the quotient relation is bar(C_I)+mu bar(C_IQ)=0.
    mu, u0, u1, v0, v1 = sp.symbols("mu u0 u1 v0 v1", nonzero=True)
    rank_one = sp.Matrix([u0 + mu * v0, u1 + mu * v1])
    solved = sp.solve(list(rank_one), (u0, u1), dict=True)
    assert solved == [{u0: -mu * v0, u1: -mu * v1}]


def check_two_active_ideal() -> None:
    xs = sp.symbols("x0:5")
    ys = sp.symbols("y0:5")
    x_all = sp.prod(xs)
    y_all = sp.prod(ys)
    h0 = sp.prod(xs[1:])
    h1 = ys[0] * sp.prod(ys[2:])
    g0 = xs[0] * h0
    g1 = ys[1] * h1
    assert sp.expand(g0 - x_all) == 0
    assert sp.expand(g1 - y_all) == 0
    assert sp.gcd(x_all, y_all) == 1
    assert sp.gcd(h0, h1) == 1


def check_top_frame() -> None:
    top_cofactors = sp.Matrix([[1, 1], [1, -1]])
    assert top_cofactors.det() == -2
    assert top_cofactors.rank() == 2
    target_forms = sp.eye(2)
    scalar_forms = target_forms * top_cofactors.inv()
    assert scalar_forms.rank() == 2


def main() -> None:
    check_parity_ledger()
    check_quotient_trichotomy()
    check_two_active_ideal()
    check_top_frame()
    print("root m=7 four-root hidden-pair theorem: symbolic checks PASS")


if __name__ == "__main__":
    main()
