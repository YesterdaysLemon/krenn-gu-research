"""Exact active-``T_0`` leakage-row audit for the GLS78 boundary.

This verifier is deliberately scoped to the coefficient-side question left by
GLS78: can complete eight-vertex rows with the silent port at ``5`` isolate
the off-kernel coefficient ``I2500 = [e_(2,0)e_(5,0)]W_25`` after the
active-``T_0`` repair channels are retained?

The source normalization is the GLS71 crossed chart.  The model keeps every
physical edge entry free, keeps all ``P_1,P_2,Q_1,Q_2`` rows at ``T_0`` ports,
and only imposes the ``P_0,Q_0`` silence at port ``5``.  Thus the row-span
checks do not assume the later ``C=0`` restricted control or ``alpha=0``.

The representative expansion and the block nonseparation checks are exact
over the independent slope field ``QQ(kappa3,kappa4,kappa5)`` (only
``kappa4`` appears in the active-port difference, and the c_5=0 slice makes
``kappa5`` inert).  The final global row-span ranks are two modular controls
and are printed explicitly as evidence only; they are not a characteristic-
zero proof.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product
from time import perf_counter

import sympy as sp


KAPPA3, KAPPA4, KAPPA5 = sp.symbols("kappa3 kappa4 kappa5")
T_SLOPE = {3: KAPPA3, 4: KAPPA4, 5: KAPPA5}
P, Q = 0, 1
VERTICES = 8
WORD_LENGTH = 8
LEAK = "I2500"

Poly = dict[tuple[str, ...], sp.Expr]


def clean(poly: Poly) -> Poly:
    out: Poly = {}
    for monomial, coefficient in poly.items():
        value = sp.expand(coefficient)
        if value != 0:
            out[monomial] = value
    return out


def one(value: int = 1) -> Poly:
    return {(): sp.Integer(value)} if value else {}


def variable(name: str) -> Poly:
    return {(name,): sp.Integer(1)}


def add(*polynomials: Poly) -> Poly:
    out: Poly = {}
    for poly in polynomials:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, sp.Integer(0)) + coefficient
    return clean(out)


def negate(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def scale(factor: sp.Expr, poly: Poly) -> Poly:
    return clean({monomial: factor * coefficient for monomial, coefficient in poly.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = out.get(monomial, sp.Integer(0)) + (
                left_coefficient * right_coefficient
            )
    return clean(out)


def subtract(left: Poly, right: Poly) -> Poly:
    return add(left, negate(right))


def assert_poly_equal(left: Poly, right: Poly) -> None:
    assert clean(subtract(left, right)) == {}, (left, right)


@lru_cache(maxsize=None)
def matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return all perfect matchings of the vertices in ``mask``."""

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


def word_index(word: tuple[int, ...]) -> int:
    index = 0
    for digit in word:
        index = 3 * index + digit
    return index


def crossed_source_edge(u: int, v: int, colour_u: int, colour_v: int) -> Poly:
    """The four nonzero central entries of the GLS71 crossed chart."""

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
    outside_types: dict[int, str],
) -> Poly:
    """Return a source-to-outside entry in an R/T row-plane chart.

    Physical vertices are numbered ``2 + port``.  At a ``T_0`` port the row
    plane is ``span(e_0^*, h)`` with ``h=e_1^*+kappa_u e_2^*`` at port ``u``.  Port 5 is
    silent for the missing ``P_0,Q_0`` source colour only; all other source
    colours are deliberately retained.
    """

    if outside_port == 5 and source_colour == 0:
        return {}

    source_name = "P" if source == P else "Q"
    if outside_types[outside_port] == "R":
        return variable(f"{source_name}{outside_port}{source_colour}") if physical_colour == 0 else {}

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
    outside_types: dict[int, str],
) -> Poly:
    """Return one entry of the full eight-vertex matching matrix."""

    if u > v:
        u, v, colour_u, colour_v = v, u, colour_v, colour_u
    if (u, v) == (P, Q):
        return {}
    if u >= 2:
        left_port, right_port = u - 2, v - 2
        return variable(f"I{left_port}{right_port}{colour_u}{colour_v}")
    if v >= 5:
        return source_edge(u, v - 2, colour_u, colour_v, outside_types)
    return crossed_source_edge(u, v, colour_u, colour_v)


