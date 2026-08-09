#!/usr/bin/env python3
"""Verify the exact two-port matching and seven-blocker incidence reduction."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matching_classification(r: int, surplus: int, residual: int) -> dict[str, int]:
    assert (surplus + residual) % 2 == 0
    roots = set(range(r))
    blockers = set(range(r, 2 * r + surplus))
    nonblockers = set(range(2 * r + surplus, 2 * r + surplus + residual))
    vertices = tuple(range(2 * r + surplus + residual))

    def allowed(edge: tuple[int, int]) -> bool:
        left, right = edge
        if left in roots and right in roots:
            return False
        return not (
            (left in roots and right in nonblockers)
            or (right in roots and left in nonblockers)
        )

    signatures = Counter()
    survivors = 0
    for matching in perfect_matchings(vertices):
        if not all(allowed(edge) for edge in matching):
            continue
        root_partners = {}
        for left, right in matching:
            if left in roots:
                root_partners[left] = right
            elif right in roots:
                root_partners[right] = left
        if set(root_partners) != roots:
            continue
        if not set(root_partners.values()) <= blockers:
            continue
        unused = tuple(sorted(blockers - set(root_partners.values())))
        assert len(unused) == surplus
        signatures[unused] += 1
        survivors += 1

    residual_matching_count = math.prod(
        range(surplus + residual - 1, 0, -2)
    )
    expected_per_signature = math.factorial(r) * residual_matching_count
    assert len(signatures) == math.comb(r + surplus, surplus)
    assert set(signatures.values()) == {expected_per_signature}
    assert survivors == len(signatures) * expected_per_signature
    return {
        "roots": r,
        "surplus": surplus,
        "residual_nonblockers": residual,
        "unused_blocker_sets": len(signatures),
        "matchings_per_set": expected_per_signature,
        "surviving_matchings": survivors,
    }


def canonical_type_ledger() -> dict[str, object]:
    colours = frozenset(range(3))
    proper_types = tuple(
        frozenset(subset)
        for size in (1, 2)
        for subset in itertools.combinations(range(3), size)
    )
    solutions = []
    for types in itertools.combinations_with_replacement(proper_types, 6):
        full = (colours,) + types
        counts = tuple(sum(colour in kind for kind in full) for colour in range(3))
        if counts == (5, 5, 5):
            solutions.append(tuple(tuple(sorted(kind)) for kind in full))
    assert len(solutions) == 1
    expected = (
        (0, 1, 2),
        (0, 1),
        (0, 1),
        (0, 2),
        (0, 2),
        (1, 2),
        (1, 2),
    )
    assert solutions[0] == expected

    # For seven nonempty blocker types with at least fifteen total
    # incidences, t3-t1 is at least one.
    checked = 0
    all_types = tuple(
        frozenset(subset)
        for size in (1, 2, 3)
        for subset in itertools.combinations(range(3), size)
    )
    for types in itertools.combinations_with_replacement(all_types, 7):
        counts = tuple(sum(colour in kind for kind in types) for colour in range(3))
        if min(counts) < 5:
            continue
        histogram = Counter(map(len, types))
        assert histogram[3] - histogram[1] >= 1
        checked += 1
    assert checked > 0
    return {
        "minimal_profile": ["012", "01", "01", "02", "02", "12", "12"],
        "overlapping_p5_systems": 3,
        "incidence_profiles_checked": checked,
    }


def main() -> None:
    records = [
        matching_classification(roots, surplus, residual)
        for roots, surplus, residual in (
            (2, 0, 0),
            (2, 0, 2),
            (2, 1, 1),
            (2, 1, 3),
            (2, 2, 0),
            (2, 2, 2),
            (2, 3, 1),
            (3, 2, 0),
            (3, 3, 1),
            (4, 2, 0),
            (5, 2, 0),
        )
    ]
    seven = records[-1]
    assert seven["unused_blocker_sets"] == 21
    assert seven["matchings_per_set"] == math.factorial(5)
    ledger = canonical_type_ledger()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero combinatorial identity",
                "matching_factorizations": records,
                "five_root_seven_blocker_terms": 21,
                "residual_cofactor_degree": 2,
                "canonical_minimal_cell": ledger,
                "arbitrary_surplus_formula_replayed": True,
                "higher_surplus_factorization_proved": False,
                "p6_extracted": False,
                "p7_extracted_without_extra_factorization": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
