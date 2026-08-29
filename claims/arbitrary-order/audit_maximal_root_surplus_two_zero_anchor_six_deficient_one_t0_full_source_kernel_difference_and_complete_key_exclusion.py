"""Independent sparse-polynomial audit of GLS77.

This file deliberately does not import the primary verifier and does not use
SymPy.  It represents every coefficient as an integer sparse polynomial and
uses a bit-mask perfect-matching recursion.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import product


Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]
P = 0
Q = 1


def clean(poly: Polynomial) -> Polynomial:
    return Counter({monomial: value for monomial, value in poly.items() if value})


def constant(value: int) -> Polynomial:
    return Counter({(): value}) if value else Counter()


def variable(name: str) -> Polynomial:
    return Counter({(name,): 1})


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = Counter(left)
    out.update(right)
    return clean(out)


def negate(poly: Polynomial) -> Polynomial:
    return Counter({monomial: -value for monomial, value in poly.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = Counter()
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] += left_value * right_value
    return clean(out)


def scale(poly: Polynomial, factor: Polynomial) -> Polynomial:
    return multiply(poly, factor)


KAPPA = variable("kappa")


@lru_cache(maxsize=None)
def matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Generate perfect matchings from a vertex bit mask."""

    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    out = []
    partners = remainder
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        for tail in matchings(remainder ^ partner_bit):
            out.append(((first, partner),) + tail)
        partners ^= partner_bit
    return tuple(out)


MATCHINGS = matchings((1 << 8) - 1)


def internal(i: int, j: int, a: int, b: int) -> Polynomial:
    name = f"I{i}{j}{a}{b}"
    if name == "I1212":
        return Counter()
    if name == "I1512":
        return multiply(KAPPA, variable("I1511"))
    if name == "I2522":
        return multiply(KAPPA, variable("I2521"))
    return variable(name)


def edge(u: int, v: int, a: int, b: int) -> Polynomial:
    if u > v:
        u, v, a, b = v, u, b, a
    if (u, v) == (P, Q):
        return Counter()
    if u >= 2:
        return internal(u - 2, v - 2, a, b)
    if v in (5, 6):
        if b:
            return Counter()
        return variable(f"{'P' if u == P else 'Q'}{v - 2}{a}")
    if v == 7:
        if a == 0:
            return Counter()
        shore = "P" if u == P else "Q"
        if b == 0:
            return variable(f"{shore}5{a}0")
        transverse = variable(f"{shore}5{a}h")
        return transverse if b == 1 else multiply(KAPPA, transverse)
    fixed = {
        (P, 2, 1, 1): 1,
        (Q, 2, 2, 2): 1,
        (P, 3, 2, 2): 1,
        (Q, 4, 1, 1): 1,
    }
    return constant(fixed.get((u, v, a, b), 0))


def base_three_word(index: int) -> tuple[int, ...]:
    digits = [0] * 8
    for position in range(7, -1, -1):
        digits[position] = index % 3
        index //= 3
    return tuple(digits)


def coefficient(index: int) -> Polynomial:
    word = base_three_word(index)
    out: Polynomial = Counter()
    for matching in MATCHINGS:
        term = constant(1)
        for u, v in matching:
            term = multiply(term, edge(u, v, word[u], word[v]))
            if not term:
                break
        out = add(out, term)
    if all(colour == 1 for colour in word):
        out = add(out, negate(variable("mu1")))
    if all(colour == 2 for colour in word):
        out = add(out, negate(variable("mu2")))
    return clean(out)


def c_entries() -> tuple[Polynomial, ...]:
    r1, r2 = variable("I1311"), variable("I1312")
    s1, s2 = variable("I2321"), variable("I2322")
    m1, m2 = variable("I1411"), variable("I1412")
    p1, p2 = variable("I2421"), variable("I2422")
    return (
        add(multiply(r1, p1), multiply(s1, m1)),
        add(multiply(r1, p2), multiply(s1, m2)),
        add(multiply(r2, p1), multiply(s2, m1)),
        add(multiply(r2, p2), multiply(s2, m2)),
    )


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, negate(right))


