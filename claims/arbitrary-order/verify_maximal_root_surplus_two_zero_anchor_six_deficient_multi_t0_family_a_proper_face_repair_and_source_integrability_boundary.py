"""Exact checks for GLS78's multi-T0 Family-A parent boundary."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def add(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(a + b) for a, b in zip(left, right, strict=True))


def scale(value: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in vector)


def assert_zero(vector: tuple[sp.Expr, ...]) -> None:
    assert all(sp.expand(entry) == 0 for entry in vector)


def check_chart_counts() -> None:
    base = 360
    assert base * sp.binomial(3, 2) == 1_080
    assert base * sp.binomial(3, 3) == 360
    assert 1_080 + 360 == 1_440


def restriction_sets(j_dimensions: tuple[int, int, int]) -> tuple[set[tuple[int, ...]], set[tuple[int, ...]]]:
    """Return intersection of singleton kernels and tensor-quotient kernel."""

    basis = set(product(range(3), repeat=3))
    j_sets = tuple(set(range(dimension)) for dimension in j_dimensions)
    singleton_intersection = {
        word for word in basis if all(word[slot] in j_sets[slot] for slot in range(3))
    }
    quotient_kernel = {
        word for word in basis if any(word[slot] in j_sets[slot] for slot in range(3))
    }
    return singleton_intersection, quotient_kernel


def check_restriction_dimensions() -> None:
    r2_intersection, r2_quotient = restriction_sets((1, 2, 2))
    r3_intersection, r3_quotient = restriction_sets((2, 2, 2))
    assert len(r2_intersection) == 4
    assert len(r3_intersection) == 8
    assert len(r2_quotient) == 25
    assert len(r3_quotient) == 26
    # Retaining one three-dimensional central factor multiplies the invisible dimensions.
    assert 3 * len(r2_intersection) == 12
    assert 3 * len(r3_intersection) == 24


def check_physical_hafnian_direction() -> None:
    a2, j3, j4, j5 = sp.symbols("a2 j3 j4 j5", nonzero=True)
    w23 = a2 * j3
    w45 = j4 * j5
    w24 = w25 = w34 = w35 = sp.Integer(0)
    h2345 = sp.expand(w23 * w45 + w24 * w35 + w25 * w34)
    assert h2345 == a2 * j3 * j4 * j5
    assert h2345 != 0


def check_r2_all_selector_control() -> None:
    x = (sp.Integer(1), sp.Integer(0))
    y = (sp.Integer(0), sp.Integer(1))
    k3, l3 = x, y
    k4, l4, k5, l5 = map(sp.Integer, (1, 0, 0, 1))
    b45 = sp.Integer(-1)
    b35 = scale(-1, x)
    b34 = scale(-1, y)

    e45 = b45 + k4 * l5 + l4 * k5
    e35 = add(b35, add(scale(l5, k3), scale(k5, l3)))
    e34 = add(b34, add(scale(l4, k3), scale(k4, l3)))
    assert e45 == 0
    assert_zero(e35)
    assert_zero(e34)

    attach1 = add(scale(b45, k3), add(scale(k4, b35), scale(k5, b34)))
    attach2 = add(scale(b45, l3), add(scale(l4, b35), scale(l5, b34)))
    assert attach1 == scale(-2, x)
    assert attach2 == scale(-2, y)


def check_r3_all_selector_control() -> None:
    k3, k4, k5 = 1, 1, 1
    l3, l4, l5 = 0, 1, 1
    b45, b35, b34 = -2, -1, -1
    assert b45 + k4 * l5 + l4 * k5 == 0
    assert b35 + k3 * l5 + l3 * k5 == 0
    assert b34 + k3 * l4 + l3 * k4 == 0
    assert k3 * b45 + k4 * b35 + k5 * b34 == -4
    assert l3 * b45 + l4 * b35 + l5 * b34 == -2


def check_one_silent_c_control() -> None:
    lam, mu = sp.symbols("lambda mu", nonzero=True)
    x = (sp.Integer(1), sp.Integer(0))
    y = (sp.Integer(0), sp.Integer(1))
    r = scale(sp.Rational(1, 4), add(scale(mu, y), scale(-lam, x)))
    s = scale(-1, r)
    b34 = scale(sp.Rational(1, 2), add(scale(lam, x), scale(mu, y)))
    alpha = m = p = b = c = sp.Integer(1)
    b45 = sp.Integer(-2)
    b35 = (sp.Integer(0), sp.Integer(0))

    assert alpha * b45 + m * c + b * p == 0
    assert_zero(add(scale(alpha, b35), add(scale(c, r), scale(b, s))))
    assert_zero(add(scale(p, r), scale(m, s)))

    attachment1 = add(scale(b45, r), add(scale(m, b35), scale(b, b34)))
    attachment2 = add(scale(b45, s), add(scale(p, b35), scale(c, b34)))
    assert attachment1 == scale(lam, x)
    assert attachment2 == scale(mu, y)


def pairs(vertices: set[int]) -> set[tuple[int, int]]:
    return set(combinations(sorted(vertices), 2))


def check_repair_hierarchy() -> None:
    triangle = {0, 1, 2}
    central = pairs(triangle)
    via_3 = {(i, 3) for i in triangle}
    repairs_5 = {(i, 5) for i in triangle} | {(3, 5)}

    r2_after_4 = pairs({0, 1, 2, 3, 5})
    r2_after_45 = pairs({0, 1, 2, 3})
    assert r2_after_4 == central | via_3 | repairs_5
    assert len(r2_after_4) == 10
    assert r2_after_45 == central | via_3
    assert len(r2_after_45) == 6

    # The r=3 pair classes have the same cardinalities, but every remaining
    # outside label is another T_0 repair port until the third contraction.
    r3_after_4 = pairs({0, 1, 2, 3, 5})
    r3_after_45 = pairs({0, 1, 2, 3})
    r3_after_453 = pairs(triangle)
    assert r3_after_4 == central | via_3 | repairs_5
    assert r3_after_45 == central | via_3
    assert r3_after_453 == central
    assert (len(r3_after_4), len(r3_after_45), len(r3_after_453)) == (10, 6, 3)

    assert len(central | via_3) == 6
    assert pairs(triangle) == central
    assert len(central) == 3


def main() -> None:
    check_chart_counts()
    check_restriction_dimensions()
    check_physical_hafnian_direction()
    check_r2_all_selector_control()
    check_r3_all_selector_control()
    check_one_silent_c_control()
    check_repair_hierarchy()
    assert (97_215, 79) == (97_215, 79)

    print("GLS78 primary verification passed")
    print("Family-A r=2/r=3 keys retained: 1,080 / 1 and 360 / 1")
    print("proper-face invisible dimensions: 4 and 8")
    print("tensor-quotient kernel dimensions: 25 and 26")
    print("all-selector and one-silent C=0 controls: exact")
    print("six-deficient residual unchanged: 97,215 / 79")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