@lru_cache(maxsize=None)
def coefficient(word: tuple[int, ...], type_code: str) -> Poly:
    """Expand the complete source identity for one colour word."""

    outside_types = {
        3: "R" if type_code == "RTT" else "T",
        4: "T",
        5: "T",
    }
    out: Poly = {}
    for matching in MATCHINGS:
        term = one()
        for u, v in matching:
            term = multiply(
                term,
                edge(u, v, word[u], word[v], outside_types),
            )
            if not term:
                break
        out = add(out, term)

    if all(colour == 1 for colour in word):
        out = add(out, scale(-1, variable("mu1")))
    elif all(colour == 2 for colour in word):
        out = add(out, scale(-1, variable("mu2")))
    return out


def rows_with_silent_port(type_code: str) -> dict[tuple[int, ...], Poly]:
    """Build the 3^7 complete rows with ``c_5=0``."""

    return {
        word: coefficient(word, type_code)
        for word in product(range(3), repeat=7)
        for word in [word + (0,)]
    }


def has_leak(poly: Poly) -> bool:
    return any(LEAK in monomial for monomial in poly)


def representative_expected(type_code: str) -> Poly:
    """Expected active-T4 difference for the representative rows.

    The ``r=3`` expression has ``P300`` instead of the ``r=2`` ``P30``
    factor because port 3 is also a ``T_0`` port.
    """

    p3 = variable("P30" if type_code == "RTT" else "P300")
    q520 = variable("Q520")
    d24 = subtract(variable("I2402"), scale(KAPPA4, variable("I2401")))
    d14 = subtract(variable("I1422"), scale(KAPPA4, variable("I1421")))
    d04 = subtract(variable("I0422"), scale(KAPPA4, variable("I0421")))
    d45 = subtract(variable("I4520"), scale(KAPPA4, variable("I4510")))
    repair_from_q5 = add(
        multiply(variable("I0122"), d24),
        multiply(variable("I0220"), d14),
        multiply(variable("I1220"), d04),
    )
    direct = add(
        scale(1, multiply(variable("I1220"), d45)),
        multiply(variable(LEAK), d14),
        multiply(variable("I1520"), d24),
    )
    return multiply(p3, add(multiply(q520, repair_from_q5), direct))


def check_representative(type_code: str, rows: dict[tuple[int, ...], Poly]) -> None:
    row_1 = (0, 2, 2, 2, 0, 0, 1, 0)
    row_2 = (0, 2, 2, 2, 0, 0, 2, 0)
    assert word_index(row_1) == 2109
    assert word_index(row_2) == 2112
    actual = subtract(rows[row_2], scale(KAPPA4, rows[row_1]))
    assert_poly_equal(actual, representative_expected(type_code))
    assert has_leak(actual)


def block_rows(
    rows: dict[tuple[int, ...], Poly],
    base: tuple[int, ...],
    vary_c3_and_c4: bool,
) -> list[Poly]:
    if vary_c3_and_c4:
        p, q, c0, c1 = base
        words = [
            (p, q, c0, c1, 0, c3, c4, 0)
            for c3 in range(3)
            for c4 in range(3)
        ]
    else:
        p, q, c0, c1, c3 = base
        words = [(p, q, c0, c1, 0, c3, c4, 0) for c4 in range(3)]
    return [rows[word] for word in words]


def exact_nonseparation(rows: list[Poly]) -> tuple[bool, int]:
    """Check that every nonleak-cancelling combination kills leakage too."""

    monomials = sorted(set().union(*(set(row) for row in rows)))
    nonleak = [monomial for monomial in monomials if LEAK not in monomial]
    leak = [monomial for monomial in monomials if LEAK in monomial]
    matrix = sp.Matrix(
        [
            [row.get(monomial, sp.Integer(0)) for row in rows]
            for monomial in nonleak
        ]
    )
    nullspace = matrix.nullspace()
    for vector in nullspace:
        for monomial in leak:
            residual = sum(
                vector[column] * rows[column].get(monomial, sp.Integer(0))
                for column in range(len(rows))
            )
            if sp.factor(residual) != 0:
                return False, len(nullspace)
    return True, len(nullspace)


