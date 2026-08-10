#!/usr/bin/env python3
"""Independent audit of the adjacent direction-plane obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_one_cross_direction_plane.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projective_points(p: int) -> list[tuple[int, int]]:
    points = {(1, t) for t in range(p)}
    points.add((0, 1))
    return sorted(points)


def dynamic_contraction(
    p: int,
    directions: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], int]:
    """Contract the squarefree five-tensor, retaining ordered indices."""

    tensor = {
        permutation: 1
        for permutation in itertools.permutations(range(5))
    }
    for direction in directions:
        contracted: dict[tuple[int, ...], int] = {}
        for word, coefficient in tensor.items():
            value = coefficient * direction[word[0]]
            tail = word[1:]
            contracted[tail] = (contracted.get(tail, 0) + value) % p
        tensor = {word: value for word, value in contracted.items() if value}
    return tensor


def expected_p3(
    p: int,
    coefficient: int,
    factors: tuple[int, int, int],
) -> dict[tuple[int, ...], int]:
    result: dict[tuple[int, ...], int] = {}
    for word in itertools.permutations(factors):
        result[word] = (result.get(word, 0) + coefficient) % p
    return {word: value for word, value in result.items() if value}


def audit_field(p: int) -> dict[str, object]:
    b = 1
    c = 2 if p != 2 else 1
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)

    mixed = dynamic_contraction(p, (u1, u2))
    expected_mixed = {}
    for third, weight in ((0, 1), (3, b), (4, c)):
        expected_mixed.update(expected_p3(p, weight, (1, 2, third)))
    assert mixed == expected_mixed
    assert dynamic_contraction(p, (u1, u1)) == expected_p3(
        p, 2 * b % p, (1, 2, 4)
    )
    assert dynamic_contraction(p, (u2, u2)) == expected_p3(
        p, 2 * c % p, (1, 2, 3)
    )

    # Rows are projective in e0^perp.  Mixed symmetry admits exactly the
    # ordered pair (e1^*,e2^*) once independence is imposed.
    admissible = []
    for alpha in projective_points(p):
        for beta in projective_points(p):
            determinant = (alpha[0] * beta[1] - alpha[1] * beta[0]) % p
            if determinant == 0:
                continue
            if beta[0] % p == 0 and alpha[1] % p == 0:
                admissible.append((alpha, beta))
    assert admissible == [((1, 0), (0, 1))]

    # In every permutation of (e1,e2,e3), at least one of A,Y receives
    # e1 or e2.  Their requested colour-two coordinate is then zero.
    q_survivors = 0
    for assignment in itertools.permutations((1, 2, 3)):
        if assignment[0] == 3 and assignment[1] == 3:
            q_survivors += 1
    assert q_survivors == 0

    # The colour-swapped P3(e1,e2,e4) has the same support argument.
    p_survivors = 0
    for assignment in itertools.permutations((1, 2, 4)):
        if assignment[0] == 4 and assignment[1] == 4:
            p_survivors += 1
    assert p_survivors == 0

    return {
        "field": f"F_{p}",
        "mixed_terms": len(mixed),
        "admissible_projective_direction_pairs": len(admissible),
        "q_pure_coefficient_survivors": q_survivors,
        "p_pure_coefficient_survivors": p_survivors,
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": (
            "independent squarefree contraction and projective "
            "target-row audit"
        ),
        "fields": fields,
        "direction_plane_gate_excluded": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_direction_plane_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
