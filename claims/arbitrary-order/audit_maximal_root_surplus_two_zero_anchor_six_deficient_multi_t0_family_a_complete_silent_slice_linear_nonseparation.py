"""No-import audit of the GLS79 complete silent-slice theorem.

This audit does not import the primary verifier or any third-party algebra
package.  It first uses the proved local torus normalization to put every
nonzero ``T_0`` slope at one, reconstructs each eight-vertex coefficient
through a recursive hafnian expansion rather than a precomputed list of
perfect matchings, builds the nonleak incidence components, and checks the
stacked-rank criterion

    rank(N_C) = rank([N_C; L_C]).

The matrix calculation itself is over ``QQ`` at slope one; the theorem's
separate torus-equivariance lemma transports it to every nonzero slope.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from time import perf_counter

SLOPE = {3: 1, 4: 1}
P, Q = 0, 1
VERTEX_COUNT = 8
LEAK = "I2500"

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]


def normalize(poly: Polynomial) -> Polynomial:
    return {
        monomial: coefficient for monomial, coefficient in poly.items() if coefficient
    }


def scalar(value: int = 1) -> Polynomial:
    return {(): value} if value else {}


def indeterminate(name: str) -> Polynomial:
    return {(name,): 1}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return normalize(result)


def scale(factor: int, poly: Polynomial) -> Polynomial:
    return normalize(
        {monomial: factor * coefficient for monomial, coefficient in poly.items()}
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + (
                left_coefficient * right_coefficient
            )
    return normalize(result)


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
    if port == 5 and source_colour == 0:
        return {}
    source_name = "P" if source == P else "Q"
    port_type = "R" if type_code == "RTT" and port == 3 else "T"
    if port_type == "R":
        return (
            indeterminate(f"{source_name}{port}{source_colour}")
            if physical_colour == 0
            else {}
        )
    if physical_colour == 0:
        return indeterminate(f"{source_name}{port}{source_colour}0")
    row = indeterminate(f"{source_name}{port}{source_colour}h")
    if physical_colour == 1:
        return row
    if port == 5:
        # Every audited word has c_5=0, so this branch is unreachable.
        raise AssertionError("kappa5 must be inert on the c5=0 slice")
    return scale(SLOPE[port], row)


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
        return indeterminate(f"I{u - 2}{v - 2}{colour_u}{colour_v}")
    if v >= 5:
        return source_edge(u, v - 2, colour_u, colour_v, type_code)
    return crossed_edge(u, v, colour_u, colour_v)


def coefficient(word: tuple[int, ...], type_code: str) -> Polynomial:
    """Compute one coefficient by the pointed hafnian recurrence."""

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[tuple[Monomial, int], ...]:
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
            tail = dict(recurse(remainder ^ partner_bit))
            term = multiply(
                edge_entry(
                    first,
                    partner,
                    word[first],
                    word[partner],
                    type_code,
                ),
                tail,
            )
            result = add(result, term)
            partners ^= partner_bit
        return tuple(result.items())

    return dict(recurse((1 << VERTEX_COUNT) - 1))


def build_rows(type_code: str) -> dict[tuple[int, ...], Polynomial]:
    return {
        prefix + (0,): coefficient(prefix + (0,), type_code)
        for prefix in product(range(3), repeat=7)
    }


def contains_leak(poly: Polynomial) -> bool:
    return any(LEAK in monomial for monomial in poly)


def rational_rank(matrix: list[list[int]], column_count: int) -> int:
    """Return the exact rational row rank of a small integer matrix."""

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
    rows = build_rows(type_code)
    words = list(rows)
    target_word = (0,) * VERTEX_COUNT
    target_row = rows[target_word]
    target_nonleak = sum(LEAK not in monomial for monomial in target_row)
    target_leak = len(target_row) - target_nonleak
    assert (len(target_row), target_nonleak, target_leak) == (6, 4, 2)
    assert all(
        sum(monomial in row for row in rows.values()) == 1 for monomial in target_row
    )
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

    components: dict[int, list[Polynomial]] = defaultdict(list)
    for position, word in enumerate(words):
        components[find(position)].append(rows[word])

    component_histogram: dict[int, int] = defaultdict(int)
    leak_histogram: dict[int, int] = defaultdict(int)
    total_nullity = 0
    leak_nullity_sum = 0
    leak_nullity_max = 0
    leak_components = 0
    nonleak_rank = 0

    for block in components.values():
        component_histogram[len(block)] += 1
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
        nonleak_rank += rank
        if not any(contains_leak(row) for row in block):
            continue
        leak_components += 1
        leak_histogram[len(block)] += 1
        leak_nullity_sum += nullity
        leak_nullity_max = max(leak_nullity_max, nullity)

    expected = {
        "RTT": {
            "zero_rows": 162,
            "monomials": 16_767,
            "nonleak_monomials": 16_191,
            "leak_monomials": 576,
            "nonleak_entries": 21_294,
            "full_entries": 22_113,
            "components": 1_512,
            "component_histogram": {1: 837, 2: 675},
            "leak_components": 266,
            "leak_histogram": {1: 133, 2: 133},
            "nullity": 495,
            "leak_nullity_sum": 27,
            "leak_nullity_max": 1,
            "rank": 1_692,
            "zero_target_rank": 1_691,
            "zero_target_leak_components": 265,
            "zero_target_nonleak_monomials": 16_187,
            "zero_target_leak_monomials": 574,
            "zero_target_nonleak_entries": 21_290,
            "zero_target_full_entries": 22_107,
        },
        "TTT": {
            "zero_rows": 0,
            "monomials": 23_571,
            "nonleak_monomials": 22_590,
            "leak_monomials": 981,
            "nonleak_entries": 36_684,
            "full_entries": 38_637,
            "components": 972,
            "component_histogram": {1: 243, 2: 486, 4: 243},
            "leak_components": 324,
            "leak_histogram": {1: 81, 2: 162, 4: 81},
            "nullity": 288,
            "leak_nullity_sum": 100,
            "leak_nullity_max": 3,
            "rank": 1_899,
            "zero_target_rank": 1_898,
            "zero_target_leak_components": 323,
            "zero_target_nonleak_monomials": 22_586,
            "zero_target_leak_monomials": 979,
            "zero_target_nonleak_entries": 36_680,
            "zero_target_full_entries": 38_631,
        },
    }[type_code]
    monomial_count = len(set().union(*(set(row) for row in rows.values())))
    nonleak_monomials = len(
        {monomial for row in rows.values() for monomial in row if LEAK not in monomial}
    )
    leak_monomials = monomial_count - nonleak_monomials
    nonleak_entries = sum(
        LEAK not in monomial for row in rows.values() for monomial in row
    )
    full_entries = sum(len(row) for row in rows.values())
    zero_rows = sum(not row for row in rows.values())
    assert len(rows) == 2_187
    assert zero_rows == expected["zero_rows"]
    assert monomial_count == expected["monomials"]
    assert nonleak_monomials == expected["nonleak_monomials"]
    assert leak_monomials == expected["leak_monomials"]
    assert nonleak_entries == expected["nonleak_entries"]
    assert full_entries == expected["full_entries"]
    assert len(components) == expected["components"]
    assert dict(component_histogram) == expected["component_histogram"]
    assert leak_components == expected["leak_components"]
    assert dict(leak_histogram) == expected["leak_histogram"]
    assert total_nullity == expected["nullity"]
    assert leak_nullity_sum == expected["leak_nullity_sum"]
    assert leak_nullity_max == expected["leak_nullity_max"]
    assert nonleak_rank == expected["rank"]
    assert nonleak_rank - 1 == expected["zero_target_rank"]
    assert leak_components - 1 == expected["zero_target_leak_components"]
    assert nonleak_monomials - 4 == expected["zero_target_nonleak_monomials"]
    assert leak_monomials - 2 == expected["zero_target_leak_monomials"]
    assert nonleak_entries - 4 == expected["zero_target_nonleak_entries"]
    assert full_entries - 6 == expected["zero_target_full_entries"]

    return {
        "zero_rows": zero_rows,
        "monomials": monomial_count,
        "nonleak_monomials": nonleak_monomials,
        "leak_monomials": leak_monomials,
        "nonleak_entries": nonleak_entries,
        "full_entries": full_entries,
        "components": len(components),
        "component_histogram": dict(component_histogram),
        "leak_components": leak_components,
        "leak_histogram": dict(leak_histogram),
        "nullity": total_nullity,
        "leak_nullity_sum": leak_nullity_sum,
        "leak_nullity_max": leak_nullity_max,
        "rank": nonleak_rank,
        "zero_target_columns": len(rows) - 1,
        "zero_target_rank": nonleak_rank - 1,
        "zero_target_leak_components": leak_components - 1,
        "zero_target_nonleak_monomials": nonleak_monomials - 4,
        "zero_target_leak_monomials": leak_monomials - 2,
        "zero_target_nonleak_entries": nonleak_entries - 4,
        "zero_target_full_entries": full_entries - 6,
    }


def main() -> None:
    started = perf_counter()
    results = {type_code: audit_chart(type_code) for type_code in ("RTT", "TTT")}
    print("GLS79 no-import complete silent-slice audit passed")
    for type_code, result in results.items():
        print(
            f"{type_code}: rows=2187 zero={result['zero_rows']} "
            f"monomials={result['monomials']} components={result['components']} "
            f"sizes={result['component_histogram']}"
        )
        print(
            f"  leak-components={result['leak_components']} "
            f"sizes={result['leak_histogram']} "
            f"nullity-sum/max={result['leak_nullity_sum']}/"
            f"{result['leak_nullity_max']} exact stacked rank={result['rank']}"
        )
        print(
            f"  monomials nonleak/leak={result['nonleak_monomials']}/"
            f"{result['leak_monomials']} entries nonleak/full="
            f"{result['nonleak_entries']}/{result['full_entries']}"
        )
        print(
            f"  zero-target subset: columns={result['zero_target_columns']} "
            f"leak-components={result['zero_target_leak_components']} "
            f"exact stacked rank={result['zero_target_rank']}"
        )
        print(
            f"  zero-target monomials nonleak/leak="
            f"{result['zero_target_nonleak_monomials']}/"
            f"{result['zero_target_leak_monomials']} entries nonleak/full="
            f"{result['zero_target_nonleak_entries']}/"
            f"{result['zero_target_full_entries']}"
        )
    print(f"runtime seconds: {perf_counter() - started:.3f}")
    print("scope: exact linear c5=0 nonseparation only")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
