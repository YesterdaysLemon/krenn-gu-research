#!/usr/bin/env python3
"""Verify the maximal-overlap GHZ coefficient-hypercube theorem."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_MAXIMAL_OVERLAP_GHZ_HYPERCUBE.md"
Edge = tuple[str, str]
Monomial = tuple[Edge, ...]


def edge(left: str, right: str) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[str, ...], allowed) -> tuple[Monomial, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        if not allowed(first, second):
            continue
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining, allowed):
            output.append(tuple(sorted((edge(first, second), *tail))))
    return tuple(output)


def complete_matchings(vertices: tuple[str, ...]) -> tuple[Monomial, ...]:
    return perfect_matchings(vertices, lambda _left, _right: True)


def labels(q_size: int):
    roots = tuple(f"r{index}" for index in range(4))
    blockers = tuple(f"u{index}" for index in range(6))
    residual = ("a", "b", *(f"q{index}" for index in range(q_size)))
    return roots, blockers, residual


def common_root_survivors(q_size: int) -> Counter[Monomial]:
    roots, blockers, residual = labels(q_size)
    root_set = frozenset(roots)
    blocker_set = frozenset(blockers)

    def allowed(left: str, right: str) -> bool:
        if left in root_set:
            return right in blocker_set
        if right in root_set:
            return left in blocker_set
        return True

    return Counter(perfect_matchings((*roots, *blockers, *residual), allowed))


def cofactor_master(q_size: int) -> Counter[Monomial]:
    roots, blockers, residual = labels(q_size)
    output: Counter[Monomial] = Counter()
    for unused in itertools.combinations(blockers, 2):
        used = tuple(blocker for blocker in blockers if blocker not in unused)
        for assignment in itertools.permutations(used):
            root_part = tuple(
                edge(root, assignment[index]) for index, root in enumerate(roots)
            )
            for residual_part in complete_matchings((*residual, *unused)):
                output[tuple(sorted((*root_part, *residual_part)))] += 1
    return output


def endpoint_survivors(q_size: int, root_vertex: str) -> Counter[Monomial]:
    roots, blockers, residual = labels(q_size)
    all_roots = (*roots, root_vertex)
    port_residual = tuple(vertex for vertex in residual if vertex != root_vertex)
    root_set = frozenset(all_roots)
    blocker_set = frozenset(blockers)

    def allowed(left: str, right: str) -> bool:
        if left in root_set:
            return right in blocker_set
        if right in root_set:
            return left in blocker_set
        return True

    vertices = (*all_roots, *blockers, *port_residual)
    return Counter(perfect_matchings(vertices, allowed))


def endpoint_p6_expansion(q_size: int, root_vertex: str) -> Counter[Monomial]:
    roots, blockers, residual = labels(q_size)
    all_roots = (*roots, root_vertex)
    port_residual = tuple(vertex for vertex in residual if vertex != root_vertex)
    output: Counter[Monomial] = Counter()
    for assignment in itertools.permutations(blockers):
        root_part = tuple(
            edge(root, assignment[index]) for index, root in enumerate(all_roots)
        )
        leftover = assignment[-1]
        for port_part in complete_matchings((leftover, *port_residual)):
            output[tuple(sorted((*root_part, *port_part)))] += 1
    return output


def verify_matching_case(q_size: int) -> dict[str, int]:
    assert q_size % 2 == 0
    survivors = common_root_survivors(q_size)
    cofactor = cofactor_master(q_size)
    assert survivors == cofactor
    assert all(value == 1 for value in survivors.values())
    expected = math.comb(6, 2) * math.factorial(4) * math.prod(range(q_size + 3, 0, -2))
    assert len(survivors) == expected

    endpoint_counts = {}
    for root_vertex in ("a", "b"):
        endpoint = endpoint_survivors(q_size, root_vertex)
        p6 = endpoint_p6_expansion(q_size, root_vertex)
        assert endpoint == p6
        assert all(value == 1 for value in endpoint.values())
        endpoint_expected = math.factorial(6) * math.prod(range(q_size + 1, 0, -2))
        assert len(endpoint) == endpoint_expected
        endpoint_counts[root_vertex] = len(endpoint)
    return {
        "residual_q_vertices": q_size,
        "cofactor_monomials": len(survivors),
        "endpoint_a_p6_monomials": endpoint_counts["a"],
        "endpoint_b_p6_monomials": endpoint_counts["b"],
    }


def coefficient_hypercube(residual_vertices: int) -> dict[str, int]:
    assert residual_vertices >= 2 and residual_vertices % 2 == 0
    common_roots = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
    )
    choices = tuple(
        (
            (41 + 6 * index, 43 + 6 * index, 47 + 6 * index),
            (53 + 6 * index, 59 + 6 * index, 61 + 6 * index),
        )
        for index in range(residual_vertices)
    )
    coefficients: dict[tuple[int, tuple[int, ...]], Fraction] = {}
    for colour in range(3):
        common = math.prod(root[colour] for root in common_roots)
        for bits in itertools.product((0, 1), repeat=residual_vertices):
            value = Fraction(common)
            for index, bit in enumerate(bits):
                value *= choices[index][bit][colour]
            coefficients[colour, bits] = value
            assert value != 0

    square_minors = 0
    for colour in range(3):
        for left, right in itertools.combinations(range(residual_vertices), 2):
            other = tuple(
                index
                for index in range(residual_vertices)
                if index not in (left, right)
            )
            for other_bits in itertools.product((0, 1), repeat=len(other)):
                base = [0] * residual_vertices
                for index, bit in zip(other, other_bits):
                    base[index] = bit
                word00 = tuple(base)
                base[left] = 1
                word10 = tuple(base)
                base[right] = 1
                word11 = tuple(base)
                base[left] = 0
                word01 = tuple(base)
                assert coefficients[colour, word00] * coefficients[colour, word11] == (
                    coefficients[colour, word10] * coefficients[colour, word01]
                )
                square_minors += 1

    # Ratios along a coordinate do not depend on the other bits.
    ratio_checks = 0
    for colour in range(3):
        for coordinate in range(residual_vertices):
            ratios = set()
            for other_bits in itertools.product((0, 1), repeat=residual_vertices - 1):
                word0 = list(other_bits)
                word0.insert(coordinate, 0)
                word1 = word0.copy()
                word1[coordinate] = 1
                ratios.add(
                    coefficients[colour, tuple(word1)]
                    / coefficients[colour, tuple(word0)]
                )
                ratio_checks += 1
            assert ratios == {
                Fraction(
                    choices[coordinate][1][colour],
                    choices[coordinate][0][colour],
                )
            }
    return {
        "residual_vertices": residual_vertices,
        "corners_per_colour": 2**residual_vertices,
        "square_minors_checked": square_minors,
        "edge_ratio_checks": ratio_checks,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact arbitrary-order characteristic-zero compatibility theorem",
        "rank-one Segre",
        "opposite corners",
        "companion cofactor tensors",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md",
        "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md",
        "SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md",
    ):
        assert (ROOT / dependency).exists()

    matching_cases = tuple(verify_matching_case(q_size) for q_size in (0, 2, 4))
    cubes = tuple(coefficient_hypercube(size) for size in (2, 4, 6))
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "matching_identity_replay": "exact monomials",
                "matching_cases": matching_cases,
                "coefficient_cubes": cubes,
                "arbitrary_even_ambient_order_proved_in_written_argument": True,
                "endpoint_p6_restrictions_identified": True,
                "intermediate_corners_are_p6_restrictions": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
