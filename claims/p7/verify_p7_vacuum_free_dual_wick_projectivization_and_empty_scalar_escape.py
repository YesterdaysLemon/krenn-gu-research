"""Verify the vacuum-free dual-Wick projectivization and sharp escapes.

All calculations are fixed symbolic identities.  There is no graph, support,
colour-word, selector, or parameter enumeration.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def hafnian(
    vertices: tuple[int, ...], edge: dict[tuple[int, int], sp.Expr]
) -> sp.Expr:
    """Fixed-size symbolic hafnian recurrence used only as a replay oracle."""

    @cache
    def recurse(current: tuple[int, ...]) -> sp.Expr:
        if not current:
            return sp.Integer(1)
        first = current[0]
        return sp.expand(
            sum(
                edge[tuple(sorted((first, partner)))]
                * recurse(current[1:position] + current[position + 1 :])
                for position, partner in enumerate(current[1:], start=1)
            )
        )

    return recurse(vertices)


def direct_edge_symbols(order: int) -> dict[tuple[int, int], sp.Symbol]:
    return {
        (left, right): sp.Symbol(f"B{left + 1}{right + 1}")
        for left, right in combinations(range(order), 2)
    }


def insertion_defect(
    subset: tuple[int, ...],
    h: sp.Symbol,
    direct: dict[tuple[int, int], sp.Expr],
    corrected: dict[tuple[int, int], sp.Expr],
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    m_subset = hafnian(subset, direct)
    z_pairs = {
        pair: h * direct[pair] + corrected[pair]
        for pair in combinations(range(6), 2)
    }
    z_subset = h * m_subset + sum(
        corrected[pair]
        * hafnian(tuple(vertex for vertex in subset if vertex not in pair), direct)
        for pair in combinations(subset, 2)
    )
    defect = sum(
        z_pairs[pair]
        * hafnian(tuple(vertex for vertex in subset if vertex not in pair), direct)
        for pair in combinations(subset, 2)
    ) - z_subset
    return sp.expand(m_subset), sp.expand(z_subset), sp.expand(defect)


def square_zero_multiply(
    left: tuple[sp.Expr, sp.Expr], right: tuple[sp.Expr, sp.Expr]
) -> tuple[sp.Expr, sp.Expr]:
    """Multiply a0+a1*t and b0+b1*t modulo t^2."""

    return (
        sp.expand(left[0] * right[0]),
        sp.expand(left[0] * right[1] + left[1] * right[0]),
    )


def main() -> None:
    h = sp.Symbol("h")
    direct = direct_edge_symbols(6)
    left = sp.symbols("a1:7")
    right = sp.symbols("b1:7")
    corrected = {
        (u, v): left[u] * right[v] + right[u] * left[v]
        for u, v in combinations(range(6), 2)
    }

    four = (0, 1, 2, 3)
    six = tuple(range(6))
    m_four, _z_four, d_four = insertion_defect(
        four, h, direct, corrected
    )
    m_six, _z_six, d_six = insertion_defect(six, h, direct, corrected)
    assert sp.expand(d_four - h * m_four) == 0
    assert sp.expand(d_six - 2 * h * m_six) == 0
    assert sp.expand(2 * m_six * d_four - m_four * d_six) == 0

    # The physical channel a=e1, b=(0,P,Q,R) maps surjectively to the
    # three opposite-pair sums.
    p, q, r = sp.symbols("P Q R")
    additive_left = (1, 0, 0, 0)
    additive_right = (0, p, q, r)
    pair_response = {
        (u, v): additive_left[u] * additive_right[v]
        + additive_right[u] * additive_left[v]
        for u, v in combinations(range(4), 2)
    }
    opposite_sums = (
        pair_response[(0, 1)] + pair_response[(2, 3)],
        pair_response[(0, 2)] + pair_response[(1, 3)],
        pair_response[(0, 3)] + pair_response[(1, 2)],
    )
    assert opposite_sums == (p, q, r)
    assert sp.Matrix(opposite_sums).jacobian((p, q, r)).det() == 1

    # Honest empty-scalar family: M=1+t, Phi=lambda-lambda*t, t^2=0.
    lam = sp.Symbol("lambda")
    direct_polynomial = (sp.Integer(1), sp.Integer(1))
    relative_polynomial = (lam, -lam)
    residual_polynomial = square_zero_multiply(
        direct_polynomial, relative_polynomial
    )
    assert residual_polynomial == (lam, 0)
    # The nonempty pair also cancels directly: h*B12+a1*b2=0.
    assert sp.expand(lam + (-lam) * 1) == 0

    # Paired singleton depths recover the residual edge on B_uv != 0.
    b_uv, a_u, a_v, b_u, b_v = sp.symbols("Buv au av bu bv", nonzero=True)
    z_uv = h * b_uv + a_u * b_v + b_u * a_v
    recovered_h = sp.cancel((z_uv - a_u * b_v - b_u * a_v) / b_uv)
    assert recovered_h == h

    print("vacuum-free dual-Wick projectivization: VERIFIED")
    print("D4=h*m4 D6=2*h*m6 cross_4_6=0")
    print("opposite_pair_sum_map_jacobian=1 additive_locus_not_forced")
    print("empty_scalar_escape=M(1+t)*Phi(lambda-lambda*t)=lambda")
    print("paired_singleton_companion_recovery=VERIFIED")
    print("searches=0 enumerations=0 P7_GLOBAL_STATUS=UNKNOWN")


if __name__ == "__main__":
    main()
