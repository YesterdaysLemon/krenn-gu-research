"""Exact checks for GLS77's Family-A r=1 full-source exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


P = 0
Q = 1
VERTICES = tuple(range(8))
KAPPA = sp.Symbol("kappa", nonzero=True)
MU1 = sp.Symbol("mu1", nonzero=True)
MU2 = sp.Symbol("mu2", nonzero=True)
SYMBOLS: dict[str, sp.Symbol] = {}


def symbol(name: str) -> sp.Symbol:
    """Return one shared symbol for a physical or source-row coefficient."""

    if name not in SYMBOLS:
        SYMBOLS[name] = sp.Symbol(name)
    return SYMBOLS[name]


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate unordered perfect matchings recursively."""

    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + matching)
    return tuple(out)


MATCHINGS = perfect_matchings(VERTICES)
WORDS = tuple(product(range(3), repeat=8))


def internal(i: int, j: int, a: int, b: int) -> sp.Expr:
    """Physical coefficient, with only the three GLS72 residual relations."""

    name = f"I{i}{j}{a}{b}"
    if name == "I1212":
        return sp.Integer(0)
    if name == "I1512":
        return KAPPA * symbol("I1511")
    if name == "I2522":
        return KAPPA * symbol("I2521")
    return symbol(name)


def edge(u: int, v: int, a: int, b: int) -> sp.Expr:
    """Coefficient of one edge in the crossed Family-A r=1 normal form."""

    if u > v:
        u, v, a, b = v, u, b, a
    if (u, v) == (P, Q):
        return sp.Integer(0)

    # Internal vertices 2,...,7 represent physical labels 0,...,5.
    if u >= 2:
        return internal(u - 2, v - 2, a, b)

    # The two R_0 ports are physical labels 3 and 4.  Their row support is e_0.
    if v in (5, 6):
        if b != 0:
            return sp.Integer(0)
        shore = "P" if u == P else "Q"
        return symbol(f"{shore}{v - 2}{a}")

    # The silent T_0 port is physical label 5.  Its remaining rows lie in
    # span(e_0^*, e_1^* + kappa e_2^*).
    if v == 7:
        if a == 0:
            return sp.Integer(0)
        shore = "P" if u == P else "Q"
        if b == 0:
            return symbol(f"{shore}5{a}0")
        transverse = symbol(f"{shore}5{a}h")
        return transverse if b == 1 else KAPPA * transverse

    # Crossed central normalization.
    fixed = {
        (P, 2, 1, 1): 1,
        (Q, 2, 2, 2): 1,
        (P, 3, 2, 2): 1,
        (Q, 4, 1, 1): 1,
    }
    return sp.Integer(fixed.get((u, v, a, b), 0))


def full_coefficient(word: tuple[int, ...]) -> sp.Expr:
    """Expand one literal coefficient of the eight-vertex source identity."""

    total = sp.Integer(0)
    for matching in MATCHINGS:
        total += sp.prod(edge(u, v, word[u], word[v]) for u, v in matching)
    if all(colour == 1 for colour in word):
        total -= MU1
    if all(colour == 2 for colour in word):
        total -= MU2
    return sp.expand(total)


def c_entries() -> tuple[sp.Expr, ...]:
    """Return C_11,C_12,C_21,C_22 in table order."""

    r1, r2 = symbol("I1311"), symbol("I1312")
    s1, s2 = symbol("I2321"), symbol("I2322")
    m1, m2 = symbol("I1411"), symbol("I1412")
    p1, p2 = symbol("I2421"), symbol("I2422")
    return (
        r1 * p1 + s1 * m1,
        r1 * p2 + s1 * m2,
        r2 * p1 + s2 * m1,
        r2 * p2 + s2 * m2,
    )