def check_exact_blocks(type_code: str, rows: dict[tuple[int, ...], Poly]) -> dict[str, int]:
    """Run exact three-row and 3x3-block tests in the active slope field.

    The RTT expressions use only ``kappa4``.  The TTT expressions use
    ``kappa3,kappa4``; ``kappa5`` is absent because every tested row has
    ``c_5=0`` and the ``P_0,Q_0`` source entries at port 5 are silent.
    """

    three_row_leak_blocks = 0
    three_row_separators = 0
    three_row_nullity_sum = 0
    three_row_max_nullity = 0

    for base in product(range(3), repeat=5):
        block = block_rows(rows, base, vary_c3_and_c4=False)
        difference = subtract(block[2], scale(KAPPA4, block[1]))
        if not has_leak(difference):
            continue
        three_row_leak_blocks += 1
        separated, nullity = exact_nonseparation(block)
        assert separated
        three_row_nullity_sum += nullity
        three_row_max_nullity = max(three_row_max_nullity, nullity)
        if not separated:
            three_row_separators += 1

    three_by_three_blocks = 0
    three_by_three_separators = 0
    three_by_three_nullity_sum = 0
    three_by_three_max_nullity = 0
    for base in product(range(3), repeat=4):
        block = block_rows(rows, base, vary_c3_and_c4=True)
        assert any(has_leak(row) for row in block)
        three_by_three_blocks += 1
        separated, nullity = exact_nonseparation(block)
        assert separated
        three_by_three_nullity_sum += nullity
        three_by_three_max_nullity = max(three_by_three_max_nullity, nullity)
        if not separated:
            three_by_three_separators += 1

    expected_three_rows = {"RTT": 28, "TTT": 78}[type_code]
    expected_three_sum = {"RTT": 0, "TTT": 0}[type_code]
    expected_three_max = {"RTT": 0, "TTT": 0}[type_code]
    expected_grid_sum = {"RTT": 173, "TTT": 100}[type_code]
    expected_grid_max = {"RTT": 7, "TTT": 5}[type_code]
    assert three_row_leak_blocks == expected_three_rows
    assert three_row_separators == 0
    assert three_row_nullity_sum == expected_three_sum
    assert three_row_max_nullity == expected_three_max
    assert three_by_three_blocks == 81
    assert three_by_three_separators == 0
    assert three_by_three_nullity_sum == expected_grid_sum
    assert three_by_three_max_nullity == expected_grid_max
    return {
        "three_row_leak_blocks": three_row_leak_blocks,
        "three_row_separators": three_row_separators,
        "three_row_nullity_sum": three_row_nullity_sum,
        "three_row_max_nullity": three_row_max_nullity,
        "three_by_three_blocks": three_by_three_blocks,
        "three_by_three_separators": three_by_three_separators,
        "three_by_three_nullity_sum": three_by_three_nullity_sum,
        "three_by_three_max_nullity": three_by_three_max_nullity,
    }


def evaluate_modular(
    value: sp.Expr,
    kappa_values: tuple[int, int, int],
    prime: int,
) -> int:
    kappa3, kappa4, kappa5 = kappa_values
    return int(
        value.subs(
            {
                KAPPA3: kappa3,
                KAPPA4: kappa4,
                KAPPA5: kappa5,
            }
        )
    ) % prime


def exact_field(type_code: str) -> str:
    return "QQ(kappa4)" if type_code == "RTT" else "QQ(kappa3,kappa4)"


def insert_reduced(row: dict[int, int], pivots: dict[int, dict[int, int]], prime: int) -> bool:
    """Sparse Gaussian insertion; return whether the row raises rank."""

    while row:
        pivot = min(row)
        if pivot not in pivots:
            inverse = pow(row[pivot], -1, prime)
            pivots[pivot] = {
                column: coefficient * inverse % prime
                for column, coefficient in row.items()
                if coefficient * inverse % prime
            }
            return True
        factor = row[pivot]
        pivot_row = pivots[pivot]
        for column, coefficient in pivot_row.items():
            residual = (row.get(column, 0) - factor * coefficient) % prime
            if residual:
                row[column] = residual
            elif column in row:
                del row[column]
    return False


