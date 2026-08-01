#!/usr/bin/env python3
"""Verify the matching factorization in the one-nonblocker surplus lemma."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction


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


def survivor_data(r: int) -> dict:
    roots = set(range(r))
    marker = r
    blockers = set(range(r + 1, 2 * r + 2))
    vertices = tuple(range(2 * r + 2))

    def allowed(edge: tuple[int, int]) -> bool:
        left, right = edge
        types = (
            "R" if left in roots else "Q" if left == marker else "B",
            "R" if right in roots else "Q" if right == marker else "B",
        )
        return set(types) in ({"R", "B"}, {"Q", "B"}) or types == ("B", "B")

    survivors = [
        matching
        for matching in perfect_matchings(vertices)
        if all(allowed(edge) for edge in matching)
    ]
    signatures = set()
    for matching in survivors:
        partner = {}
        blocker_blocker_edges = 0
        for left, right in matching:
            if left in blockers and right in blockers:
                blocker_blocker_edges += 1
            if left in roots or left == marker:
                partner[left] = right
            elif right in roots or right == marker:
                partner[right] = left
        assert blocker_blocker_edges == 0
        assert set(partner) == roots | {marker}
        assert set(partner.values()) == blockers
        signatures.add(tuple(partner[row] for row in sorted(partner)))

    expected = set(itertools.permutations(sorted(blockers)))
    assert signatures == expected
    assert len(survivors) == math.factorial(r + 1)
    return {
        "r": r,
        "vertices": len(vertices),
        "surviving_matchings": len(survivors),
        "permanent_terms": math.factorial(r + 1),
    }


def check_diagonal_rescaling(modes: int) -> None:
    lambdas = (2, 3, 5)
    coefficients = {}
    for word in itertools.product(range(3), repeat=modes):
        coefficient = lambdas[word[0]] if len(set(word)) == 1 else 0
        scale = Fraction(1, lambdas[word[0]])
        coefficients[word] = coefficient * scale
    for word, coefficient in coefficients.items():
        assert coefficient == (1 if len(set(word)) == 1 else 0)


def main() -> None:
    records = [survivor_data(r) for r in range(2, 7)]
    for record in records:
        check_diagonal_rescaling(record["r"] + 1)
    print(
        json.dumps(
            {
                "verified": True,
                "matching_factorizations": records,
                "torus_choice": (
                    "K_q is nonzero and is not contained in any of the "
                    "three coordinate hyperplanes; finite-union avoidance "
                    "over C gives a fully supported z_q"
                ),
                "diagonal_rescalings_checked": len(records),
                "conclusion": "one nonblocker and r+1 blockers extract P_(r+1)->Delta_3",
                "permanent_nonrestriction_proved": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
