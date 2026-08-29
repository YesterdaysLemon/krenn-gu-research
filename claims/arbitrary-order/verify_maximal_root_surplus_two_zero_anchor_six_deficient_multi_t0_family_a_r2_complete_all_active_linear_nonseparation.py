"""Exact all-active ``r=2`` linear leakage nonseparation verifier.

This primary verifier covers the Family-A chart
``S_0 R_2 R_1 R_0 T_0 T_0`` with port ``3`` the ``R_0`` port and ports
``4,5`` active ``T_0`` ports.  It expands all 105 perfect matchings of the
complete eight-vertex source/physical matrix, retaining every source-row
coordinate, including ``P_0`` and ``Q_0`` at port ``5``.

For the 6,558 zero-target words, an exact incidence decomposition over
``QQ(kappa4,kappa5)`` proves that the nonleak right kernel contains no
leakage direction for ``I2500``.  The full 6,561-row calculation separately
checks all three GHZ target words and finds no kernel vector supported on a
target row.

This is a scoped scalar-linear source-integrability obstruction.  It does
not test nonlinear coefficient-ideal syzygies, arbitrary multipliers,
activity localization, either key exclusion, or the global conjecture.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from time import perf_counter

import sympy as sp


KAPPA4, KAPPA5 = sp.symbols("kappa4 kappa5")
T_SLOPE = {4: KAPPA4, 5: KAPPA5}
P, Q = 0, 1
VERTICES = 8
LEAK = "I2500"

Poly = dict[tuple[str, ...], sp.Expr]


def clean(poly: Poly) -> Poly:
    """Remove exact zero coefficients."""

    out: Poly = {}
    for monomial, coefficient in poly.items():
        value = sp.expand(coefficient)
        if value != 0:
            out[monomial] = value
    return out


def one(value: int = 1) -> Poly:
    """Return a constant polynomial."""

    return {(): sp.Integer(value)} if value else {}


def variable(name: str) -> Poly:
    """Return one literal source or physical coordinate."""

    return {(name,): sp.Integer(1)}


def add(*polynomials: Poly) -> Poly:
    """Add polynomial dictionaries."""

    out: Poly = {}
    for poly in polynomials:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, sp.Integer(0)) + coefficient
    return clean(out)


def negate(poly: Poly) -> Poly:
    """Negate a polynomial dictionary."""

    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def scale(factor: sp.Expr, poly: Poly) -> Poly:
    """Scale a polynomial dictionary."""

    return clean(
        {monomial: factor * coefficient for monomial, coefficient in poly.items()}
    )


def multiply(left: Poly, right: Poly) -> Poly:
    """Multiply and canonically sort literal monomial names."""

    out: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = out.get(monomial, sp.Integer(0)) + (
                left_coefficient * right_coefficient
            )
    return clean(out)


def subtract(left: Poly, right: Poly) -> Poly:
    """Subtract polynomial dictionaries."""

    return add(left, negate(right))


def assert_poly_equal(left: Poly, right: Poly) -> None:
    """Assert equality after exact coefficient simplification."""

    assert clean(subtract(left, right)) == {}, (left, right)


@lru_cache(maxsize=None)
def matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate perfect matchings of a vertex bit mask."""

    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    out: list[tuple[tuple[int, int], ...]] = []
    partners = remainder
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        for tail in matchings(remainder ^ partner_bit):
            out.append(((first, partner),) + tail)
        partners ^= partner_bit
    return tuple(out)


MATCHINGS = matchings((1 << VERTICES) - 1)


def crossed_source_edge(
    u: int,
    v: int,
    colour_u: int,
    colour_v: int,
) -> Poly:
    """Return the fixed nonzero central crossed-chart source entries."""

    if u > v:
        u, v, colour_u, colour_v = v, u, colour_v, colour_u
    fixed = {
        (P, 2, 1, 1): 1,
        (Q, 2, 2, 2): 1,
        (P, 3, 2, 2): 1,
        (Q, 4, 1, 1): 1,
    }
    return one(fixed.get((u, v, colour_u, colour_v), 0))


def source_edge(
    source: int,
    outside_port: int,
    source_colour: int,
    physical_colour: int,
) -> Poly:
    """Return a complete ``R_0`` or ``T_0`` source-row entry."""

    source_name = "P" if source == P else "Q"
    if outside_port == 3:
        return (
            variable(f"{source_name}{outside_port}{source_colour}")
            if physical_colour == 0
            else {}
        )
    if physical_colour == 0:
        return variable(f"{source_name}{outside_port}{source_colour}0")
    row_name = f"{source_name}{outside_port}{source_colour}h"
    if physical_colour == 1:
        return variable(row_name)
    return scale(T_SLOPE[outside_port], variable(row_name))


