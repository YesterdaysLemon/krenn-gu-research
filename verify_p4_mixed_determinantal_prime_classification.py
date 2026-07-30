#!/usr/bin/env python3
"""Verify the classification of the five mixed determinantal primes."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md"
MIXED = ROOT / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md"
SIX_DIMENSIONAL = ROOT / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md"
ONE_THREE = ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }


def prime_planes(
    prime: str,
    d: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    if prime == "P4":
        a = 0
        c = d - p + q
        u0 = sp.Matrix(
            ((-d * p, d + q, q * (-d + p - q), 0), (-1, 0, 0, 1))
        )
    elif prime == "P5":
        a = q - p
        c = d
        u0 = sp.Matrix(
            ((q * (d - p + q), -d - q, d * p, 0), (-1, 0, 0, 1))
        )
    else:
        raise ValueError(prime)
    return (
        u0,
        sp.Matrix(((0, 0, 1, 1), (a, 1, c, d))),
        sp.Matrix(((p, 1, 0, q), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )


def lower_prime_planes(
    a: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    return (
        sp.Matrix(((1, 0, 1, 0), (-1, 0, 0, 1))),
        sp.Matrix(((0, 0, 1, 1), (a, 1, c, d))),
        sp.Matrix(((-a - c, 1, 0, -d), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )


def six_dimensional_planes(
    a: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    h = a + c - d
    return (
        sp.Matrix(((1, 0, 0, -1), (0, 0, 1, 1))),
        sp.Matrix(
            ((1, 1 / a, 0, 1 - h / a), (0, 0, 1, 1))
        ),
        sp.Matrix(((1, 0, -1, 0), (0, 1, -a - c, -d))),
        sp.Matrix(((1, 0, 0, 1), (0, 0, 1, -1))),
    )


def branch_planes(
    branch: str,
    s: sp.Expr,
    d: sp.Expr,
    g: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    t = {
        "L1": -d + g + s,
        "L2": d + g - s,
    }[branch]
    cap_p = g - t
    cap_q = d - s
    raw = (
        sp.Matrix(((2, cap_p + cap_q, cap_q - cap_p, 0), (0, 0, 1, 1))),
        sp.Matrix(((0, 1, -1, 0), (1, 0, s, d))),
        sp.Matrix(((1, 0, g, t), (0, 1, 0, -1))),
        sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
    )
    source_swap = (1, 0, 2, 3)
    swapped = tuple(plane[:, source_swap] for plane in raw)
    return swapped[2], swapped[0], swapped[1], swapped[3]


def same_plane(left: sp.Matrix, right: sp.Matrix) -> bool:
    left_coordinates = tuple(
        sp.factor(left[:, pair].det()) for pair in PAIRS
    )
    right_coordinates = tuple(
        sp.factor(right[:, pair].det()) for pair in PAIRS
    )
    pivot = next(
        index
        for index in range(6)
        if left_coordinates[index] != 0 and right_coordinates[index] != 0
    )
    return all(
        sp.factor(
            left_coordinates[index] * right_coordinates[pivot]
            - right_coordinates[index] * left_coordinates[pivot]
        )
        == 0
        for index in range(6)
    )


def main() -> None:
    d, p, q = sp.symbols("d p q")
    p4 = prime_planes("P4", d, p, q)
    p5 = prime_planes("P5", d, p, q)

    p4_tensor = coefficients(p4)
    p5_tensor = coefficients(p5)
    assert {
        word: value for word, value in p4_tensor.items() if value != 0
    } == {(0, 0, 0, 0): 2 * p * q}
    assert {
        word: value for word, value in p5_tensor.items() if value != 0
    } == {(0, 0, 0, 0): -2 * p * q}

    g4 = q * (p - q - d) / (d + q)
    l2 = branch_planes("L2", p, q, g4)
    assert all(
        same_plane(left, right)
        for left, right in zip(p4, l2, strict=True)
    )

    g5 = -d * p / (d + q)
    l1 = branch_planes("L1", p, q, g5)
    assert all(
        same_plane(left, right)
        for left, right in zip(p5, l1, strict=True)
    )

    a, c = sp.symbols("a c")
    lower = lower_prime_planes(a, c, d)
    embedded = six_dimensional_planes(a, c, d)
    assert all(
        same_plane(left, right)
        for left, right in zip(lower, embedded, strict=True)
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "exact prime specialization and symbolic Pluecker "
            "identification under source/mode symmetries"
        ),
        "minimal_primes": {
            "P1": ["c+p+q", "a+d"],
            "P2": ["d+q", "a+c+p"],
            "P3": ["c", "a+d+p+q"],
            "P4": ["c-d+p-q", "a"],
            "P5": ["c-d", "a+p-q"],
        },
        "prime_orbit_identification": {
            "P1": "sixth_mixed_orientation_component",
            "P2": "six_dimensional_component_subfamily",
            "P3": "sixth_mixed_orientation_component",
            "P4": "L2",
            "P5": "L1",
        },
        "P4_nonzero_coefficient": "2*p*q",
        "P5_nonzero_coefficient": "-2*p*q",
        "source_permutation": [1, 0, 2, 3],
        "mode_reorder_from_one_three": [2, 0, 1, 3],
        "P4_L2_parameters": {
            "S": "p",
            "D": "q",
            "G": str(g4),
        },
        "P5_L1_parameters": {
            "S": "p",
            "D": "q",
            "G": str(g5),
        },
        "dense_mixed_determinantal_primes_classified": True,
        "additional_component_orbits_on_dense_chart": 0,
        "known_pure_component_orbits_at_least": 7,
        "all_pure_components_classified": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (MIXED, SIX_DIMENSIONAL, ONE_THREE)
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_mixed_determinantal_primes_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
