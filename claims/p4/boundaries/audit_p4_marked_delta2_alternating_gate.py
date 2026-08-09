#!/usr/bin/env python3
"""Independent finite-field audit of the alternating-gate formulas."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
THEOREM = REPO_ROOT / "claims/p4/classifications/P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md"


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


def rank_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [
            value * inverse % prime for value in rows[pivot_row]
        ]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            multiple = rows[row][column]
            if multiple:
                rows[row] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        rows[row],
                        rows[pivot_row],
                        strict=True,
                    )
                ]
        pivot_row += 1
    return pivot_row


def projective_lines(prime):
    lines = [(1, value) for value in range(prime)]
    lines.append((0, 1))
    return lines


def coefficient_support(row_pairs, prime):
    result = {}
    for word in itertools.product((0, 1), repeat=4):
        rows = [
            row_pairs[mode][word[mode]]
            for mode in range(4)
        ]
        value = permanent_dynamic(rows, prime)
        if value:
            result[word] = value
    return result


def nullspace_audit(prime):
    transverse_systems = 0
    tangent_systems = 0
    e2 = (0, 0, 1, 0)
    e3 = (0, 0, 0, 1)
    for p, q in projective_lines(prime):
        for r, t in projective_lines(prime):
            lam = (p * t + q * r) % prime
            if not lam:
                continue
            delta = (p * t - q * r) % prime

            # Variables are x2,x3,y2,y3,z2,z3,d2,d3.
            matrix = [
                [0, 0, 0, lam, 0, -delta, 0, 0],
                [0, -lam, 0, 0, 0, 0, 0, -delta],
                [0, 0, lam, 0, -delta, 0, 0, 0],
                [-lam, 0, 0, 0, 0, 0, -delta, 0],
            ]
            assert rank_mod(matrix, prime) == 4

            if delta:
                x2, x3, y2, y3 = 1, 2 % prime, 3 % prime, 4 % prime
                inv_delta = pow(delta, -1, prime)
                z2 = lam * y2 * inv_delta % prime
                z3 = lam * y3 * inv_delta % prime
                d2 = -lam * x2 * inv_delta % prime
                d3 = -lam * x3 * inv_delta % prime
                rows = (
                    (e2, e3),
                    ((p, q, x2, x3), e2),
                    (e3, (r, -t, y2, y3)),
                    (
                        (r, t, z2, z3),
                        (p, -q, d2, d3),
                    ),
                )
                support = coefficient_support(rows, prime)
                assert set(support) == {
                    (0, 0, 0, 0),
                    (1, 1, 1, 1),
                }
                transverse_systems += 1
            else:
                # lambda != 0 and Delta=0 force x=y=0; z,d are free.
                rows = (
                    (e2, e3),
                    ((p, q, 0, 0), e2),
                    (e3, (r, -t, 0, 0)),
                    (
                        (r, t, 1, 2 % prime),
                        (p, -q, 3 % prime, 4 % prime),
                    ),
                )
                support = coefficient_support(rows, prime)
                assert set(support) == {
                    (0, 0, 0, 0),
                    (1, 1, 1, 1),
                }
                tangent_systems += 1

    assert transverse_systems
    assert tangent_systems
    return {
        "prime": prime,
        "projective_shared_direction_pairs_audited": (
            transverse_systems + tangent_systems
        ),
        "transverse_systems": transverse_systems,
        "tangent_systems": tangent_systems,
        "mixed_system_rank": 4,
    }


def main() -> None:
    output = {
        "audited": True,
        "method": (
            "dynamic-programming permanents and projective "
            "finite-field nullspace checks"
        ),
        "finite_field_audits": [
            nullspace_audit(prime) for prime in (5, 7)
        ],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "normal_form_strata": 2,
        "marked_Delta2_boundary_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "marked alternating-gate normal forms",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p4_marked_delta2_alternating_gate_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
