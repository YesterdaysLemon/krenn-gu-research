#!/usr/bin/env python3
"""Independent audit of the b=0 coordinate-normal reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_b0_coordinate_normal.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projective_points(p: int) -> list[tuple[int, int]]:
    points = {(1, value) for value in range(p)}
    points.add((0, 1))
    return sorted(points)


def dynamic_contraction(
    p: int,
    directions: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], int]:
    tensor = {
        permutation: 1
        for permutation in itertools.permutations(range(5))
    }
    for direction in directions:
        result: dict[tuple[int, ...], int] = {}
        for word, coefficient in tensor.items():
            value = coefficient * direction[word[0]]
            tail = word[1:]
            result[tail] = (result.get(tail, 0) + value) % p
        tensor = {word: value for word, value in result.items() if value}
    return tensor


def matrix_rank_mod(matrix: list[list[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(entry * inverse) % p for entry in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column] % p
            if factor:
                work[row] = [
                    (left - factor * right) % p
                    for left, right in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
    return rank


def audit_field(p: int) -> dict[str, object]:
    a, c = 2, 3
    e3 = (0, 0, 0, 1, 0)
    u0 = (a, 1, 1, 0, 0)
    u2 = (c, 0, 0, 0, 1)
    h2 = (c, 0, 0, 0, -1 % p)

    assert dynamic_contraction(p, (e3, e3)) == {}
    mixed = dynamic_contraction(p, (u2, e3))
    repeated = dynamic_contraction(p, (u2, u2))
    conic = dynamic_contraction(p, (u0, e3, h2))
    propagated = dynamic_contraction(p, (u0, e3, h2, h2))
    assert len(mixed) == 12
    assert len(repeated) == 6
    assert len(conic) == 10
    assert propagated == {
        (1,): -2 * c % p,
        (2,): -2 * c % p,
    }

    admissible_pairs = []
    points = projective_points(p)
    for first in points:
        for second in points:
            if (
                first[0] * second[0] % p == 0
                and first[1] * second[1] % p == 0
            ):
                admissible_pairs.append((first, second))
    assert set(admissible_pairs) == {
        ((1, 0), (0, 1)),
        ((0, 1), (1, 0)),
    }

    ranks = set()
    for g in points:
        # Use a support-two slice as well as its projective limits.
        g0, g1 = g
        g2 = 1
        matrix = [
            [0, g2, g1],
            [g2, 0, g0],
            [g1, g0, 0],
        ]
        ranks.add(matrix_rank_mod(matrix, p))
    assert min(ranks) >= 2

    return {
        "field": f"F_{p}",
        "mixed_p3_terms": len(mixed),
        "repeated_u2_terms": len(repeated),
        "mixed_conic_terms": len(conic),
        "propagated_kernel_terms": len(propagated),
        "ordered_coordinate_row_pairs": len(admissible_pairs),
        "nonzero_quadratic_slice_ranks": sorted(ranks),
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": (
            "independent squarefree contraction and projective "
            "coordinate-row audit"
        ),
        "fields": fields,
        "exact_disjoint_excluded": True,
        "exact_parallel_excluded": True,
        "colour_two_coordinate_mode_common": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_coordinate_normal_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
