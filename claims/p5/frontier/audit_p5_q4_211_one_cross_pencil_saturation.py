#!/usr/bin/env python3
"""Independent finite-field audit of one-cross pencil saturation."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md"


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


def projective_lines(prime):
    return [(1, value) for value in range(prime)] + [(0, 1)]


def audit_orientation(prime, first, second, expected_third):
    zero_lines = []
    nonzero_lines = []
    for A, B in projective_lines(prime):
        line = tuple(
            (A * left + B * right) % prime
            for left, right in zip(first, second, strict=True)
        )
        value = permanent_dynamic((first, second, line), prime)
        if value:
            nonzero_lines.append((A, B))
        else:
            zero_lines.append((A, B))

    expected_projective = next(
        (A, B)
        for A, B in projective_lines(prime)
        if all(
            (
                (A * first[index] + B * second[index])
                * expected_third[(index + 1) % 3]
                - (A * first[(index + 1) % 3]
                   + B * second[(index + 1) % 3])
                * expected_third[index]
            ) % prime == 0
            for index in range(3)
        )
    )
    assert zero_lines == [expected_projective]
    return {
        "projective_lines_checked": prime + 1,
        "polarized_zero_line": list(expected_projective),
        "nonzero_lines": len(nonzero_lines),
    }


def main() -> None:
    finite_field_audits = []
    for prime in (5, 7):
        b, c = 2 % prime, 3 % prime
        h2 = (c, 0, -1 % prime)
        h1 = (b, -1 % prime, 0)
        n = (0, c, b)
        u1 = (b, 1, 0)
        u2 = (c, 0, 1)
        q_audit = audit_orientation(prime, h2, n, u1)
        p_audit = audit_orientation(prime, h1, n, u2)
        finite_field_audits.append(
            {
                "prime": prime,
                "q_orientation": q_audit,
                "p_orientation": p_audit,
                "fourth_normal_target_colour": 0,
            }
        )

    output = {
        "audited": True,
        "method": (
            "independent dynamic permanents on projective "
            "normal-pencil lines"
        ),
        "finite_field_audits": finite_field_audits,
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "q_forced_third_line": "C*u1",
        "p_forced_third_line": "C*u2",
        "q_mandatory_opposite_pencil": "span(h1,n)",
        "p_mandatory_opposite_pencil": "span(h2,n)",
        "one_cross_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "one-cross projective normal pencils",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_pencil_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