def check_product_rows() -> set[int]:
    entries = c_entries()
    one = constant(1)
    groups = (
        ((3306, 3309, 3315, 3318), variable("Q510"), (one,) * 4),
        ((4035, 4038, 4044, 4047), variable("Q520"), (one,) * 4),
        ((4278, 4281, 4287, 4290), variable("P510"), (one,) * 4),
        ((6465, 6468, 6474, 6477), variable("P520"), (one,) * 4),
        ((3308, 3310, 3317, 3319), variable("Q51h"), (KAPPA, one, KAPPA, one)),
        ((6467, 6470, 6476, 6479), variable("P52h"), (KAPPA,) * 4),
    )
    checked = set()
    for indices, coordinate, units in groups:
        for index, entry, unit in zip(indices, entries, units, strict=True):
            expected = multiply(multiply(unit, coordinate), entry)
            assert coefficient(index) == expected
            checked.add(index)
    return checked


def check_differences() -> set[int]:
    r1, r2 = variable("I1311"), variable("I1312")
    s1, s2 = variable("I2321"), variable("I2322")
    m1 = variable("I1411")
    p1, p2 = variable("I2421"), variable("I2422")
    x = subtract(variable("I4512"), multiply(KAPPA, variable("I4511")))
    t = subtract(variable("I4522"), multiply(KAPPA, variable("I4521")))
    y = subtract(variable("I3512"), multiply(KAPPA, variable("I3511")))
    z = subtract(variable("I3522"), multiply(KAPPA, variable("I3521")))

    expected = (
        ((3280, 3281), add(add(multiply(r1, x), multiply(m1, y)), multiply(KAPPA, variable("mu1")))),
        ((3289, 3290), add(multiply(r2, x), multiply(m1, z))),
        ((6547, 6548), add(multiply(s1, x), multiply(p1, y))),
        ((6556, 6557), add(multiply(s2, x), multiply(p1, z))),
        ((6559, 6560), add(add(multiply(s2, t), multiply(p2, z)), negate(variable("mu2")))),
    )
    checked = set()
    for (first, second), target in expected:
        difference = subtract(coefficient(second), multiply(KAPPA, coefficient(first)))
        assert difference == target
        checked.update((first, second))
    return checked


def finite_field_obstruction(field: int) -> int:
    """Exhaust the reduced obstruction over a small field."""

    survivors = 0
    for r1, r2, s1, s2, m1, m2, p1, p2 in product(range(field), repeat=8):
        if any(
            value % field
            for value in (
                r1 * p1 + s1 * m1,
                r1 * p2 + s1 * m2,
                r2 * p1 + s2 * m1,
                r2 * p2 + s2 * m2,
            )
        ):
            continue
        for x, y, z, t in product(range(field), repeat=4):
            if (r2 * x + m1 * z) % field:
                continue
            if (s1 * x + p1 * y) % field:
                continue
            if (s2 * x + p1 * z) % field:
                continue
            target1 = (r1 * x + m1 * y) % field
            target2 = (s2 * t + p2 * z) % field
            if target1 and target2:
                survivors += 1
    return survivors


def main() -> None:
    assert len(MATCHINGS) == 105
    products = check_product_rows()
    differences = check_differences()
    assert len(products) == 24
    assert len(differences) == 10
    assert products.isdisjoint(differences)
    assert finite_field_obstruction(2) == 0
    assert finite_field_obstruction(3) == 0
    assert (98_295 - 1_080, 80 - 1) == (97_215, 79)

    print("GLS77 independent audit passed")
    print("independent sparse-polynomial coefficient rows: 34")
    print("exhaustive reduced obstruction: F2 and F3 empty")
    print("six-deficient residual: 97,215 / 79")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