def modular_global_rank(
    type_code: str,
    rows: dict[tuple[int, ...], Poly],
    kappa_values: tuple[int, int, int],
    prime: int,
) -> tuple[int, int, int, int]:
    """Return (row count, monomial count, nonleak rank, leak increment)."""

    words = sorted(rows)
    word_positions = {word: position for position, word in enumerate(words)}
    coefficient_vectors: dict[tuple[str, ...], dict[int, int]] = defaultdict(dict)
    for word in words:
        position = word_positions[word]
        for monomial, value in rows[word].items():
            coefficient = evaluate_modular(value, kappa_values, prime)
            if coefficient:
                previous = coefficient_vectors[monomial].get(position, 0)
                coefficient_vectors[monomial][position] = (previous + coefficient) % prime
                if coefficient_vectors[monomial][position] == 0:
                    del coefficient_vectors[monomial][position]

    pivots: dict[int, dict[int, int]] = {}
    nonleak_rank = 0
    for monomial, vector in coefficient_vectors.items():
        if LEAK not in monomial and insert_reduced(dict(vector), pivots, prime):
            nonleak_rank += 1

    leak_rank_increment = 0
    for monomial, vector in coefficient_vectors.items():
        if LEAK in monomial and insert_reduced(dict(vector), pivots, prime):
            leak_rank_increment += 1

    return len(words), len(coefficient_vectors), nonleak_rank, leak_rank_increment


def check_modular_controls(
    type_code: str,
    rows: dict[tuple[int, ...], Poly],
) -> list[tuple[int, int, int, int, int, int, int]]:
    controls = [
        (1_000_003, (2, 3, 5)),
        (1_000_033, (5, 7, 11)),
    ]
    expected = {
        "RTT": (16_767, 1_692),
        "TTT": (23_571, 1_899),
    }
    results = []
    for prime, kappa_values in controls:
        row_count, monomial_count, nonleak_rank, leak_increment = modular_global_rank(
            type_code, rows, kappa_values, prime
        )
        assert row_count == 2_187
        assert (monomial_count, nonleak_rank) == expected[type_code]
        assert leak_increment == 0
        results.append(
            (
                prime,
                *kappa_values,
                monomial_count,
                nonleak_rank,
                leak_increment,
            )
        )
    return results


def main() -> None:
    started = perf_counter()
    assert len(MATCHINGS) == 105

    exact_results: dict[str, dict[str, int]] = {}
    modular_results: dict[str, list[tuple[int, int, int, int, int, int, int]]] = {}
    for type_code in ("RTT", "TTT"):
        rows = rows_with_silent_port(type_code)
        check_representative(type_code, rows)
        exact_results[type_code] = check_exact_blocks(type_code, rows)
        modular_results[type_code] = check_modular_controls(type_code, rows)

    elapsed = perf_counter() - started
    print("GLS78 active-T leakage row-span verifier passed")
    print("complete matching count: 105")
    for type_code in ("RTT", "TTT"):
        result = exact_results[type_code]
        print(
            f"{type_code} representative rows: exact {exact_field(type_code)} expansion passed "
            f"(2109, 2112)"
        )
        print(
            f"{type_code} exact {exact_field(type_code)} 3-row blocks with leakage difference: "
            f"{result['three_row_leak_blocks']}; separators: "
            f"{result['three_row_separators']}; nullity sum/max: "
            f"{result['three_row_nullity_sum']}/{result['three_row_max_nullity']}"
        )
        print(
            f"{type_code} exact {exact_field(type_code)} 3x3 (c3,c4) blocks: "
            f"{result['three_by_three_blocks']}; separators: "
            f"{result['three_by_three_separators']}; nullity sum/max: "
            f"{result['three_by_three_nullity_sum']}/"
            f"{result['three_by_three_max_nullity']}"
        )
        print("global modular row ranks (evidence only; not a characteristic-zero proof):")
        for (
            prime,
            kappa3,
            kappa4,
            kappa5,
            monomial_count,
            nonleak_rank,
            leak_increment,
        ) in modular_results[type_code]:
            print(
                f"  {type_code} p={prime}, (kappa3,kappa4,kappa5)="
                f"({kappa3},{kappa4},{kappa5}): "
                f"rows=2187 monomials={monomial_count} "
                f"nonleak-rank={nonleak_rank} leak-rank-increment={leak_increment}"
            )
    print(f"runtime seconds: {elapsed:.3f}")
    print("scope: Family-A r=2/r=3 leakage boundary only")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
