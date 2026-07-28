#!/usr/bin/env python3
"""Independent finite-field audit of the q5_311 shared-drop branch."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_311_SHARED_DROP_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projective_vectors(prime: int) -> tuple[tuple[int, ...], ...]:
    result = []
    for vector in itertools.product(range(prime), repeat=3):
        pivot = next(
            (index for index, value in enumerate(vector) if value),
            None,
        )
        if pivot is None or vector[pivot] != 1:
            continue
        if any(vector[index] for index in range(pivot)):
            continue
        result.append(vector)
    return tuple(result)


def pure_cube(vector: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple(
        vector[first] * vector[second] * vector[third] % prime
        for first, second, third in itertools.product(range(3), repeat=3)
    )


def audit_prime(prime: int) -> dict[str, int]:
    lines = projective_vectors(prime)
    first_plane = [
        vector for vector in lines if vector[1] == 0
    ]
    second_plane = [
        vector for vector in lines if vector[2] == 0
    ]
    assert len(first_plane) == len(second_plane) == prime + 1

    configurations = 0
    amplitude_pairs = 0
    compatible = 0
    for first in first_plane:
        for second in second_plane:
            if first == second:
                continue
            configurations += 1
            beta_one = first[2]
            beta_two = second[1]
            first_cube = pure_cube(first, prime)
            second_cube = pure_cube(second, prime)
            for lambda_one in range(1, prime):
                for lambda_two in range(1, prime):
                    amplitude_pairs += 1
                    left = tuple(
                        lambda_one * beta_one * value % prime
                        for value in first_cube
                    )
                    right = tuple(
                        lambda_two * beta_two * value % prime
                        for value in second_cube
                    )
                    if left == right:
                        compatible += 1

    assert compatible == 0
    return {
        "projective_lines": len(lines),
        "directions_in_each_deleted_image_plane": len(first_plane),
        "independent_direction_configurations": configurations,
        "nonzero_amplitude_pairs_checked": amplitude_pairs,
        "compatible_shared_drop_instances": compatible,
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (3, 5)}
    output = {
        "audited": True,
        "finite_fields": ["F_3", "F_5"],
        "audits": audits,
        "compatible_shared_drop_instances": 0,
        "remaining_rank_drop_branch": "disjoint_2_plus_2",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "finite-field audit; written theorem is over C",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_311_shared_drop_obstruction_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
