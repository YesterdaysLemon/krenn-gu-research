#!/usr/bin/env python3
"""Verify the arbitrary-order four-root/six-blocker cofactor transfer."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "FOUR_ROOT_SIX_BLOCKER_ARBITRARY_ORDER_KERNEL_SUPPORT_OBSTRUCTION.md"
DEPENDENCIES = (
    ROOT / "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md",
    ROOT / "SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md",
    ROOT
    / "SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md",
)
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


def labels(residual_size: int):
    roots = tuple(f"r{index}" for index in range(4))
    blockers = tuple(f"u{index}" for index in range(6))
    residual = tuple(f"q{index}" for index in range(residual_size))
    return roots, blockers, residual


def restricted_global_matchings(residual_size: int) -> Counter[Monomial]:
    roots, blockers, residual = labels(residual_size)
    root_set = frozenset(roots)
    blocker_set = frozenset(blockers)

    def allowed(left: str, right: str) -> bool:
        if left in root_set:
            return right in blocker_set
        if right in root_set:
            return left in blocker_set
        return True

    return Counter(perfect_matchings((*roots, *blockers, *residual), allowed))


def cofactor_expansion(residual_size: int) -> Counter[Monomial]:
    roots, blockers, residual = labels(residual_size)
    output: Counter[Monomial] = Counter()
    for unused in itertools.combinations(blockers, 2):
        used = tuple(blocker for blocker in blockers if blocker not in unused)
        for assignment in itertools.permutations(used):
            root_part = tuple(
                edge(root, assignment[index]) for index, root in enumerate(roots)
            )
            for residual_part in perfect_matchings(
                (*residual, *unused), lambda _left, _right: True
            ):
                output[tuple(sorted((*root_part, *residual_part)))] += 1
    return output


def matching_case(residual_size: int) -> dict[str, int]:
    assert residual_size % 2 == 0
    global_terms = restricted_global_matchings(residual_size)
    cofactor_terms = cofactor_expansion(residual_size)
    assert global_terms == cofactor_terms
    assert all(multiplicity == 1 for multiplicity in global_terms.values())
    expected = (
        math.comb(6, 2) * math.factorial(4) * math.prod(range(residual_size + 1, 0, -2))
    )
    assert len(global_terms) == expected
    return {
        "residual_vertices": residual_size,
        "matching_monomials": len(global_terms),
        "unused_blocker_pairs": math.comb(6, 2),
    }


def torus_coefficients(residual_size: int) -> dict[str, object]:
    root_vectors = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
    )
    residual_vectors = tuple(
        (41 + 6 * index, 43 + 6 * index, 47 + 6 * index)
        for index in range(residual_size)
    )
    coefficients = tuple(
        math.prod(vector[colour] for vector in root_vectors)
        * math.prod(vector[colour] for vector in residual_vectors)
        for colour in range(3)
    )
    assert all(coefficient != 0 for coefficient in coefficients)
    return {
        "residual_vertices": residual_size,
        "diagonal_coefficients": coefficients,
        "coefficient_torus": True,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for dependency in DEPENDENCIES:
        assert dependency.exists()
    for phrase in (
        "Exact arbitrary-order characteristic-zero necessary theorem",
        "J_H intersects (C^*)^3",
        "at most two of H_(u_0),...,H_(u_5)",
        "arbitrary-order local-to-global reduction in full: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    cases = tuple(matching_case(size) for size in (0, 2, 4))
    coefficients = tuple(torus_coefficients(size) for size in (0, 2, 4))
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_dependencies": [dependency.name for dependency in DEPENDENCIES],
                "exact_matching_cases": cases,
                "torus_coefficient_cases": coefficients,
                "arbitrary_even_order_proved_in_written_bijection": True,
                "kernel_support_modes_at_least_two": 2,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
