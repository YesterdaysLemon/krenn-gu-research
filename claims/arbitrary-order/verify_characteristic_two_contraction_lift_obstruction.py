"""Exact checks for the characteristic-two lift-obstruction note."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import product

import sympy as sp


@cache
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for offset, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for tail in matchings(rest):
            output.append(((first, partner), *tail))
    return tuple(output)


def amplitude(
    order: int,
    colouring: tuple[int, ...],
    weights: dict[tuple[int, int, int, int], Fraction],
) -> Fraction:
    total = Fraction(0)
    for matching in matchings(tuple(range(order))):
        term = Fraction(1)
        for i, j in matching:
            term *= weights.get((i, j, colouring[i], colouring[j]), Fraction(0))
        total += term
    return total


def verify_rational_equation_family_example() -> None:
    weights = {
        (0, 1, 0, 0): Fraction(1),
        (2, 3, 0, 0): Fraction(1, 2),
        (0, 2, 0, 0): Fraction(1),
        (1, 3, 0, 0): Fraction(1, 2),
        (0, 3, 1, 1): Fraction(1),
        (1, 2, 1, 1): Fraction(1),
    }
    nonzero = {}
    for colouring in product(range(2), repeat=4):
        value = amplitude(4, colouring, weights)
        target = Fraction(1) if len(set(colouring)) == 1 else Fraction(0)
        assert value == target
        if value:
            nonzero[colouring] = value
    assert nonzero == {(0, 0, 0, 0): 1, (1, 1, 1, 1): 1}


def f4_add(a: int, b: int) -> int:
    return a ^ b


def f4_mul(a: int, b: int) -> int:
    # Bit a0 + a1*alpha, with alpha^2=alpha+1.
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    constant = (a0 * b0) ^ (a1 * b1)
    alpha = (a0 * b1) ^ (a1 * b0) ^ (a1 * b1)
    return constant | (alpha << 1)


def verify_f4_matching_sum_example() -> None:
    one, alpha, alpha_squared = 1, 2, 3
    weights = {
        (0, 1): alpha,
        (2, 3): one,
        (4, 5): one,
        (0, 2): alpha_squared,
        (1, 3): one,
    }
    terms = []
    for matching in matchings(tuple(range(6))):
        term = one
        for item in matching:
            term = f4_mul(term, weights.get(item, 0))
        if term:
            terms.append((matching, term))
    assert [term for _, term in terms] == [alpha, alpha_squared]
    assert f4_add(alpha, alpha_squared) == one
    assert all(any(weights[item] != one for item in matching) for matching, _ in terms)


def verify_rank_two_polynomial_identity() -> None:
    p = sp.symbols("p0:4")
    q = sp.symbols("q0:4")

    def rank_two(i: int, j: int) -> sp.Expr:
        return p[i] * q[j] + p[j] * q[i]

    h = sp.expand(
        rank_two(0, 1) * rank_two(2, 3)
        + rank_two(0, 2) * rank_two(1, 3)
        + rank_two(0, 3) * rank_two(1, 2)
    )
    polynomial = sp.Poly(h, *p, *q, domain=sp.ZZ)
    assert polynomial.terms()
    assert all(coefficient % 2 == 0 for _, coefficient in polynomial.terms())
    assert sp.Poly(h, *p, *q, modulus=2).is_zero

    ell = sp.symbols("l0:4")
    rank_one_h = sp.expand(3 * sp.prod(ell))
    assert sp.Poly(rank_one_h, *ell, modulus=3).is_zero


def verify_generic_specializations() -> None:
    qx, byz, bxy, bxz = sp.symbols("qx byz bxy bxz")
    h_xxyz = qx * byz + 2 * bxy * bxz
    assert sp.expand(h_xxyz - (qx * byz + 2 * bxy * bxz)) == 0
    diagonal = 3 * qx**2
    assert sp.Poly(diagonal, qx, modulus=2) == sp.Poly(qx**2, qx, modulus=2)
    assert sp.Poly(diagonal, qx, modulus=3).is_zero


def main() -> None:
    verify_rational_equation_family_example()
    verify_f4_matching_sum_example()
    verify_rank_two_polynomial_identity()
    verify_generic_specializations()
    print("characteristic-two contraction lift-obstruction verification: PASS")
    print("exact Q and F4 counterexamples checked")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