def edge(
    u: int,
    v: int,
    colour_u: int,
    colour_v: int,
) -> Poly:
    """Return one source or physical edge entry."""

    if u > v:
        u, v, colour_u, colour_v = v, u, colour_v, colour_u
    if (u, v) == (P, Q):
        return {}
    if u >= 2:
        left_port, right_port = u - 2, v - 2
        return variable(f"I{left_port}{right_port}{colour_u}{colour_v}")
    if v >= 5:
        return source_edge(u, v - 2, colour_u, colour_v)
    return crossed_source_edge(u, v, colour_u, colour_v)


@lru_cache(maxsize=None)
def coefficient(word: tuple[int, ...]) -> Poly:
    """Expand one complete eight-vertex colour coefficient."""

    assert len(word) == VERTICES
    out: Poly = {}
    for matching in MATCHINGS:
        term = one()
        for u, v in matching:
            term = multiply(term, edge(u, v, word[u], word[v]))
            if not term:
                break
        out = add(out, term)

    for target in range(3):
        if all(colour == target for colour in word):
            out = add(out, scale(-1, variable(f"mu{target}")))
            break
    return out


def is_target_word(word: tuple[int, ...]) -> bool:
    """Return whether a word is one of the three pure GHZ target words."""

    return any(all(colour == target for colour in word) for target in range(3))


def has_leak(poly: Poly) -> bool:
    """Return whether a polynomial contains an ``I2500`` monomial."""

    return any(LEAK in monomial for monomial in poly)


def expected_representative_difference() -> Poly:
    """Return the exact RTT port-4 repair identity."""

    d24 = subtract(variable("I2402"), scale(KAPPA4, variable("I2401")))
    d14 = subtract(variable("I1422"), scale(KAPPA4, variable("I1421")))
    d04 = subtract(variable("I0422"), scale(KAPPA4, variable("I0421")))
    d34 = subtract(variable("I3402"), scale(KAPPA4, variable("I3401")))
    d45 = subtract(variable("I4520"), scale(KAPPA4, variable("I4510")))
    q_repair = add(
        multiply(variable("I0122"), d24),
        multiply(variable("I0220"), d14),
        multiply(variable("I1220"), d04),
    )
    return add(
        multiply(
            add(
                multiply(variable("P30"), variable("Q520")),
                multiply(variable("P500"), variable("Q32")),
            ),
            q_repair,
        ),
        multiply(
            variable("I1220"),
            add(
                multiply(variable("P500"), d34),
                multiply(variable("P30"), d45),
            ),
        ),
        multiply(
            variable("P500"),
            add(
                multiply(variable("I1320"), d24),
                multiply(variable("I2300"), d14),
            ),
        ),
        multiply(
            variable("P30"),
            add(
                multiply(variable(LEAK), d14),
                multiply(variable("I1520"), d24),
            ),
        ),
    )


def check_representative(rows: dict[tuple[int, ...], Poly]) -> None:
    """Check the named full-source RTT leakage identity."""

    row_1 = (0, 2, 2, 2, 0, 0, 1, 0)
    row_2 = (0, 2, 2, 2, 0, 0, 2, 0)
    actual = subtract(rows[row_2], scale(KAPPA4, rows[row_1]))
    assert_poly_equal(actual, expected_representative_difference())
    assert has_leak(actual)
    assert any("P500" in monomial for monomial in actual)


def component_word_blocks(
    rows: dict[tuple[int, ...], Poly],
) -> list[list[tuple[int, ...]]]:
    """Split rows into components joined by shared nonleak monomials."""

    words = list(rows)
    parent = list(range(len(words)))
    sizes = [1] * len(words)

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return
        if sizes[left_root] < sizes[right_root]:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        sizes[left_root] += sizes[right_root]

    first_row: dict[tuple[str, ...], int] = {}
    for position, word in enumerate(words):
        for monomial in rows[word]:
            if LEAK in monomial:
                continue
            previous = first_row.setdefault(monomial, position)
            union(position, previous)

    blocks: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for position, word in enumerate(words):
        blocks[find(position)].append(word)
    return list(blocks.values())


def nonleak_nullspace(
    block: list[Poly],
) -> tuple[list[tuple[str, ...]], list[sp.Matrix]]:
    """Return leakage monomials and the exact nonleak right nullspace."""

    monomials = sorted(set().union(*(set(row) for row in block)))
    nonleak = [monomial for monomial in monomials if LEAK not in monomial]
    leak = [monomial for monomial in monomials if LEAK in monomial]
    matrix = (
        sp.Matrix(
            [
                [row.get(monomial, sp.Integer(0)) for row in block]
                for monomial in nonleak
            ]
        )
        if nonleak
        else sp.zeros(0, len(block))
    )
    return leak, matrix.nullspace()


