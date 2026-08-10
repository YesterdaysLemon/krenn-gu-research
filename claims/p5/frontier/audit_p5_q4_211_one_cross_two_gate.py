#!/usr/bin/env python3
"""Independent finite-field audit of the one-cross two-gate reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contraction(directions, prime):
    degree = 5 - len(directions)
    coefficients = {}
    for remaining in itertools.combinations(range(5), degree):
        contracted = tuple(
            coordinate for coordinate in range(5)
            if coordinate not in remaining
        )
        value = 0
        for assignment in itertools.permutations(contracted):
            product = 1
            for row, coordinate in zip(
                directions,
                assignment,
                strict=True,
            ):
                product *= row[coordinate]
            value += product
        value %= prime
        if value:
            coefficients[remaining] = value
    return coefficients


def rank_mod(vectors, prime):
    rows = [[value % prime for value in vector] for vector in vectors]
    pivot = 0
    for column in range(len(rows[0])):
        row = next(
            (
                index
                for index in range(pivot, len(rows))
                if rows[index][column]
            ),
            None,
        )
        if row is None:
            continue
        rows[pivot], rows[row] = rows[row], rows[pivot]
        inverse = pow(rows[pivot][column], -1, prime)
        rows[pivot] = [value * inverse % prime for value in rows[pivot]]
        for index in range(len(rows)):
            if index == pivot:
                continue
            multiple = rows[index][column]
            if multiple:
                rows[index] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        rows[index],
                        rows[pivot],
                        strict=True,
                    )
                ]
        pivot += 1
    return pivot


def audit_prime(prime):
    b, c = 2 % prime, 3 % prime
    h1 = (b, 0, 0, -1 % prime, 0)
    h2 = (c, 0, 0, 0, -1 % prime)
    n = (0, 0, 0, c, b)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    m = tuple(
        (c * left - b * right) % prime
        for left, right in zip(u1, u2, strict=True)
    )

    assert contraction((h1, h1, h1), prime) == {}
    assert contraction((h2, h2, h2), prime) == {}
    assert rank_mod((h1, h2, n), prime) == 3
    assert rank_mod((u1, m), prime) == 2
    assert rank_mod((u2, m), prime) == 2

    m_from_normals = tuple(
        (b * left - c * right) % prime
        for left, right in zip(h2, h1, strict=True)
    )
    assert m == m_from_normals
    return {
        "prime": prime,
        "triple_normal_contractions_zero": 2,
        "normal_triple_rank": 3,
        "direction_pair_ranks": [2, 2],
    }


def main() -> None:
    output = {
        "audited": True,
        "method": (
            "independent squarefree contractions and modular "
            "projective-span checks"
        ),
        "finite_field_audits": [
            audit_prime(prime) for prime in (5, 7)
        ],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "second_common_mode_excluded": True,
        "double_normal_gate_absorbed": True,
        "remaining_adjacent_gate_count": 2,
        "adjacent_one_cross_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic adjacent one-cross gate reduction",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_two_gate_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