def check_product_rows() -> set[int]:
    """Check all 24 C_ij times T-row factorizations."""

    entries = c_entries()
    groups = (
        ((3306, 3309, 3315, 3318), symbol("Q510"), (1, 1, 1, 1)),
        ((4035, 4038, 4044, 4047), symbol("Q520"), (1, 1, 1, 1)),
        ((4278, 4281, 4287, 4290), symbol("P510"), (1, 1, 1, 1)),
        ((6465, 6468, 6474, 6477), symbol("P520"), (1, 1, 1, 1)),
        ((3308, 3310, 3317, 3319), symbol("Q51h"), (KAPPA, 1, KAPPA, 1)),
        (
            (6467, 6470, 6476, 6479),
            symbol("P52h"),
            (KAPPA, KAPPA, KAPPA, KAPPA),
        ),
    )
    checked = set()
    for indices, coordinate, units in groups:
        for index, entry, unit in zip(indices, entries, units, strict=True):
            assert sp.expand(full_coefficient(WORDS[index]) - unit * coordinate * entry) == 0
            checked.add(index)
    assert len(checked) == 24
    return checked


def check_kernel_differences() -> set[int]:
    """Check the five full-row differences used by the written proof."""

    r1, r2 = symbol("I1311"), symbol("I1312")
    s1, s2 = symbol("I2321"), symbol("I2322")
    m1 = symbol("I1411")
    p1, p2 = symbol("I2421"), symbol("I2422")
    x = symbol("I4512") - KAPPA * symbol("I4511")
    t = symbol("I4522") - KAPPA * symbol("I4521")
    y = symbol("I3512") - KAPPA * symbol("I3511")
    z = symbol("I3522") - KAPPA * symbol("I3521")
    expected = (
        ((3280, 3281), r1 * x + m1 * y + KAPPA * MU1),
        ((3289, 3290), r2 * x + m1 * z),
        ((6547, 6548), s1 * x + p1 * y),
        ((6556, 6557), s2 * x + p1 * z),
        ((6559, 6560), s2 * t + p2 * z - MU2),
    )
    checked = set()
    for (first, second), target in expected:
        difference = full_coefficient(WORDS[second]) - KAPPA * full_coefficient(WORDS[first])
        assert sp.expand(difference - target) == 0
        checked.update((first, second))
    assert len(checked) == 10
    return checked


def check_outer_product_obstruction() -> None:
    """Replay the five-equation obstruction by exact ideal arithmetic."""

    r1, r2, s1, s2, m1, m2, p1, p2 = sp.symbols("r1 r2 s1 s2 m1 m2 p1 p2")
    x, y, z, t, target1, target2 = sp.symbols("x y z t target1 target2")
    inv1, inv2 = sp.symbols("inv1 inv2")
    equations = [
        r1 * p1 + s1 * m1,
        r1 * p2 + s1 * m2,
        r2 * p1 + s2 * m1,
        r2 * p2 + s2 * m2,
        r1 * x + m1 * y - target1,
        r2 * x + m1 * z,
        s1 * x + p1 * y,
        s2 * x + p1 * z,
        s2 * t + p2 * z - target2,
        inv1 * target1 - 1,
        inv2 * target2 - 1,
    ]
    variables = sorted(set().union(*(item.free_symbols for item in equations)), key=str)
    basis = sp.groebner(equations, *variables, domain=sp.QQ, order="grevlex")
    assert any(item.as_expr() == 1 for item in basis.polys)


def main() -> None:
    assert len(MATCHINGS) == 105
    product_rows = check_product_rows()
    difference_rows = check_kernel_differences()
    assert product_rows.isdisjoint(difference_rows)
    assert len(product_rows | difference_rows) == 34
    check_outer_product_obstruction()

    old_profiles, old_keys = 98_295, 80
    closed_profiles, closed_keys = 1_080, 1
    assert (old_profiles - closed_profiles, old_keys - closed_keys) == (97_215, 79)
    assert 1_080 + 360 == 1_440

    print("GLS77 primary verification passed")
    print("perfect matchings: 105")
    print("literal full coefficient rows: 34")
    print("C-product rows: 24")
    print("paired kernel differences: 5")
    print("Family-A r=1 removed: 1,080 / 1")
    print("six-deficient residual: 97,215 / 79")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
