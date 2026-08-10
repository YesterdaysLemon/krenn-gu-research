#!/usr/bin/env python3
"""Independent finite-field audit of the disjoint exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dynamic(rows, prime):
    states = {0: 1}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, 0) + coefficient * value
                ) % prime
        states = next_states
    return states[(1 << len(rows)) - 1]


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


def audit_prime(prime):
    a, b, c = 2 % prime, 3 % prime, 4 % prime
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1 % prime, 0)
    h2 = (c, 0, 0, 0, -1 % prime)

    assert contraction((u1, h2, h2), prime) == {
        (1, 2): -2 * c % prime
    }
    assert contraction((u0, h2, h2), prime) == {
        (1, 3): -2 * c % prime,
        (2, 3): -2 * c % prime,
    }
    assert contraction((u0, h1, h1, h2), prime) == {
        (1,): 2 * b % prime,
        (2,): 2 * b % prime,
    }
    assert contraction((u2, h1, h1), prime) == {
        (1, 2): -2 * b % prime
    }

    kernel_patterns = 0
    for vb, vc, vd, zb, zc, zd in itertools.product(
        range(prime),
        repeat=6,
    ):
        rows = (
            (vb, -vb, zb),
            (vc, vc, zc),
            (vd, -vd, zd),
        )
        actual = permanent_dynamic(rows, prime)
        expected = -2 * vb * vd * zc % prime
        assert actual == expected
        kernel_patterns += 1

    all_s_tests = 0
    for e3_values in itertools.product(range(prime), repeat=4):
        e4_values = tuple(
            (value + index + 1) % prime
            for index, value in enumerate(e3_values)
        )
        rows = [
            (0, 0, e3_values[index], e4_values[index])
            for index in range(4)
        ]
        assert permanent_dynamic(rows, prime) == 0
        all_s_tests += 1

    return {
        "prime": prime,
        "source_contractions_checked": 4,
        "three_s_one_d_scalar_patterns": kernel_patterns,
        "all_s_colour_zero_tests": all_s_tests,
    }


def main() -> None:
    output = {
        "audited": True,
        "method": (
            "independent squarefree contractions and dynamic "
            "permanent kernel-pattern checks"
        ),
        "finite_field_audits": [
            audit_prime(prime) for prime in (5, 7)
        ],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "exact_disjoint_incidence_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic exact disjoint q4_211 incidence",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_disjoint_exclusion_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