def analyze_components(
    rows: dict[tuple[int, ...], Poly],
) -> dict[str, object]:
    """Compute exact component, nullity, target-support, and leak data."""

    word_blocks = component_word_blocks(rows)
    component_histogram = Counter(len(words) for words in word_blocks)
    total_nullity = 0
    leak_components = 0
    leak_histogram: Counter[int] = Counter()
    leak_nullity_sum = 0
    leak_nullity_max = 0
    separators = 0
    target_supported_nullities = 0

    for words in word_blocks:
        block = [rows[word] for word in words]
        leak, nullspace = nonleak_nullspace(block)
        total_nullity += len(nullspace)
        has_block_leak = any(has_leak(row) for row in block)
        if has_block_leak:
            leak_components += 1
            leak_histogram[len(block)] += 1
            leak_nullity_sum += len(nullspace)
            leak_nullity_max = max(leak_nullity_max, len(nullspace))
        for vector in nullspace:
            if any(
                value != 0 and is_target_word(word)
                for word, value in zip(words, vector)
            ):
                target_supported_nullities += 1
            if any(
                sp.factor(
                    sum(
                        vector[column] * block[column].get(monomial, sp.Integer(0))
                        for column in range(len(block))
                    )
                )
                != 0
                for monomial in leak
            ):
                separators += 1

    return {
        "rows": len(rows),
        "components": len(word_blocks),
        "component_histogram": dict(component_histogram),
        "leak_components": leak_components,
        "leak_histogram": dict(leak_histogram),
        "total_nullity": total_nullity,
        "leak_nullity_sum": leak_nullity_sum,
        "leak_nullity_max": leak_nullity_max,
        "rank": len(rows) - total_nullity,
        "separators": separators,
        "target_supported_nullities": target_supported_nullities,
    }


def check_full_result(result: dict[str, object]) -> None:
    """Assert the full target-row census."""

    assert result == {
        "rows": 6_561,
        "components": 2_916,
        "component_histogram": {1: 729, 2: 1_458, 4: 729},
        "leak_components": 266,
        "leak_histogram": {1: 133, 2: 133},
        "total_nullity": 1_764,
        "leak_nullity_sum": 0,
        "leak_nullity_max": 0,
        "rank": 4_797,
        "separators": 0,
        "target_supported_nullities": 0,
    }


def check_zero_target_result(result: dict[str, object]) -> None:
    """Assert the corrected 6,558-row zero-target census."""

    assert result == {
        "rows": 6_558,
        "components": 2_915,
        "component_histogram": {1: 728, 2: 1_458, 3: 2, 4: 727},
        "leak_components": 265,
        "leak_histogram": {1: 132, 2: 133},
        "total_nullity": 1_764,
        "leak_nullity_sum": 0,
        "leak_nullity_max": 0,
        "rank": 4_794,
        "separators": 0,
        "target_supported_nullities": 0,
    }


def main() -> None:
    """Run the exact RTT primary verification."""

    started = perf_counter()
    assert len(MATCHINGS) == 105
    words = list(product(range(3), repeat=VERTICES))
    rows = {word: coefficient(word) for word in words}
    zero_target_rows = {
        word: row for word, row in rows.items() if not is_target_word(word)
    }
    assert len(rows) == 6_561
    assert len(zero_target_rows) == 6_558

    check_representative(rows)

    full_result = analyze_components(rows)
    zero_result = analyze_components(zero_target_rows)
    check_full_result(full_result)
    check_zero_target_result(zero_result)

    elapsed = perf_counter() - started
    print("GLS80-R2 RTT complete all-active linear nonseparation verifier passed")
    print("matching count: 105")
    print("source chart: Family-A S0 R2 R1 R0 T0 T0; all P0/Q0 rows retained")
    print("exact coefficient field: QQ(kappa4,kappa5)")
    print(
        f"full rows={full_result['rows']} target-supported nullities="
        f"{full_result['target_supported_nullities']} "
        f"full rank={full_result['rank']}"
    )
    print(
        f"zero-target rows={zero_result['rows']} "
        f"components={zero_result['components']} "
        f"sizes={zero_result['component_histogram']}"
    )
    print(
        f"leak components={zero_result['leak_components']} "
        f"sizes={zero_result['leak_histogram']} "
        f"nullity sum/max={zero_result['leak_nullity_sum']}/"
        f"{zero_result['leak_nullity_max']} "
        f"separators={zero_result['separators']}"
    )
    print(
        f"exact nonleak rank=stacked rank={zero_result['rank']} "
        f"total nullity={zero_result['total_nullity']}"
    )
    print(
        "scope: exact scalar linear row combinations only; nonlinear syzygies, "
        "activity localization, key exclusion, and arbitrary full-source "
        "couplings remain open"
    )
    print("global status: UNRESOLVED")
    print(f"elapsed seconds: {elapsed:.2f}")


if __name__ == "__main__":
    main()
