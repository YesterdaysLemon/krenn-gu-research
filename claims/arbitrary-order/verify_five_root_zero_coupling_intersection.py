#!/usr/bin/env python3
"""Verify the combinatorics in the five-root intersection lemma."""

from __future__ import annotations

import itertools
import json
from collections import Counter


VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def exponent_vector(bits: tuple[int, ...]) -> tuple[int, ...]:
    exponents = [0] * len(VERTICES)
    for edge, endpoint in zip(EDGES, bits, strict=True):
        exponents[edge[endpoint]] += 1
    return tuple(exponents)


def relabel_orientation(
    bits: tuple[int, ...],
    permutation: tuple[int, ...],
) -> tuple[int, ...]:
    oriented = set()
    for (left, right), endpoint in zip(EDGES, bits, strict=True):
        head = (left, right)[endpoint]
        tail = (right, left)[endpoint]
        oriented.add((permutation[tail], permutation[head]))
    return tuple(
        1 if (left, right) in oriented else 0
        for left, right in EDGES
    )


def main() -> None:
    orientations = tuple(itertools.product((0, 1), repeat=len(EDGES)))
    histogram = Counter(map(exponent_vector, orientations))
    regular = tuple(
        bits
        for bits in orientations
        if exponent_vector(bits) == (2, 2, 2, 2, 2)
    )
    if len(orientations) != 1024 or len(regular) != 24:
        raise AssertionError("regular-tournament coefficient changed")

    # In the truncated Chow ring h_i^3=0, total degree ten leaves only
    # the exponent vector (2,2,2,2,2).
    surviving = {
        exponents: coefficient
        for exponents, coefficient in histogram.items()
        if all(exponent <= 2 for exponent in exponents)
    }
    if surviving != {(2, 2, 2, 2, 2): 24}:
        raise AssertionError("truncated Chow product changed")

    orbit = {
        relabel_orientation(bits, permutation)
        for bits in (regular[0],)
        for permutation in itertools.permutations(VERTICES)
    }
    stabilizer = tuple(
        permutation
        for permutation in itertools.permutations(VERTICES)
        if relabel_orientation(regular[0], permutation) == regular[0]
    )
    if orbit != set(regular) or len(stabilizer) != 5:
        raise AssertionError("regular-tournament orbit changed")

    print(
        json.dumps(
            {
                "verified": True,
                "ambient_variety": "(P2)^5",
                "dimension": 10,
                "bilinear_divisors": len(EDGES),
                "endpoint_choices": len(orientations),
                "top_intersection_coefficient": len(regular),
                "surviving_chow_monomial": "h0^2 h1^2 h2^2 h3^2 h4^2",
                "regular_tournament_orbits": 1,
                "regular_tournament_stabilizer": len(stabilizer),
                "conclusion": (
                    "every ten-form five-root system has a "
                    "simultaneous projective zero"
                ),
                "fully_supported_zero_guaranteed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
