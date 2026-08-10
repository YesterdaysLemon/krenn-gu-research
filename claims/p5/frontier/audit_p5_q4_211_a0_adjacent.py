#!/usr/bin/env python3
"""Independent audit of the a=0 adjacent reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_ADJACENT_REDUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_a0_adjacent.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(columns: tuple[tuple[int, ...], ...], p: int) -> int:
    matrix = [
        [columns[column][row] % p for column in range(len(columns))]
        for row in range(len(columns[0]))
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, p)
        matrix[rank] = [(entry * inverse) % p for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column] % p
            if factor:
                matrix[row] = [
                    (left - factor * right) % p
                    for left, right in zip(
                        matrix[row], matrix[rank], strict=True
                    )
                ]
        rank += 1
    return rank


def audit_field(p: int) -> dict[str, object]:
    b, c = 1, 2
    h0 = (0, 1, -1 % p, 0, 0)
    h1 = (b, 0, 0, -1 % p, 0)
    h2 = (c, 0, 0, 0, -1 % p)
    n = (0, 0, 0, c, b)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    s = (0, 1, 1, 0, 0)

    assert rank_mod((h0, h1, h2), p) == 3
    assert rank_mod((h0, h1, n), p) == 3
    for row in (h0, h1, h2, n):
        assert sum(left * right for left, right in zip(row, s)) % p == 0
    assert tuple(
        (c * u1[index] - b * h2[index] - n[index]) % p
        for index in range(5)
    ) == (0, 0, 0, 0, 0)
    assert tuple(
        (b * u2[index] - c * h1[index] - n[index]) % p
        for index in range(5)
    ) == (0, 0, 0, 0, 0)

    # Any at-least-two incidence set avoiding A,Y is exactly {C,D}.
    modes = ("A", "Y", "C", "D")
    allowed = []
    for size in range(2, 5):
        for subset in itertools.combinations(modes, size):
            if "A" not in subset and "Y" not in subset:
                allowed.append(subset)
    assert allowed == [("C", "D")]

    return {
        "field": f"F_{p}",
        "common_row_rank": 3,
        "opposite_row_rank": 3,
        "allowed_h0_incidence_sets": len(allowed),
        "q_direction_identity": True,
        "p_direction_identity": True,
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": "independent row-rank and incidence-forcing audit",
        "fields": fields,
        "h0_modes_in_one_cross": ["C", "D"],
        "rigid_direction_forced": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_a0_adjacent_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
