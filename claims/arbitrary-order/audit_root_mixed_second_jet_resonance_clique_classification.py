"""Independent no-import audit of the mixed-second-jet resonance cliques."""

from __future__ import annotations

import json
from itertools import combinations_with_replacement, permutations, product
from math import gcd

Row = tuple[int, int, int]


def projective(row: Row) -> Row:
    common = 0
    for value in row:
        common = gcd(common, abs(value))
    answer = tuple(value // common for value in row)
    leading = next(value for value in answer if value)
    if leading < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def rank_one_relation(a: Row, b: Row) -> bool:
    for zero in range(3):
        if a[zero] != 0 or b[zero] != 0:
            continue
        other = tuple(index for index in range(3) if index != zero)
        if a[other[0]] * b[other[0]] == a[other[1]] * b[other[1]]:
            return True
    return False


def classified(triple: tuple[Row, Row, Row]) -> str | None:
    if triple[0] == triple[1] == triple[2]:
        nonzero = [value for value in triple[0] if value]
        if len(nonzero) == 2 and nonzero[0] == nonzero[1]:
            return "balanced"
    supports = [{index for index, value in enumerate(row) if value} for row in triple]
    if {frozenset(item) for item in supports} == {
        frozenset({0}),
        frozenset({1}),
        frozenset({2}),
    }:
        return "axes"
    return None


def main() -> None:
    rows = sorted(
        {
            projective(row)
            for row in product(range(-3, 4), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    counts = {"balanced": 0, "axes": 0}
    checked_triples = 0
    permutation_checks = 0
    for triple in combinations_with_replacement(rows, 3):
        checked_triples += 1
        if not all(rank_one_relation(triple[i], triple[j]) for i in range(3) for j in range(i + 1, 3)):
            continue
        kind = classified(triple)
        if kind is None:
            raise AssertionError(("unclassified compatible triple", triple))
        counts[kind] += 1
        for permutation in permutations((0, 1, 2)):
            transformed = tuple(tuple(row[index] for index in permutation) for row in triple)
            if not all(rank_one_relation(transformed[i], transformed[j]) for i in range(3) for j in range(i + 1, 3)):
                raise AssertionError((triple, permutation))
            if classified(transformed) != kind:
                raise AssertionError((triple, transformed, kind))
            permutation_checks += 1

    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    fourth_partners = [row for row in rows if all(rank_one_relation(row, axis) for axis in axes)]
    if fourth_partners:
        raise AssertionError(fourth_partners)

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integers; no sympy or repository imports",
                "projective_covectors": len(rows),
                "checked_multiset_triples": checked_triples,
                "compatible_triples": counts,
                "permutation_checks": permutation_checks,
                "three_axis_fourth_partners": len(fourth_partners),
                "finite_boxes_are_theorem_evidence": False,
                "cofactor_realizability_proved": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
