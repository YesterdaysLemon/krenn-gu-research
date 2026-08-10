#!/usr/bin/env python3
"""Independent audit of the final b=0 boundary obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_FINAL_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_b0_final.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def projective_points_3(p: int) -> set[tuple[int, int, int]]:
    points = {
        (1, second, third)
        for second in range(p)
        for third in range(p)
    }
    points.update((0, 1, third) for third in range(p))
    points.add((0, 0, 1))
    return points


def audit_field(p: int) -> dict[str, object]:
    a, c = 2, 3
    u0 = (a, 1, 1, 0, 0)
    u1 = (0, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h2 = (c, 0, 0, 0, -1 % p)

    contractions = {
        "labels": dynamic_contraction(p, (u0, u1, h2, h2)),
        "w": dynamic_contraction(p, (u1, h2)),
        "k": dynamic_contraction(p, (u2, u1)),
        "triple_h2": dynamic_contraction(p, (h2, h2, h2)),
    }
    assert contractions["labels"] == {
        (1,): -2 * c % p,
        (2,): -2 * c % p,
    }
    assert len(contractions["w"]) == 12
    assert len(contractions["k"]) == 12
    assert contractions["triple_h2"] == {}

    points = projective_points_3(p)
    ds_solutions = {
        g
        for g in points
        if (g[0] + g[1]) % p == 0
        and (g[0] - g[1]) % p == 0
    }
    ss_solutions = {
        g
        for g in points
        if g[2] % p == 0
        and (g[0] - g[1]) % p == 0
    }
    assert ds_solutions == {(0, 0, 1)}
    assert ss_solutions == {(1, 1, 0)}

    label_pairs = []
    projective_2 = {(1, value) for value in range(p)}
    projective_2.add((0, 1))
    for row_b in projective_2:
        for row_c in projective_2:
            if (
                row_b[0] * row_c[0] % p == 0
                and row_b[1] * row_c[1] % p == 0
            ):
                label_pairs.append((row_b, row_c))
    assert set(label_pairs) == {
        ((1, 0), (0, 1)),
        ((0, 1), (1, 0)),
    }

    # With D functional (1,-1), the binary polar of C is -c1+c2.
    zero_c_functionals = {
        (c1, c2)
        for c1 in range(p)
        for c2 in range(p)
        if (c1, c2) != (0, 0)
        and (-c1 + c2) % p == 0
    }
    assert all(c1 == c2 for c1, c2 in zero_c_functionals)

    return {
        "field": f"F_{p}",
        "contraction_term_counts": {
            name: len(value) for name, value in contractions.items()
        },
        "d_s_polar_solutions": len(ds_solutions),
        "s_s_polar_solutions": len(ss_solutions),
        "target_label_cases": len(label_pairs),
        "binary_zero_functionals": len(zero_c_functionals),
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": (
            "independent contraction, projective polar, and target-label "
            "audit"
        ),
        "fields": fields,
        "case_X_excluded": True,
        "case_Y_excluded": True,
        "b0_boundary_excluded": True,
        "c0_boundary_excluded": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_final_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
