"""Exact all-active ``r=3`` linear leakage nonseparation verifier.

This is the primary verifier for the Family-A chart
``S_0 R_2 R_1 T_0 T_0 T_0``.  It expands the complete eight-vertex matching
polynomial with all three active ``T_0`` ports and retains every source-row
coordinate, including the ``P_0`` and ``Q_0`` coordinates at port ``5``.

For the 6,558 zero-target colour rows, the verifier splits the literal
monomial space into the part containing ``I2500`` and its complement.  An
exact incidence-component decomposition over
``QQ(kappa3,kappa4,kappa5)`` proves that the right kernel of the nonleak
projection is contained in the right kernel of the leakage projection.
Thus no scalar linear combination of these complete rows can cancel all
repair terms while retaining an ``I2500`` term.

The calculation is a scoped source-integrability obstruction.  It does not
test nonlinear coefficient-ideal syzygies, arbitrary multipliers, activity
localization, either key exclusion, or the global conjecture.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from time import perf_counter

import sympy as sp


KAPPA3, KAPPA4, KAPPA5 = sp.symbols("kappa3 kappa4 kappa5")
T_SLOPE = {3: KAPPA3, 4: KAPPA4, 5: KAPPA5}
P, Q = 0, 1
VERTICES = 8
LEAK = "I2500"

Poly = dict[tuple[str, ...], sp.Expr]


def clean(poly: Poly) -> Poly:
    """Remove zero coefficients after exact expansion."""

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
    """Return one literal edge/source coordinate."""

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


def active_source_edge(
    source: int,
    outside_port: int,
    source_colour: int,
    physical_colour: int,
) -> Poly:
    """Return every source entry in the active ``T_0`` row plane.

    The row plane is ``span(e_0^*, e_1^*+kappa_u e_2^*)``.  In particular,
    unlike the earlier one-silent slice, source colour ``0`` at port ``5``
    is retained.
    """

    source_name = "P" if source == P else "Q"
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
        return active_source_edge(u, v - 2, colour_u, colour_v)
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

    if all(colour == 0 for colour in word):
        out = add(out, scale(-1, variable("mu0")))
    elif all(colour == 1 for colour in word):
        out = add(out, scale(-1, variable("mu1")))
    elif all(colour == 2 for colour in word):
        out = add(out, scale(-1, variable("mu2")))
    return out


def is_zero_target(word: tuple[int, ...]) -> bool:
    """Return whether the colour word has no diagonal GHZ target term."""

    return not is_target_word(word)


def is_target_word(word: tuple[int, ...]) -> bool:
    """Return whether a word is one of the three pure GHZ target words."""

    return any(all(colour == target for colour in word) for target in range(3))


def has_leak(poly: Poly) -> bool:
    """Return whether a polynomial contains an ``I2500`` monomial."""

    return any(LEAK in monomial for monomial in poly)


def expected_representative_difference() -> Poly:
    """Return the full-source port-4 difference used as a regression check."""

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
                multiply(variable("P300"), variable("Q520")),
                multiply(variable("P500"), variable("Q320")),
            ),
            q_repair,
        ),
        multiply(
            variable("I1220"),
            add(
                multiply(variable("P500"), d34),
                multiply(variable("P300"), d45),
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
            variable("P300"),
            add(
                multiply(variable(LEAK), d14),
                multiply(variable("I1520"), d24),
            ),
        ),
    )


def expected_two_port_difference() -> Poly:
    """Return the exact ``D_3 D_4`` repair expression.

    This difference is included to make the cross-port direction explicit:
    it removes the ``I2500`` term while retaining a port-5 source repair.
    """

    d342 = add(
        variable("I3422"),
        scale(-KAPPA4, variable("I3421")),
        scale(-KAPPA3, variable("I3412")),
        scale(KAPPA3 * KAPPA4, variable("I3411")),
    )
    d24 = subtract(variable("I2402"), scale(KAPPA4, variable("I2401")))
    d132 = subtract(variable("I1322"), scale(KAPPA3, variable("I1321")))
    d142 = subtract(variable("I1422"), scale(KAPPA4, variable("I1421")))
    d230 = subtract(variable("I2302"), scale(KAPPA3, variable("I2301")))
    return multiply(
        variable("P500"),
        add(
            multiply(variable("I1220"), d342),
            multiply(d132, d24),
            multiply(d142, d230),
        ),
    )


def check_representative(rows: dict[tuple[int, ...], Poly]) -> None:
    """Check the named full-source leakage identity."""

    row_1 = (0, 2, 2, 2, 0, 0, 1, 0)
    row_2 = (0, 2, 2, 2, 0, 0, 2, 0)
    assert rows[row_1]
    assert rows[row_2]
    actual = subtract(rows[row_2], scale(KAPPA4, rows[row_1]))
    assert_poly_equal(actual, expected_representative_difference())
    assert has_leak(actual)
    assert any("P500" in monomial for monomial in actual)


def check_two_port_difference(rows: dict[tuple[int, ...], Poly]) -> None:
    """Check that a second active-port difference kills the named leak."""

    prefix = (0, 2, 2, 2, 0)

    def row(c3: int, c4: int) -> Poly:
        return rows[prefix + (c3, c4, 0)]

    actual = add(
        row(2, 2),
        scale(-KAPPA4, row(2, 1)),
        scale(-KAPPA3, row(1, 2)),
        scale(KAPPA3 * KAPPA4, row(1, 1)),
    )
    assert_poly_equal(actual, expected_two_port_difference())
    assert not has_leak(actual)


def component_word_blocks(
    rows: dict[tuple[int, ...], Poly],
) -> list[list[tuple[int, ...]]]:
    """Split rows by shared nonleak monomials.

    If two rows share a nonleak monomial, their columns are joined.  The
    resulting connected components are the exact block decomposition of the
    nonleak coefficient matrix.
    """

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


def component_blocks(rows: dict[tuple[int, ...], Poly]) -> list[list[Poly]]:
    """Return the polynomial blocks corresponding to ``component_word_blocks``."""

    return [[rows[word] for word in words] for words in component_word_blocks(rows)]


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


def component_nullity_and_nonseparation(block: list[Poly]) -> tuple[int, bool]:
    """Return exact nonleak nullity and whether leakage is also killed."""

    leak, nullspace = nonleak_nullspace(block)
    for vector in nullspace:
        for monomial in leak:
            residual = sum(
                vector[column] * block[column].get(monomial, sp.Integer(0))
                for column in range(len(block))
            )
            if sp.factor(residual) != 0:
                return len(nullspace), False
    return len(nullspace), True


def check_full_target_components(
    rows: dict[tuple[int, ...], Poly],
) -> dict[str, object]:
    """Check target rows and leakage on the complete 6,561-row family."""

    blocks_by_word = component_word_blocks(rows)
    blocks = [[rows[word] for word in words] for words in blocks_by_word]
    component_histogram = Counter(len(block) for block in blocks)
    leak_blocks = [block for block in blocks if any(has_leak(row) for row in block)]
    leak_histogram = Counter(len(block) for block in leak_blocks)

    total_nullity = 0
    leak_nullity_sum = 0
    leak_nullity_max = 0
    separators = 0
    target_supported_nullities = 0
    for words, block in zip(blocks_by_word, blocks):
        leak, nullspace = nonleak_nullspace(block)
        total_nullity += len(nullspace)
        if any(has_leak(row) for row in block):
            leak_nullity_sum += len(nullspace)
            leak_nullity_max = max(leak_nullity_max, len(nullspace))
            for vector in nullspace:
                residuals = [
                    sum(
                        vector[column] * block[column].get(monomial, sp.Integer(0))
                        for column in range(len(block))
                    )
                    for monomial in leak
                ]
                if any(sp.factor(residual) != 0 for residual in residuals):
                    separators += 1
        for vector in nullspace:
            if any(
                value != 0 and is_target_word(word)
                for word, value in zip(words, vector)
            ):
                target_supported_nullities += 1

    assert len(rows) == 6_561
    assert len(blocks) == 1_944
    assert dict(component_histogram) == {1: 243, 2: 729, 4: 729, 8: 243}
    assert len(leak_blocks) == 324
    assert dict(leak_histogram) == {1: 81, 2: 162, 4: 81}
    assert total_nullity == 1_098
    assert leak_nullity_sum == 55
    assert leak_nullity_max == 1
    assert separators == 0
    assert target_supported_nullities == 0
    assert len(rows) - total_nullity == 5_463

    return {
        "rows": len(rows),
        "components": len(blocks),
        "component_histogram": dict(component_histogram),
        "leak_components": len(leak_blocks),
        "leak_histogram": dict(leak_histogram),
        "total_nullity": total_nullity,
        "leak_nullity_sum": leak_nullity_sum,
        "leak_nullity_max": leak_nullity_max,
        "rank": 5_463,
        "separators": separators,
        "target_supported_nullities": target_supported_nullities,
    }


def check_exact_component_census(
    rows: dict[tuple[int, ...], Poly],
) -> dict[str, object]:
    """Assert the complete exact zero-target row census and inclusion."""

    blocks = component_blocks(rows)
    component_histogram = Counter(len(block) for block in blocks)
    leak_blocks = [block for block in blocks if any(has_leak(row) for row in block)]
    leak_histogram = Counter(len(block) for block in leak_blocks)

    total_nullity = 0
    leak_nullity_sum = 0
    leak_nullity_max = 0
    separators = 0
    for block in blocks:
        nullity, nonseparating = component_nullity_and_nonseparation(block)
        total_nullity += nullity
        if any(has_leak(row) for row in block):
            leak_nullity_sum += nullity
            leak_nullity_max = max(leak_nullity_max, nullity)
            if not nonseparating:
                separators += 1

    expected_histogram = {1: 242, 2: 729, 4: 729, 7: 2, 8: 241}
    expected_leak_histogram = {1: 80, 2: 162, 4: 81}
    expected_total_nullity = 1_098
    expected_rank = 5_460
    assert len(rows) == 6_558
    assert len(blocks) == 1_943
    assert dict(component_histogram) == expected_histogram
    assert len(leak_blocks) == 323
    assert dict(leak_histogram) == expected_leak_histogram
    assert total_nullity == expected_total_nullity
    assert leak_nullity_sum == 55
    assert leak_nullity_max == 1
    assert separators == 0
    assert len(rows) - total_nullity == expected_rank

    return {
        "rows": len(rows),
        "components": len(blocks),
        "component_histogram": dict(component_histogram),
        "leak_components": len(leak_blocks),
        "leak_histogram": dict(leak_histogram),
        "total_nullity": total_nullity,
        "leak_nullity_sum": leak_nullity_sum,
        "leak_nullity_max": leak_nullity_max,
        "rank": expected_rank,
        "separators": separators,
    }


def main() -> None:
    """Run the exact primary verification."""

    started = perf_counter()
    assert len(MATCHINGS) == 105
    words = list(product(range(3), repeat=VERTICES))
    all_rows = {word: coefficient(word) for word in words}
    zero_target_rows = {
        word: row for word, row in all_rows.items() if is_zero_target(word)
    }

    check_representative(all_rows)
    check_two_port_difference(all_rows)
    full_result = check_full_target_components(all_rows)
    result = check_exact_component_census(zero_target_rows)

    elapsed = perf_counter() - started
    print("GLS80 r=3 complete all-active linear nonseparation verifier passed")
    print("matching count: 105")
    print("source chart: Family-A S0 R2 R1 T0 T0 T0; all P0/Q0 rows retained")
    print("exact coefficient field: QQ(kappa3,kappa4,kappa5)")
    print(
        f"full rows={full_result['rows']} target-supported nullities="
        f"{full_result['target_supported_nullities']} "
        f"full rank={full_result['rank']}"
    )
    print(
        f"zero-target rows={result['rows']} components={result['components']} "
        f"sizes={result['component_histogram']}"
    )
    print(
        f"leak components={result['leak_components']} "
        f"sizes={result['leak_histogram']} "
        f"nullity sum/max={result['leak_nullity_sum']}/"
        f"{result['leak_nullity_max']} separators={result['separators']}"
    )
    print(
        f"exact nonleak rank=stacked rank={result['rank']} "
        f"total nullity={result['total_nullity']}"
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
