"""No-import audit of the GLS80 complete all-active linear no-go.

The audit uses the local torus normalization to set every nonzero ``T_0``
slope to one, reconstructs all eight-vertex coefficients by a pointed
hafnian recurrence, removes all three diagonal GHZ target words, and checks
the exact rational stacked-rank criterion on every nonleak incidence
component.  It imports neither a primary verifier nor a third-party package.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from time import perf_counter


P, Q = 0, 1
VERTICES = 8
LEAK = "I2500"

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]


def scalar(value: int = 1) -> Polynomial:
    return {(): value} if value else {}


def variable(name: str) -> Polynomial:
    return {(name,): 1}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + (
                left_coefficient * right_coefficient
            )
            if result[monomial] == 0:
                del result[monomial]
    return result


def crossed_edge(u: int, v: int, colour_u: int, colour_v: int) -> Polynomial:
    if u > v:
        u, v, colour_u, colour_v = v, u, colour_v, colour_u
    fixed = {
        (P, 2, 1, 1): 1,
        (Q, 2, 2, 2): 1,
        (P, 3, 2, 2): 1,
        (Q, 4, 1, 1): 1,
    }
    return scalar(fixed.get((u, v, colour_u, colour_v), 0))


def source_edge(
    source: int,
    port: int,
    source_colour: int,
    physical_colour: int,
    type_code: str,
) -> Polynomial:
    source_name = "P" if source == P else "Q"
    if type_code == "RTT" and port == 3:
        return (
            variable(f"{source_name}{port}{source_colour}")
            if physical_colour == 0
            else {}
        )
    if physical_colour == 0:
        return variable(f"{source_name}{port}{source_colour}0")
    # Torus-normalized T_0 slope one: colours 1 and 2 use one h coordinate.
    return variable(f"{source_name}{port}{source_colour}h")


def edge_entry(
    u: int,
    v: int,
    colour_u: int,
    colour_v: int,
    type_code: str,
) -> Polynomial:
    if u > v:
        u, v, colour_u, colour_v = v, u, colour_v, colour_u
    if (u, v) == (P, Q):
        return {}
    if u >= 2:
        return variable(f"I{u - 2}{v - 2}{colour_u}{colour_v}")
    if v >= 5:
        return source_edge(u, v - 2, colour_u, colour_v, type_code)
    return crossed_edge(u, v, colour_u, colour_v)


def coefficient(word: tuple[int, ...], type_code: str) -> Polynomial:
    """Compute one literal left-side matching coefficient recursively."""

    @lru_cache(maxsize=None)
    def hafnian(mask: int) -> tuple[tuple[Monomial, int], ...]:
        if mask == 0:
            return tuple(scalar().items())
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        result: Polynomial = {}
        partners = remainder
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            term = multiply(
                edge_entry(
                    first,
                    partner,
                    word[first],
                    word[partner],
                    type_code,
                ),
                dict(hafnian(remainder ^ partner_bit)),
            )
            result = add(result, term)
            partners ^= partner_bit
        return tuple(result.items())

    return dict(hafnian((1 << VERTICES) - 1))


def is_target(word: tuple[int, ...]) -> bool:
    return any(all(colour == target for colour in word) for target in range(3))


def rational_rank(matrix: list[list[int]], column_count: int) -> int:
    rows = [
        [Fraction(value) for value in row]
        for row in matrix
        if any(value != 0 for value in row)
    ]
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def audit_chart(type_code: str) -> dict[str, object]:
    all_words = list(product(range(3), repeat=VERTICES))
    rows = {
        word: coefficient(word, type_code) for word in all_words if not is_target(word)
    }
    words = list(rows)
    parent = list(range(len(words)))
    sizes = [1] * len(words)

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left = find(left)
        right = find(right)
        if left == right:
            return
        if sizes[left] < sizes[right]:
            left, right = right, left
        parent[right] = left
        sizes[left] += sizes[right]

    first_occurrence: dict[Monomial, int] = {}
    for position, word in enumerate(words):
        for monomial in rows[word]:
            if LEAK in monomial:
                continue
            previous = first_occurrence.setdefault(monomial, position)
            union(position, previous)

    component_words: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for position, word in enumerate(words):
        component_words[find(position)].append(word)

    component_histogram = Counter(len(block) for block in component_words.values())
    leak_histogram: Counter[int] = Counter()
    total_nullity = 0
    leak_nullity_sum = 0
    leak_nullity_max = 0
    leak_components = 0
    rank_sum = 0
    for word_block in component_words.values():
        block = [rows[word] for word in word_block]
        monomials = sorted(set().union(*(set(row) for row in block)))
        nonleak = [monomial for monomial in monomials if LEAK not in monomial]
        leak = [monomial for monomial in monomials if LEAK in monomial]
        nonleak_matrix = [
            [row.get(monomial, 0) for row in block] for monomial in nonleak
        ]
        leak_matrix = [[row.get(monomial, 0) for row in block] for monomial in leak]
        rank = rational_rank(nonleak_matrix, len(block))
        full_rank = rational_rank(nonleak_matrix + leak_matrix, len(block))
        assert rank == full_rank
        nullity = len(block) - rank
        total_nullity += nullity
        rank_sum += rank
        if not leak:
            continue
        leak_components += 1
        leak_histogram[len(block)] += 1
        leak_nullity_sum += nullity
        leak_nullity_max = max(leak_nullity_max, nullity)

    all_monomials = set().union(*(set(row) for row in rows.values()))
    nonleak_monomials = sum(LEAK not in monomial for monomial in all_monomials)
    leak_monomials = len(all_monomials) - nonleak_monomials
    nonleak_entries = sum(
        LEAK not in monomial for row in rows.values() for monomial in row
    )
    full_entries = sum(len(row) for row in rows.values())

    expected = {
        "RTT": {
            "components": 2_915,
            "histogram": {1: 728, 2: 1_458, 3: 2, 4: 727},
            "leak_components": 265,
            "leak_histogram": {1: 132, 2: 133},
            "nullity": 1_764,
            "leak_nullity_sum": 0,
            "leak_nullity_max": 0,
            "rank": 4_794,
        },
        "TTT": {
            "components": 1_943,
            "histogram": {1: 242, 2: 729, 4: 729, 7: 2, 8: 241},
            "leak_components": 323,
            "leak_histogram": {1: 80, 2: 162, 4: 81},
            "nullity": 1_098,
            "leak_nullity_sum": 55,
            "leak_nullity_max": 1,
            "rank": 5_460,
        },
    }[type_code]
    assert len(rows) == 6_558
    assert len(component_words) == expected["components"]
    assert dict(component_histogram) == expected["histogram"]
    assert leak_components == expected["leak_components"]
    assert dict(leak_histogram) == expected["leak_histogram"]
    assert total_nullity == expected["nullity"]
    assert leak_nullity_sum == expected["leak_nullity_sum"]
    assert leak_nullity_max == expected["leak_nullity_max"]
    assert rank_sum == expected["rank"]

    return {
        "rows": len(rows),
        "components": len(component_words),
        "histogram": dict(component_histogram),
        "leak_components": leak_components,
        "leak_histogram": dict(leak_histogram),
        "nullity": total_nullity,
        "leak_nullity_sum": leak_nullity_sum,
        "leak_nullity_max": leak_nullity_max,
        "rank": rank_sum,
        "nonleak_monomials": nonleak_monomials,
        "leak_monomials": leak_monomials,
        "nonleak_entries": nonleak_entries,
        "full_entries": full_entries,
    }


def main() -> None:
    started = perf_counter()
    results = {type_code: audit_chart(type_code) for type_code in ("RTT", "TTT")}
    print("GLS80 no-import complete all-active linear audit passed")
    for type_code, result in results.items():
        print(
            f"{type_code}: rows={result['rows']} components={result['components']} "
            f"sizes={result['histogram']}"
        )
        print(
            f"  leak-components={result['leak_components']} "
            f"sizes={result['leak_histogram']} nullity-sum/max="
            f"{result['leak_nullity_sum']}/{result['leak_nullity_max']}"
        )
        print(
            f"  exact nonleak/stacked rank={result['rank']}/{result['rank']} "
            f"total-nullity={result['nullity']}"
        )
        print(
            f"  monomials nonleak/leak={result['nonleak_monomials']}/"
            f"{result['leak_monomials']} entries nonleak/full="
            f"{result['nonleak_entries']}/{result['full_entries']}"
        )
    print(f"runtime seconds: {perf_counter() - started:.3f}")
    print("scope: exact universal scalar-linear zero-target row span only")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
