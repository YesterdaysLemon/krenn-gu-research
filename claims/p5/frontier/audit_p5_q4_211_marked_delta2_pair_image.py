#!/usr/bin/env python3
"""Independent finite-field audit of the marked-Delta2 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
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
        rows[pivot] = [
            value * inverse % prime for value in rows[pivot]
        ]
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


def pair_image(left, right, prime):
    return [
        [
            (
                first[i] * second[j] + first[j] * second[i]
            ) % prime
            for first in left
            for second in right
        ]
        for i, j in PAIRS
    ]


def audit_prime(prime):
    assignments_checked = 0
    for A in range(1, prime):
        for T in range(1, prime):
            for B in range(prime):
                planes = (
                    ((0, 1, T, -B), (1, 0, 0, -A)),
                    ((1, 0, 0, A), (0, 1, -T, B)),
                    ((1, 0, 0, A), (B, A, -A * T, 0)),
                )
                u0 = ((0, 0, 1, 0), (0, 0, 0, 1))
                e2 = (0, 0, 1, 0)
                e3 = (0, 0, 0, 1)
                for at_h1, at_h2, remaining in itertools.permutations(
                    range(3)
                ):
                    full = pair_image(
                        planes[at_h1] + (e3,),
                        planes[at_h2] + (e2,),
                        prime,
                    )
                    opposite = pair_image(u0, planes[remaining], prime)
                    assert rank_mod(full, prime) == 6
                    assert rank_mod(opposite, prime) == 4
                    assignments_checked += 1
    return {
        "prime": prime,
        "plane_assignments_checked": assignments_checked,
        "full_pair_image_rank": 6,
        "opposite_pair_image_rank": 4,
        "flattening_rank_lower_bound": 4,
    }


def main() -> None:
    output = {
        "audited": True,
        "method": "independent finite-field pair-image row reduction",
        "finite_field_audits": [audit_prime(prime) for prime in (3, 5)],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "all_rank_two_marked_family_excluded": True,
        "rank_one_normal_pencil_gates_retained": True,
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "all-rank-two marked Delta2 family",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_marked_delta2_pair_image_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
