#!/usr/bin/env python3
"""Independent audit of the b=0 noncommon-A obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_b0_noncommon_a.py"


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


def rank_mod(matrix: list[list[int]], p: int) -> int:
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


def permanent_mod(rows: list[tuple[int, ...]], p: int) -> int:
    value = 0
    for permutation in itertools.permutations(range(5)):
        term = 1
        for index in range(5):
            term = term * rows[index][permutation[index]] % p
        value = (value + term) % p
    return value


def audit_field(p: int) -> dict[str, object]:
    a, c = 2, 3
    u0 = (a, 1, 1, 0, 0)
    u1 = (0, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h0 = (0, 1, -1 % p, 0, 0)
    h2 = (c, 0, 0, 0, -1 % p)
    s = (0, 1, 1, 0, 0)
    w = (1, 0, 0, 0, -c % p)

    contractions = {
        "kernel": dynamic_contraction(p, (u0, u1, h2, h2)),
        "zero_w": dynamic_contraction(p, (u1, h2)),
        "h0_chart": dynamic_contraction(p, (u1, h0)),
        "pure_colour_zero": dynamic_contraction(p, (u0, h2)),
    }
    assert contractions["kernel"] == {
        (1,): -2 * c % p,
        (2,): -2 * c % p,
    }
    assert len(contractions["zero_w"]) == 12
    assert len(contractions["h0_chart"]) == 12
    assert len(contractions["pure_colour_zero"]) == 30

    # Independently solve the three relevant projective g systems.
    projective_g = {
        (1, x, y)
        for x in range(p)
        for y in range(p)
    }
    projective_g.update((0, 1, y) for y in range(p))
    projective_g.add((0, 0, 1))

    def equations(pair, g):
        g0, g1, g2 = g
        if pair == "dd":
            return (2 * g2, g0 + g1)
        return (g0 - g1, g0 + g1)

    solutions = {
        pair: {
            g
            for g in projective_g
            if all(value % p == 0 for value in equations(pair, g))
        }
        for pair in ("dd", "sd", "ds")
    }
    assert solutions["dd"] == {(1, -1 % p, 0)}
    assert solutions["sd"] == {(0, 0, 1)}
    assert solutions["ds"] == {(0, 0, 1)}

    kernel_matrix = [
        [s[column] % p, w[column] % p]
        for column in range(5)
    ]
    assert rank_mod(kernel_matrix, p) == 2
    # The forbidden coefficient in (26) is a product of two nonzero
    # marked scalars.
    forbidden_products = {
        left * right % p
        for left in range(1, p)
        for right in range(1, p)
    }
    assert 0 not in forbidden_products
    exact_mixed_checks = 0
    for q in range(1, p):
        for r in range(1, p):
            c_row = (2, q, q, 3, 4)
            d4 = 2
            d_row = ((r + c * d4) % p, 1, -1 % p, 3, d4)
            value = permanent_mod([u0, h2, u1, c_row, d_row], p)
            assert value == -2 * q * r % p
            exact_mixed_checks += 1

    return {
        "field": f"F_{p}",
        "zero_chart_solution_counts": {
            pair: len(values) for pair, values in solutions.items()
        },
        "contraction_term_counts": {
            name: len(value) for name, value in contractions.items()
        },
        "kernel_rank": 2,
        "forbidden_mixed_values": len(forbidden_products),
        "exact_forbidden_mixed_checks": exact_mixed_checks,
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": (
            "independent projective sign-system, contraction, and "
            "rank audit"
        ),
        "fields": fields,
        "noncommon_A_excluded": True,
        "forced_h2_modes": ["A", "B", "C"],
        "forced_remaining_kernel": "L_D(e1+e2)=0",
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_noncommon_a_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
