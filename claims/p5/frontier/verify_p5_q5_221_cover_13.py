#!/usr/bin/env python3
"""Verify the exact cover-13 obstruction in normalized q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_COVER_13_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(matrix):
    order = len(matrix)
    return sp.factor(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(order))
            for permutation in itertools.permutations(range(order))
        )
    )


def tensor_coefficient(source_factors, rows):
    return permanent(
        [
            [
                sum(
                    left * right
                    for left, right in zip(row, factor, strict=True)
                )
                for factor in source_factors
            ]
            for row in rows
        ]
    )


def restricted_p3(planes):
    factors = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    return {
        bits: tensor_coefficient(
            factors,
            tuple(planes[mode][bits[mode]] for mode in range(3)),
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def main() -> None:
    # Support-two Q02 chart: Q,R have normal u1 and S has normal h1.
    support_two_planes = (
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, 1)),
    )
    support_two_tensor = restricted_p3(support_two_planes)
    assert {
        bits: value
        for bits, value in support_two_tensor.items()
        if value
    } == {(1, 1, 0): -2}

    # Full-support chart.  The two equality normals are opposite
    # rectangle vertices; the local factors at Q,R are e3,e2.
    full_planes = (
        ((-1, 1, 0), (-1, 0, 1)),
        ((1, 1, 0), (1, 0, 1)),
        ((1, 1, 0), (-1, 0, 1)),
    )
    full_tensor = restricted_p3(full_planes)
    assert {
        bits: value
        for bits, value in full_tensor.items()
        if value
    } == {
        (1, 0, 0): 2,
        (1, 0, 1): -2,
    }

    e = tuple(
        tuple(1 if row == column else 0 for column in range(4))
        for row in range(4)
    )
    h0 = tuple(left - right for left, right in zip(e[0], e[1]))
    u0 = tuple(left + right for left, right in zip(e[0], e[1]))
    h1 = tuple(left - right for left, right in zip(e[2], e[3]))
    u1 = tuple(left + right for left, right in zip(e[2], e[3]))
    t2 = (e[0], e[1], e[2], e[3])

    # Support-two block vanishing with completely generic x-block rows
    # at Q,R and a generic span(h0,u1) row at S.
    q0, q1, r0, r1, s0, s1 = sp.symbols(
        "q0 q1 r0 r1 s0 s1"
    )
    q_row = tuple(q0 * u0[index] + q1 * h0[index] for index in range(4))
    r_row = tuple(r0 * u0[index] + r1 * h0[index] for index in range(4))
    s_row = tuple(s0 * h0[index] + s1 * u1[index] for index in range(4))
    support_two_required = tensor_coefficient(
        t2,
        (h1, q_row, r_row, s_row),
    )
    assert support_two_required == 0

    # Full-support rectangle.  Three h1 contractions vanish because T2
    # has only two source factors in the second coordinate block.
    q = sp.symbols("q0:4")
    r = sp.symbols("r0:4")
    s = sp.symbols("s0:4")
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    q_plus = tuple(q[index] + alpha * h1[index] for index in range(4))
    r_plus = tuple(r[index] + beta * h1[index] for index in range(4))

    def rectangle_value(q_row, r_row):
        return tensor_coefficient(t2, (h1, q_row, r_row, s))

    c02 = rectangle_value(q, r)
    c22 = rectangle_value(q_plus, r)
    c00 = rectangle_value(q, r_plus)
    c20 = rectangle_value(q_plus, r_plus)
    triple_h1 = tensor_coefficient(t2, (h1, h1, h1, s))
    assert triple_h1 == 0
    rectangle_identity = sp.factor(c20 - c22 - c00 + c02)
    assert rectangle_identity == 0

    output = {
        "verified": True,
        "field": "C",
        "cover_orbit": 13,
        "support_two_Q02_tensor_support": ["110"],
        "support_two_factor_directions": ["h1", "h1", "u0"],
        "full_support_Q02_tensor_support": ["100", "101"],
        "full_support_QR_factor_directions": ["e3", "e2"],
        "support_two_required_T2_2222": str(
            support_two_required
        ),
        "triple_h1_T2_coefficient": str(triple_h1),
        "full_support_rectangle_identity": str(rectangle_identity),
        "exact_cover_excluded": True,
        "monotone_cover_excluded": False,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_cover_13_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
