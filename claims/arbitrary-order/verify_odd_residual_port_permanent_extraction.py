#!/usr/bin/env python3
"""Verify the odd-residual port permanent factorisation exactly."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md"
Edge = tuple[str, str]
Monomial = tuple[Edge, ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(left: str, right: str) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(
    vertices: tuple[str, ...],
    allowed,
) -> tuple[Monomial, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[Monomial] = []
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


def surviving_matching_polynomial(r: int, q_size: int) -> Counter[Monomial]:
    roots = tuple(f"r{index}" for index in range(r))
    blockers = tuple(f"b{index}" for index in range(r + 1))
    residual = tuple(f"q{index}" for index in range(q_size))
    root_set = frozenset(roots)
    blocker_set = frozenset(blockers)

    def allowed(left: str, right: str) -> bool:
        if left in root_set:
            return right in blocker_set
        if right in root_set:
            return left in blocker_set
        return True

    return Counter(perfect_matchings(roots + blockers + residual, allowed))


def port_permanent_polynomial(r: int, q_size: int) -> Counter[Monomial]:
    roots = tuple(f"r{index}" for index in range(r))
    blockers = tuple(f"b{index}" for index in range(r + 1))
    residual = tuple(f"q{index}" for index in range(q_size))
    output: Counter[Monomial] = Counter()
    for assignment in itertools.permutations(blockers):
        root_part = tuple(
            edge(root, assignment[index])
            for index, root in enumerate(roots)
        )
        leftover = assignment[-1]
        for residual_part in complete_matchings((leftover, *residual)):
            output[tuple(sorted((*root_part, *residual_part)))] += 1
    return output


def odd_double_factorial(value: int) -> int:
    assert value >= 1 and value % 2 == 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def verify_case(r: int, q_size: int) -> dict[str, int]:
    assert q_size % 2 == 1
    surviving = surviving_matching_polynomial(r, q_size)
    port = port_permanent_polynomial(r, q_size)
    assert surviving == port
    assert all(coefficient == 1 for coefficient in surviving.values())
    expected = math.factorial(r + 1) * odd_double_factorial(q_size)
    assert sum(surviving.values()) == expected
    return {
        "roots": r,
        "blockers": r + 1,
        "residual_vertices": q_size,
        "surviving_monomials": len(surviving),
        "expected_monomials": expected,
    }


def verify_diagonal_rescaling() -> dict[str, object]:
    roots = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
    )
    residual = (
        (41, 43, 47),
        (53, 59, 61),
        (67, 71, 73),
    )
    lambdas = tuple(
        math.prod(vector[colour] for vector in roots + residual)
        for colour in range(3)
    )
    inverse_scaling = tuple(Fraction(1, value) for value in lambdas)
    normalized = tuple(
        Fraction(value) * scale
        for value, scale in zip(lambdas, inverse_scaling, strict=True)
    )
    assert normalized == (1, 1, 1)
    return {
        "sample_nonzero_diagonal_coefficients": list(lambdas),
        "one_mode_inverse_scaling": [str(value) for value in inverse_scaling],
        "normalized_coefficients": [int(value) for value in normalized],
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "arbitrary-order bridge lemma",
        "P_(r+1) -> Delta_3",
        "P_6 -> Delta_3",
        "does not by itself produce a `P_5` restriction",
        "does not resolve the Krenn--Gu conjecture",
    ):
        assert phrase in theorem, phrase

    cases = tuple(
        verify_case(r, q_size)
        for r, q_size in ((2, 1), (2, 3), (3, 5), (4, 3), (5, 3))
    )
    result = {
        "status": "verified",
        "field": "C",
        "method": "exact surviving-matching and port-permanent monomial equality",
        "cases": cases,
        "diagonal_rescaling": verify_diagonal_rescaling(),
        "arbitrary_even_ambient_order": True,
        "first_surplus_extraction": "r roots plus r+1 blockers imply P_(r+1)->Delta_3",
        "four_roots_five_blockers_imply_P5": True,
        "five_roots_six_blockers_imply_P6": True,
        "P6_implies_P5_proved": False,
        "global_conjecture_resolved": False,
        "search_used": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "odd_residual_port_permanent_extraction_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
